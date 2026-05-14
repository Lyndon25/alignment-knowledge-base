#!/usr/bin/env python3
"""
Playwright 浏览器自动化 — RVPN登录 + 批量论文下载
=====================================================
策略: 打开真实浏览器 → 用户手动登录RVPN (处理验证码) → 脚本接管下载

用法:
  python rvpn_playwright.py              # 完整流程
  python rvpn_playwright.py --dry-run    # 列出待下载URL
  python rvpn_playwright.py --resume     # 重用已登录的浏览器session
"""

import os, sys, json, re, time
from pathlib import Path
import asyncio

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
KB_DIR = PROJECT_ROOT / "knowledge_base"
MISSING_PATH = PROJECT_ROOT / "data" / "results" / "missing_papers.json"
SESSION_DIR = PROJECT_ROOT / "data" / "tmp_dl" / "playwright_session"

try:
    from credentials_local import ZJU_USERNAME, ZJU_PASSWORD
except ImportError:
    import os
    ZJU_USERNAME = os.environ.get("ZJU_USERNAME", "")
    ZJU_PASSWORD = os.environ.get("ZJU_PASSWORD", "")
    if not ZJU_USERNAME:
        print("WARNING: No credentials found. Create resources/code/credentials.local.py")
        print("  or set ZJU_USERNAME / ZJU_PASSWORD environment variables.")
RVPN_LOGIN = "https://rvpn.zju.edu.cn/por/login_psw.csp"
DOWNLOAD_DELAY = 2.0

DOMAIN_MAP = {
    "03": "03_causal_intervention",
    "05": "05_ethics_governance",
    "06": "06_philosophy_of_science",
    "07": "07_philosophy_of_mind",
    "08": "08_representational_ontology",
    "10": "10_causal_sufficiency",
    "11": "11_vector_grounding",
}


def load_missing_papers():
    """加载真正的缺失论文（过滤笔记/重复）"""
    if not MISSING_PATH.exists():
        return []
    with open(MISSING_PATH, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    # 过滤中文笔记，按(domain, id)去重
    seen = {}
    filtered = []
    for p in papers:
        title = p.get('title', '')
        # 纯中文且包含"："的标题 = 笔记
        if not re.search(r'[a-zA-Z]', title[:20]) and '：' in title:
            continue
        key = (p['domain'], p['id'])
        if key in seen:
            old = seen[key]
            # 保留有DOI的
            if p.get('doi') and not old.get('doi'):
                seen[key] = p
        else:
            seen[key] = p

    return list(seen.values())


def construct_urls(paper: dict) -> list[str]:
    """构造可能的下载URL"""
    urls = []
    doi = paper.get('doi', '')
    pdf_url = paper.get('pdf_url', '')

    if pdf_url and pdf_url.startswith('http'):
        urls.append(pdf_url)

    if doi:
        urls.extend([
            f"https://link.springer.com/content/pdf/{doi}.pdf",
            f"https://onlinelibrary.wiley.com/doi/pdfdirect/{doi}",
            f"https://journals.sagepub.com/doi/pdf/{doi}",
            f"https://www.tandfonline.com/doi/pdf/{doi}",
            f"https://doi.org/{doi}",
        ])

    return urls


def safe_filename(paper: dict) -> str:
    authors = paper.get('authors', 'Unknown')
    first = authors.split(",")[0].split(" and ")[0].split(";")[0].strip()
    first = re.sub(r'[<>:"/\\|?*]', '', first)
    title = paper.get('title', '')
    stitle = re.sub(r'[<>:"/\\|?*]', '', title[:80].strip())
    stitle = re.sub(r'\s+', '_', stitle)
    year = paper.get('year', 0)
    return f"{paper['id']}_{first}_{year}_{stitle}"


def check_existing(domain_key: str, paper_id: str) -> bool:
    dname = DOMAIN_MAP.get(domain_key, domain_key)
    ddir = KB_DIR / dname / "papers"
    if not ddir.exists():
        return False
    return bool(list(ddir.glob(f"{paper_id}_*")))


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Playwright RVPN downloader")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true",
                       help="Reuse existing browser session")
    args = parser.parse_args()

    missing = load_missing_papers()
    print(f"Papers to download: {len(missing)}")

    if args.dry_run:
        for p in missing:
            print(f"\n[{p['domain']}-{p['id']}] {p['title'][:80]}")
            for u in construct_urls(p):
                print(f"  {u[:120]}")
        return

    # Filter out already-existing papers
    todo = [p for p in missing if not check_existing(p['domain'], p['id'])]
    print(f"Already have: {len(missing) - len(todo)}, Remaining: {len(todo)}")

    if not todo:
        print("All papers downloaded!")
        return

    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        # Use persistent context to keep cookies
        SESSION_DIR.mkdir(parents=True, exist_ok=True)
        context = None

        if args.resume and SESSION_DIR.exists():
            context = await p.chromium.launch_persistent_context(
                str(SESSION_DIR),
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            print("[OK] Using saved browser session")
        else:
            # Fresh session
            browser = await p.chromium.launch(
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

        page = await context.new_page()

        # Step 1: Navigate to RVPN login
        print("\n" + "="*60)
        print("  Step 1: Login to RVPN")
        print("="*60)
        print("  Browser opened. Please manually:")
        print(f"  - Username: {ZJU_USERNAME}")
        print(f"  - Password: {ZJU_PASSWORD}")
        print("  - Solve any CAPTCHA and click Login")
        print("  The script will auto-detect login success...")
        print("="*60)

        await page.goto(RVPN_LOGIN, wait_until='domcontentloaded', timeout=60000)
        await page.wait_for_timeout(3000)  # let JS finish

        # Try to pre-fill credentials (try multiple possible selectors)
        try:
            name_input = await page.wait_for_selector(
                'input[name="svpn_name"], #svpn_name, input[type="text"]',
                timeout=10000
            )
            if name_input:
                await name_input.fill(ZJU_USERNAME)
                print("[OK] Pre-filled username")

            pw_input = await page.wait_for_selector(
                'input[name="svpn_password"], #svpn_password, input[type="password"]',
                timeout=5000
            )
            if pw_input:
                await pw_input.fill(ZJU_PASSWORD)
                print("[OK] Pre-filled password")
        except Exception as e:
            print(f"[INFO] Auto-fill skipped: {e}")
            print("  Please fill credentials manually in the browser.")

        # Wait for login success — detect via URL change away from login page
        print("\n  Waiting for login (max 5 minutes)...")
        try:
            await page.wait_for_url(
                lambda url: 'login' not in url.lower() and 'por/' in url.lower(),
                timeout=300000  # 5 min
            )
            print(f"[OK] Login detected! URL: {page.url}")
        except Exception:
            print("[WARN] Timeout waiting for login. Checking current state...")
            if 'login' in page.url.lower():
                print("  Still on login page. Please log in manually.")
                await page.wait_for_timeout(30000)
            print(f"  Current URL: {page.url}")

        # Step 2: Download papers
        print("\n" + "="*60)
        print(f"  Step 2: Downloading {len(todo)} papers")
        print("="*60)

        downloaded = 0
        failed = 0

        for i, paper in enumerate(todo):
            domain_key = paper['domain']
            dname = DOMAIN_MAP.get(domain_key, domain_key)
            ddir = KB_DIR / dname / "papers"
            ddir.mkdir(parents=True, exist_ok=True)

            print(f"\n[{i+1}/{len(todo)}] [{domain_key}-{paper['id']}] "
                  f"{paper['title'][:80]}")

            urls = construct_urls(paper)
            success = False

            for url in urls:
                try:
                    print(f"  Trying: {url[:120]}")
                    resp = await page.goto(url, wait_until='load', timeout=30000)

                    # Check if we got a PDF
                    content_type = (await resp.header_value('content-type') or '').lower()

                    if 'pdf' in content_type or url.endswith('.pdf'):
                        body = await resp.body()
                        if body[:4] == b'%PDF':
                            fname = safe_filename(paper)
                            save_path = ddir / f"{fname}.pdf"
                            save_path.write_bytes(body)
                            print(f"  OK -> {save_path.name} "
                                  f"({len(body)//1024} KB)")
                            success = True
                            downloaded += 1
                            break

                    # Check if page rendered as PDF viewer
                    current = page.url
                    if current.endswith('.pdf') or 'pdf' in current:
                        body = await page.evaluate(
                            "() => document.body.innerText"
                        )
                        if len(body) < 100:  # PDF viewer has no text
                            # Try to get PDF via fetch
                            pdf_data = await page.evaluate("""
                                async () => {
                                    const r = await fetch(window.location.href);
                                    const blob = await r.blob();
                                    const buf = await blob.arrayBuffer();
                                    return Array.from(new Uint8Array(buf));
                                }
                            """)
                            if pdf_data and len(pdf_data) > 1000:
                                save_path = ddir / f"{safe_filename(paper)}.pdf"
                                save_path.write_bytes(bytes(pdf_data))
                                print(f"  OK -> {save_path.name}")
                                success = True
                                downloaded += 1
                                break

                except Exception as e:
                    print(f"  Error: {str(e)[:100]}")
                    continue

                await asyncio.sleep(1)

            if not success:
                print(f"  FAILED: All URLs exhausted")
                failed += 1

            await asyncio.sleep(DOWNLOAD_DELAY)

        # Save session for resume
        await context.storage_state(path=str(SESSION_DIR / "state.json"))
        print(f"\nSession saved to {SESSION_DIR}")

        await context.close()

    print(f"\n{'='*60}")
    print(f"  FINAL: {downloaded} downloaded, {failed} failed")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
