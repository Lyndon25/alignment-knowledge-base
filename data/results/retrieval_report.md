# 文献检索完成报告

**日期**: 2026-05-13（更新 2026-05-14）  
**数据源**: arXiv, Semantic Scholar, PhilArchive, PhilPapers, Springer, Oxford, Cambridge, Wiley, Sage  
**方法**: 11个并行检索Agent + ScholarAIO工具链 + Unpaywall OA解析

---

## 总体统计

| 指标 | 数值 |
|------|------|
| 文献总量 | **276篇** |
| 研究领域 | **11个** (7核心 + 4研究空白) |
| 2025-2026年文献 | **~257篇 (93%)** |
| 必读文献 | **55篇** |
| 重要文献 | **130篇** |
| 参考文献 | **91篇** |
| 核心阅读笔记 | **55篇** (每领域5篇) |
| PDF下载成功 | **215篇 (78%)** |
| 缺全文（付费墙） | **~61篇** (主要在哲学领域) |
| 文献间关系 | **500+条边** |
| 总存储 | **~586 MB** |

## 各领域详情

### 01 SAE与特征分解 (28篇)
- **年份**: 2023(1), 2024(2), 2025(19), 2026(6)
- **PDF**: 28个 (2个Anthropic HTML)
- **核心覆盖**: SAE架构(JumpReLU/TopK/Gated/Matryoshka), 特征吸收, 评估基准(SAEBench/FMS/CE-Bench), 特征流形, 跨层编码器, SAE导向, 特征竞争/不稳定性
- **Wiki**: `knowledge_base/01_sae_features/wiki.html` (98 KB)

### 02 激活与表征工程 (28篇)
- **年份**: 2023(2), 2025(17), 2026(9)
- **PDF**: 28个
- **核心覆盖**: RepE范式, CAA, 导向向量可辨识性危机, 安全-效用权衡(AlphaSteer/COAST), 跨模型迁移, 外科手术式拒绝消融, 双用途风险
- **Wiki**: `knowledge_base/02_activation_engineering/wiki.html` (132 KB)

### 03 因果干预与心灵哲学 (32篇)
- **年份**: 100% 2025-2026
- **PDF**: 24个 (均可从arXiv下载)
- **核心覆盖**: 因果抽象理论(DAS/PLOT), 路径修补(RelP/APP/CIRCUS), 贝叶斯因果网, 对齐审计, 预测加工/自由能原理, 能动性/意向性哲学
- **Wiki**: `knowledge_base/03_causal_intervention/wiki.html` (116 KB)

### 04 AI对齐理论与安全 (35篇)
- **年份**: 2022(1), 2023(1), 2025(19), 2026(14)
- **PDF**: 35个
- **核心覆盖**: 可扩展监督(辩论/W2SG), 过程/结果奖励模型(SP-PRM/PROF), Constitutional AI/RLAIF, 安全案例/RSP, 欺骗对齐检测, 自动红队测试, 越狱防御, 对齐审计
- **Wiki**: `knowledge_base/04_alignment_safety/wiki.html` (119 KB)

### 05 AI伦理与治理 (20篇)
- **年份**: 2026(3), 2025(16), 2024(1)
- **PDF**: 12个 (8篇付费墙后提供外部链接)
- **核心覆盖**: AI道德患者地位, AI权利/人格, 价值对齐多元论, 参与式/民主对齐, XAI治理, 国际协调
- **Wiki**: `knowledge_base/05_ethics_governance/wiki.html` (93 KB)

### 06 科学哲学：可解释性的认识论 (27篇)
- **年份**: 2026(3), 2025(22), 前-2024(2)
- **PDF**: 0个 (哲学论文主要在PhilArchive/付费期刊)
- **核心覆盖**: 理解认识论, 特征本体论(实在论vs工具论), 机械论解释形式化, 可解释性的局限, 解释-干预统一, 外部主义挑战
- **Wiki**: `knowledge_base/06_philosophy_of_science/wiki.html` (116 KB)

### 07 心灵哲学与AI (23篇)
- **年份**: 2026(2), 2025(19), 前-2024(2)
- **PDF**: 8个
- **核心覆盖**: 意识理论(AST/GWT/IIT/预测加工), 延展心灵+LLM, Vector Grounding Problem, 计算proto-qualia, 能动性归因, 意向立场形式化
- **Wiki**: `knowledge_base/07_philosophy_of_mind/wiki.html` (126 KB)

## 四核心研究空白 (独立知识库)

| 编号 | 领域 | 论文数 | PDF | % 2025-26 |
|------|------|--------|-----|-----------|
| 08 | 表征本体论张力 | 20篇 | 10 | 90% |
| 09 | 理解认识论张力 | 20篇 | 20 | 90% |
| 10 | 因果充分性空缺 | 22篇 | 16 | 91% |
| 11 | 向量奠基问题 | 21篇 | 10 | 91% |

每个空白建立了独立领域Wiki（三层设计：卡片浏览 + 详情面板 + vis-network图谱）

### G1: 表征本体论张力
ML文献中0%的结构实在论(Culcu 2025) vs SAE实践中的实在论预设。包含智识地理图谱。

### G2: 理解认识论张力
内部机制vs行为验证——外部主义挑战MI的内部主义预设。Internalism-Externalism光谱。

### G3: 因果充分性空缺
当前因果干预方法的因果效力尚未被充分哲学论证。Pearl层级定位。

### G4: 向量奠基问题
Milliere & Coelho Mollo (2026)——对SAE特征语义合法性的最紧急挑战。6立场语义景观。

## 跨领域桥梁文献 (12篇关键)
详见 `knowledge_base/index.html` 中的完整列表和关系图谱。

## 待完成事项
- [ ] ~61篇付费论文通过ZJU机构访问补下载（详见 `data/results/zju_download_guide.md`）
- [ ] 06科学哲学：部分PhilArchive论文需浏览器手动下载（Cloudflare防爬）
- [ ] 后续可按需运行 `ingest` + `enrich` 对核心论文做深度文本提取
- [ ] 补下载完成后更新各领域Wiki中的论文路径
