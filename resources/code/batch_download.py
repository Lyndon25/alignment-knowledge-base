#!/usr/bin/env python3
"""
批量论文下载工具 - 支持多策略自动下载
==============================================
策略优先级:
  1. arXiv API (DOI或标题搜索)
  2. Unpaywall OA (检查开放获取版本)
  3. 直接URL (wiki中已有的pdf链接)
  4. DOI构造URL (按出版商模式)
  5. 浙大机构访问 (需RVPN连接)

用法:
  python batch_download.py              # 默认: 使用策略1-4 (无需机构访问)
  python batch_download.py --campus     # 启用策略5 (需ZJU校园网/RVPN)
  python batch_download.py --list-only  # 仅列出缺失论文,不下载
  python batch_download.py --domain 06  # 仅处理特定领域
"""

import os, sys, json, re, time, hashlib
from pathlib import Path
from urllib.parse import urlparse, urljoin, quote
import urllib.request
import urllib.error

# ============================================================
# Configuration
# ============================================================
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
KB_DIR = PROJECT_ROOT / "knowledge_base"
USER_AGENT = "ScholarAIO/1.3.1 (batch-download; mailto:student@zju.edu.cn)"
REQUEST_DELAY = 1.5  # seconds between downloads
TIMEOUT = 30

DOMAIN_MAP = {
    "01": "01_sae_features",
    "02": "02_activation_engineering",
    "03": "03_causal_intervention",
    "04": "04_alignment_safety",
    "05": "05_ethics_governance",
    "06": "06_philosophy_of_science",
    "07": "07_philosophy_of_mind",
    "08": "08_representational_ontology",
    "09": "09_epistemology_understanding",
    "10": "10_causal_sufficiency",
    "11": "11_vector_grounding",
}

# Publisher DOI → URL patterns (for strategy 4)
DOI_TO_PDF = {
    "arxiv.org": lambda doi: f"https://arxiv.org/pdf/{doi.split('/')[-1]}",
    "link.springer.com": lambda doi: f"https://link.springer.com/content/pdf/{doi}.pdf",
    "academic.oup.com": lambda doi: f"https://academic.oup.com/view-large/document/{doi}",
    "cambridge.org": lambda doi: f"https://www.cambridge.org/core/services/aop-cambridge-core/content/view/{doi.replace('10.1017/', '')}",
    "tandfonline.com": lambda doi: f"https://www.tandfonline.com/doi/pdf/{doi}",
    "wiley.com": lambda doi: f"https://onlinelibrary.wiley.com/doi/pdfdirect/{doi}",
    "sagepub.com": lambda doi: f"https://journals.sagepub.com/doi/pdf/{doi}",
    "brill.com": lambda doi: f"https://brill.com/view/journals/.../{doi}",
    "philarchive.org": None,  # blocked by Cloudflare
}

# ============================================================
# Paper Data Extraction
# ============================================================

def extract_papers_from_wiki(wiki_path: Path) -> list[dict]:
    """从wiki HTML中提取论文元数据"""
    papers = []
    content = wiki_path.read_text(encoding='utf-8', errors='replace')

    # 找到 PAPERS 数组的起始位置
    start_marker = "const PAPERS = ["
    start = content.find(start_marker)
    if start == -1:
        print(f"  WARN: PAPERS 数组未找到 in {wiki_path.name}")
        return papers

    # 简单切割: 找每个 { id: "..." 的对象
    segment = content[start + len(start_marker):]

    # 用正则提取每个 paper 对象 (简化: 匹配 { 到 }, 之间)
    # 由于对象嵌套, 用大括号计数
    paper_strs = []
    depth = 0
    buf = []
    in_object = False
    for ch in segment:
        if ch == '{':
            depth += 1
            in_object = True
        if in_object:
            buf.append(ch)
        if ch == '}':
            depth -= 1
            if depth == 0 and in_object:
                paper_strs.append(''.join(buf))
                buf = []
                in_object = False

    for ps in paper_strs:
        paper = parse_paper_object(ps)
        if paper:
            papers.append(paper)

    return papers


def parse_paper_object(text: str) -> dict | None:
    """解析单个 paper JS 对象"""
    def get_str(key):
        m = re.search(rf'{key}:\s*"([^"]*)"', text)
        return m.group(1) if m else ""

    def get_int(key):
        m = re.search(rf'{key}:\s*(\d+)', text)
        return int(m.group(1)) if m else 0

    pid = get_str("id")
    if not pid:
        return None

    return {
        "id": pid,
        "title": get_str("title"),
        "authors": get_str("authors"),
        "year": get_int("year"),
        "doi": get_str("doi"),
        "pdf": get_str("pdf"),
        "priority": get_str("priority"),
    }


def extract_all_papers(domain_filter: str = None) -> dict[str, list[dict]]:
    """从所有wiki提取论文"""
    all_papers = {}
    for dkey, dname in sorted(DOMAIN_MAP.items()):
        if domain_filter and dkey != domain_filter:
            continue
        wiki_path = KB_DIR / dname / "wiki.html"
        if wiki_path.exists():
            papers = extract_papers_from_wiki(wiki_path)
            all_papers[dkey] = papers
            print(f"  [{dkey}] {dname}: {len(papers)} papers extracted")
        else:
            print(f"  [{dkey}] {dname}: wiki not found")
    return all_papers


# ============================================================
# Local PDF Check
# ============================================================

def get_existing_files(domain_key: str) -> dict[str, str]:
    """获取某领域已存在的文件（PDF/MD/HTML） -> {id: extension}"""
    domain_dir = KB_DIR / DOMAIN_MAP[domain_key] / "papers"
    if not domain_dir.exists():
        return {}
    existing = {}
    for f in domain_dir.iterdir():
        m = re.match(r'^(\d+)', f.stem)
        if m:
            pid = m.group(1)
            ext = f.suffix.lower()
            # 保留最佳格式 (PDF > HTML > MD)
            if pid not in existing or (ext == '.pdf' and existing[pid] != '.pdf'):
                existing[pid] = ext
    return existing


# ============================================================
# Download Strategies
# ============================================================

def try_arxiv_by_doi(doi: str) -> str | None:
    """Strategy 1: 通过arXiv ID获取PDF URL"""
    if not doi:
        return None
    # arXiv DOI模式: 10.48550/arXiv.XXXX.XXXXX
    m = re.match(r'10\.48550/(?:arXiv\.)?(\d{4}\.\d{4,}(?:v\d+)?)', doi, re.I)
    if m:
        arxiv_id = m.group(1).rstrip('v123456789')  # remove version
    else:
        # 也检查裸 arXiv ID in doi field
        m = re.match(r'(?:arxiv:)?(\d{4}\.\d{4,})', doi, re.I)
        if m:
            arxiv_id = m.group(1)
        else:
            return None

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    return pdf_url


def try_arxiv_by_title(title: str) -> str | None:
    """Strategy 1b: 用标题搜索arXiv"""
    if not title:
        return None
    try:
        query = quote(title[:200])
        api_url = f"https://export.arxiv.org/api/query?search_query=ti:{query}&max_results=3"
        req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read().decode('utf-8')

        # 找第一个匹配的entry
        entries = re.findall(r'<entry>(.*?)</entry>', data, re.DOTALL)
        for entry in entries:
            id_match = re.search(r'<id>http://arxiv\.org/abs/([^<]+)</id>', entry)
            if id_match:
                arxiv_id = id_match.group(1)
                return f"https://arxiv.org/pdf/{arxiv_id}"
    except Exception:
        pass
    return None


def try_unpaywall(doi: str, email: str = "student@zju.edu.cn") -> str | None:
    """Strategy 2: Unpaywall OA 检查"""
    if not doi:
        return None
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode())

        best = data.get("best_oa_location", {})
        oa_url = best.get("url_for_pdf", "") or best.get("url", "")
        if oa_url:
            return oa_url
    except Exception:
        pass
    return None


def construct_pdf_url_from_doi(doi: str) -> str | None:
    """Strategy 4: 根据DOI构造可能的PDF URL"""
    if not doi:
        return None

    # 尝试常见模式
    patterns = [
        f"https://link.springer.com/content/pdf/{doi}.pdf",
        f"https://onlinelibrary.wiley.com/doi/pdfdirect/{doi}",
        f"https://journals.sagepub.com/doi/pdf/{doi}",
        f"https://www.tandfonline.com/doi/pdf/{doi}",
        f"https://academic.oup.com/view-large/document/{doi}",
    ]
    return patterns  # 返回列表供逐个尝试


# ============================================================
# Download Engine
# ============================================================

def download_pdf(url: str, save_path: Path) -> bool:
    """下载PDF到指定路径"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/pdf,text/html,*/*",
            }
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()

            # 验证是否为PDF
            if len(data) > 1000 and (data[:4] == b'%PDF' or 'pdf' in content_type.lower()):
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_bytes(data)
                return True
            elif b'<html' in data[:500].lower() or b'<!DOCTYPE' in data[:500]:
                # 可能是登录页面或付费墙
                return False
            else:
                # 未知格式但仍保存
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_bytes(data)
                return True
    except urllib.error.HTTPError as e:
        if e.code in (403, 404, 410):
            return False
        print(f"    HTTP {e.code} for {url[:80]}")
        return False
    except Exception as e:
        print(f"    Error: {e}")
        return False


def safe_filename(authors: str, year: int, title: str) -> str:
    """生成安全的文件名"""
    first_author = authors.split(",")[0].split(" and ")[0].split(";")[0].strip()
    first_author = re.sub(r'[<>:"/\\|?*]', '', first_author)
    short_title = re.sub(r'[<>:"/\\|?*]', '', title[:80].strip())
    short_title = re.sub(r'\s+', '_', short_title)
    if year:
        return f"{first_author}_{year}_{short_title}"
    return f"{first_author}_{short_title}"


def process_missing_papers(all_papers: dict, use_campus: bool = False,
                           list_only: bool = False) -> dict:
    """主处理流程"""
    stats = {"total": 0, "already_have": 0, "downloaded": 0, "failed": 0, "skipped_notes": 0}
    missing_list = []

    for domain_key in sorted(all_papers.keys()):
        papers = all_papers[domain_key]
        existing_files = get_existing_files(domain_key)
        domain_dir = KB_DIR / DOMAIN_MAP[domain_key] / "papers"

        for paper in papers:
            stats["total"] += 1

            title = paper.get("title", "")
            # 跳过阅读笔记条目 (中文导读/笔记标签)
            if "导读" in title or "阅读笔记" in title or "笔记" in title:
                stats["skipped_notes"] += 1
                continue

            # 检查是否已有文件 (PDF > MD > HTML)
            if paper["id"] in existing_files:
                stats["already_have"] += 1
                continue

            title = paper.get("title", "")
            doi = paper.get("doi", "")
            pdf_url = paper.get("pdf", "")

            print(f"\n[{domain_key}-{paper['id']}] {title[:80]}")

            if list_only:
                missing_list.append({
                    "domain": domain_key,
                    "id": paper["id"],
                    "title": title,
                    "doi": doi,
                    "pdf_url": pdf_url,
                    "authors": paper.get("authors", ""),
                    "year": paper.get("year", 0),
                })
                stats["failed"] += 1
                continue

            # 尝试下载
            dl_url = None
            strategy = ""

            # Strategy 1: arXiv
            if doi:
                dl_url = try_arxiv_by_doi(doi)
                if dl_url:
                    strategy = "arxiv_doi"

            # Strategy 1b: arXiv title search
            if not dl_url and title:
                dl_url = try_arxiv_by_title(title)
                if dl_url:
                    strategy = "arxiv_title"

            # Strategy 2: Unpaywall OA
            if not dl_url and doi:
                dl_url = try_unpaywall(doi)
                if dl_url:
                    strategy = "unpaywall_oa"

            # Strategy 3: Direct URL from wiki
            if not dl_url and pdf_url and not any(
                host in pdf_url for host in
                ["link.springer.com", "academic.oup.com", "cambridge.org",
                 "tandfonline.com", "sagepub.com", "wiley.com", "brill.com"]
            ):
                dl_url = pdf_url
                strategy = "direct_oa"

            # Strategy 4: 构造DOI URL + 尝试下载
            if not dl_url and doi and not use_campus:
                candidate_urls = construct_pdf_url_from_doi(doi)
                for url in candidate_urls:
                    # 仅尝试已知的OA友好模式
                    if "link.springer.com/content/pdf" in url:
                        # Springer 有时允许未认证访问
                        test_path = domain_dir / f"__test_{paper['id']}.pdf"
                        if download_pdf(url, test_path):
                            dl_url = url
                            strategy = "doi_constructed"
                            test_path.unlink()  # 删除测试文件
                            break

            # 下载
            if dl_url:
                print(f"  [{strategy}] {dl_url[:100]}")
                filename = safe_filename(
                    paper.get("authors", "Unknown"),
                    paper.get("year", 0),
                    title
                )
                save_path = domain_dir / f"{paper['id']}_{filename}.pdf"
                if download_pdf(dl_url, save_path):
                    size = save_path.stat().st_size
                    print(f"  OK -> {save_path.name} ({size//1024} KB)")
                    stats["downloaded"] += 1
                    time.sleep(REQUEST_DELAY)
                    continue
                else:
                    print(f"  FAILED: download returned non-PDF content")

            # 所有策略失败
            stats["failed"] += 1
            missing_list.append({
                "domain": domain_key,
                "id": paper["id"],
                "title": title,
                "doi": doi,
                "pdf_url": pdf_url,
                "authors": paper.get("authors", ""),
                "year": paper.get("year", 0),
            })
            if use_campus:
                print(f"  PAYWALLED (needs campus IP to access)")
            else:
                print(f"  PAYWALLED (try --campus mode on ZJU network)")

    return stats, missing_list


# ============================================================
# Campus IP batch download
# ============================================================

def campus_download(missing_list: list[dict]):
    """在ZJU校园网环境下批量下载付费论文"""
    print(f"\n{'='*60}")
    print(f"  Campus IP Download Mode")
    print(f"  Papers to attempt: {len(missing_list)}")
    print(f"{'='*60}\n")

    downloaded = 0
    failed = 0

    for paper in missing_list:
        domain_key = paper["domain"]
        domain_dir = KB_DIR / DOMAIN_MAP[domain_key] / "papers"

        print(f"[{domain_key}-{paper['id']}] {paper['title'][:80]}")

        dl_url = None
        strategy = ""

        # 1. 使用wiki中的direct pdf URL
        if paper.get("pdf_url"):
            dl_url = paper["pdf_url"]
            strategy = "direct_url"
        # 2. 用DOI构造
        elif paper.get("doi"):
            urls = construct_pdf_url_from_doi(paper["doi"])
            # 先测试哪个可用
            for url in urls:
                test_path = domain_dir / f"__probe_{paper['id']}.pdf"
                if download_pdf(url, test_path):
                    dl_url = url
                    strategy = "doi_constructed"
                    test_path.unlink(missing_ok=True)
                    break
                test_path.unlink(missing_ok=True)

        if dl_url:
            print(f"  [{strategy}] {dl_url[:100]}")
            filename = safe_filename(
                paper.get("authors", "Unknown"),
                paper.get("year", 0),
                paper.get("title", "")
            )
            save_path = domain_dir / f"{paper['id']}_{filename}.pdf"
            if download_pdf(dl_url, save_path):
                size = save_path.stat().st_size
                print(f"  OK -> {save_path.name} ({size//1024} KB)")
                downloaded += 1
            else:
                print(f"  FAILED")
                failed += 1
        else:
            print(f"  SKIP: no URL source")
            failed += 1

        time.sleep(REQUEST_DELAY)

    print(f"\n{'='*60}")
    print(f"  Campus download complete: {downloaded} OK, {failed} failed")
    print(f"{'='*60}")


# ============================================================
# Reporting
# ============================================================

def print_report(stats: dict, missing_list: list[dict]):
    """打印最终报告"""
    print(f"\n{'='*60}")
    print(f"  DOWNLOAD REPORT")
    print(f"{'='*60}")
    print(f"  Total papers:    {stats['total']}")
    print(f"  Already have:    {stats['already_have']}")
    print(f"  Skipped (notes): {stats['skipped_notes']}")
    print(f"  Newly downloaded:{stats['downloaded']}")
    print(f"  Still missing:   {stats['failed']}")
    print(f"{'='*60}")

    if missing_list:
        print(f"\n--- Still Missing ({len(missing_list)} papers) ---\n")
        # Group by domain
        by_domain = {}
        for p in missing_list:
            d = p["domain"]
            by_domain.setdefault(d, []).append(p)

        for dkey in sorted(by_domain.keys()):
            items = by_domain[dkey]
            dname = DOMAIN_MAP.get(dkey, dkey)
            print(f"\n[{dkey}] {dname}: {len(items)} papers")
            for p in items:
                print(f"  {p['id']}: {p['title'][:100]}")
                if p.get("doi"):
                    print(f"       DOI: {p['doi']}")
                if p.get("pdf_url"):
                    print(f"       URL: {p['pdf_url'][:120]}")

        # Save to JSON for later use
        missing_path = PROJECT_ROOT / "data" / "results" / "missing_papers.json"
        missing_path.parent.mkdir(parents=True, exist_ok=True)
        missing_path.write_text(
            json.dumps(missing_list, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        print(f"\nMissing papers list saved to: {missing_path}")


# ============================================================
# Main
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch paper downloader")
    parser.add_argument("--campus", action="store_true",
                       help="Enable campus IP mode (attempt paywalled URLs)")
    parser.add_argument("--list-only", action="store_true",
                       help="Only list missing papers, do not download")
    parser.add_argument("--domain", type=str, default=None,
                       help="Only process specific domain (e.g. 06)")
    args = parser.parse_args()

    print("=" * 60)
    print("  Batch Paper Downloader")
    print(f"  Mode: {'List Only' if args.list_only else 'Campus IP' if args.campus else 'OA + arXiv'}")
    print("=" * 60)

    # Step 1: Extract metadata
    print("\n[1] Extracting paper metadata from wikis...")
    all_papers = extract_all_papers(args.domain)
    total = sum(len(v) for v in all_papers.values())
    print(f"  Total papers found: {total}")

    # Step 2: Check existing + download missing
    print("\n[2] Processing missing papers...")
    stats, missing_list = process_missing_papers(
        all_papers, use_campus=args.campus, list_only=args.list_only
    )

    # Step 3: Report
    print_report(stats, missing_list)

    # Step 4: Campus mode follow-up
    if not args.campus and not args.list_only and missing_list:
        print(f"\n{'='*60}")
        print(f"  {len(missing_list)} papers still behind paywalls.")
        print(f"  To download them, connect to ZJU campus network (RVPN)")
        print(f"  and run: python batch_download.py --campus")
        print(f"  See: data/results/zju_download_guide.md")
        print(f"{'='*60}")

    if args.campus and missing_list:
        print("\n[3] Attempting campus IP downloads...")
        campus_download(missing_list)


if __name__ == "__main__":
    main()
