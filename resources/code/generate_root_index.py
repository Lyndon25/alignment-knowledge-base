#!/usr/bin/env python3
"""Generate root index.html — graph-centric project dashboard with navigation."""
import json
from pathlib import Path

STATS_PATH = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\knowledge_base\_stats.json")
OUTPUT_PATH = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\index.html")

with open(STATS_PATH, 'r', encoding='utf-8') as f:
    stats = json.load(f)

domains = stats['domains']
t = stats['totals']

domain_order = [
    ("01_sae_features", "MI", "#f5a623"),
    ("02_activation_engineering", "MI", "#0d9488"),
    ("03_causal_intervention", "MI", "#7c3aed"),
    ("04_alignment_safety", "Align", "#6366f1"),
    ("05_ethics_governance", "Ethics", "#dc2626"),
    ("06_philosophy_of_science", "Phil", "#ea580c"),
    ("07_philosophy_of_mind", "Phil", "#c026d3"),
]
gap_order = [
    ("08_representational_ontology", "Gap", "#d97706"),
    ("09_epistemology_understanding", "Gap", "#0d9488"),
    ("10_causal_sufficiency", "Gap", "#7c3aed"),
    ("11_vector_grounding", "Gap", "#dc2626"),
]

all_domains = domain_order + gap_order

# Build sidebar domain list HTML
sidebar_domains_html = ""
for key, cat, color in all_domains:
    d = domains[key]
    is_gap = key in [g[0] for g in gap_order]
    label_prefix = "G" if is_gap else key[:2]
    sidebar_domains_html += f'''          <button class="s-domain" data-domain="{key}" onclick="focusDomain('{key}')">
            <span class="s-dot" style="background:{color}"></span>
            <span class="s-name">{d['title']}</span>
            <span class="s-count">{d['paper_count']}</span>
          </button>\n'''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>对齐 · 可解释性 · 知识图谱</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@300;400;500;600&family=Sora:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.6/dist/dist/vis-network.min.css" rel="stylesheet">

  <style>
    :root {{
      --bg-void: #06080f;
      --bg-primary: #0c0f1a;
      --bg-secondary: #12182a;
      --bg-tertiary: #1a2238;
      --bg-elevated: #222d4a;
      --text-primary: #dce3f0;
      --text-secondary: #8899bb;
      --text-muted: #556688;
      --text-faint: #334466;
      --border-subtle: rgba(68, 102, 153, 0.08);
      --border-medium: rgba(68, 102, 153, 0.18);
      --border-strong: rgba(68, 102, 153, 0.30);
      --c-mi: #f5a623;
      --c-phil: #2dd4bf;
      --c-ethics: #f87171;
      --c-align: #818cf8;
      --c-gap: #a78bfa;
      --font-display: 'DM Serif Display', Georgia, serif;
      --font-body: 'Sora', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --transition-fast: 150ms ease;
      --transition-base: 250ms cubic-bezier(0.22, 1, 0.36, 1);
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: var(--font-body);
      background: var(--bg-void);
      color: var(--text-primary);
      line-height: 1.6;
      overflow: hidden;
      height: 100vh; width: 100vw;
    }}

    /* ═══════════════════════════════ APP LAYOUT ═══════════════════ */
    .app {{
      display: grid;
      grid-template-columns: 240px 1fr;
      grid-template-rows: 44px 1fr auto;
      grid-template-areas:
        "sidebar topbar"
        "sidebar graph"
        "sidebar detail";
      height: 100vh; width: 100vw;
    }}

    /* ═══════════════════════════════ TOPBAR ═══════════════════════ */
    .topbar {{
      grid-area: topbar;
      background: rgba(12, 15, 26, 0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0 1rem;
      display: flex; align-items: center; gap: 0.5rem;
      z-index: 20;
    }}
    .nav-btn {{
      width: 28px; height: 28px;
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-sm);
      background: transparent;
      color: var(--text-muted);
      font-size: 0.8rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: all var(--transition-fast);
      opacity: 0.6;
    }}
    .nav-btn:hover {{ opacity: 1; border-color: var(--border-strong); color: var(--text-secondary); }}
    .nav-btn:disabled {{ opacity: 0.2; cursor: default; }}

    .topbar-divider {{
      width: 1px; height: 20px;
      background: var(--border-medium);
      margin: 0 0.5rem;
    }}
    .topbar-breadcrumb {{
      font-family: var(--font-mono);
      font-size: 0.6rem;
      color: var(--text-faint);
      letter-spacing: 0.05em;
      flex: 1;
    }}
    .topbar-breadcrumb .current {{ color: var(--text-secondary); }}
    .topbar-spacer {{ flex: 1; }}
    .topbar-stats {{
      display: flex; gap: 1rem;
      font-family: var(--font-mono);
      font-size: 0.55rem;
      color: var(--text-faint);
    }}
    .topbar-stats span {{ color: var(--text-secondary); }}
    .topbar-stats strong {{ color: var(--text-primary); font-weight: 600; }}

    .topbar-link {{
      padding: 0.3rem 0.8rem; border-radius: 999px;
      border: 1px solid var(--border-medium);
      background: transparent;
      color: var(--text-muted);
      font-size: 0.6rem; font-family: var(--font-mono);
      text-decoration: none;
      text-transform: uppercase; letter-spacing: 0.08em;
      transition: all var(--transition-fast);
    }}
    .topbar-link:hover {{
      border-color: var(--border-strong);
      color: var(--text-secondary);
      background: var(--bg-tertiary);
    }}

    /* ═══════════════════════════════ SIDEBAR ══════════════════════ */
    .sidebar {{
      grid-area: sidebar;
      background: var(--bg-primary);
      border-right: 1px solid var(--border-medium);
      padding: 1rem 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      overflow-y: auto;
      z-index: 15;
    }}
    .sidebar::-webkit-scrollbar {{ width: 3px; }}
    .sidebar::-webkit-scrollbar-thumb {{ background: var(--border-strong); border-radius: 3px; }}

    .s-brand {{
      padding-bottom: 0.6rem;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .s-brand-top {{
      display: flex; align-items: center; gap: 0.5rem;
      margin-bottom: 0.15rem;
    }}
    .s-logo {{
      width: 28px; height: 28px;
      border: 1.5px solid var(--border-strong);
      border-radius: var(--radius-sm);
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-mono); font-size: 0.55rem; font-weight: 600;
      color: var(--text-muted);
    }}
    .s-title {{
      font-family: var(--font-display);
      font-size: 0.95rem; letter-spacing: -0.02em;
      line-height: 1.2;
    }}
    .s-sub {{
      font-family: var(--font-mono); font-size: 0.48rem;
      text-transform: uppercase; letter-spacing: 0.15em;
      color: var(--text-faint); margin-left: calc(28px + 0.5rem);
    }}

    .s-section {{ }}
    .s-label {{
      font-family: var(--font-mono); font-size: 0.48rem;
      text-transform: uppercase; letter-spacing: 0.15em;
      color: var(--text-faint);
      margin-bottom: 0.3rem; padding-left: 0.25rem;
    }}

    .s-search {{ position: relative; }}
    .s-search input {{
      width: 100%;
      padding: 0.4rem 0.5rem 0.4rem 1.5rem;
      background: var(--bg-tertiary);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-sm);
      color: var(--text-primary);
      font-family: var(--font-mono);
      font-size: 0.6rem; outline: none;
      transition: border var(--transition-fast);
    }}
    .s-search input::placeholder {{ color: var(--text-faint); }}
    .s-search input:focus {{ border-color: var(--border-strong); }}
    .s-search .s-icon {{
      position: absolute; left: 0.45rem; top: 50%;
      transform: translateY(-50%);
      color: var(--text-faint); font-size: 0.55rem;
      pointer-events: none;
    }}

    .s-filters {{ display: flex; flex-direction: column; gap: 0.2rem; }}
    .s-fbtn {{
      display: flex; align-items: center; gap: 0.4rem;
      padding: 0.3rem 0.5rem;
      border: none; border-radius: var(--radius-sm);
      background: transparent;
      color: var(--text-secondary);
      font-family: var(--font-body); font-size: 0.72rem; font-weight: 500;
      cursor: pointer; transition: all var(--transition-fast);
      text-align: left; width: 100%;
    }}
    .s-fbtn:hover {{ background: var(--bg-tertiary); color: var(--text-primary); }}
    .s-fbtn.active {{ background: var(--bg-tertiary); color: var(--text-primary); }}
    .s-fdot {{
      width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
    }}
    .s-fbtn .s-fcount {{
      margin-left: auto;
      font-family: var(--font-mono); font-size: 0.5rem;
      color: var(--text-faint);
      background: var(--bg-elevated);
      padding: 1px 5px; border-radius: 3px;
    }}
    .s-fbtn.active .s-fcount {{ color: var(--text-secondary); }}

    /* Domain quick list */
    .s-domains {{
      display: flex; flex-direction: column; gap: 0.15rem;
      flex: 1; min-height: 0;
      overflow-y: auto;
    }}
    .s-domains::-webkit-scrollbar {{ width: 2px; }}
    .s-domains::-webkit-scrollbar-thumb {{ background: var(--border-strong); border-radius: 2px; }}
    .s-domain {{
      display: flex; align-items: center; gap: 0.4rem;
      padding: 0.25rem 0.5rem;
      border: none; border-radius: var(--radius-sm);
      background: transparent;
      color: var(--text-muted);
      font-family: var(--font-body); font-size: 0.65rem;
      cursor: pointer; transition: all var(--transition-fast);
      text-align: left; width: 100%;
    }}
    .s-domain:hover {{ background: var(--bg-tertiary); color: var(--text-secondary); }}
    .s-domain.active {{ background: var(--bg-tertiary); color: var(--text-primary); }}
    .s-dot {{ width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }}
    .s-name {{ flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .s-count {{
      font-family: var(--font-mono); font-size: 0.5rem;
      color: var(--text-faint);
    }}

    /* Sidebar stats */
    .s-stats {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.3rem;
      padding: 0.5rem;
      background: var(--bg-secondary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
    }}
    .s-stat-item {{ text-align: center; }}
    .s-stat-val {{
      font-family: var(--font-display);
      font-size: 0.9rem; color: var(--text-primary);
      line-height: 1.2;
    }}
    .s-stat-lbl {{
      font-family: var(--font-mono); font-size: 0.45rem;
      text-transform: uppercase; letter-spacing: 0.1em;
      color: var(--text-faint);
    }}

    /* Legend */
    .s-legend {{
      display: flex; flex-direction: column; gap: 0.2rem;
      padding: 0.4rem 0.5rem;
      background: var(--bg-tertiary);
      border-radius: var(--radius-sm);
    }}
    .s-leg-item {{
      display: flex; align-items: center; gap: 0.4rem;
      font-size: 0.55rem; color: var(--text-muted);
      font-family: var(--font-mono);
    }}
    .s-leg-dot {{ width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }}
    .s-leg-line {{
      width: 14px; height: 0;
      border-top: 1.5px dashed var(--text-faint);
      flex-shrink: 0;
    }}

    .s-footer {{
      font-family: var(--font-mono); font-size: 0.48rem;
      color: var(--text-faint); text-align: center;
      padding-top: 0.4rem;
      border-top: 1px solid var(--border-subtle);
    }}

    /* ═══════════════════════════════ GRAPH ════════════════════════ */
    .graph-area {{
      grid-area: graph;
      position: relative;
      overflow: hidden;
      background:
        radial-gradient(ellipse at 25% 40%, rgba(20, 30, 60, 0.5) 0%, transparent 65%),
        radial-gradient(ellipse at 75% 60%, rgba(40, 20, 60, 0.25) 0%, transparent 55%),
        var(--bg-void);
    }}
    #knowledgeGraph {{ width: 100%; height: 100%; }}

    .graph-watermark {{
      position: absolute; bottom: 1rem; left: 1rem;
      font-family: var(--font-mono); font-size: 0.5rem;
      color: var(--text-faint); opacity: 0.4;
      pointer-events: none;
      line-height: 1.6;
    }}

    .graph-toolbar {{
      position: absolute;
      bottom: 1rem; right: 1rem;
      display: flex; gap: 0.3rem;
      z-index: 5;
    }}
    .graph-btn {{
      width: 32px; height: 32px;
      border: 1px solid var(--border-medium);
      border-radius: 50%;
      background: var(--bg-primary);
      color: var(--text-muted);
      font-size: 0.85rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: all var(--transition-fast);
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}
    .graph-btn:hover {{
      border-color: var(--border-strong);
      color: var(--text-secondary);
      background: var(--bg-secondary);
    }}
    .graph-btn.ghost {{
      background: transparent;
      border-color: transparent;
      box-shadow: none;
    }}
    .graph-btn.ghost:hover {{ background: var(--bg-primary); border-color: var(--border-medium); }}

    .vis-tooltip {{
      font-family: var(--font-body) !important;
      background: var(--bg-elevated) !important;
      border: 1px solid var(--border-strong) !important;
      border-radius: var(--radius-sm) !important;
      color: var(--text-primary) !important;
      font-size: 0.7rem !important;
      padding: 0.5rem 0.75rem !important;
      box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
      line-height: 1.5 !important;
      max-width: 260px !important;
    }}

    /* ═══════════════════════════════ DETAIL PANEL ═════════════════ */
    .detail-panel {{
      grid-area: detail;
      background: var(--bg-primary);
      border-top: 1px solid var(--border-medium);
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.35s cubic-bezier(0.22, 1, 0.36, 1);
      z-index: 10;
    }}
    .detail-panel.open {{ max-height: 340px; overflow-y: auto; }}
    .detail-panel::-webkit-scrollbar {{ width: 4px; }}
    .detail-panel::-webkit-scrollbar-thumb {{ background: var(--border-strong); border-radius: 4px; }}

    .detail-inner {{
      padding: 1.25rem 1.5rem;
      display: grid;
      grid-template-columns: 1fr 260px;
      gap: 1.25rem;
      align-items: start;
    }}

    .detail-title {{
      font-family: var(--font-display);
      font-size: 1.1rem; line-height: 1.3;
      margin-bottom: 0.3rem;
    }}
    .detail-meta {{
      font-size: 0.78rem; color: var(--text-muted);
      margin-bottom: 0.5rem;
    }}
    .detail-desc {{
      font-size: 0.82rem; color: var(--text-secondary);
      line-height: 1.7;
    }}
    .detail-tags {{
      display: flex; gap: 0.3rem; flex-wrap: wrap;
      margin-top: 0.5rem;
    }}
    .detail-tag {{
      padding: 0.15rem 0.55rem; border-radius: 999px;
      background: var(--bg-tertiary); color: var(--text-muted);
      font-size: 0.62rem; font-family: var(--font-mono);
      border: 1px solid var(--border-medium);
    }}

    .detail-actions {{
      display: flex; flex-direction: column; gap: 0.4rem;
    }}
    .detail-btn {{
      display: block; padding: 0.5rem 1rem;
      border-radius: var(--radius-sm);
      background: var(--bg-tertiary);
      border: 1px solid var(--border-medium);
      color: var(--text-secondary);
      text-decoration: none;
      font-size: 0.78rem; text-align: center;
      transition: all var(--transition-fast);
    }}
    .detail-btn:hover {{
      background: var(--bg-elevated);
      border-color: var(--border-strong);
      color: var(--text-primary);
    }}
    .detail-btn.primary {{
      background: var(--c-align);
      border-color: var(--c-align);
      color: white;
    }}
    .detail-btn.primary:hover {{
      opacity: 0.9;
    }}

    .detail-stats {{
      display: grid; grid-template-columns: 1fr 1fr 1fr;
      gap: 0.4rem;
    }}
    .detail-stat {{ text-align: center; padding: 0.4rem; background: var(--bg-secondary); border-radius: var(--radius-sm); }}
    .detail-stat .v {{ font-family: var(--font-display); font-size: 1rem; color: var(--text-primary); }}
    .detail-stat .l {{ font-size: 0.55rem; color: var(--text-faint); font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em; }}

    .detail-empty {{
      grid-column: 1 / -1;
      display: flex; align-items: center; justify-content: center;
      gap: 0.5rem;
      font-family: var(--font-mono);
      font-size: 0.65rem;
      color: var(--text-faint);
      padding: 1.5rem;
    }}
    .detail-empty kbd {{
      padding: 0.1rem 0.35rem;
      background: var(--bg-tertiary);
      border: 1px solid var(--border-medium);
      border-radius: 3px;
      font-family: var(--font-mono);
      font-size: 0.55rem;
    }}

    /* ═══════════════════════════════ OVERLAY ══════════════════════ */
    .detail-overlay {{
      position: fixed; inset: 0; z-index: 25;
      background: rgba(0,0,0,0.3);
      display: none;
    }}
    .detail-overlay.show {{ display: block; }}

    /* ═══════════════════════════════ RESPONSIVE ═══════════════════ */
    @media (max-width: 820px) {{
      .app {{
        grid-template-columns: 1fr;
        grid-template-rows: auto 44px 1fr auto;
        grid-template-areas:
          "sidebar"
          "topbar"
          "graph"
          "detail";
      }}
      .sidebar {{ max-height: 180px; flex-direction: row; flex-wrap: wrap; gap: 0.4rem; padding: 0.6rem; border-right: none; border-bottom: 1px solid var(--border-medium); }}
      .sidebar .s-brand {{ display: none; }}
      .sidebar .s-filters {{ flex: 1; min-width: 120px; }}
      .sidebar .s-domains {{ display: none; }}
      .sidebar .s-stats {{ flex: 1; min-width: 120px; }}
      .sidebar .s-legend {{ flex-direction: row; flex-wrap: wrap; }}
      .sidebar .s-footer {{ display: none; }}
      .detail-inner {{ grid-template-columns: 1fr; }}
      .detail-panel.open {{ max-height: 50vh; }}
    }}

    .vis-network:focus {{ outline: none; }}

    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .detail-inner > * {{ animation: fadeIn 0.25s ease both; }}
  </style>
</head>
<body>

  <div class="app">

    <!-- ═══════════════════ TOPBAR ═══════════════════ -->
    <header class="topbar">
      <button class="nav-btn" id="navBack" onclick="navigateBack()" disabled title="后退">‹</button>
      <button class="nav-btn" id="navFwd" onclick="navigateFwd()" disabled title="前进">›</button>
      <div class="topbar-divider"></div>
      <div class="topbar-breadcrumb">
        <span id="breadcrumb"><span class="current">浏览全部领域</span></span>
      </div>
      <div class="topbar-spacer"></div>
      <div class="topbar-stats">
        <span><strong id="ts-papers">{t['papers']}</strong> 文献</span>
        <span><strong id="ts-domains">{t['domains']}</strong> 领域</span>
        <span><strong id="ts-notes">{t['notes']}</strong> 笔记</span>
      </div>
      <div class="topbar-divider"></div>
      <a href="knowledge_base/index.html" class="topbar-link">知识库 →</a>
    </header>

    <!-- ═══════════════════ SIDEBAR ═══════════════════ -->
    <aside class="sidebar">
      <div class="s-brand">
        <div class="s-brand-top">
          <div class="s-logo">◇</div>
          <div class="s-title">知识图谱</div>
        </div>
        <div class="s-sub">对齐 · 可解释性 · 哲学</div>
      </div>

      <div class="s-section s-search">
        <span class="s-icon">⌕</span>
        <input type="text" id="graphSearch" placeholder="搜索领域与文献…" autocomplete="off">
      </div>

      <div class="s-section">
        <div class="s-label">筛选</div>
        <div class="s-filters">
          <button class="s-fbtn active" data-cat="all" onclick="applyFilter('all')">
            <span class="s-fdot" style="background:var(--text-muted)"></span> 全部领域 <span class="s-fcount">{t['domains']}</span>
          </button>
          <button class="s-fbtn" data-cat="mi" onclick="applyFilter('mi')">
            <span class="s-fdot" style="background:var(--c-mi)"></span> 机械可解释性 <span class="s-fcount">3</span>
          </button>
          <button class="s-fbtn" data-cat="align" onclick="applyFilter('align')">
            <span class="s-fdot" style="background:var(--c-align)"></span> 对齐 &amp; 安全 <span class="s-fcount">1</span>
          </button>
          <button class="s-fbtn" data-cat="ethics" onclick="applyFilter('ethics')">
            <span class="s-fdot" style="background:var(--c-ethics)"></span> 伦理 &amp; 治理 <span class="s-fcount">1</span>
          </button>
          <button class="s-fbtn" data-cat="phil" onclick="applyFilter('phil')">
            <span class="s-fdot" style="background:var(--c-phil)"></span> 科学 &amp; 心灵哲学 <span class="s-fcount">2</span>
          </button>
          <button class="s-fbtn" data-cat="gap" onclick="applyFilter('gap')">
            <span class="s-fdot" style="background:var(--c-gap)"></span> 研究空白 <span class="s-fcount">4</span>
          </button>
        </div>
      </div>

      <div class="s-section" style="flex:1;min-height:0;display:flex;flex-direction:column;">
        <div class="s-label">领域快速导航</div>
        <div class="s-domains" id="domainList">
{sidebar_domains_html}
        </div>
      </div>

      <div class="s-section">
        <div class="s-stats">
          <div class="s-stat-item"><div class="s-stat-val">{t['papers']}</div><div class="s-stat-lbl">文献</div></div>
          <div class="s-stat-item"><div class="s-stat-val">{t['must']}</div><div class="s-stat-lbl">必读</div></div>
          <div class="s-stat-item"><div class="s-stat-val">{t['notes']}</div><div class="s-stat-lbl">笔记</div></div>
          <div class="s-stat-item"><div class="s-stat-val">11</div><div class="s-stat-lbl">领域</div></div>
        </div>
      </div>

      <div class="s-section">
        <div class="s-legend">
          <div class="s-leg-item"><span class="s-leg-dot" style="background:var(--c-mi)"></span> 机械可解释性</div>
          <div class="s-leg-item"><span class="s-leg-dot" style="background:var(--c-phil)"></span> 科学技术 &amp; 心灵哲学</div>
          <div class="s-leg-item"><span class="s-leg-dot" style="background:var(--c-ethics)"></span> 伦理 &amp; 治理</div>
          <div class="s-leg-item"><span class="s-leg-dot" style="background:var(--c-align)"></span> 对齐 &amp; 安全</div>
          <div class="s-leg-item"><span class="s-leg-dot" style="background:var(--c-gap);opacity:0.7"></span> 核心研究空白</div>
          <div class="s-leg-item"><span class="s-leg-line"></span> 跨领域关联</div>
        </div>
      </div>

      <div class="s-footer">点击节点 · 拖拽探索 · Esc 关闭详情</div>
    </aside>

    <!-- ═══════════════════ GRAPH ═══════════════════ -->
    <div class="graph-area">
      <div id="knowledgeGraph"></div>
      <div class="graph-watermark">✦ 节点大小 = 文献数量 · 菱形 = 研究空白</div>
      <div class="graph-toolbar">
        <button class="graph-btn ghost" onclick="resetView()" title="重置视角">⟲</button>
        <button class="graph-btn" onclick="zoomIn()" title="放大">＋</button>
        <button class="graph-btn" onclick="zoomOut()" title="缩小">−</button>
      </div>
    </div>

    <!-- ═══════════════════ DETAIL PANEL ═══════════════════ -->
    <div class="detail-panel" id="detailPanel">
      <div class="detail-inner" id="detailContent">
        <div class="detail-empty">
          点击图中的 <kbd>●</kbd> 节点查看领域详情
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.6/dist/vis-network.min.js"></script>
  <script>
  /* ═══════════════════════════════════════════════════════════════
     DATA — 11 domains + 4 research gaps
     ═══════════════════════════════════════════════════════════════ */
  const DOMAINS = [
    {{ id:'01', label:'SAE与\\n特征分解', cat:'mi', color:'#f5a623', papers:{domains['01_sae_features']['paper_count']}, must:{domains['01_sae_features']['must_count']}, notes:{domains['01_sae_features']['note_count']}, path:'knowledge_base/01_sae_features/wiki.html',
      title:'{domains['01_sae_features']['title']}', sub:'{domains['01_sae_features']['subtitle']}',
      tags:{json.dumps(domains['01_sae_features']['tags'][:8])},
      desc:'稀疏自编码器（SAE）将神经网络激活分解为可解释的、单语义的特征。本领域涵盖SAE架构设计、缩放定律、评估基准、特征吸收与分裂现象，以及跨层编码器（Crosscoder）等前沿方法。' }},
    {{ id:'02', label:'激活与\\n表征工程', cat:'mi', color:'#0d9488', papers:{domains['02_activation_engineering']['paper_count']}, must:{domains['02_activation_engineering']['must_count']}, notes:{domains['02_activation_engineering']['note_count']}, path:'knowledge_base/02_activation_engineering/wiki.html',
      title:'{domains['02_activation_engineering']['title']}', sub:'{domains['02_activation_engineering']['subtitle']}',
      tags:{json.dumps(domains['02_activation_engineering']['tags'][:8])},
      desc:'不依赖SAE的替代范式：通过直接操控模型内部激活来理解其表征结构。包括导向向量（Steering Vectors）、表征工程（RepE）、非线性激活追踪（NLA）等方法，以及它们在安全-效用权衡中的应用。' }},
    {{ id:'03', label:'因果干预\\n与心灵哲学', cat:'mi', color:'#7c3aed', papers:{domains['03_causal_intervention']['paper_count']}, must:{domains['03_causal_intervention']['must_count']}, notes:{domains['03_causal_intervention']['note_count']}, path:'knowledge_base/03_causal_intervention/wiki.html',
      title:'{domains['03_causal_intervention']['title']}', sub:'{domains['03_causal_intervention']['subtitle']}',
      tags:{json.dumps(domains['03_causal_intervention']['tags'][:8])},
      desc:'使用因果干预方法（Path Patching、Interchange Intervention、Causal Abstraction）定位模型内部因果结构。本领域同时探讨这些方法对心灵哲学（意向立场、预测加工理论）的启发。' }},
    {{ id:'04', label:'AI对齐\\n理论与安全', cat:'align', color:'#6366f1', papers:{domains['04_alignment_safety']['paper_count']}, must:{domains['04_alignment_safety']['must_count']}, notes:{domains['04_alignment_safety']['note_count']}, path:'knowledge_base/04_alignment_safety/wiki.html',
      title:'{domains['04_alignment_safety']['title']}', sub:'{domains['04_alignment_safety']['subtitle']}',
      tags:{json.dumps(domains['04_alignment_safety']['tags'][:8])},
      desc:'AI对齐的核心理论问题：什么是"对齐"？如何确保AI系统的行为符合人类意图？涵盖可扩展监督（Scalable Oversight）、宪法AI（Constitutional AI）、负责任扩展政策（RSP）、欺骗对齐（Deceptive Alignment）和安全案例（Safety Cases）。' }},
    {{ id:'05', label:'AI伦理\\n与治理', cat:'ethics', color:'#dc2626', papers:{domains['05_ethics_governance']['paper_count']}, must:{domains['05_ethics_governance']['must_count']}, notes:{domains['05_ethics_governance']['note_count']}, path:'knowledge_base/05_ethics_governance/wiki.html',
      title:'{domains['05_ethics_governance']['title']}', sub:'{domains['05_ethics_governance']['subtitle']}',
      tags:{json.dumps(domains['05_ethics_governance']['tags'][:8])},
      desc:'AI系统的伦理意涵与治理框架：道德患者地位（Moral Patienthood）、AI权利、参与式对齐（Participatory Alignment）、可解释性作为治理基础设施（XAI 2.0）、国际协调与安全标准。' }},
    {{ id:'06', label:'科学哲学\\n可解释性', cat:'phil', color:'#ea580c', papers:{domains['06_philosophy_of_science']['paper_count']}, must:{domains['06_philosophy_of_science']['must_count']}, notes:{domains['06_philosophy_of_science']['note_count']}, path:'knowledge_base/06_philosophy_of_science/wiki.html',
      title:'{domains['06_philosophy_of_science']['title']}', sub:'{domains['06_philosophy_of_science']['subtitle']}',
      tags:{json.dumps(domains['06_philosophy_of_science']['tags'][:8])},
      desc:'从科学哲学角度审视机械可解释性的认识论地位：SAE发现的特征具有什么本体论地位？内部机制分析能否产生真正的科学理解？可解释性"幻觉"的认识论风险是什么？' }},
    {{ id:'07', label:'心灵哲学\\n与AI', cat:'phil', color:'#c026d3', papers:{domains['07_philosophy_of_mind']['paper_count']}, must:{domains['07_philosophy_of_mind']['must_count']}, notes:{domains['07_philosophy_of_mind']['note_count']}, path:'knowledge_base/07_philosophy_of_mind/wiki.html',
      title:'{domains['07_philosophy_of_mind']['title']}', sub:'{domains['07_philosophy_of_mind']['subtitle']}',
      tags:{json.dumps(domains['07_philosophy_of_mind']['tags'][:8])},
      desc:'AI系统是否可能拥有意识、意向性或道德地位？机械可解释性如何为这些哲学问题提供经验证据？涵盖意识理论测试、意向立场、延展心灵论题和计算"感受质"问题。' }},
    {{ id:'G1', label:'表征本体论\\n发现vs构建', cat:'gap', color:'#d97706', papers:{domains['08_representational_ontology']['paper_count']}, must:{domains['08_representational_ontology']['must_count']}, notes:{domains['08_representational_ontology']['note_count']}, path:'knowledge_base/08_representational_ontology/wiki.html',
      title:'{domains['08_representational_ontology']['title']}', sub:'{domains['08_representational_ontology']['subtitle']}',
      tags:{json.dumps(domains['08_representational_ontology']['tags'][:8])},
      desc:'核心问题：SAE/激活工程揭示的特征是"被发现"的（实在论）还是"被构建"的（工具论）？文献系统综述显示ML文献中0%的结构实在论立场（Culcu 2025），但SAE从业者普遍以实在论方式言说。' }},
    {{ id:'G2', label:'理解认识论\\n机制vs行为', cat:'gap', color:'#0d9488', papers:{domains['09_epistemology_understanding']['paper_count']}, must:{domains['09_epistemology_understanding']['must_count']}, notes:{domains['09_epistemology_understanding']['note_count']}, path:'knowledge_base/09_epistemology_understanding/wiki.html',
      title:'{domains['09_epistemology_understanding']['title']}', sub:'{domains['09_epistemology_understanding']['subtitle']}',
      tags:{json.dumps(domains['09_epistemology_understanding']['tags'][:8])},
      desc:'核心问题：纯内部机制分析是否足以产生科学理解，还是必须结合行为验证？内部主义者（Beckmann & Queloz 2026）与外部主义者（Friedman & Duede 2026）之间的辩论。' }},
    {{ id:'G3', label:'因果充分性\\n相关vs因果', cat:'gap', color:'#7c3aed', papers:{domains['10_causal_sufficiency']['paper_count']}, must:{domains['10_causal_sufficiency']['must_count']}, notes:{domains['10_causal_sufficiency']['note_count']}, path:'knowledge_base/10_causal_sufficiency/wiki.html',
      title:'{domains['10_causal_sufficiency']['title']}', sub:'{domains['10_causal_sufficiency']['subtitle']}',
      tags:{json.dumps(domains['10_causal_sufficiency']['tags'][:8])},
      desc:'核心问题：当前因果干预方法（path patching, interchange intervention）是否捕捉了真正的因果结构？非线性困境（Sutter 2025）揭示：无约束的因果抽象是平凡可满足的。MI方法停留在Pearl L2，抵达L3是关键检验。' }},
    {{ id:'G4', label:'向量奠基\\n分布vs语义', cat:'gap', color:'#dc2626', papers:{domains['11_vector_grounding']['paper_count']}, must:{domains['11_vector_grounding']['must_count']}, notes:{domains['11_vector_grounding']['note_count']}, path:'knowledge_base/11_vector_grounding/wiki.html',
      title:'{domains['11_vector_grounding']['title']}', sub:'{domains['11_vector_grounding']['subtitle']}',
      tags:{json.dumps(domains['11_vector_grounding']['tags'][:8])},
      desc:'核心问题：神经网络向量是否拥有真正的语义内容？Millière & Coelho Mollo (2026)将Harnad的符号奠基问题重构为向量时代版本。直接威胁SAE特征和导向向量的语义合法性——当前最紧急的哲学-技术交叉问题。' }},
  ];

  const edges = [
    {{from:'07',to:'01',label:'Vector Grounding',type:'related',width:2}},
    {{from:'07',to:'03',label:'意识因果检验',type:'related',width:2}},
    {{from:'07',to:'06',label:'意向立场 vs 机制',type:'related',width:1.5}},
    {{from:'06',to:'01',label:'特征本体论',type:'related',width:2.5}},
    {{from:'06',to:'03',label:'因果 vs 机制解释',type:'related',width:2}},
    {{from:'06',to:'02',label:'理解 vs 控制',type:'related',width:1.5}},
    {{from:'01',to:'03',label:'SAE特征因果验证',type:'cites',width:1.5}},
    {{from:'01',to:'02',label:'特征 vs 导向',type:'cites',width:2}},
    {{from:'02',to:'04',label:'导向安全应用',type:'cites',width:1.5}},
    {{from:'03',to:'04',label:'因果审计对齐',type:'cites',width:2}},
    {{from:'04',to:'05',label:'安全治理接口',type:'cites',width:1.5}},
    {{from:'01',to:'04',label:'SAE审计',type:'cites',width:1}},
    {{from:'05',to:'06',label:'XAI社会技术',type:'related',width:1.5}},
    {{from:'G1',to:'01',label:'SAE特征本体',type:'cites',width:2}},
    {{from:'G1',to:'06',label:'实在论辩论',type:'related',width:2}},
    {{from:'G2',to:'06',label:'理解标准',type:'related',width:2}},
    {{from:'G2',to:'03',label:'机制解释',type:'cites',width:1.5}},
    {{from:'G3',to:'03',label:'因果忠诚性',type:'related',width:2}},
    {{from:'G3',to:'06',label:'干预主义因果',type:'related',width:1.5}},
    {{from:'G4',to:'01',label:'SAE语义地位',type:'related',width:2}},
    {{from:'G4',to:'07',label:'奠基问题',type:'related',width:2}},
    {{from:'G4',to:'02',label:'导向向量语义',type:'cites',width:1.5}},
    {{from:'G1',to:'G4',label:'本体论→奠基',type:'cites',width:1}},
    {{from:'G2',to:'G3',label:'理解→因果',type:'cites',width:1}},
  ];

  const catColorMap = {{
    mi: {{ bg: '#f5a623', border: '#d48b1a' }},
    phil: {{ bg: '#2dd4bf', border: '#1fa894' }},
    ethics: {{ bg: '#f87171', border: '#d45555' }},
    align: {{ bg: '#818cf8', border: '#6366d1' }},
    gap: {{ bg: '#a78bfa', border: '#8b5cf6' }},
  }};

  /* ═══════════════════════════════════════════════════════════════
     STATE
     ═══════════════════════════════════════════════════════════════ */
  let network = null;
  let nodesDataSet = null;
  let edgesDataSet = null;
  let currentFilter = 'all';
  let selectedId = null;

  // Navigation history
  let historyStack = [];
  let historyIndex = -1;

  function pushHistory(id) {{
    // Remove forward entries
    historyStack = historyStack.slice(0, historyIndex + 1);
    historyStack.push(id);
    historyIndex = historyStack.length - 1;
    updateNavButtons();
  }}

  function navigateBack() {{
    if (historyIndex > 0) {{
      historyIndex--;
      const id = historyStack[historyIndex];
      focusNodeById(id);
      updateNavButtons();
    }}
  }}

  function navigateFwd() {{
    if (historyIndex < historyStack.length - 1) {{
      historyIndex++;
      const id = historyStack[historyIndex];
      focusNodeById(id);
      updateNavButtons();
    }}
  }}

  function updateNavButtons() {{
    document.getElementById('navBack').disabled = historyIndex <= 0;
    document.getElementById('navFwd').disabled = historyIndex >= historyStack.length - 1;
  }}

  // Keyboard
  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') deselectNode();
    if ((e.ctrlKey || e.metaKey) && e.key === 'z') {{ e.preventDefault(); navigateBack(); }}
  }});

  /* ═══════════════════════════════════════════════════════════════
     INIT GRAPH
     ═══════════════════════════════════════════════════════════════ */
  function buildNodes(filter) {{
    const filtered = filter === 'all' ? DOMAINS : DOMAINS.filter(d => d.cat === filter);
    return filtered.map(d => {{
      const cc = catColorMap[d.cat] || catColorMap.gap;
      const isGap = d.cat === 'gap';
      const size = 22 + d.papers * 1.0;
      return {{
        id: d.id,
        label: d.label,
        title: `<strong>${{d.title}}</strong><br><em>${{d.sub}}</em><br><br>📄 ${{d.papers}} papers · ⭐ ${{d.must}} must-reads · 📝 ${{d.notes}} notes`,
        color: {{ background: d.color, border: d.color }},
        font: {{ color: '#dce3f0', size: 10, face: 'Sora', strokeWidth: 2, strokeColor: '#0c0f1a' }},
        size: size,
        shape: isGap ? 'diamond' : 'dot',
        borderWidth: isGap ? 2.5 : 2,
        borderWidthSelected: 3,
        shadow: {{
          enabled: true,
          color: d.color + '40',
          size: 15,
          x: 0, y: 0
        }},
        _data: d,
      }};
    }});
  }}

  function buildEdges(filter) {{
    const ids = new Set(DOMAINS.filter(d => filter === 'all' || d.cat === filter).map(d => d.id));
    return edges
      .filter(e => ids.has(e.from) && ids.has(e.to))
      .map(e => ({{
        from: e.from, to: e.to,
        label: e.label,
        color: {{ color: 'rgba(100,130,180,0.2)', highlight: 'rgba(100,130,180,0.4)' }},
        width: e.width || 1,
        smooth: {{ type: 'curvedCW', roundness: 0.12 }},
        font: {{
          color: 'rgba(85,102,136,0.5)',
          size: 7, face: 'JetBrains Mono',
          strokeWidth: 2, strokeColor: '#0c0f1a',
          align: 'middle'
        }},
        dashes: e.type === 'cites',
      }}));
  }}

  function initGraph() {{
    const nodes = buildNodes('all');
    const edg = buildEdges('all');

    nodesDataSet = new vis.DataSet(nodes);
    edgesDataSet = new vis.DataSet(edg);

    const container = document.getElementById('knowledgeGraph');
    network = new vis.Network(container, {{ nodes: nodesDataSet, edges: edgesDataSet }}, {{
      nodes: {{
        font: {{ face: 'Sora', size: 10, color: '#dce3f0', strokeWidth: 2, strokeColor: '#0c0f1a' }},
        borderWidth: 2, borderWidthSelected: 3,
        shadow: {{ enabled: true, size: 12, x: 0, y: 0 }}
      }},
      edges: {{
        smooth: {{ type: 'curvedCW', roundness: 0.12 }},
        font: {{ size: 7, face: 'JetBrains Mono', color: 'rgba(85,102,136,0.5)', strokeWidth: 2, strokeColor: '#0c0f1a', align: 'middle' }},
      }},
      physics: {{
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {{ gravitationalConstant: -30, centralGravity: 0.004, springLength: 180, springConstant: 0.05, damping: 0.4 }},
        stabilization: {{ iterations: 100, fit: true }}
      }},
      interaction: {{ hover: true, tooltipDelay: 200, keyboard: false }},
    }});

    network.on('click', function(params) {{
      if (params.nodes.length > 0) {{
        selectNode(params.nodes[0]);
      }} else {{
        deselectNode();
      }}
    }});

    network.on('doubleClick', function(params) {{
      if (params.nodes.length > 0) {{
        const d = DOMAINS.find(x => x.id === params.nodes[0]);
        if (d && d.path) window.location.href = d.path;
      }}
    }});

    network.on('stabilizationIterationsDone', function() {{
      network.fit({{ animation: false, padding: 40 }});
    }});
  }}

  /* ═══════════════════════════════════════════════════════════════
     SELECTION
     ═══════════════════════════════════════════════════════════════ */
  function selectNode(id) {{
    selectedId = id;
    pushHistory(id);

    const d = DOMAINS.find(x => x.id === id);
    if (!d) return;

    // Highlight in graph
    network.selectNodes([id]);
    network.focus(id, {{ scale: 1.5, animation: true }});

    const allIds = nodesDataSet.getIds();
    const neighbors = network.getConnectedNodes(id);
    allIds.forEach(nid => {{
      nodesDataSet.update({{ id: nid, opacity: nid === id ? 1 : (neighbors.includes(nid) ? 0.85 : 0.2) }});
    }});
    edgesDataSet.forEach(e => {{
      const connected = neighbors.includes(e.from) && neighbors.includes(e.to);
      edgesDataSet.update({{
        id: e.id,
        color: {{ color: connected ? 'rgba(100,130,180,0.4)' : 'rgba(255,255,255,0.03)' }},
        width: connected ? (e.width || 1) * 1.5 : 0.3,
        font: {{ color: connected ? 'rgba(85,102,136,0.8)' : 'rgba(0,0,0,0)', size: connected ? 7 : 0 }}
      }});
    }});

    // Active state in sidebar — fuzzy match domain key
    document.querySelectorAll('.s-domain').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.s-domain').forEach(el => {{
      const key = el.dataset.domain;
      if (key.startsWith(id) || key.includes(id)) el.classList.add('active');
    }});

    // Show detail
    showDetail(d);
    updateBreadcrumb(`聚焦: ${{d.title}}`);
  }}

  function focusNodeById(id) {{
    if (network && nodesDataSet.get(id)) {{
      network.selectNodes([id]);
      network.focus(id, {{ scale: 1.5, animation: true }});
      selectNode(id);
    }}
  }}

  function deselectNode() {{
    selectedId = null;
    nodesDataSet.forEach(n => nodesDataSet.update({{ id: n.id, opacity: 1 }}));
    edgesDataSet.forEach(e => edgesDataSet.update({{
      id: e.id,
      color: {{ color: 'rgba(100,130,180,0.2)' }},
      width: e.width || 1,
      font: {{ color: 'rgba(85,102,136,0.5)', size: 7 }}
    }}));

    network.unselectAll();

    document.querySelectorAll('.s-domain').forEach(el => el.classList.remove('active'));
    document.getElementById('detailPanel').classList.remove('open');
    document.getElementById('detailContent').innerHTML =
      `<div class="detail-empty">点击图中的 <kbd>●</kbd> 节点查看领域详情</div>`;
    updateBreadcrumb('浏览全部领域');
  }}

  function focusDomain(key) {{
    // Map key (e.g. "08_representational_ontology") to graph ID
    const map = {{
      '01_sae_features': '01', '02_activation_engineering': '02',
      '03_causal_intervention': '03', '04_alignment_safety': '04',
      '05_ethics_governance': '05', '06_philosophy_of_science': '06',
      '07_philosophy_of_mind': '07',
      '08_representational_ontology': 'G1', '09_epistemology_understanding': 'G2',
      '10_causal_sufficiency': 'G3', '11_vector_grounding': 'G4',
    }};
    const id = map[key];
    if (id && nodesDataSet.get(id)) {{
      selectNode(id);
    }}
  }}

  /* ═══════════════════════════════════════════════════════════════
     DETAIL PANEL
     ═══════════════════════════════════════════════════════════════ */
  function showDetail(d) {{
    const panel = document.getElementById('detailPanel');
    const tags = d.tags.map(t => `<span class="detail-tag">${{t}}</span>`).join('');
    const isGap = d.cat === 'gap';

    document.getElementById('detailContent').innerHTML = `
      <div>
        <div class="detail-title">${{d.title}}</div>
        <div class="detail-meta">${{d.sub}}</div>
        <div class="detail-desc">${{d.desc}}</div>
        <div class="detail-tags">${{tags}}</div>
      </div>
      <div>
        <div class="detail-stats">
          <div class="detail-stat"><div class="v">${{d.papers}}</div><div class="l">文献</div></div>
          <div class="detail-stat"><div class="v">${{d.must}}</div><div class="l">必读</div></div>
          <div class="detail-stat"><div class="v">${{d.notes}}</div><div class="l">笔记</div></div>
        </div>
        <div class="detail-actions" style="margin-top:0.75rem">
          <a href="${{d.path}}" class="detail-btn primary">进入领域 Wiki →</a>
          <button class="detail-btn" onclick="deselectNode()">关闭详情</button>
        </div>
        ${{isGap ? '<div style="margin-top:0.5rem;font-size:0.7rem;color:var(--text-faint);line-height:1.5;padding:0.5rem;background:var(--bg-secondary);border-radius:var(--radius-sm)">⚠ 此为跨领域研究空白专题库</div>' : ''}}
      </div>
    `;
    panel.classList.add('open');
  }}

  /* ═══════════════════════════════════════════════════════════════
     FILTERS
     ═══════════════════════════════════════════════════════════════ */
  function applyFilter(cat) {{
    if (cat === currentFilter) return;
    currentFilter = cat;

    document.querySelectorAll('.s-fbtn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.s-fbtn[data-cat="${{cat}}"]`).classList.add('active');

    const nodes = buildNodes(cat);
    const edg = buildEdges(cat);

    nodesDataSet.clear();
    edgesDataSet.clear();
    nodesDataSet.add(nodes);
    edgesDataSet.add(edg);

    deselectNode();
    network.setData({{ nodes: nodesDataSet, edges: edgesDataSet }});
    network.stabilize(80);

    updateBreadcrumb(cat === 'all' ? '浏览全部领域' : `筛选: ${{cat}}`);
  }}

  /* ═══════════════════════════════════════════════════════════════
     CONTROLS
     ═══════════════════════════════════════════════════════════════ */
  function zoomIn() {{ if (network) network.moveTo({{ scale: network.getScale() * 1.4 }}); }}
  function zoomOut() {{ if (network) network.moveTo({{ scale: network.getScale() / 1.4 }}); }}
  function resetView() {{ if (network) network.fit({{ animation: true, padding: 40 }}); }}

  function updateBreadcrumb(text) {{
    document.getElementById('breadcrumb').innerHTML = `<span class="current">${{text}}</span>`;
  }}

  /* ═══════════════════════════════════════════════════════════════
     SEARCH
     ═══════════════════════════════════════════════════════════════ */
  let searchTimer;
  document.getElementById('graphSearch').addEventListener('input', function() {{
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {{
      const q = this.value.toLowerCase().trim();
      if (!q) {{
        nodesDataSet.forEach(n => nodesDataSet.update({{ id: n.id, opacity: 1 }}));
        edgesDataSet.forEach(e => edgesDataSet.update({{
          id: e.id,
          color: {{ color: 'rgba(100,130,180,0.2)' }},
          width: e.width || 1,
          font: {{ color: 'rgba(85,102,136,0.5)', size: 7 }}
        }}));
        return;
      }}
      nodesDataSet.forEach(n => {{
        const d = n._data;
        const match = !d ? false :
          d.title.toLowerCase().includes(q) ||
          d.sub.toLowerCase().includes(q) ||
          (d.tags && d.tags.some(t => t.toLowerCase().includes(q))) ||
          d.desc.toLowerCase().includes(q);
        nodesDataSet.update({{ id: n.id, opacity: match ? 1 : 0.12 }});
      }});
    }}, 200);
  }});

  /* ═══════════════════════════════════════════════════════════════
     KEYBOARD SHORTCUTS
     ═══════════════════════════════════════════════════════════════ */
  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') deselectNode();
    if (e.altKey && e.key === 'ArrowLeft') {{ e.preventDefault(); navigateBack(); }}
    if (e.altKey && e.key === 'ArrowRight') {{ e.preventDefault(); navigateFwd(); }}
    // Number keys for filters
    if (e.key === '1') applyFilter('all');
    if (e.key === '2') applyFilter('mi');
    if (e.key === '3') applyFilter('align');
    if (e.key === '4') applyFilter('ethics');
    if (e.key === '5') applyFilter('phil');
    if (e.key === '6') applyFilter('gap');
  }});

  /* ═══════════════════════════════════════════════════════════════
     START
     ═══════════════════════════════════════════════════════════════ */
  document.addEventListener('DOMContentLoaded', () => {{
    initGraph();
  }});
  </script>
</body>
</html>'''

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Generated {OUTPUT_PATH}")
