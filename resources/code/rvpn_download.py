#!/usr/bin/env python3
"""
RVPN自动登录 + 批量论文下载
=============================
使用ZJU统一认证账号登录RVPN，然后批量下载付费论文。

用法:
  python rvpn_download.py              # 登录RVPN + 下载缺失论文
  python rvpn_download.py --test       # 仅测试登录
  python rvpn_download.py --dry-run    # 列出将要下载的URL，不实际下载
"""

import os, sys, json, re, time, hashlib
from pathlib import Path
from urllib.parse import urlparse, urljoin, quote
import urllib.request
import urllib.error
import http.cookiejar
import ssl

# cryptography for RSA encryption
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

# ============================================================
# Configuration
# ============================================================
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
KB_DIR = PROJECT_ROOT / "knowledge_base"

# ZJU Credentials
try:
    from credentials_local import ZJU_USERNAME, ZJU_PASSWORD
except ImportError:
    import os
    ZJU_USERNAME = os.environ.get("ZJU_USERNAME", "")
    ZJU_PASSWORD = os.environ.get("ZJU_PASSWORD", "")
    if not ZJU_USERNAME:
        print("WARNING: No credentials found. Create resources/code/credentials.local.py")
        print("  or set ZJU_USERNAME / ZJU_PASSWORD environment variables.")

# RVPN Settings
RVPN_BASE = "https://rvpn.zju.edu.cn"
LOGIN_URL = f"{RVPN_BASE}/por/login_psw.csp"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# RSA Public Key from RVPN login page
RSA_MODULUS_HEX = (
    "A419991B7BACC8A07E6EE77EB42981567AD0762F286691135006583E8750F028"
    "8F833E7AE7B6A9CCF81C214649788D84E908B11BCB494F73DA21657A1252FF4D"
    "83ADF7BD3203883A72D0E81ADA9973E8186E1C76BA1C1CD82B09D6A80E5FC31A"
    "37D81D8F07816A4EE1E56E7960F86DDF7BE00E623781162A6C08F5C62E0E3797"
    "9D108CE544EF139C05E1B6E70A59A0058EBB73649CC326A620C738C215BB5ED8"
    "12C6B9C2ACB265E9025D52DD0079E7985E4BF28FCF45D308C2A75AF3E188237C"
    "079A0FB1031851D2272F5228EBE6E0FF09033B2CFFA946E2A357936E3CA05F9A"
    "16F12A63C9FF1602B5B7111F4DFC8E13CE91847536F6878B115E990AADA4D819"
)
RSA_EXPONENT = 65537

# 域名映射 (与 batch_download.py 一致)
DOMAIN_MAP = {
    "03": "03_causal_intervention", "05": "05_ethics_governance",
    "06": "06_philosophy_of_science", "07": "07_philosophy_of_mind",
    "08": "08_representational_ontology", "10": "10_causal_sufficiency",
    "11": "11_vector_grounding",
}

DOWNLOAD_DELAY = 2.0  # 礼貌延迟
TIMEOUT = 60

# ============================================================
# RSA Encryption (PKCS#1 v1.5, compatible with RVPN's JS RSA)
# ============================================================

def rsa_encrypt_password(password: str) -> str:
    """
    使用RVPN的RSA公钥加密密码
    与 rsa.js 的 RSAEncrypt + pkcs1pad2 兼容
    """
    n = int(RSA_MODULUS_HEX, 16)

    # 构建RSA公钥
    from cryptography.hazmat.primitives.asymmetric import rsa as rsa_types
    public_numbers = rsa_types.RSAPublicNumbers(RSA_EXPONENT, n)
    public_key = public_numbers.public_key(default_backend())

    # 密码转UTF-8字节
    password_bytes = password.encode('utf-8')

    # PKCS#1 v1.5 加密 (等同 JS 的 pkcs1pad2 + RSAEncrypt)
    # key_size = 2048 bits = 256 bytes
    ciphertext = public_key.encrypt(
        password_bytes,
        padding.PKCS1v15()
    )

    # 转为十六进制字符串 (与 JS 的 byte2Hex 兼容)
    hex_str = ciphertext.hex()
    return hex_str


# ============================================================
# RVPN Session Management
# ============================================================

class RVPNSession:
    """RVPN 登录会话"""

    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
            urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
        )
        self.logged_in = False
        self.session_cookies = {}

    def _request(self, url: str, data: bytes = None,
                 headers: dict = None, method: str = "GET") -> tuple:
        """发起HTTP请求"""
        default_headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        if headers:
            default_headers.update(headers)
        if data is not None:
            default_headers["Content-Type"] = "application/x-www-form-urlencoded"

        req = urllib.request.Request(
            url, data=data, headers=default_headers, method=method
        )
        try:
            resp = self.opener.open(req, timeout=TIMEOUT)
            body = resp.read()
            return resp.getcode(), resp.headers, body
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read()

    def login(self) -> bool:
        """登录RVPN"""
        print("[RVPN] Logging in to rvpn.zju.edu.cn...")

        # Step 1: 获取登录页面 (获取初始Cookie和可能的token)
        code, headers, body = self._request(LOGIN_URL)
        if code != 200:
            print(f"  FAILED: Login page returned HTTP {code}")
            return False

        page_text = body.decode('utf-8', errors='replace')

        # 提取 form action (可能包含动态参数)
        action_match = re.search(r'action="([^"]*)"', page_text)
        form_action = action_match.group(1) if action_match else "login_psw.csp"
        post_url = urljoin(LOGIN_URL, form_action)

        # 提取隐藏字段
        hidden_match = re.search(r'name="svpn_req_randcode"[^>]*value="([^"]*)"', page_text)
        randcode = hidden_match.group(1) if hidden_match else ""

        # 检查是否需要验证码
        if 'EnableRandCode' in page_text:
            enable_randcode = re.search(r"EnableRandCode:\s*'(\d)'", page_text)
            if enable_randcode and enable_randcode.group(1) == '1':
                print("  ERROR: CAPTCHA required! Cannot auto-login.")
                return False

        print(f"  POST -> {post_url}")

        # Step 2: RSA加密密码
        print(f"  Encrypting password (RSA-2048 PKCS#1 v1.5)...")
        encrypted_pw = rsa_encrypt_password(ZJU_PASSWORD)
        print(f"  Encrypted password: {encrypted_pw[:40]}...")

        # Step 3: 提交登录
        post_data = urllib.parse.urlencode({
            "svpn_name": ZJU_USERNAME,
            "svpn_password": encrypted_pw,
            "svpn_req_randcode": randcode,
        }).encode('utf-8')

        code, headers, body = self._request(
            post_url, data=post_data,
            headers={"Referer": LOGIN_URL}
        )

        print(f"  Login response: HTTP {code}")

        # 检查登录结果
        body_text = body.decode('utf-8', errors='replace')

        # 失败标志
        if "用户名或密码错误" in body_text or "密码错误" in body_text or "账号不存在" in body_text:
            print("  FAILED: Invalid username or password!")
            return False

        if "验证码" in body_text and "错误" in body_text:
            print("  FAILED: CAPTCHA validation failed!")
            return False

        # 成功标志：重定向或session cookie
        location = headers.get("Location", "")
        if location:
            print(f"  Redirect -> {location}")

        # 检查是否有认证Cookie
        for cookie in self.cookie_jar:
            self.session_cookies[cookie.name] = cookie.value

        # 常见的SSL VPN认证Cookie名称
        auth_cookies = ['TWFID', 'SVPNMSID', 'SESSION_ID', 'JSESSIONID',
                       'svpn_session_id', 'HTTP_REFERER']
        has_auth = any(name in self.session_cookies for name in auth_cookies)
        has_twfid = 'TWFID' in self.session_cookies

        if has_auth or len(self.session_cookies) > 2:
            print(f"  OK: Login successful! ({len(self.session_cookies)} cookies)")
            print(f"  Session cookies: {list(self.session_cookies.keys())}")
            self.logged_in = True
            return True
        else:
            print(f"  UNCERTAIN: Got {len(self.session_cookies)} cookies")
            print(f"  Cookies: {list(self.session_cookies.keys())}")
            # 如果获得了新cookie就认为可能成功了
            if len(self.session_cookies) >= 2:
                print("  Proceeding optimistically...")
                self.logged_in = True
                return True
            return False

    def download_via_proxy(self, target_url: str, save_path: Path) -> bool:
        """
        通过RVPN代理访问并下载论文
        登录后，使用 /por/ 前缀来代理访问外部URL
        """
        if not self.logged_in:
            print("  Not logged in!")
            return False

        # RVPN代理URL格式: https://rvpn.zju.edu.cn/por/service.csp?...
        # 对于web资源，通常格式是: https://rvpn.zju.edu.cn/<original_url>
        # 或者通过 service.csp 参数传递
        proxy_url = f"{RVPN_BASE}/por/service.csp?"
        # 尝试不同的代理格式
        proxy_formats = [
            # 格式1: 直接代理
            f"{RVPN_BASE}{target_url[target_url.find('://'):]}" if '://' in target_url else None,
            # 格式2: 通过 /por/ 代理
            f"{RVPN_BASE}/por/?url={quote(target_url)}",
        ]

        for proxy_url in proxy_formats:
            if proxy_url is None:
                continue
            try:
                code, headers, body = self._request(proxy_url)
                if code == 200 and len(body) > 1000:
                    # 验证是否为PDF
                    if body[:4] == b'%PDF':
                        save_path.parent.mkdir(parents=True, exist_ok=True)
                        save_path.write_bytes(body)
                        return True
            except Exception:
                continue

        return False

    def download_direct(self, url: str, save_path: Path) -> bool:
        """直接下载 (如果RVPN cookie中包含了IP代理)"""
        try:
            code, headers, body = self._request(url)
            if code == 200 and len(body) > 1000 and body[:4] == b'%PDF':
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_bytes(body)
                return True
        except Exception:
            pass
        return False


# ============================================================
# Main
# ============================================================

def load_missing_papers() -> list[dict]:
    """加载缺失论文列表"""
    missing_path = PROJECT_ROOT / "data" / "results" / "missing_papers.json"
    if not missing_path.exists():
        print("No missing_papers.json found. Run batch_download.py --list-only first.")
        return []

    with open(missing_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    # 过滤掉中文笔记条目 (同一ID的重复)
    # 按 (domain, id) 去重，保留有doi或有url的
    seen = {}
    filtered = []
    for p in papers:
        key = (p['domain'], p['id'])
        title = p.get('title', '')
        # 跳过中文笔记标题
        if any(kw in title for kw in ['导读', '笔记', '：']):
            if not re.search(r'[a-zA-Z]', title[:20]):  # 前20字符无英文 = 纯中文笔记
                continue

        if key in seen:
            # 保留有更多元数据的那个
            existing = seen[key]
            if (p.get('doi') or p.get('pdf_url')) and not (existing.get('doi') or existing.get('pdf_url')):
                seen[key] = p
        else:
            seen[key] = p

    return list(seen.values())


def construct_download_urls(paper: dict) -> list[str]:
    """根据论文元数据构造可能的下载URL"""
    urls = []

    doi = paper.get('doi', '')
    pdf_url = paper.get('pdf_url', '')

    # 1. 已有直接URL
    if pdf_url and pdf_url.startswith('http'):
        urls.append(pdf_url)

    # 2. 从DOI构造
    if doi:
        doi_patterns = [
            f"https://link.springer.com/content/pdf/{doi}.pdf",
            f"https://onlinelibrary.wiley.com/doi/pdfdirect/{doi}",
            f"https://journals.sagepub.com/doi/pdf/{doi}",
            f"https://www.tandfonline.com/doi/pdf/{doi}",
            f"https://academic.oup.com/view-large/document/{doi}",
            f"https://www.cambridge.org/core/services/aop-cambridge-core/content/view/{doi.split('10.1017/')[-1] if '10.1017/' in doi else doi}",
        ]
        urls.extend(doi_patterns)
        # 也尝试DOI resolver
        urls.append(f"https://doi.org/{doi}")

    return urls


def safe_filename(paper: dict) -> str:
    """生成安全的文件名"""
    authors = paper.get('authors', 'Unknown')
    first_author = authors.split(",")[0].split(" and ")[0].split(";")[0].strip()
    first_author = re.sub(r'[<>:"/\\|?*]', '', first_author)

    title = paper.get('title', '')
    short_title = re.sub(r'[<>:"/\\|?*]', '', title[:80].strip())
    short_title = re.sub(r'\s+', '_', short_title)

    year = paper.get('year', 0)
    return f"{paper['id']}_{first_author}_{year}_{short_title}"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="RVPN auto-login + paper downloader")
    parser.add_argument("--test", action="store_true", help="Only test RVPN login")
    parser.add_argument("--dry-run", action="store_true", help="List URLs without downloading")
    args = parser.parse_args()

    # Load missing papers
    print("=" * 60)
    print("  RVPN Downloader for ZJU Paywalled Papers")
    print("=" * 60)

    missing = load_missing_papers()
    print(f"\n[1] Missing papers to attempt: {len(missing)}")

    if args.dry_run:
        print("\n--- Download URLs ---")
        for p in missing:
            print(f"\n[{p['domain']}-{p['id']}] {p['title'][:80]}")
            for url in construct_download_urls(p):
                print(f"  {url[:120]}")
        return

    # Create RVPN session
    print(f"\n[2] Creating RVPN session...")
    session = RVPNSession()

    if not session.login():
        print("\n  Login failed. Check credentials in key.txt")
        print("  Alternatively, try manual login via browser at:")
        print("  https://rvpn.zju.edu.cn")
        sys.exit(1)

    if args.test:
        print("\n  Login test PASSED. Run without --test to download.")
        return

    # Download papers
    print(f"\n[3] Downloading papers via RVPN session...")
    downloaded = 0
    failed = 0

    for i, paper in enumerate(missing):
        domain_key = paper['domain']
        domain_name = DOMAIN_MAP.get(domain_key, domain_key)
        domain_dir = KB_DIR / domain_name / "papers"

        print(f"\n[{i+1}/{len(missing)}] [{domain_key}-{paper['id']}] {paper['title'][:80]}")

        # 跳过已有本地文件的
        filename = safe_filename(paper)
        existing = list(domain_dir.glob(f"{paper['id']}_*")) if domain_dir.exists() else []
        if existing:
            print(f"  SKIP: already exists ({existing[0].name})")
            downloaded += 1
            continue

        # 构造并尝试下载
        urls = construct_download_urls(paper)
        success = False

        for url in urls:
            save_path = domain_dir / f"{filename}.pdf"
            print(f"  Trying: {url[:120]}")

            # 先尝试直接下载 (RVPN cookie可能生效)
            if session.download_direct(url, save_path):
                size = save_path.stat().st_size
                print(f"  OK -> {save_path.name} ({size//1024} KB)")
                success = True
                downloaded += 1
                break

            # 再尝试通过RVPN代理
            if session.download_via_proxy(url, save_path):
                size = save_path.stat().st_size
                print(f"  OK (proxy) -> {save_path.name} ({size//1024} KB)")
                success = True
                downloaded += 1
                break

        if not success:
            print(f"  FAILED: all URLs returned non-PDF content")
            failed += 1

        time.sleep(DOWNLOAD_DELAY)

    print(f"\n{'='*60}")
    print(f"  FINAL: {downloaded} downloaded, {failed} failed")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
