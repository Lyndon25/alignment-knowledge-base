#!/usr/bin/env python3
"""
CARSI 直连下载 — 通过浙大统一认证直接访问出版商
==================================================
无需VPN客户端。利用 ZJU 的 CARSI 联邦身份认证，
在出版商页面选择浙大登录，验证后直接下载PDF。

用法:
  python carsi_download.py
  python carsi_download.py --test    # 仅测试登录一个出版商
"""

import os, sys, json, re, time, asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
KB_DIR = PROJECT_ROOT / "knowledge_base"
MISSING_PATH = PROJECT_ROOT / "data" / "results" / "missing_papers.json"

try:
    from credentials_local import ZJU_USERNAME, ZJU_PASSWORD
except ImportError:
    import os
    ZJU_USERNAME = os.environ.get("ZJU_USERNAME", "")
    ZJU_PASSWORD = os.environ.get("ZJU_PASSWORD", "")
    if not ZJU_USERNAME:
        print("WARNING: No credentials found. Create resources/code/credentials.local.py")
        print("  or set ZJU_USERNAME / ZJU_PASSWORD environment variables.")

CARSI_IDP = "Zhejiang University"
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
    if not MISSING_PATH.exists():
        return []
    with open(MISSING_PATH, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    seen = {}
    for p in papers:
        title = p.get('title', '')
        # 只移除明确的阅读笔记（包含"导读"或"阅读笔记"关键词）
        if '导读' in title or '阅读笔记' in title:
            continue
        # 保留: 有DOI的 > 有pdf_url的 > 其他
        key = (p['domain'], p['id'])
        if key in seen:
            existing_score = (1 if seen[key].get('doi') else 0) + (1 if seen[key].get('pdf_url','').startswith('http') else 0)
            new_score = (1 if p.get('doi') else 0) + (1 if p.get('pdf_url','').startswith('http') else 0)
            if new_score > existing_score:
                seen[key] = p
        else:
            seen[key] = p
    return list(seen.values())


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


async def login_via_carsi(page, publisher_url: str) -> bool:
    """
    通过CARSI机构登录访问出版商页面。
    流程: 出版商 → "机构登录" → 选浙大 → CAS验证 → 回到出版商
    """
    print(f"  Navigating to: {publisher_url[:120]}")
    try:
        await page.goto(publisher_url, wait_until='load', timeout=30000)
        await page.wait_for_timeout(2000)
    except Exception:
        pass  # May fail with HTTP error, which is fine

    current_url = page.url
    current_title = await page.title()

    # 如果已经是浙大CAS页面，直接填写凭证
    if 'zjuam.zju.edu.cn' in current_url or 'cas/login' in current_url:
        print("  -> On ZJU CAS login page")
        # 填写凭证
        try:
            await page.fill('input[name="username"]', ZJU_USERNAME)
            await page.fill('input[name="password"]', ZJU_PASSWORD)
            print("  [OK] Filled ZJU credentials")
            print("  >>> WAITING: 请在浏览器中手动输入验证码(authcode)，然后点击登录 <<<")

            # 等待登录成功（离开CAS页面）
            await page.wait_for_url(
                lambda url: 'zjuam' not in url and 'cas' not in url,
                timeout=120000
            )
            print("  [OK] CAS login complete!")
            return True
        except Exception as e:
            print(f"  [WARN] CAS fill failed: {e}")
            return False

    # 检查是否已在出版商认证状态
    if any(kw in current_title.lower() for kw in ['pdf', 'article', 'download']):
        print(f"  -> Already authenticated! Title: {current_title[:50]}")
        return True

    # 需要找到 "机构登录" 链接
    print("  Looking for institutional login...")

    # 常见CARSI入口文本
    inst_selectors = [
        'text=Institutional login',
        'text=Access through your institution',
        'text=Log in via institution',
        'text=Institution',
        'text=Sign in via your institution',
        'a:has-text("Institution")',
        'a:has-text("Login")',
    ]

    clicked = False
    for selector in inst_selectors:
        try:
            el = await page.wait_for_selector(selector, timeout=3000)
            if el:
                await el.click()
                clicked = True
                print(f"  Clicked: {selector}")
                await page.wait_for_timeout(2000)
                break
        except Exception:
            continue

    if not clicked:
        # Check if already authenticated
        if 'download' in current_url.lower() or '/pdf/' in current_url.lower():
            return True
        print("  [WARN] Could not find institutional login button")
        return False

    # 在机构选择器中搜索浙大
    print("  Looking for ZJU in institution list...")
    zju_selectors = [
        'text=Zhejiang University',
        'text=Zhejiang',
        'text=浙江大学',
        'input[placeholder*="institution"]',
        'input[placeholder*="search"]',
    ]

    for selector in zju_selectors:
        try:
            el = await page.wait_for_selector(selector, timeout=3000)
            if el:
                tag = await el.evaluate('el => el.tagName')
                if tag == 'INPUT':
                    await el.fill('Zhejiang University')
                    await page.wait_for_timeout(2000)
                else:
                    await el.click()
                await page.wait_for_timeout(1500)
                break
        except Exception:
            continue

    # 点击浙大选项
    try:
        zju_btn = await page.wait_for_selector(
            'text=Zhejiang University', timeout=5000
        )
        if zju_btn:
            await zju_btn.click()
            print("  Clicked Zhejiang University")
            await page.wait_for_timeout(3000)
    except Exception:
        print("  [WARN] Could not select ZJU")

    # 现在应该在CAS页面
    if 'zjuam' in page.url or 'cas' in page.url:
        try:
            await page.fill('input[name="username"]', ZJU_USERNAME)
            await page.fill('input[name="password"]', ZJU_PASSWORD)
            print("  [OK] Filled CAS credentials")
            print("  >>> WAITING: Enter CAPTCHA code if shown, then login <<<")
            await page.wait_for_url(
                lambda url: 'zjuam' not in url and 'cas' not in url,
                timeout=120000
            )
            print("  [OK] CAS login complete!")
            return True
        except Exception as e:
            print(f"  CAS login failed: {e}")
            return False

    return True


async def download_current_page(page, save_path: Path) -> bool:
    """从当前页面下载PDF（支持多种方式）"""
    # 检查当前URL是否是PDF
    if page.url.endswith('.pdf'):
        try:
            body = await page.evaluate("""
                async () => {
                    const r = await fetch(window.location.href);
                    return Array.from(new Uint8Array(await r.arrayBuffer()));
                }
            """)
            if body and len(body) > 1000:
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_bytes(bytes(body))
                return True
        except Exception:
            pass

    # 查找页面上的PDF下载链接
    try:
        pdf_links = await page.evaluate("""
            () => {
                const links = [];
                document.querySelectorAll('a').forEach(a => {
                    if (a.href && a.href.match(/\.pdf$/i)) {
                        links.push(a.href);
                    }
                });
                // Also check meta tags
                document.querySelectorAll('meta[name="citation_pdf_url"]').forEach(m => {
                    links.push(m.content);
                });
                return links;
            }
        """)
        for link in pdf_links:
            try:
                resp = await page.context.request.get(link)
                if resp.ok and len(await resp.body()) > 1000:
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    save_path.write_bytes(await resp.body())
                    return True
            except Exception:
                continue
    except Exception:
        pass

    return False


async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    missing = load_missing_papers()
    todo = [p for p in missing if not check_existing(p['domain'], p['id'])]
    print(f"Papers to download: {len(todo)} (of {len(missing)} total)")

    if args.test and todo:
        # Pick first paper with a DOI
        todo_with_doi = [p for p in todo if p.get('doi')]
        todo = todo_with_doi[:1] if todo_with_doi else todo[:1]
        if todo_with_doi:
            print(f"Test target: [{todo[0]['domain']}-{todo[0]['id']}] {todo[0]['title'][:60]}")

    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        print("\n" + "="*60)
        print("  CARSI Downloader — 通过浙大统一认证下载论文")
        print("="*60)
        print("  当浏览器跳转到浙大CAS登录页时:")
        print(f"    - 用户名已预填: {ZJU_USERNAME}")
        print(f"    - 密码已预填: {ZJU_PASSWORD}")
        print("    - 请输入验证码 (authcode) 并点击登录")
        print("  脚本在登录成功后会继续自动下载")
        print("="*60)

        downloaded = 0
        failed = 0
        cas_logged_in = False  # Track if CAS session is active

        for i, paper in enumerate(todo):
            domain_key = paper['domain']
            dname = DOMAIN_MAP.get(domain_key, domain_key)
            ddir = KB_DIR / dname / "papers"

            print(f"\n[{i+1}/{len(todo)}] [{domain_key}-{paper['id']}] "
                  f"{paper['title'][:80]}")

            doi = paper.get('doi', '')
            pdf_url = paper.get('pdf_url', '')

            # 构造访问URL
            target_url = None
            if pdf_url and pdf_url.startswith('http'):
                target_url = pdf_url
            elif doi:
                # Springer优先尝试（已知对CARSI友好）
                target_url = f"https://link.springer.com/article/{doi}"
            else:
                print("  SKIP: no URL source")
                failed += 1
                continue

            # CARSI登录
            if not cas_logged_in or i == 0:
                ok = await login_via_carsi(page, target_url)
                if not ok:
                    failed += 1
                    continue
                cas_logged_in = True
            else:
                # 后续论文直接用已认证session访问
                await page.goto(target_url, wait_until='load', timeout=30000)

            await page.wait_for_timeout(2000)

            # 下载
            fname = safe_filename(paper)
            save_path = ddir / f"{fname}.pdf"

            success = await download_current_page(page, save_path)

            if not success:
                # 尝试直接用PDF URL
                for pdf_pattern in [
                    f"https://link.springer.com/content/pdf/{doi}.pdf" if doi else None,
                    f"https://onlinelibrary.wiley.com/doi/pdfdirect/{doi}" if doi else None,
                ]:
                    if pdf_pattern is None:
                        continue
                    try:
                        await page.goto(pdf_pattern, wait_until='load', timeout=30000)
                        await page.wait_for_timeout(1000)
                        success = await download_current_page(page, save_path)
                        if success:
                            break
                    except Exception:
                        continue

            if success:
                size = save_path.stat().st_size
                print(f"  OK -> {save_path.name} ({size//1024} KB)")
                downloaded += 1
            else:
                print(f"  FAILED")
                failed += 1

            await asyncio.sleep(DOWNLOAD_DELAY)

        await context.close()

    print(f"\n{'='*60}")
    print(f"  FINAL: {downloaded} downloaded, {failed} failed")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
