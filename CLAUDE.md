# CLAUDE.md

## Project Overview

This is an academic research project in **philosophy of science & technology, ethics, and AI alignment** from a mechanistic interpretability perspective. The core ambition is to bridge industry empirical research (primarily Anthropic's mechanistic interpretability work) with philosophical analysis, producing technically-informed philosophical scholarship.

**Primary language:** Chinese (中文). Code, technical terms, and paper titles may remain in English. Writing drafts and outlines are in Chinese.

## Research Domains

The project sits at the intersection of three fields:

1. **Mechanistic Interpretability (机械可解释性)** — Understanding the internal computations of neural networks. Key topics:
   - Sparse Autoencoders (SAEs) for feature decomposition
   - Non-Linear Activation (NLA) / activation engineering
   - Circuit-level analysis and causal intervention
   - Superposition hypothesis and polysemanticity
   - Dictionary learning for interpretability
   - Anthropic's published research (Transformer Circuits threads, etc.)

2. **AI Alignment Theory (AI对齐理论)** — What it means for AI systems to be aligned with human values, and how to achieve it:
   - Inner vs. outer alignment distinction
   - Deceptive alignment and mesa-optimization
   - Scalable oversight and debate
   - Value learning and specification
   - Mechanistic anomaly detection as alignment audit tooling

3. **Philosophy of Science & Ethics (科学技术哲学/伦理学)** — The philosophical lens:
   - Epistemology of black-box vs. white-box models
   - Ontology of learned representations
   - Ethical implications of interpretability (or lack thereof)
   - Scientific understanding vs. engineering control
   - Agency, intentionality, and moral patienthood in AI systems

## Four Core Research Gaps (Identified from Literature)

Based on systematic review of 276 papers across 11 domains, four unresolved philosophical-technical tensions form the project's core contribution space:

### Gap 1: 表征本体论张力 (Representational Ontology)
**Are SAE/discovered features *discovered* (realism) or *constructed* (instrumentalism)?**
- ML literature shows 0% structural realism about features (Culcu 2025)
- SAE practitioners routinely speak of "discovering" features as if they pre-exist
- Only 1/20 papers in the dedicated literature review defends structural realism
- Knowledge base: `knowledge_base/08_representational_ontology/`

### Gap 2: 理解认识论张力 (Epistemology of Understanding)
**Does internal mechanism analysis alone suffice for scientific understanding, or must it be complemented by behavioral validation?**
- Internalists (e.g., Beckmann & Queloz 2026) argue mechanistic organization = understanding
- Externalists (e.g., Friedman & Duede 2026) argue behavioral testing is necessary
- Rigorous complementarism is emerging as the most defensible position
- Knowledge base: `knowledge_base/09_epistemology_understanding/`

### Gap 3: 因果充分性空缺 (Causal Sufficiency)
**Do causal intervention methods capture genuine causal structure or merely intervention-invariant correlations?**
- The Non-Linear Dilemma (Sutter 2025): unconstrained causal abstraction is trivially satisfiable
- Interchange intervention accuracy ≠ causal faithfulness
- MI methods sit at Pearl's L2 (intervention); reaching L3 (counterfactuals) is the key test
- Knowledge base: `knowledge_base/10_causal_sufficiency/`

### Gap 4: 向量奠基问题 (Vector Grounding Problem)
**Do vectors learned by neural networks possess genuine semantic content?**
- Milliere & Coelho Mollo (2026) reformulated Harnad's Symbol Grounding Problem for the vector era
- Six identifiable positions: Semantic Pessimists, Distributional Optimists, Externalist Solutionists, Multimodal/Embodied Solutionists, Moderates, Methodological Critics
- Directly threatens the semantic legitimacy of SAE "concept" features and steering vectors
- Knowledge base: `knowledge_base/11_vector_grounding/`

## Directory Structure

```
.
├── index.html                      # Knowledge graph visualization (vis-network)
├── config.yaml                     # ScholarAIO main configuration
├── config.local.yaml               # API keys (NOT in git)
├── research/                       # Active research notes and drafts per sub-topic
│   ├── mechanistic_interpretability/
│   ├── alignment_theory/
│   ├── ethics/
│   └── philosophy_of_science/
├── knowledge_base/                 # Curated literature knowledge base (276 papers)
│   ├── index.html                  # Master wiki: cross-domain graph + stats
│   ├── 01_sae_features/            # SAE与特征分解 (28 papers)
│   ├── 02_activation_engineering/  # 激活与表征工程 (28 papers)
│   ├── 03_causal_intervention/     # 因果干预与心灵哲学 (32 papers)
│   ├── 04_alignment_safety/        # AI对齐理论与安全 (35 papers)
│   ├── 05_ethics_governance/       # AI伦理与治理 (20 papers)
│   ├── 06_philosophy_of_science/   # 科学哲学：可解释性的认识论 (27 papers)
│   ├── 07_philosophy_of_mind/      # 心灵哲学与AI (23 papers)
│   ├── 08_representational_ontology/  # Gap 1: 表征本体论 (20 papers)
│   ├── 09_epistemology_understanding/ # Gap 2: 理解认识论 (20 papers)
│   ├── 10_causal_sufficiency/         # Gap 3: 因果充分性 (22 papers)
│   ├── 11_vector_grounding/           # Gap 4: 向量奠基 (21 papers)
│   ├── excerpts/                   # Important quoted passages with commentary
│   └── reading_lists/              # Thematic reading lists
├── writing/                        # Formal writing outputs
│   ├── outlines/                   # Paper/chapter outlines
│   ├── drafts/                     # Draft manuscripts
│   └── translations/               # Translations of key English papers
├── resources/                      # External resources and tooling
│   ├── anthropic/                  # Anthropic-specific materials (papers, blog posts)
│   ├── code/                       # Code for analysis/experiments + download automation
│   ├── templates/                  # Wiki HTML template (wiki_template.html)
│   └── tools/                      # Tool configurations
└── data/                           # Data artifacts
    ├── experiments/                # Experiment logs and results
    ├── figures/                    # Generated figures and visualizations
    ├── results/                    # Analysis results (retrieval report)
    ├── inbox/                      # ScholarAIO ingest inbox
    └── papers/                     # ScholarAIO flat papers directory
```

### Each domain/wiki folder contains:
- `wiki.html` — Interactive literature wiki (card browse + detail modal + vis-network graph + notes)
- `papers/` — Downloaded PDFs with standardized naming: `{NNN}_{FirstAuthor}_{Year}_{ShortTitle}.pdf`
- `notes/` — Chinese reading notes for top 4-5 papers

## Literature Knowledge Base Stats

| Domain | Papers | % 2025-26 |
|--------|--------|-----------|
| 01 SAE与特征分解 | 28 | 89% |
| 02 激活与表征工程 | 28 | 93% |
| 03 因果干预与心灵哲学 | 32 | 100% |
| 04 AI对齐理论与安全 | 35 | 94% |
| 05 AI伦理与治理 | 20 | 95% |
| 06 科学哲学 | 27 | 93% |
| 07 心灵哲学与AI | 23 | 91% |
| 08 表征本体论 (Gap 1) | 20 | 90% |
| 09 理解认识论 (Gap 2) | 20 | 90% |
| 10 因果充分性 (Gap 3) | 22 | 91% |
| 11 向量奠基 (Gap 4) | 21 | 91% |
| **Total** | **276** | **~93%** |

PDF coverage: 263/276 (~95%). ~13 remaining: 5 conference talks/book chapters (no preprint), 4 paywalled (need ZJU CARSI), 3 books, 1 NeurIPS paper without preprint. Core reading notes: 60 (5+ per domain, domains 08 and 10 have additional notes for recent papers). Total relations: 500+. Total storage: ~600 MB.

Download automation: `resources/code/batch_download.py` (OA+arXiv strategies), `resources/code/rvpn_download.py` (RSA-encrypted RVPN login), `resources/code/rvpn_playwright.py` (browser-based SSO + batch download), `resources/code/carsi_download.py` (CARSI institutional access). See `data/results/zju_download_guide.md`.

### Download Strategy Reference (lessons from 215→263 PDFs)

**What works (in order of effectiveness):**
1. **arXiv API / direct PDF** — covers ~70% of ML/CS papers. Use `export.arxiv.org/api/query?id_list=` for metadata, `arxiv.org/pdf/{id}.pdf` for PDF.
2. **PhilArchive** — `philpapers.org/archive/{RECID}.pdf` bypasses Cloudflare (unlike `philarchive.org`). Covers ~60% of philosophy papers. Find RECID via PhilPapers search.
3. **OpenReview** — `openreview.net/pdf?id={forum_id}` for NeurIPS/ICML papers without arXiv preprints.
4. **Unpaywall API** — `api.unpaywall.org/v2/{DOI}` for OA status check. Free, no key needed for basic use.
5. **ACL Anthology** — `aclanthology.org/{paper_id}.pdf` for CL papers.

**What doesn't work (for ZJU context):**
- **RVPN programmatic login**: RSA-encrypted password login succeeds and obtains TWFID cookie, but RVPN web-only mode cannot proxy external URLs — requires EasyConnect client with admin privileges.
- **CARSI without browser**: ZJU CAS requires CAPTCHA; Playwright can pre-fill credentials but user must solve CAPTCHA. Even then, most paywalled papers lack DOI metadata to feed into the pipeline.
- **PhilArchive for Taylor & Francis / UChicago papers**: These publishers don't allow PhilArchive deposition (404 on all attempts).
- **Crossref for Chinese titles**: GBK encoding issues on Windows cause garbled queries returning wrong results.

**Key constraints:**
- Windows `PYTHONIOENCODING=utf-8` prefix required for all Python scripts handling Chinese text
- `curl` on Windows Git Bash may mangle Unicode filenames (use ASCII-safe names)
- WebFetch tool blocked for `arxiv.org`, `neurips.cc`, `servicenow.com` — use curl/bash instead

## Key References & Starting Points

### Anthropic Mechanistic Interpretability (core empirical foundation)
- "Toy Models of Superposition" (Elhage et al., 2022)
- "A Mathematical Framework for Transformer Circuits" (Elhage et al., 2021)
- "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning" (Bricken et al., 2023)
- "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet" (Templeton et al., 2024)
- Anthropic's Transformer Circuits Thread (https://transformer-circuits.pub)

### Philosophical Foundations
- Bostrom, *Superintelligence* (2014)
- Dennett, *The Intentional Stance* (1987) — relevant for interpreting model internals
- Woodward, *Making Things Happen* (2003) — interventionist theory of causation
- Harnad, "The Symbol Grounding Problem" (1990)
- de Regt, *Understanding Scientific Understanding* (2017)

### Critical Recent Papers (2025-2026) — See domain wikis for full lists
- Millière & Coelho Mollo (2026) — The Vector Grounding Problem
- Sutter et al. (2025) — The Non-Linear Dilemma in Causal Abstraction
- Culcu (2025) — Structuralist Framework for DNN Representations (0% structural realism finding)
- Queloz & Beckmann (2026) — Mechanistic Indicators of Understanding in LLMs

## Working Conventions

### File Naming
- Use Chinese for outline/draft filenames where natural, English for technical content
- Paper PDFs: `{NNN}_{FirstAuthor}_{Year}_{ShortTitle}.pdf`
- Paper notes: `{NNN}_{FirstAuthor}_{Year}_{ShortTitle}_notes.md`
- Figures: `topic_descriptor.{png,svg,pdf}`

### Notes Format
- Each reading note should include: full citation, key claims, methodology, relevance to this project, critical commentary
- Use frontmatter YAML for structured metadata when useful

### Research Process
1. Literature review: identify key papers → download PDFs → build domain wiki
2. Deep reading: write notes for top 5 papers per domain, annotate inter-paper relationships
3. Develop analysis in `research/` — one file per argument or claim cluster
4. Create paper outlines in `writing/outlines/`
5. Draft in `writing/drafts/`

### Wiki Maintenance
- Each domain wiki is an interactive HTML file with three views: browse (cards), graph (vis-network), notes
- When adding new papers, update the PAPERS array and rebuild relations
- Cross-domain bridges identified in `knowledge_base/index.html` — maintain these connections
- Relation types: `cites`, `extends`, `contradicts`, `shares`, `empirical`, `philosophical`

## Topics of Active Interest

- Whether SAE-discovered features constitute legitimate scientific explanations (epistemology of interpretability)
- The ontology of "features" — are they real, instrumental, or something else? (Gap 1)
- Can internal mechanism analysis alone produce scientific understanding? (Gap 2)
- Do causal intervention methods capture genuine causal structure? (Gap 3)
- Do neural network vectors have genuine semantic content? (Gap 4)
- Mechanistic interpretability as a response to the "black box" critique in AI ethics
- Comparative analysis: NLA vs. SAE as interpretability paradigms
- Can mechanistic understanding ground attributions of agency or responsibility?
- The relationship between superposition and polysemanticity

## ScholarAIO Configuration

- LLM backend: DeepSeek (openai-compat, model: deepseek-chat)
- PDF parser: MinerU (cloud, token configured)
- Config files: `config.yaml` (main) + `config.local.yaml` (keys, NOT in git)
- Papers directory: `data/papers/` (flat ScholarAIO structure)
- Knowledge base: `knowledge_base/` (organized by domain with wikis)

## Common Commands

### Wiki Regeneration (after updating the template)
```bash
# Regenerate all 11 domain wikis from template + extracted data
python resources/code/regenerate_wikis.py
```

### Batch Download Missing PDFs
```bash
# Download from OA sources (arXiv, PhilArchive, OpenReview)
python resources/code/batch_download.py

# Include ZJU campus network attempts
python resources/code/batch_download.py --campus

# List missing papers without downloading
python resources/code/batch_download.py --list-only

# Restrict to a single domain
python resources/code/batch_download.py --domain 06
```

### Institutional Access Downloads
```bash
# CARSI institutional access
python resources/code/carsi_download.py

# RVPN browser-based download (Playwright)
python resources/code/rvpn_playwright.py
```

### ScholarAIO Ingestion
```bash
python -m scholaraio search --query "..."
python -m scholaraio ingest --config config.yaml
```

### PDF Download Strategy (in order of effectiveness)
1. **arXiv API / direct PDF** — covers ~70% of ML/CS papers
2. **PhilArchive** — `philpapers.org/archive/{RECID}.pdf` (bypasses Cloudflare)
3. **OpenReview** — `openreview.net/pdf?id={forum_id}` for NeurIPS/ICML
4. **Unpaywall API** — `api.unpaywall.org/v2/{DOI}` for OA status check
5. **ACL Anthology** — `aclanthology.org/{paper_id}.pdf` for CL papers

Windows-specific constraints: prefix with `PYTHONIOENCODING=utf-8` for Chinese text; use `curl` not WebFetch for PDF URLs; avoid `grep -P` (use `grep -oE`); use ASCII-safe filenames for downloaded PDFs.

## Wiki Data Model

Each domain wiki (`knowledge_base/{NN}_*/wiki.html`) is generated from `resources/templates/wiki_template.html`. It contains inline JavaScript data arrays:

### PAPER object fields
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | 3-digit zero-padded ID |
| `title` | string | Full English title |
| `authors` | string | Full author list |
| `year` | number | Publication year |
| `venue` | string | Venue/journal |
| `doi` | string | DOI or "N/A" |
| `pdf` | string | Relative path to PDF |
| `priority` | "must"|"important"|"ref" | Reading priority |
| `tags` | string[] | Topic tags |
| `summary_cn` | string | 1-sentence Chinese summary (used for graph node labels) |
| `abstract_cn` | string | Extended Chinese abstract |
| `methodology` | string | Method description |
| `findings` | string | Core findings |
| `limitations` | string | Limitations |
| `relevance` | string | Relevance to this project |
| `relations` | array | Inter-paper relationships: `{target, type, label}` |

### Relation types
`cites`, `extends`, `contradicts`, `shares`, `empirical`, `philosophical`

### Graph node labels
Graph nodes display the **core conclusion** (from `summary_cn`, truncated to ~35 chars) instead of paper titles, with tooltips showing the full title + authors + summary.

### Cross-domain bridges
Hardcoded in `knowledge_base/index.html` as HTML cards. Each bridge connects 2-3 domains with a description and linked papers.

## Git Workflow
- PDFs are gitignored (`knowledge_base/*/papers/` and `*.pdf`) — do not commit them
- `config.local.yaml` and `key.txt` are gitignored
- Primary version-controlled artifacts: wiki HTML files, research notes, writing drafts, Python scripts
- Commit messages: bilingual (Chinese description, English technical terms)

## Notes for Claude

- When suggesting readings, prioritize works that bridge technical and philosophical perspectives
- Chinese is the working language for prose; use it for summaries, outlines, drafts unless specified otherwise
- Technical precision matters — do not oversimplify mechanistic interpretability concepts
- The project aims for philosophical rigor grounded in technical accuracy; flag any claims that misrepresent the underlying ML research
- `knowledge_base/index.html` is the master wiki — update it when adding new domains or key cross-domain bridges
- The 4 research gaps (08-11) are the project's core contribution space — frame new work in relation to them
- ScholarAIO tools (search/import/ingest/enrich/arxiv) are available for literature retrieval
- When adding papers to a domain wiki, always annotate inter-paper relations (1-3 per paper)
- When downloading papers: try arXiv first for ML/CS, PhilPapers for philosophy, OpenReview for NeurIPS without arXiv, Unpaywall for OA status check
- `curl` is preferred over WebFetch for known PDF URLs (arXiv, PhilArchive, OpenReview) since WebFetch blocks many academic domains
- For paywalled papers: check Unpaywall first; if closed, flag as needing ZJU institutional access rather than spending cycles on dead ends
- Avoid `grep -P` on Windows Git Bash (locale issues); use `grep -oE` or pipe to `python -c` instead
- Non-ASCII characters in filenames (e.g., ä, é) get mangled by Windows shell; use ASCII-safe equivalents when naming downloaded PDFs
