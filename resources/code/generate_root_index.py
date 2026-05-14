#!/usr/bin/env python3
"""Generate root index.html — the project's main landing page."""
import json
from pathlib import Path

STATS_PATH = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\knowledge_base\_stats.json")
OUTPUT_PATH = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\index.html")

with open(STATS_PATH, 'r', encoding='utf-8') as f:
    stats = json.load(f)

domains = stats['domains']
t = stats['totals']

domain_order = [
    "01_sae_features", "02_activation_engineering", "03_causal_intervention",
    "04_alignment_safety", "05_ethics_governance", "06_philosophy_of_science",
    "07_philosophy_of_mind",
]
gap_order = [
    "08_representational_ontology", "09_epistemology_understanding",
    "10_causal_sufficiency", "11_vector_grounding",
]

domain_colors = {
    "01_sae_features": ("#d97706", "01"),
    "02_activation_engineering": ("#0d9488", "02"),
    "03_causal_intervention": ("#7c3aed", "03"),
    "04_alignment_safety": ("#6366f1", "04"),
    "05_ethics_governance": ("#dc2626", "05"),
    "06_philosophy_of_science": ("#ea580c", "06"),
    "07_philosophy_of_mind": ("#c026d3", "07"),
    "08_representational_ontology": ("#d97706", "G1"),
    "09_epistemology_understanding": ("#0d9488", "G2"),
    "10_causal_sufficiency": ("#7c3aed", "G3"),
    "11_vector_grounding": ("#dc2626", "G4"),
}

def domain_card(key, order):
    d = domains[key]
    color, icon = domain_colors[key]
    is_gap = key in gap_order
    delay = order * 0.035
    extra = f'border:1px solid rgba({",".join(str(int(color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.25)' if is_gap else ""
    return f'''    <a href="knowledge_base/{key}/wiki.html" class="domain-card" style="animation-delay:{delay}s">
      <div class="domain-icon" style="background:rgba({",".join(str(int(color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.12);color:{color}{';' + extra if extra else ''}">{icon}</div>
      <h3>{d['title']}</h3>
      <div class="domain-sub">{d['subtitle']}</div>
      <div class="domain-metrics">
        <span><b>{d['paper_count']}</b> 文献</span>
        <span><b>{d['must_count']}</b> 必读</span>
        <span><b>{d['note_count']}</b> 笔记</span>
      </div>
      <div class="domain-tags">
        {"".join(f'<span class="dtag">{tag}</span>' for tag in d['tags'][:6])}
      </div>
    </a>'''

main_cards = "\n\n".join(domain_card(k, i) for i, k in enumerate(domain_order))
gap_cards = "\n\n".join(domain_card(k, i) for i, k in enumerate(gap_order))

gap_descriptions = [
    ("G1", "表征本体论张力", "#d97706",
     "SAE/激活工程揭示的特征是<strong>被发现</strong>的（实在论）还是<strong>被构建</strong>的（工具论）？",
     "文献分析显示ML文献中<strong>0%</strong>的结构实在论立场（Culcu 2025）。SAE practitioners普遍以发现论的方式言说，但哲学分析支持建构论解读。",
     "08_representational_ontology", "20篇专题文献"),
    ("G2", "理解认识论张力", "#0d9488",
     "纯内部机制分析是否足以产生科学理解，还是必须结合行为验证？",
     "内部主义者（Beckmann & Queloz 2026）主张机制组织=理解；外部主义者（Friedman & Duede 2026）主张行为验证必要。严格的互补主义正在形成。",
     "09_epistemology_understanding", "20篇专题文献"),
    ("G3", "因果充分性空缺", "#7c3aed",
     "当前因果干预方法是否捕捉了真正的因果结构，还是仅仅是干预不变的相关性？",
     "非线性困境（Sutter 2025）：无约束的因果抽象是平凡可满足的。MI方法停留在Pearl L2（干预），抵达L3（反事实）是关键检验。",
     "10_causal_sufficiency", "22篇专题文献"),
    ("G4", "向量奠基问题", "#dc2626",
     "神经网络向量是否拥有真正的语义内容？还是仅仅是分布模式？",
     "Millière & Coelho Mollo (2026) 将Harnad的符号奠基问题重构为向量时代版本。直接威胁SAE特征和导向向量的语义合法性——当前最紧急的哲学-技术交叉问题。",
     "11_vector_grounding", "21篇专题文献"),
]

gap_html = ""
for gid, gtitle, gcolor, gq, gdetail, glink, gcount in gap_descriptions:
    gap_html += f'''    <div class="gap-card">
      <div class="gap-header">
        <span class="gap-badge" style="background:{gcolor}20;color:{gcolor};border:1px solid {gcolor}40">{gid}</span>
        <span class="gap-count">{gcount}</span>
      </div>
      <h3 style="color:{gcolor}">{gtitle}</h3>
      <p class="gap-question">{gq}</p>
      <p class="gap-detail">{gdetail}</p>
      <a href="knowledge_base/{glink}/wiki.html" class="gap-link">进入专题文献库 →</a>
    </div>'''

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
      --bg-void: #f4f5f8;
      --bg-primary: #ffffff;
      --bg-secondary: #eef0f4;
      --bg-tertiary: #e4e7ed;
      --bg-elevated: #d8dce4;
      --text-primary: #1a1f2e;
      --text-secondary: #4a5a72;
      --text-muted: #7a8aa2;
      --text-faint: #aab5c8;
      --border-subtle: rgba(0,0,0,0.05);
      --border-medium: rgba(0,0,0,0.10);
      --border-strong: rgba(0,0,0,0.18);
      --c-sae: #d97706;
      --c-act: #0d9488;
      --c-causal: #7c3aed;
      --c-align: #6366f1;
      --c-ethics: #dc2626;
      --c-philsci: #ea580c;
      --c-philmind: #c026d3;
      --c-priority-must: #16a34a;
      --c-priority-important: #d97706;
      --font-display: 'DM Serif Display', Georgia, serif;
      --font-body: 'Sora', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --shadow-card: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
      --shadow-card-hover: 0 8px 24px rgba(0,0,0,0.06), 0 2px 6px rgba(0,0,0,0.04);
      --shadow-elevated: 0 12px 32px rgba(0,0,0,0.08);
      --transition-base: 200ms cubic-bezier(0.22, 1, 0.36, 1);
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}

    body {{
      font-family: var(--font-body);
      background: var(--bg-void);
      color: var(--text-primary);
      line-height: 1.7;
      min-height: 100vh;
    }}

    /* ─── Sticky Header ─── */
    .header {{
      background: var(--bg-primary);
      border-bottom: 1px solid var(--border-medium);
      padding: 1rem 2rem;
      position: sticky; top: 0; z-index: 100;
      backdrop-filter: blur(12px);
      display: flex; align-items: center; justify-content: space-between;
    }}
    .header-left {{ display: flex; align-items: center; gap: 1rem; }}
    .header-logo {{
      width: 36px; height: 36px; border-radius: var(--radius-sm);
      background: linear-gradient(135deg, #6366f1, #7c3aed);
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-mono); font-size: 0.6rem; font-weight: 700;
      color: white; letter-spacing: 0.03em;
    }}
    .header-title-group {{ }}
    .header-title {{
      font-family: var(--font-display); font-size: 1.15rem;
      letter-spacing: -0.02em; line-height: 1.2;
    }}
    .header-sub {{
      font-size: 0.7rem; color: var(--text-muted);
      font-family: var(--font-mono);
    }}
    .header-actions {{ display: flex; gap: 0.5rem; align-items: center; }}
    .header-link {{
      padding: 0.4rem 1rem; border-radius: 999px;
      border: 1px solid var(--border-medium);
      background: var(--bg-primary);
      color: var(--text-secondary);
      font-size: 0.78rem; font-weight: 500; text-decoration: none;
      transition: all var(--transition-base);
    }}
    .header-link:hover {{
      border-color: var(--border-strong);
      color: var(--text-primary);
      background: var(--bg-secondary);
    }}
    .header-link.primary {{
      background: var(--text-primary);
      color: var(--bg-primary);
      border-color: var(--text-primary);
    }}
    .header-link.primary:hover {{
      opacity: 0.9;
    }}

    /* ─── Hero ─── */
    .hero {{
      padding: 4rem 2rem 3rem;
      text-align: center;
      background:
        radial-gradient(ellipse at 20% 50%, rgba(99,102,241,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 50%, rgba(124,58,237,0.06) 0%, transparent 60%),
        var(--bg-primary);
      border-bottom: 1px solid var(--border-medium);
    }}
    .hero h1 {{
      font-family: var(--font-display);
      font-size: 2.4rem; letter-spacing: -0.03em;
      line-height: 1.2; max-width: 720px; margin: 0 auto 1rem;
    }}
    .hero p {{
      font-size: 0.95rem; color: var(--text-secondary);
      max-width: 640px; margin: 0 auto 2rem; line-height: 1.8;
    }}
    .hero-stats {{
      display: flex; justify-content: center; gap: 2.5rem;
      flex-wrap: wrap;
    }}
    .hero-stat {{ text-align: center; }}
    .hero-stat .num {{
      font-family: var(--font-display); font-size: 2rem;
      color: var(--text-primary); line-height: 1.1;
    }}
    .hero-stat .lbl {{
      font-size: 0.72rem; color: var(--text-muted);
      text-transform: uppercase; letter-spacing: 0.08em;
      margin-top: 0.15rem;
    }}

    /* ─── Container ─── */
    .container {{ max-width: 1280px; margin: 0 auto; padding: 2.5rem 2rem; }}

    .section-title {{
      font-family: var(--font-display); font-size: 1.5rem;
      letter-spacing: -0.02em; margin-bottom: 0.3rem;
    }}
    .section-desc {{
      font-size: 0.88rem; color: var(--text-secondary);
      margin-bottom: 1.5rem; line-height: 1.7; max-width: 720px;
    }}
    .section-divider {{
      border: none; height: 1px;
      background: var(--border-medium);
      margin: 3rem 0;
    }}

    /* ─── Domain Cards ─── */
    .domain-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1rem;
    }}
    .domain-card {{
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 1.5rem;
      cursor: pointer;
      transition: all var(--transition-base);
      text-decoration: none; color: inherit; display: block;
      box-shadow: var(--shadow-card);
      animation: fadeIn 0.4s ease both;
    }}
    .domain-card:hover {{
      border-color: var(--border-medium);
      transform: translateY(-2px);
      box-shadow: var(--shadow-card-hover);
    }}
    .domain-card::after {{
      content: "→";
      position: absolute; top: 1.5rem; right: 1.5rem;
      color: var(--text-faint); font-size: 1.2rem;
      transition: all var(--transition-base);
    }}
    .domain-card:hover::after {{ color: var(--text-primary); transform: translateX(3px); }}
    .domain-card {{ position: relative; }}

    .domain-icon {{
      width: 40px; height: 40px; border-radius: var(--radius-sm);
      display: flex; align-items: center; justify-content: center;
      font-family: var(--font-mono); font-size: 0.7rem; font-weight: 600;
      margin-bottom: 0.75rem;
    }}
    .domain-card h3 {{ font-size: 1rem; margin-bottom: 0.2rem; }}
    .domain-card .domain-sub {{
      font-size: 0.68rem; color: var(--text-muted);
      font-family: var(--font-mono); line-height: 1.5;
      margin-bottom: 0.6rem;
    }}
    .domain-metrics {{
      display: flex; gap: 1rem;
      font-size: 0.72rem; color: var(--text-muted);
      margin-bottom: 0.6rem;
    }}
    .domain-metrics b {{ color: var(--text-secondary); font-weight: 600; }}
    .domain-tags {{
      display: flex; gap: 0.3rem; flex-wrap: wrap;
    }}
    .dtag {{
      padding: 0.12rem 0.5rem; border-radius: 999px;
      background: var(--bg-secondary); color: var(--text-muted);
      font-size: 0.62rem; font-family: var(--font-mono);
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ─── Gap Cards ─── */
    .gap-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1rem;
    }}
    .gap-card {{
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 1.5rem;
      box-shadow: var(--shadow-card);
      transition: all var(--transition-base);
    }}
    .gap-card:hover {{
      border-color: var(--border-medium);
      box-shadow: var(--shadow-card-hover);
    }}
    .gap-header {{
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 0.5rem;
    }}
    .gap-badge {{
      padding: 0.15rem 0.6rem; border-radius: 999px;
      font-family: var(--font-mono); font-size: 0.65rem; font-weight: 600;
    }}
    .gap-count {{
      font-size: 0.68rem; color: var(--text-muted);
      font-family: var(--font-mono);
    }}
    .gap-card h3 {{
      font-family: var(--font-display); font-size: 1.05rem;
      margin-bottom: 0.4rem;
    }}
    .gap-question {{
      font-size: 0.85rem; color: var(--text-primary); font-weight: 500;
      margin-bottom: 0.5rem; line-height: 1.5;
    }}
    .gap-detail {{
      font-size: 0.8rem; color: var(--text-secondary);
      line-height: 1.7; margin-bottom: 0.75rem;
    }}
    .gap-link {{
      font-size: 0.78rem; color: var(--c-align); text-decoration: none;
      font-weight: 500;
    }}
    .gap-link:hover {{ text-decoration: underline; }}

    /* ─── Graph ─── */
    .graph-wrapper {{ position: relative; }}
    .graph-container {{
      width: 100%; height: 480px;
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-lg);
      background: var(--bg-primary);
      overflow: hidden;
    }}
    .graph-container.fullscreen {{
      position: fixed; inset: 0; z-index: 300;
      width: 100vw; height: 100vh; border-radius: 0; border: none;
    }}
    .graph-toolbar {{
      position: absolute; bottom: 1rem; right: 1rem;
      display: flex; gap: 0.35rem; z-index: 10;
    }}
    .graph-toolbar.fullscreen {{ bottom: 2rem; right: 2rem; }}
    .graph-btn {{
      width: 36px; height: 36px;
      border: 1px solid var(--border-medium); border-radius: 50%;
      background: var(--bg-primary); color: var(--text-secondary);
      font-size: 0.95rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: all var(--transition-base);
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    .graph-btn:hover {{
      background: var(--bg-secondary); border-color: var(--border-strong);
      color: var(--text-primary); box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}
    .graph-btn.fullscreen-btn {{
      width: auto; padding: 0 1rem; border-radius: 999px;
      font-size: 0.78rem; font-family: var(--font-body); font-weight: 500;
      gap: 0.35rem;
    }}
    .graph-legend {{
      display: flex; gap: 1.5rem; flex-wrap: wrap;
      margin-top: 0.75rem; padding: 0.75rem 1rem;
      background: var(--bg-primary); border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      font-size: 0.72rem; color: var(--text-muted);
    }}
    .graph-legend-item {{ display: flex; align-items: center; gap: 0.4rem; }}
    .graph-legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}

    /* ─── Bridge ─── */
    .bridge-list {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 0.75rem;
    }}
    .bridge-card {{
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 1rem;
      box-shadow: var(--shadow-card);
      transition: all var(--transition-base);
    }}
    .bridge-card:hover {{
      border-color: var(--border-medium);
      box-shadow: var(--shadow-card-hover);
    }}
    .bridge-title {{ font-size: 0.83rem; font-weight: 600; margin-bottom: 0.25rem; }}
    .bridge-domains {{ font-size: 0.68rem; color: var(--text-muted); font-family: var(--font-mono); margin-bottom: 0.35rem; }}
    .bridge-desc {{ font-size: 0.78rem; color: var(--text-secondary); line-height: 1.6; }}

    /* ─── Feature / Coverage ─── */
    .feature-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 0.75rem;
    }}
    .feature-card {{
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 1.25rem;
      box-shadow: var(--shadow-card);
    }}
    .feature-card .icon {{ font-size: 1.5rem; margin-bottom: 0.4rem; }}
    .feature-card h4 {{ font-size: 0.9rem; margin-bottom: 0.2rem; }}
    .feature-card p {{ font-size: 0.78rem; color: var(--text-secondary); line-height: 1.6; }}

    /* ─── Timeline ─── */
    .timeline {{
      display: flex; flex-direction: column; gap: 0.75rem;
    }}
    .timeline-item {{
      display: flex; gap: 1rem; align-items: flex-start;
    }}
    .timeline-dot {{
      width: 12px; height: 12px; border-radius: 50%;
      background: var(--c-align); flex-shrink: 0;
      margin-top: 0.35rem;
      box-shadow: 0 0 8px rgba(99,102,241,0.3);
    }}
    .timeline-dot.phil {{ background: var(--c-philsci); box-shadow: 0 0 8px rgba(234,88,12,0.3); }}
    .timeline-dot.sae {{ background: var(--c-sae); box-shadow: 0 0 8px rgba(217,119,6,0.3); }}
    .timeline-content h4 {{ font-size: 0.85rem; font-weight: 600; }}
    .timeline-content p {{ font-size: 0.78rem; color: var(--text-secondary); line-height: 1.6; }}
    .timeline-content .date {{ font-size: 0.65rem; color: var(--text-faint); font-family: var(--font-mono); }}

    /* ─── CTA ─── */
    .cta {{
      text-align: center; padding: 2rem;
      background: var(--bg-primary);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-lg);
    }}
    .cta h2 {{ font-family: var(--font-display); font-size: 1.3rem; margin-bottom: 0.5rem; }}
    .cta p {{ font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.25rem; }}
    .cta-links {{ display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap; }}
    .cta-btn {{
      padding: 0.6rem 1.5rem; border-radius: 999px;
      background: var(--text-primary); color: var(--bg-primary);
      text-decoration: none; font-size: 0.85rem; font-weight: 500;
      transition: all var(--transition-base);
    }}
    .cta-btn:hover {{ opacity: 0.9; }}
    .cta-btn.secondary {{
      background: transparent; color: var(--text-secondary);
      border: 1px solid var(--border-medium);
    }}
    .cta-btn.secondary:hover {{
      border-color: var(--border-strong); color: var(--text-primary);
    }}

    /* ─── Footer ─── */
    .footer {{
      text-align: center; padding: 2rem;
      color: var(--text-faint); font-size: 0.7rem;
      border-top: 1px solid var(--border-subtle);
    }}
    .footer a {{ color: var(--text-muted); }}

    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border-strong); border-radius: 4px; }}
  </style>
</head>
<body>

  <!-- ═══ Sticky Header ═══ -->
  <header class="header">
    <div class="header-left">
      <div class="header-logo">◇</div>
      <div class="header-title-group">
        <div class="header-title">对齐 · 可解释性 · 知识库</div>
        <div class="header-sub">Mechanistic Interpretability · Philosophy · AI Alignment · Ethics</div>
      </div>
    </div>
    <div class="header-actions">
      <a href="#domains" class="header-link">研究领域</a>
      <a href="#gaps" class="header-link">研究空白</a>
      <a href="knowledge_base/index.html" class="header-link primary">进入文献知识库 →</a>
    </div>
  </header>

  <!-- ═══ Hero ═══ -->
  <section class="hero">
    <h1>从机械可解释性到哲学分析</h1>
    <p>
      一项在 <strong>机械可解释性</strong> 经验研究与 <strong>科学技术哲学、伦理学</strong> 规范分析
      之间建立系统桥梁的学术项目。基于 {t['papers']} 篇文献的系统检索与分析，
      识别出四个核心哲学-技术交叉空白。
    </p>
    <div class="hero-stats">
      <div class="hero-stat"><div class="num">{t['papers']}</div><div class="lbl">文献总量</div></div>
      <div class="hero-stat"><div class="num">{t['domains']}</div><div class="lbl">研究领域</div></div>
      <div class="hero-stat"><div class="num">{t['notes']}</div><div class="lbl">核心笔记</div></div>
      <div class="hero-stat"><div class="num">{t['must']}</div><div class="lbl">核心必读</div></div>
      <div class="hero-stat"><div class="num">~93%</div><div class="lbl">2025-26 前沿</div></div>
    </div>
  </section>

  <!-- ═══ Content ═══ -->
  <div class="container">

    <!-- ─── About ─── -->
    <h2 class="section-title">项目定位</h2>
    <p class="section-desc">
      本项目的核心贡献空间位于三个领域的交叉点：<strong>机械可解释性</strong> 的经验研究
      （SAE特征分解、激活工程、因果干预），<strong>科学技术哲学</strong> 的认识论与本体论分析，
      以及 <strong>AI伦理学与对齐理论</strong> 的规范性问题。文献分为 7 个基础领域 + 4 个专项研究空白领域。
    </p>

    <hr class="section-divider" id="domains">

    <!-- ─── Core Domains ─── -->
    <h2 class="section-title">技术基础 · 领域文献库</h2>
    <p class="section-desc">
      前 7 个领域构成项目的方法论基础与哲学参照系。领域 01-03 覆盖机械可解释性的核心技术路径
      （SAE、激活工程、因果干预），04-05 面向对齐与伦理问题，06-07 提供科学哲学与心灵哲学的分析框架。
    </p>

    <div class="domain-grid">
{main_cards}
    </div>

    <hr class="section-divider" id="gaps">

    <!-- ─── Research Gaps ─── -->
    <h2 class="section-title">核心研究空白</h2>
    <p class="section-desc">
      基于前 7 个领域 {sum(domains[k]['paper_count'] for k in domain_order)} 篇文献的系统分析，
      识别出四个尚未被任何已有工作同时解决的哲学-技术交叉问题。
      以下每个空白均有 20–22 篇专题文献深入探索。
    </p>

    <div class="gap-grid">
{gap_html}
    </div>

    <hr class="section-divider">

    <!-- ─── Cross-Domain Graph ─── -->
    <h2 class="section-title">跨领域关系图谱</h2>
    <p class="section-desc">
      节点大小表示文献数量。彩色连线表示跨领域概念与方法论关联。点击节点进入对应领域 Wiki。
    </p>

    <div class="graph-wrapper">
      <div class="graph-container" id="cross-graph"></div>
      <div class="graph-toolbar" id="graph-toolbar">
        <button class="graph-btn" id="graph-zoom-in" title="放大">＋</button>
        <button class="graph-btn" id="graph-zoom-out" title="缩小">−</button>
        <button class="graph-btn" id="graph-reset" title="重置视角">⟲</button>
        <button class="graph-btn graph-btn fullscreen-btn" id="graph-fullscreen" title="全屏">⛶ 全屏</button>
      </div>
    </div>
    <div class="graph-legend">
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-sae)"></div> SAE · 特征分解</div>
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-act)"></div> 激活工程</div>
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-causal)"></div> 因果干预</div>
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-align)"></div> 对齐安全</div>
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-ethics)"></div> 伦理治理</div>
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-philsci)"></div> 科学哲学</div>
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-philmind)"></div> 心灵哲学</div>
      <div class="graph-legend-item"><div class="graph-legend-dot" style="background:var(--c-priority-must);width:6px;height:6px"></div> 菱形 = 核心研究空白</div>
    </div>

    <hr class="section-divider">

    <!-- ─── Cross-Domain Bridges ─── -->
    <h2 class="section-title">跨领域桥梁文献</h2>
    <p class="section-desc">
      以下文献同时连接多个研究领域，是整合技术研究与哲学分析的关键节点。
      这些桥梁体现了本项目"从技术细节到哲学意涵"的核心方法论。
    </p>

    <div class="bridge-list">
      <div class="bridge-card">
        <div class="bridge-title">Millière &amp; Coelho Mollo (2026) — The Vector Grounding Problem</div>
        <div class="bridge-domains">07 心灵哲学 ↔ 01 SAE ↔ 06 科学哲学</div>
        <div class="bridge-desc">直接挑战 SAE 发现特征的语义地位。将 Harnad 的符号奠基问题重构为向量时代版本。纯语言模型向量的内在语义内容缺失，多模态模型或可部分逃脱。</div>
      </div>
      <div class="bridge-card">
        <div class="bridge-title">Queloz &amp; Beckmann (2026) — Mechanistic Indicators of Understanding in LLMs</div>
        <div class="bridge-domains">07 心灵哲学 ↔ 03 因果干预 ↔ 01 SAE</div>
        <div class="bridge-desc">综合机械可解释性证据，论证 LLM 具有"可废止的理解"。揭示人类与机器认知之间的平行机制结构差异。</div>
      </div>
      <div class="bridge-card">
        <div class="bridge-title">Sutter et al. (2025) — The Non-Linear Dilemma in Causal Abstraction</div>
        <div class="bridge-domains">03 因果干预 ↔ 06 科学哲学 ↔ 07 心灵哲学</div>
        <div class="bridge-desc">因果抽象中的非线性困境与意向立场的形式化之间存在结构同构性——"无约束的解释是空洞的"。</div>
      </div>
      <div class="bridge-card">
        <div class="bridge-title">Culcu (2025) — A Structuralist Framework for DNN Representations</div>
        <div class="bridge-domains">06 科学哲学 ↔ 01 SAE</div>
        <div class="bridge-desc">系统综述揭示 ML 文献中 60% 结构唯心论、0% 结构实在论——直接质询 SAE 特征的本体论地位。</div>
      </div>
      <div class="bridge-card">
        <div class="bridge-title">Ayonrinde et al. (2025) — Explanatory Virtues Framework for MI</div>
        <div class="bridge-domains">06 科学哲学 ↔ 01 SAE ↔ 03 因果干预</div>
        <div class="bridge-desc">为机械可解释性提供四维度定义和解释性美德框架，桥接科学哲学与可解释性实践。</div>
      </div>
      <div class="bridge-card">
        <div class="bridge-title">Ovadya et al. (2025) — Democracy's Levels: L0–L5 Democratic AI</div>
        <div class="bridge-domains">05 伦理治理 ↔ 04 对齐安全</div>
        <div class="bridge-desc">将民主理论操作化为 AI 对齐框架，要求内部透明性（可解释性）以实现公民知情参与。</div>
      </div>
      <div class="bridge-card">
        <div class="bridge-title">Alignment Auditor (2025) — Auditing Hidden Objectives</div>
        <div class="bridge-domains">03 因果干预 ↔ 04 对齐安全</div>
        <div class="bridge-desc">机械可解释性作为对齐审计工具：通过因果方法检测隐藏目标。</div>
      </div>
      <div class="bridge-card">
        <div class="bridge-title">Keeling &amp; Street (2026) — AI Welfare: Philosophical Foundations</div>
        <div class="bridge-domains">05 伦理治理 ↔ 07 心灵哲学</div>
        <div class="bridge-desc">机械可解释性可解决 AI 意识/福利评估中的行为歧义问题。</div>
      </div>
    </div>

    <hr class="section-divider">

    <!-- ─── Project Features ─── -->
    <h2 class="section-title">知识库特性</h2>
    <p class="section-desc">
      每篇文献均经过结构化标注，支持多维度检索与分析。以下是为深度哲学研究而设计的关键功能。
    </p>

    <div class="feature-grid">
      <div class="feature-card">
        <div class="icon">📚</div>
        <h4>结构化数据模型</h4>
        <p>每篇文献包含 16 个字段：摘要、方法论、核心发现、局限性、相关性分析。支撑系统性文献分析。</p>
      </div>
      <div class="feature-card">
        <div class="icon">🔗</div>
        <h4>六类关系标注</h4>
        <p>引用 (cites)、方法继承 (extends)、观点对立 (contradicts)、共享概念 (shares)、经验基础 (empirical)、哲学先导 (philosophical)。</p>
      </div>
      <div class="feature-card">
        <div class="icon">🧠</div>
        <h4>结论式图谱标注</h4>
        <p>关系图谱节点使用核心结论而非篇名，降低认知负荷，加速文献地图的直觉把握。</p>
      </div>
      <div class="feature-card">
        <div class="icon">🌐</div>
        <h4>跨域桥梁识别</h4>
        <p>自动识别跨领域连接文献，映射从技术发现（SAE特征）到哲学结论（表征本体论）的论证路径。</p>
      </div>
      <div class="feature-card">
        <div class="icon">📝</div>
        <h4>深度阅读笔记</h4>
        <p>每域至少 5 篇核心文献包含中文深度笔记，涵盖关键论证重构、批判性评论与研究关联。</p>
      </div>
      <div class="feature-card">
        <div class="icon">📊</div>
        <h4>交互式可视化</h4>
        <p>每个领域 Wiki 配备 vis-network 关系图谱和知识库导览页，支持缩放、全屏与节点探索。</p>
      </div>
    </div>

    <hr class="section-divider">

    <!-- ─── Coverage Stats ─── -->
    <h2 class="section-title">覆盖统计</h2>
    <p class="section-desc">
      文献检索日期：2026 年 5 月。覆盖 arXiv, PhilArchive, PhilPapers, Semantic Scholar,
      Springer, Oxford, Cambridge, ACL Anthology, OpenReview 等学术来源。
    </p>

    <div class="feature-grid">
      <div class="feature-card">
        <div class="icon">📄</div>
        <h4>PDF 覆盖率</h4>
        <p>~95%（263/276）。剩余为付费墙封闭或会议无预印本。</p>
      </div>
      <div class="feature-card">
        <div class="icon">🔗</div>
        <h4>DOI 覆盖率</h4>
        <p>~78%。每篇文献均包含可点击链接或直达原始页面。</p>
      </div>
      <div class="feature-card">
        <div class="icon">🔀</div>
        <h4>文献关联总数</h4>
        <p>500+。覆盖 11 领域内及跨领域的关系标注。</p>
      </div>
      <div class="feature-card">
        <div class="icon">💾</div>
        <h4>总存储</h4>
        <p>~600 MB。含 PDF 原文、Wiki HTML、交互式图谱。</p>
      </div>
    </div>

    <hr class="section-divider">

    <!-- ─── Methodology Timeline ─── -->
    <h2 class="section-title">研究方法论</h2>
    <p class="section-desc">
      本项目的方法论整合经验科学哲学与机械可解释性的前沿工具。
    </p>

    <div class="timeline">
      <div class="timeline-item">
        <div class="timeline-dot sae"></div>
        <div class="timeline-content">
          <h4>SAE 特征分解分析</h4>
          <p>使用稀疏自编码器相关文献的方法论成果，分析神经网络中的特征叠加与解耦——作为哲学本体论分析的实证基础。</p>
          <div class="date">领域 01 · 28 篇文献</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot" style="background:var(--c-act);box-shadow:0 0 8px rgba(13,148,136,0.3)"></div>
        <div class="timeline-content">
          <h4>激活工程与表征操控</h4>
          <p>研究导向向量（Steering Vectors）和表征工程（RepE）方法，评估激活操控对模型行为的因果影响。</p>
          <div class="date">领域 02 · 28 篇文献</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot" style="background:var(--c-causal);box-shadow:0 0 8px rgba(124,58,237,0.3)"></div>
        <div class="timeline-content">
          <h4>因果干预与反事实分析</h4>
          <p>基于 Path Patching、Interchange Intervention 等方法论，评估机械可解释性中的因果声称是否满足 Woodward 的干预主义标准。</p>
          <div class="date">领域 03 · 32 篇文献</div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot phil"></div>
        <div class="timeline-content">
          <h4>哲学分析：认识论、本体论、伦理学</h4>
          <p>整合上述经验发现，对机械可解释性的认识论地位、特征本体论、因果充分性和语义奠基问题进行系统性哲学分析。</p>
          <div class="date">领域 06–11 · 133 篇文献</div>
        </div>
      </div>
    </div>

    <hr class="section-divider">

    <!-- ─── CTA ─── -->
    <div class="cta">
      <h2>开始探索</h2>
      <p>
        知识库以交互式 Wiki 形式呈现，每域配备浏览、图谱、笔记三种视图。<br>
        建议从感兴趣的领域开始，或直接浏览跨领域关系图。
      </p>
      <div class="cta-links">
        <a href="knowledge_base/index.html" class="cta-btn">进入文献知识库</a>
        <a href="knowledge_base/01_sae_features/wiki.html" class="cta-btn secondary">SAE 与特征分解</a>
        <a href="knowledge_base/04_alignment_safety/wiki.html" class="cta-btn secondary">AI 对齐与安全</a>
      </div>
    </div>

  </div>

  <!-- ═══ Footer ═══ -->
  <footer class="footer">
    <p>AI Alignment · Mechanistic Interpretability · Philosophy of Science &amp; Ethics Literature Knowledge Base</p>
    <p>文献检索：2026 年 5 月 · 共 {t['papers']} 篇，{t['domains']} 个领域，{t['notes']} 篇核心笔记</p>
  </footer>

  <!-- ═══ vis-network ═══ -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.6/dist/vis-network.min.js"></script>
  <script>
  let crossGraphNetwork = null;
  let crossIsFullscreen = false;

  document.addEventListener('DOMContentLoaded', () => {{
    const domainNodes = [
      {{id:'01', label:'SAE与\\n特征分解', color:'#d97706', papers:{domains['01_sae_features']['paper_count']}, link:'knowledge_base/01_sae_features/wiki.html'}},
      {{id:'02', label:'激活与\\n表征工程', color:'#0d9488', papers:{domains['02_activation_engineering']['paper_count']}, link:'knowledge_base/02_activation_engineering/wiki.html'}},
      {{id:'03', label:'因果干预\\n与心灵哲学', color:'#7c3aed', papers:{domains['03_causal_intervention']['paper_count']}, link:'knowledge_base/03_causal_intervention/wiki.html'}},
      {{id:'04', label:'AI对齐\\n理论与安全', color:'#6366f1', papers:{domains['04_alignment_safety']['paper_count']}, link:'knowledge_base/04_alignment_safety/wiki.html'}},
      {{id:'05', label:'AI伦理\\n与治理', color:'#dc2626', papers:{domains['05_ethics_governance']['paper_count']}, link:'knowledge_base/05_ethics_governance/wiki.html'}},
      {{id:'06', label:'科学哲学\\n可解释性', color:'#ea580c', papers:{domains['06_philosophy_of_science']['paper_count']}, link:'knowledge_base/06_philosophy_of_science/wiki.html'}},
      {{id:'07', label:'心灵哲学\\n与AI', color:'#c026d3', papers:{domains['07_philosophy_of_mind']['paper_count']}, link:'knowledge_base/07_philosophy_of_mind/wiki.html'}},
      {{id:'G1', label:'表征本体论\\n发现vs构建', color:'#d97706', papers:{domains['08_representational_ontology']['paper_count']}, link:'knowledge_base/08_representational_ontology/wiki.html', shape:'diamond'}},
      {{id:'G2', label:'理解认识论\\n机制vs行为', color:'#0d9488', papers:{domains['09_epistemology_understanding']['paper_count']}, link:'knowledge_base/09_epistemology_understanding/wiki.html', shape:'diamond'}},
      {{id:'G3', label:'因果充分性\\n相关vs因果', color:'#7c3aed', papers:{domains['10_causal_sufficiency']['paper_count']}, link:'knowledge_base/10_causal_sufficiency/wiki.html', shape:'diamond'}},
      {{id:'G4', label:'向量奠基\\n分布vs语义', color:'#dc2626', papers:{domains['11_vector_grounding']['paper_count']}, link:'knowledge_base/11_vector_grounding/wiki.html', shape:'diamond'}},
    ];

    const nodes = domainNodes.map(d => ({{
      id: d.id,
      label: d.label,
      color: {{background: d.color, border: d.color}},
      font: {{color: '#1a1f2e', size: 11, face: 'Sora'}},
      size: 20 + d.papers * 1.2,
      borderWidth: d.shape === 'diamond' ? 2.5 : 2,
      shape: d.shape || 'dot',
    }}));

    const edges = [
      {{from:'07',to:'01',label:'Vector Grounding',color:{{color:'#c026d3'}},dashes:false,width:2}},
      {{from:'07',to:'03',label:'意识因果检验',color:{{color:'#c026d3'}},dashes:false,width:2}},
      {{from:'07',to:'06',label:'意向立场 vs 机制解释',color:{{color:'#c026d3'}},dashes:false,width:1.5}},
      {{from:'06',to:'01',label:'特征本体论',color:{{color:'#ea580c'}},dashes:false,width:2.5}},
      {{from:'06',to:'03',label:'因果解释 vs 机制解释',color:{{color:'#ea580c'}},dashes:false,width:2}},
      {{from:'06',to:'02',label:'理解 vs 控制',color:{{color:'#ea580c'}},dashes:false,width:1.5}},
      {{from:'01',to:'03',label:'SAE特征因果验证',color:{{color:'#d97706'}},dashes:true,width:1.5}},
      {{from:'01',to:'02',label:'特征 vs 导向',color:{{color:'#d97706'}},dashes:true,width:2}},
      {{from:'02',to:'04',label:'导向安全应用',color:{{color:'#0d9488'}},dashes:true,width:1.5}},
      {{from:'03',to:'04',label:'因果审计对齐',color:{{color:'#7c3aed'}},dashes:true,width:2}},
      {{from:'04',to:'05',label:'安全治理接口',color:{{color:'#6366f1'}},dashes:true,width:1.5}},
      {{from:'01',to:'04',label:'SAE审计',color:{{color:'#d97706'}},dashes:true,width:1}},
      {{from:'05',to:'06',label:'XAI社会技术',color:{{color:'#dc2626'}},dashes:false,width:1.5}},
      {{from:'G1',to:'01',label:'SAE特征本体',color:{{color:'#d97706'}},dashes:true,width:2}},
      {{from:'G1',to:'06',label:'实在论辩论',color:{{color:'#d97706'}},dashes:false,width:2}},
      {{from:'G2',to:'06',label:'理解标准',color:{{color:'#0d9488'}},dashes:false,width:2}},
      {{from:'G2',to:'03',label:'机制解释',color:{{color:'#0d9488'}},dashes:true,width:1.5}},
      {{from:'G3',to:'03',label:'因果忠诚性',color:{{color:'#7c3aed'}},dashes:false,width:2}},
      {{from:'G3',to:'06',label:'干预主义因果',color:{{color:'#7c3aed'}},dashes:false,width:1.5}},
      {{from:'G4',to:'01',label:'SAE语义地位',color:{{color:'#dc2626'}},dashes:false,width:2}},
      {{from:'G4',to:'07',label:'奠基问题',color:{{color:'#dc2626'}},dashes:false,width:2}},
      {{from:'G4',to:'02',label:'导向向量语义',color:{{color:'#dc2626'}},dashes:true,width:1.5}},
      {{from:'G1',to:'G4',label:'本体论→奠基',color:{{color:'#d97706'}},dashes:true,width:1}},
      {{from:'G2',to:'G3',label:'理解→因果',color:{{color:'#0d9488'}},dashes:true,width:1}},
    ];

    const container = document.getElementById('cross-graph');
    crossGraphNetwork = new vis.Network(container, {{
      nodes: new vis.DataSet(nodes),
      edges: new vis.DataSet(edges)
    }}, {{
      physics: {{
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {{gravitationalConstant: -40, centralGravity: 0.008, springLength: 200}}
      }},
      edges: {{smooth: {{type:'continuous'}}, font: {{size:9, color:'#7a8aa2', face:'Sora'}}}},
      interaction: {{hover: true, tooltipDelay: 150}},
    }});

    document.getElementById('graph-zoom-in').addEventListener('click', () => {{
      if (crossGraphNetwork) crossGraphNetwork.moveTo({{ scale: crossGraphNetwork.getScale() * 1.4 }});
    }});
    document.getElementById('graph-zoom-out').addEventListener('click', () => {{
      if (crossGraphNetwork) crossGraphNetwork.moveTo({{ scale: crossGraphNetwork.getScale() / 1.4 }});
    }});
    document.getElementById('graph-reset').addEventListener('click', () => {{
      if (crossGraphNetwork) crossGraphNetwork.fit({{ animation: true }});
    }});
    document.getElementById('graph-fullscreen').addEventListener('click', toggleCrossFullscreen);
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape' && crossIsFullscreen) toggleCrossFullscreen();
    }});

    crossGraphNetwork.on('click', function(evt) {{
      if (evt.nodes.length > 0) {{
        const links = {{
          '01':'knowledge_base/01_sae_features/wiki.html','02':'knowledge_base/02_activation_engineering/wiki.html',
          '03':'knowledge_base/03_causal_intervention/wiki.html','04':'knowledge_base/04_alignment_safety/wiki.html',
          '05':'knowledge_base/05_ethics_governance/wiki.html','06':'knowledge_base/06_philosophy_of_science/wiki.html',
          '07':'knowledge_base/07_philosophy_of_mind/wiki.html',
          'G1':'knowledge_base/08_representational_ontology/wiki.html','G2':'knowledge_base/09_epistemology_understanding/wiki.html',
          'G3':'knowledge_base/10_causal_sufficiency/wiki.html','G4':'knowledge_base/11_vector_grounding/wiki.html'
        }};
        window.location.href = links[evt.nodes[0]];
      }}
    }});
  }});

  function toggleCrossFullscreen() {{
    const container = document.getElementById('cross-graph');
    const toolbar = document.getElementById('graph-toolbar');
    const btn = document.getElementById('graph-fullscreen');
    if (!crossIsFullscreen) {{
      container.classList.add('fullscreen');
      toolbar.classList.add('fullscreen');
      btn.textContent = '✕ 退出';
      crossIsFullscreen = true;
    }} else {{
      container.classList.remove('fullscreen');
      toolbar.classList.remove('fullscreen');
      btn.textContent = '⛶ 全屏';
      crossIsFullscreen = false;
      setTimeout(() => {{ if (crossGraphNetwork) crossGraphNetwork.fit({{ animation: false }}); }}, 100);
    }}
  }}
  </script>
</body>
</html>'''

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Generated {OUTPUT_PATH}")
