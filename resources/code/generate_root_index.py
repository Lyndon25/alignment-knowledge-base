#!/usr/bin/env python3
"""Generate root index.html — minimalist poster-style landing page with graph."""
import json
from pathlib import Path

STATS_PATH = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\knowledge_base\_stats.json")
OUTPUT_PATH = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\index.html")

with open(STATS_PATH, 'r', encoding='utf-8') as f:
    stats = json.load(f)

domains = stats['domains']
t = stats['totals']

all_entries = [
    ("01_sae_features", "01", "SAE与\n特征分解", "#d97706"),
    ("02_activation_engineering", "02", "激活与\n表征工程", "#0d9488"),
    ("03_causal_intervention", "03", "因果干预\n与心灵哲学", "#7c3aed"),
    ("04_alignment_safety", "04", "AI对齐\n理论与安全", "#6366f1"),
    ("05_ethics_governance", "05", "AI伦理\n与治理", "#dc2626"),
    ("06_philosophy_of_science", "06", "科学哲学\n可解释性", "#ea580c"),
    ("07_philosophy_of_mind", "07", "心灵哲学\n与AI", "#c026d3"),
    ("08_representational_ontology", "G1", "表征本体论\n发现vs构建", "#d97706"),
    ("09_epistemology_understanding", "G2", "理解认识论\n机制vs行为", "#0d9488"),
    ("10_causal_sufficiency", "G3", "因果充分性\n相关vs因果", "#7c3aed"),
    ("11_vector_grounding", "G4", "向量奠基\n分布vs语义", "#dc2626"),
]

# Build domain quick link HTML
domain_links_html = ""
for key, short_id, label, color in all_entries:
    d = domains[key]
    is_gap = key.startswith("08") or key.startswith("09") or key.startswith("10") or key.startswith("11")
    prefix = "0" if not is_gap else "G"
    domain_links_html += f'''          <a class="d-link" href="knowledge_base/{key}/wiki.html" style="--accent:{color}">
            <span class="d-link-id">{short_id}</span>
            <span class="d-link-name">{d['title']}</span>
            <span class="d-link-count">{d['paper_count']}</span>
          </a>\n'''

# Gap descriptions for the bottom section
gap_items = [
    ("G1", "表征本体论", "#d97706", "发现还是构建？", "08_representational_ontology", "20"),
    ("G2", "理解认识论", "#0d9488", "机制还是行为？", "09_epistemology_understanding", "20"),
    ("G3", "因果充分性", "#7c3aed", "相关还是因果？", "10_causal_sufficiency", "22"),
    ("G4", "向量奠基", "#dc2626", "分布还是语义？", "11_vector_grounding", "21"),
]
gap_html = ""
for gid, gtitle, gcolor, gq, gpath, gcount in gap_items:
    gap_html += f'''          <a class="g-card" href="knowledge_base/{gpath}/wiki.html" style="--accent:{gcolor}">
            <div class="g-badge">{gid}</div>
            <div class="g-title">{gtitle}</div>
            <div class="g-q">{gq}</div>
            <div class="g-count">{gcount}篇专题文献 →</div>
          </a>\n'''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>对齐 · 可解释性 · 知识图谱</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@300;400;500;600&family=Sora:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.6/dist/vis-network.min.css" rel="stylesheet">

  <style>
    /* ═══════════════════════════════════════════════
       DESIGN SYSTEM — Poster Edition
       ═══════════════════════════════════════════════ */
    :root {{
      --bg-void: #f4f5f8;
      --bg-primary: #ffffff;
      --bg-card: #f8f9fb;
      --text-primary: #1a1f2e;
      --text-secondary: #4a5a72;
      --text-muted: #7a8aa2;
      --text-faint: #b0bccf;
      --border-subtle: rgba(0,0,0,0.04);
      --border-medium: rgba(0,0,0,0.08);
      --border-strong: rgba(0,0,0,0.14);
      --c-sae: #d97706;
      --c-act: #0d9488;
      --c-causal: #7c3aed;
      --c-align: #6366f1;
      --c-ethics: #dc2626;
      --c-philsci: #ea580c;
      --c-philmind: #c026d3;
      --font-display: 'DM Serif Display', Georgia, serif;
      --font-body: 'Sora', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --transition: 250ms cubic-bezier(0.22, 1, 0.36, 1);
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}

    body {{
      font-family: var(--font-body);
      background: var(--bg-void);
      color: var(--text-primary);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }}

    /* ─── Utility Bar ─── */
    .util {{
      position: fixed; top: 0; left: 0; right: 0;
      z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0.75rem 2rem;
      mix-blend-mode: difference;
      pointer-events: none;
    }}
    .util > * {{ pointer-events: auto; }}
    .util-brand {{
      display: flex; align-items: center; gap: 0.5rem;
      font-family: var(--font-mono);
      font-size: 0.65rem; font-weight: 500;
      color: var(--text-primary);
      text-decoration: none;
      letter-spacing: 0.04em;
    }}
    .util-brand mark {{
      background: none;
      color: var(--text-primary);
      font-family: var(--font-display);
      font-size: 0.85rem;
      font-style: italic;
    }}
    .util-cta {{
      padding: 0.4rem 1.2rem;
      border-radius: 999px;
      background: var(--bg-primary);
      color: var(--text-primary);
      font-family: var(--font-body);
      font-size: 0.78rem; font-weight: 500;
      text-decoration: none;
      border: 1px solid var(--border-medium);
      transition: all var(--transition);
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .util-cta:hover {{
      border-color: var(--text-primary);
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
      transform: translateY(-1px);
    }}

    /* ─── Poster Section ─── */
    .poster {{
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 5rem 2rem 3rem;
      position: relative;
      overflow: hidden;
    }}

    .poster::before {{
      content: '';
      position: absolute;
      top: -20%; right: -10%;
      width: 60%; height: 80%;
      background: radial-gradient(ellipse, rgba(99,102,241,0.03) 0%, transparent 70%);
      pointer-events: none;
    }}
    .poster::after {{
      content: '';
      position: absolute;
      bottom: -10%; left: -10%;
      width: 50%; height: 60%;
      background: radial-gradient(ellipse, rgba(124,58,237,0.03) 0%, transparent 70%);
      pointer-events: none;
    }}

    .poster-title {{
      text-align: center;
      margin-bottom: 2rem;
      position: relative;
      z-index: 1;
    }}
    .poster-title h1 {{
      font-family: var(--font-display);
      font-size: clamp(2rem, 5vw, 3.6rem);
      letter-spacing: -0.03em;
      line-height: 1.15;
      color: var(--text-primary);
      margin-bottom: 0.5rem;
    }}
    .poster-title h1 em {{
      font-style: italic;
      color: var(--text-muted);
    }}
    .poster-title .sub {{
      font-family: var(--font-mono);
      font-size: clamp(0.6rem, 1.2vw, 0.8rem);
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.25em;
    }}

    /* ─── Graph Frame ─── */
    .graph-frame {{
      width: 100%;
      max-width: 960px;
      aspect-ratio: 16 / 9;
      background: var(--bg-primary);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-xl);
      box-shadow:
        0 4px 16px rgba(0,0,0,0.03),
        0 1px 4px rgba(0,0,0,0.02);
      position: relative;
      z-index: 1;
      overflow: hidden;
      margin-bottom: 2.5rem;
      transition: box-shadow var(--transition);
    }}
    .graph-frame:hover {{
      box-shadow:
        0 12px 40px rgba(0,0,0,0.05),
        0 2px 8px rgba(0,0,0,0.03);
    }}
    #knowledgeGraph {{
      width: 100%;
      height: 100%;
    }}
    .graph-frame .graph-hint {{
      position: absolute;
      bottom: 0.75rem; left: 50%;
      transform: translateX(-50%);
      font-family: var(--font-mono);
      font-size: 0.55rem;
      color: var(--text-faint);
      background: var(--bg-primary);
      padding: 0.2rem 0.8rem;
      border-radius: 999px;
      border: 1px solid var(--border-subtle);
      white-space: nowrap;
      opacity: 0;
      transition: opacity var(--transition);
      pointer-events: none;
    }}
    .graph-frame:hover .graph-hint {{
      opacity: 1;
    }}

    /* floating zoom controls inside graph frame */
    .graph-zoom {{
      position: absolute;
      bottom: 0.75rem; right: 0.75rem;
      display: flex; gap: 0.25rem;
      z-index: 5;
      opacity: 0;
      transition: opacity var(--transition);
    }}
    .graph-frame:hover .graph-zoom {{
      opacity: 1;
    }}
    .gz-btn {{
      width: 30px; height: 30px;
      border: 1px solid var(--border-medium);
      border-radius: 50%;
      background: var(--bg-primary);
      color: var(--text-muted);
      font-size: 0.85rem;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: all var(--transition);
      box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .gz-btn:hover {{
      border-color: var(--border-strong);
      color: var(--text-primary);
    }}

    /* ─── Stats Row ─── */
    .stats {{
      display: flex;
      justify-content: center;
      gap: 2.5rem;
      flex-wrap: wrap;
      margin-bottom: 2rem;
      position: relative;
      z-index: 1;
    }}
    .stat-item {{
      text-align: center;
    }}
    .stat-num {{
      font-family: var(--font-display);
      font-size: 1.8rem;
      line-height: 1;
      color: var(--text-primary);
      letter-spacing: -0.02em;
    }}
    .stat-lbl {{
      font-family: var(--font-mono);
      font-size: 0.6rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-top: 0.15rem;
    }}
    .stat-divider {{
      width: 1px;
      background: var(--border-medium);
      align-self: stretch;
    }}

    /* ─── CTA ─── */
    .cta-row {{
      display: flex;
      gap: 1rem;
      align-items: center;
      margin-bottom: 3rem;
      position: relative;
      z-index: 1;
    }}
    .cta-primary {{
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.85rem 2.2rem;
      background: var(--text-primary);
      color: var(--bg-primary);
      font-family: var(--font-body);
      font-size: 1rem;
      font-weight: 500;
      text-decoration: none;
      border-radius: 999px;
      border: none;
      transition: all var(--transition);
      box-shadow: 0 4px 20px rgba(26,31,46,0.12);
      letter-spacing: 0.01em;
    }}
    .cta-primary:hover {{
      background: #2a3048;
      box-shadow: 0 8px 32px rgba(26,31,46,0.18);
      transform: translateY(-2px);
    }}
    .cta-primary .arrow {{
      font-family: var(--font-body);
      transition: transform var(--transition);
    }}
    .cta-primary:hover .arrow {{
      transform: translateX(4px);
    }}
    .cta-secondary {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.85rem 1.5rem;
      background: transparent;
      color: var(--text-muted);
      font-family: var(--font-body);
      font-size: 0.85rem;
      font-weight: 400;
      text-decoration: none;
      border-radius: 999px;
      border: 1px solid var(--border-medium);
      transition: all var(--transition);
    }}
    .cta-secondary:hover {{
      border-color: var(--border-strong);
      color: var(--text-secondary);
    }}

    /* ─── Domain Grid Quick Links ─── */
    .domain-section {{
      width: 100%;
      max-width: 960px;
      margin: 0 auto;
      padding-top: 2rem;
      border-top: 1px solid var(--border-subtle);
      position: relative;
      z-index: 1;
    }}
    .domain-section .sec-label {{
      font-family: var(--font-mono);
      font-size: 0.55rem;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--text-faint);
      margin-bottom: 1rem;
      text-align: center;
    }}
    .domain-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 0.5rem;
    }}
    .d-link {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 0.75rem;
      border-radius: var(--radius-md);
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      text-decoration: none;
      color: var(--text-secondary);
      transition: all var(--transition);
    }}
    .d-link:hover {{
      border-color: var(--accent);
      background: var(--bg-card);
      color: var(--text-primary);
    }}
    .d-link-id {{
      font-family: var(--font-mono);
      font-size: 0.6rem;
      font-weight: 600;
      color: var(--accent);
      min-width: 1.5rem;
    }}
    .d-link-name {{
      font-size: 0.78rem;
      flex: 1;
      line-height: 1.3;
    }}
    .d-link-count {{
      font-family: var(--font-mono);
      font-size: 0.55rem;
      color: var(--text-faint);
    }}

    /* ─── Research Gaps ─── */
    .gap-section {{
      width: 100%;
      max-width: 960px;
      margin: 2rem auto 0;
      padding-top: 2rem;
      border-top: 1px solid var(--border-subtle);
      position: relative;
      z-index: 1;
    }}
    .gap-section .sec-label {{
      font-family: var(--font-mono);
      font-size: 0.55rem;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--text-faint);
      margin-bottom: 1rem;
      text-align: center;
    }}
    .gap-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 0.5rem;
    }}
    .g-card {{
      display: block;
      padding: 0.75rem;
      border-radius: var(--radius-md);
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      text-decoration: none;
      color: var(--text-secondary);
      transition: all var(--transition);
    }}
    .g-card:hover {{
      border-color: var(--accent);
      background: var(--bg-card);
    }}
    .g-badge {{
      font-family: var(--font-mono);
      font-size: 0.55rem;
      font-weight: 600;
      color: var(--accent);
      margin-bottom: 0.2rem;
    }}
    .g-title {{
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 0.1rem;
    }}
    .g-q {{
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-bottom: 0.3rem;
    }}
    .g-count {{
      font-family: var(--font-mono);
      font-size: 0.55rem;
      color: var(--text-faint);
    }}

    /* ─── Footer ─── */
    .footer {{
      text-align: center;
      padding: 2rem;
      color: var(--text-faint);
      font-family: var(--font-mono);
      font-size: 0.55rem;
      letter-spacing: 0.05em;
    }}
    .footer a {{
      color: var(--text-muted);
      text-decoration: none;
    }}
    .footer a:hover {{ color: var(--text-secondary); }}

    /* Animation */
    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(20px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .poster-title {{ animation: fadeUp 0.6s ease both; }}
    .graph-frame {{ animation: fadeUp 0.6s ease 0.15s both; }}
    .stats {{ animation: fadeUp 0.6s ease 0.3s both; }}
    .cta-row {{ animation: fadeUp 0.6s ease 0.4s both; }}
    .domain-section {{ animation: fadeUp 0.6s ease 0.5s both; }}
    .gap-section {{ animation: fadeUp 0.6s ease 0.55s both; }}

    .vis-tooltip {{
      font-family: var(--font-body) !important;
      background: var(--bg-primary) !important;
      border: 1px solid var(--border-medium) !important;
      border-radius: var(--radius-sm) !important;
      color: var(--text-primary) !important;
      font-size: 0.7rem !important;
      padding: 0.5rem 0.75rem !important;
      box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
      line-height: 1.5 !important;
      max-width: 260px !important;
    }}

    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border-strong); border-radius: 4px; }}

    /* Small screens */
    @media (max-width: 640px) {{
      .util {{ padding: 0.5rem 1rem; }}
      .poster {{ padding: 4rem 1rem 2rem; }}
      .stats {{ gap: 1.5rem; }}
      .stat-divider {{ display: none; }}
      .cta-row {{ flex-direction: column; }}
      .domain-grid {{ grid-template-columns: 1fr 1fr; }}
      .gap-grid {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>

  <!-- ═══ Utility Bar ═══ -->
  <div class="util">
    <a href="/" class="util-brand">
      <mark>◇</mark> KG
    </a>
    <a href="knowledge_base/index.html" class="util-cta">知识库 →</a>
  </div>

  <!-- ═══ Poster ═══ -->
  <section class="poster">

    <div class="poster-title">
      <h1>对齐 · 可解释性<br><em>知识图谱</em></h1>
      <div class="sub">AI Alignment · Mechanistic Interpretability · Philosophy of Science</div>
    </div>

    <div class="graph-frame" id="graphFrame">
      <div id="knowledgeGraph"></div>
      <div class="graph-hint">点击节点查看详情 · 拖拽探索</div>
      <div class="graph-zoom">
        <button class="gz-btn" onclick="zoomIn()" title="放大">＋</button>
        <button class="gz-btn" onclick="zoomOut()" title="缩小">−</button>
        <button class="gz-btn" onclick="resetGraph()" title="重置">⟲</button>
      </div>
    </div>

    <div class="stats">
      <div class="stat-item">
        <div class="stat-num">{t['papers']}</div>
        <div class="stat-lbl">文献总量</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-num">{t['domains']}</div>
        <div class="stat-lbl">研究领域</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-num">{t['notes']}</div>
        <div class="stat-lbl">核心笔记</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-num">{t['must']}</div>
        <div class="stat-lbl">核心必读</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <div class="stat-num">~93%</div>
        <div class="stat-lbl">2025–2026</div>
      </div>
    </div>

    <div class="cta-row">
      <a href="knowledge_base/index.html" class="cta-primary">
        进入文献知识库 <span class="arrow">→</span>
      </a>
      <a href="#domains" class="cta-secondary">
        ↓ 浏览领域
      </a>
    </div>

    <div class="domain-section" id="domains">
      <div class="sec-label">研究领域</div>
      <div class="domain-grid">
{domain_links_html}
      </div>
    </div>

    <div class="gap-section">
      <div class="sec-label">核心研究空白</div>
      <div class="gap-grid">
{gap_html}
      </div>
    </div>

  </section>

  <footer class="footer">
    <p>基于 {t['papers']} 篇文献的系统检索与分析 · 2026 年 5 月</p>
    <p style="margin-top:0.3rem">覆盖 arXiv, PhilArchive, PhilPapers, Semantic Scholar, Springer, Oxford, Cambridge 等</p>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.6/dist/vis-network.min.js"></script>
  <script>
  const DOMAINS = [
    {{ id:'01', label:'SAE与\\n特征分解', color:'#d97706', papers:{domains['01_sae_features']['paper_count']}, path:'knowledge_base/01_sae_features/wiki.html',
      title:'{domains['01_sae_features']['title']}', sub:'{domains['01_sae_features']['subtitle']}', notes:{domains['01_sae_features']['note_count']} }},
    {{ id:'02', label:'激活与\\n表征工程', color:'#0d9488', papers:{domains['02_activation_engineering']['paper_count']}, path:'knowledge_base/02_activation_engineering/wiki.html',
      title:'{domains['02_activation_engineering']['title']}', sub:'{domains['02_activation_engineering']['subtitle']}', notes:{domains['02_activation_engineering']['note_count']} }},
    {{ id:'03', label:'因果干预\\n与心灵哲学', color:'#7c3aed', papers:{domains['03_causal_intervention']['paper_count']}, path:'knowledge_base/03_causal_intervention/wiki.html',
      title:'{domains['03_causal_intervention']['title']}', sub:'{domains['03_causal_intervention']['subtitle']}', notes:{domains['03_causal_intervention']['note_count']} }},
    {{ id:'04', label:'AI对齐\\n理论与安全', color:'#6366f1', papers:{domains['04_alignment_safety']['paper_count']}, path:'knowledge_base/04_alignment_safety/wiki.html',
      title:'{domains['04_alignment_safety']['title']}', sub:'{domains['04_alignment_safety']['subtitle']}', notes:{domains['04_alignment_safety']['note_count']} }},
    {{ id:'05', label:'AI伦理\\n与治理', color:'#dc2626', papers:{domains['05_ethics_governance']['paper_count']}, path:'knowledge_base/05_ethics_governance/wiki.html',
      title:'{domains['05_ethics_governance']['title']}', sub:'{domains['05_ethics_governance']['subtitle']}', notes:{domains['05_ethics_governance']['note_count']} }},
    {{ id:'06', label:'科学哲学\\n可解释性', color:'#ea580c', papers:{domains['06_philosophy_of_science']['paper_count']}, path:'knowledge_base/06_philosophy_of_science/wiki.html',
      title:'{domains['06_philosophy_of_science']['title']}', sub:'{domains['06_philosophy_of_science']['subtitle']}', notes:{domains['06_philosophy_of_science']['note_count']} }},
    {{ id:'07', label:'心灵哲学\\n与AI', color:'#c026d3', papers:{domains['07_philosophy_of_mind']['paper_count']}, path:'knowledge_base/07_philosophy_of_mind/wiki.html',
      title:'{domains['07_philosophy_of_mind']['title']}', sub:'{domains['07_philosophy_of_mind']['subtitle']}', notes:{domains['07_philosophy_of_mind']['note_count']} }},
    {{ id:'G1', label:'表征本体论\\n发现vs构建', color:'#d97706', papers:{domains['08_representational_ontology']['paper_count']}, path:'knowledge_base/08_representational_ontology/wiki.html',
      title:'{domains['08_representational_ontology']['title']}', sub:'{domains['08_representational_ontology']['subtitle']}', notes:{domains['08_representational_ontology']['note_count']} }},
    {{ id:'G2', label:'理解认识论\\n机制vs行为', color:'#0d9488', papers:{domains['09_epistemology_understanding']['paper_count']}, path:'knowledge_base/09_epistemology_understanding/wiki.html',
      title:'{domains['09_epistemology_understanding']['title']}', sub:'{domains['09_epistemology_understanding']['subtitle']}', notes:{domains['09_epistemology_understanding']['note_count']} }},
    {{ id:'G3', label:'因果充分性\\n相关vs因果', color:'#7c3aed', papers:{domains['10_causal_sufficiency']['paper_count']}, path:'knowledge_base/10_causal_sufficiency/wiki.html',
      title:'{domains['10_causal_sufficiency']['title']}', sub:'{domains['10_causal_sufficiency']['subtitle']}', notes:{domains['10_causal_sufficiency']['note_count']} }},
    {{ id:'G4', label:'向量奠基\\n分布vs语义', color:'#dc2626', papers:{domains['11_vector_grounding']['paper_count']}, path:'knowledge_base/11_vector_grounding/wiki.html',
      title:'{domains['11_vector_grounding']['title']}', sub:'{domains['11_vector_grounding']['subtitle']}', notes:{domains['11_vector_grounding']['note_count']} }},
  ];

  const EDGES = [
    {{from:'07',to:'01',label:'Vector Grounding',dashes:false,width:1.5}},
    {{from:'07',to:'03',label:'意识因果',dashes:false,width:1.5}},
    {{from:'07',to:'06',label:'意向立场',dashes:false,width:1}},
    {{from:'06',to:'01',label:'特征本体论',dashes:false,width:2}},
    {{from:'06',to:'03',label:'因果vs机制',dashes:false,width:1.5}},
    {{from:'06',to:'02',label:'理解vs控制',dashes:false,width:1}},
    {{from:'01',to:'03',label:'SAE因果验证',dashes:true,width:1.5}},
    {{from:'01',to:'02',label:'特征vs导向',dashes:true,width:1.5}},
    {{from:'02',to:'04',label:'安全应用',dashes:true,width:1}},
    {{from:'03',to:'04',label:'因果审计',dashes:true,width:1.5}},
    {{from:'04',to:'05',label:'治理接口',dashes:true,width:1}},
    {{from:'01',to:'04',label:'SAE审计',dashes:true,width:0.8}},
    {{from:'05',to:'06',label:'XAI治理',dashes:false,width:1}},
    {{from:'G1',to:'01',label:'特征本体',dashes:true,width:1.5}},
    {{from:'G1',to:'06',label:'实在论',dashes:false,width:1.5}},
    {{from:'G2',to:'06',label:'理解标准',dashes:false,width:1.5}},
    {{from:'G2',to:'03',label:'机制解釋',dashes:true,width:1}},
    {{from:'G3',to:'03',label:'因果忠诚性',dashes:false,width:1.5}},
    {{from:'G3',to:'06',label:'干预主义',dashes:false,width:1}},
    {{from:'G4',to:'01',label:'SAE语义',dashes:false,width:1.5}},
    {{from:'G4',to:'07',label:'奠基问题',dashes:false,width:1.5}},
    {{from:'G4',to:'02',label:'向量语义',dashes:true,width:1}},
    {{from:'G1',to:'G4',label:'本体→奠基',dashes:true,width:0.8}},
    {{from:'G2',to:'G3',label:'理解→因果',dashes:true,width:0.8}},
  ];

  let network = null;

  function initGraph() {{
    const nodes = DOMAINS.map(d => ({{
      id: d.id,
      label: d.label,
      color: {{ background: d.color, border: d.color }},
      font: {{ color: '#1a1f2e', size: 10, face: 'Sora', strokeWidth: 2, strokeColor: '#ffffff' }},
      size: 18 + d.papers * 1.0,
      shape: d.id.startsWith('G') ? 'diamond' : 'dot',
      borderWidth: d.id.startsWith('G') ? 2.5 : 2,
      title: `<strong>${{d.title}}</strong><br><em>${{d.sub}}</em><br><br>📄 ${{d.papers}} papers · 📝 ${{d.notes}} notes`,
    }}));

    const edges = EDGES.map(e => ({{
      from: e.from, to: e.to,
      label: e.label,
      color: {{ color: 'rgba(0,0,0,0.08)', highlight: 'rgba(0,0,0,0.2)' }},
      width: e.width || 1,
      smooth: {{ type: 'curvedCW', roundness: 0.12 }},
      font: {{ size: 7, color: 'rgba(0,0,0,0.25)', face: 'JetBrains Mono', strokeWidth: 2, strokeColor: '#ffffff', align: 'middle' }},
      dashes: e.dashes,
    }}));

    const container = document.getElementById('knowledgeGraph');
    network = new vis.Network(container, {{ nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) }}, {{
      nodes: {{ font: {{ face: 'Sora', size: 10, color: '#1a1f2e', strokeWidth: 2, strokeColor: '#ffffff' }}, borderWidth: 2 }},
      edges: {{ smooth: {{ type: 'curvedCW', roundness: 0.12 }} }},
      physics: {{
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {{ gravitationalConstant: -25, centralGravity: 0.003, springLength: 160, springConstant: 0.04, damping: 0.45 }},
        stabilization: {{ iterations: 80, fit: true }}
      }},
      interaction: {{ hover: true, tooltipDelay: 150, keyboard: false }},
    }});

    network.on('click', function(params) {{
      if (params.nodes.length > 0) {{
        const d = DOMAINS.find(x => x.id === params.nodes[0]);
        if (d && d.path) window.location.href = d.path;
      }}
    }});

    network.on('stabilizationIterationsDone', function() {{
      network.fit({{ animation: false, padding: 30 }});
    }});

    // Redraw on resize
    window.addEventListener('resize', () => {{
      network.fit({{ animation: false, padding: 30 }});
    }});
  }}

  function zoomIn() {{ if (network) network.moveTo({{ scale: network.getScale() * 1.3 }}); }}
  function zoomOut() {{ if (network) network.moveTo({{ scale: network.getScale() / 1.3 }}); }}
  function resetGraph() {{ if (network) network.fit({{ animation: true, padding: 30 }}); }}

  document.addEventListener('DOMContentLoaded', initGraph);
  </script>
</body>
</html>'''

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Generated {OUTPUT_PATH}")
