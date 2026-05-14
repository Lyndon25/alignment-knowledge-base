# ZJU机构访问下载指南

**日期**: 2026-05-13  
**状态**: ~61篇论文缺全文（主要在哲学领域，受付费墙限制）

---

## 前提条件

1. 连接 ZJU RVPN: https://rvpn.zju.edu.cn (已验证可达)
2. 使用 ZJU 学号/工号登录
3. 连接后即可获得校内IP，访问各大出版商订阅内容

## 缺失论文来源分布

| 来源 | 估计篇数 | 访问方式 |
|------|---------|---------|
| Springer Link | ~20篇 | RVPN后直接访问或CARSI |
| Oxford Academic | ~10篇 | RVPN后直接访问 |
| Cambridge Core | ~8篇 | RVPN后直接访问 |
| Taylor & Francis | ~5篇 | RVPN后直接访问 |
| Sage Journals | ~5篇 | RVPN后直接访问 |
| PhilArchive/PhilPapers | ~8篇 | 直接访问（无需付费墙，但被Cloudflare防爬）|
| Wiley | ~3篇 | RVPN后直接访问 |
| Brill | ~2篇 | RVPN后直接访问 |

## 推荐下载流程

### 方法1: RVPN + 浏览器直接下载（推荐）

1. 浏览器打开 https://rvpn.zju.edu.cn 并登录
2. 在RVPN内访问各出版商页面
3. 搜索论文标题 → 下载PDF → 保存到对应领域 papers/ 目录

### 方法2: CARSI认证

部分出版商支持CARSI：
1. 在出版商页面选择 "Institutional Login" 或 "Access through your institution"
2. 搜索 "Zhejiang University" 或 "ZJU"
3. 通过ZJU统一身份认证登录
4. 下载PDF

### 方法3: 浙大图书馆数据库导航

1. 访问 http://libweb.zju.edu.cn
2. 进入"数据库导航"
3. 按出版商筛选 → 直接跳转到订阅内容
4. 搜索并下载

## 缺失论文重点清单

### 领域06: 科学哲学（缺~13篇）
主要来源: Springer (Synthese), Oxford (Brit J Phil Sci), Cambridge (Phil Sci), PhilArchive

关键缺失:
- 结构实在论相关 (Culcu 2025)
- 机械论解释形式化 (Synthese 2025)
- 可解释性认识论 (多项)
- 理解 vs 预测哲学 (多项)

### 领域07: 心灵哲学（缺~12篇）
主要来源: Springer (Phenom Cog Sci), PhilArchive

关键缺失:
- 意识理论 (AST/GWT/IIT)
- 延展心灵 + LLM
- 能动性归因
- 意向立场形式化

### 领域08: 表征本体论（缺~10篇）
主要来源: PhilArchive, Springer, Oxford

关键缺失:
- 特征实在论 vs 工具论
- 表征本体论张力
- 结构实在论应用

### 领域10: 因果充分性（缺~6篇）
主要来源: Springer, Cambridge

### 领域11: 向量奠基（缺~11篇）
主要来源: PhilArchive, Oxford, Springer

### 领域03: 因果干预（缺~7篇）
部分可能有arXiv版本

---

## 文件命名规范（保存时使用）

```
{编号}_{第一作者}_{年份}_{简短标题}.pdf
```

例如: `001_Bricken_2023_Towards_Monosemanticity.pdf`

各领域编号见各领域 `papers/` 目录现有文件，接续编号即可。

---

## 批量下载提示

如果RVPN连接后想批量下载，可以：
1. 使用浏览器扩展（如Zotero Connector）自动抓取元数据和PDF
2. 下载后用 `scholaraio import` 导入并自动提取元数据
3. 按命名规范手动重命名后放入对应 `papers/` 目录

---

## 完成后

```bash
scholaraio ingest <新PDF路径>  # 提取全文文本
scholaraio enrich <论文ID>      # LLM富化元数据
```

然后更新对应领域的 wiki.html。
