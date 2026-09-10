"""
UI Card and badge components for impactx, inspired by modern enterprise ML platforms.
"""

def render_platform_header_content(
    title: str = "impactx Code Classification & Architecture ML Platform",
    subtitle: str = "Production ML Dashboard",
    status_text: str = "Local Engine Active",
    theme: str = "dark",
) -> str:
    """Renders inner content of the platform header (title, subtitle, and live connection indicator)."""
    is_dark = (theme.lower() == "dark")
    title_color = "#FFFFFF" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#64748B"

    return f"""
    <div style="display: flex; flex-direction: column; justify-content: center; gap: 4px; padding: 2px 0;">
        <h1 style="font-size: 22px; font-weight: 800; color: {title_color}; margin: 0; letter-spacing: -0.4px; line-height: 1.2;">
            {title}
        </h1>
        <div style="font-size: 13px; color: {sub_color}; display: flex; align-items: center; gap: 10px; margin-top: 2px;">
            <span>{subtitle}</span>
            <span style="display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.12); color: #10B981; padding: 2px 10px; border-radius: 9999px; font-weight: 600; font-size: 11px; border: 1px solid rgba(16, 185, 129, 0.25);">
                <span style="width: 6px; height: 6px; border-radius: 50%; background-color: #10B981; box-shadow: 0 0 6px #10B981;"></span>
                {status_text}
            </span>
        </div>
    </div>
    """

def render_platform_header(
    title: str = "impactx Code Change Impact & Architecture ML Platform",
    subtitle: str = "Production ML Code Intelligence Dashboard",
    status_text: str = "Local Engine Active",
    theme: str = "dark",
) -> str:
    """Renders the standalone platform header with outer card container."""
    is_dark = (theme.lower() == "dark")
    bg = "#13161F" if is_dark else "#FFFFFF"
    border = "rgba(255, 255, 255, 0.08)" if is_dark else "#E2E8F0"
    content = render_platform_header_content(title, subtitle, status_text, theme)

    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; border-radius: 14px; background: {bg}; border: 1px solid {border}; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
        {content}
    </div>
    """

def render_hero(
    title: str = "Predict the ripple effect before you change the code.",
    subtitle: str = "ML-Powered Code Change Impact and Unused Code Prediction System.",
    badge: str = "impactx Engine — Local Analysis",
) -> str:
    """Returns platform header string."""
    return render_platform_header(
        title="impactx — Code Change Impact & Architecture ML Platform",
        subtitle="Production ML Code Intelligence Dashboard",
        status_text="Local Engine Active",
    )

def render_metric_card(title: str, value: str | int, subtext: str = "", icon: str = "") -> str:
    """Returns HTML for a modern ML platform metric card."""
    icon_html = f"<span style='margin-right: 6px;'>{icon}</span>" if icon else ""
    return f"""
    <div class="metric-card">
        <div class="metric-title">{icon_html}{title}</div>
        <div class="metric-value">{value}</div>
        {f'<div class="metric-subtext">{subtext}</div>' if subtext else ''}
    </div>
    """

def render_risk_badge(level: str) -> str:
    """Returns styled HTML badge for HIGH, MEDIUM, or LOW risk."""
    level_upper = str(level).upper()
    if level_upper == "HIGH":
        return '<span class="badge-high">HIGH RISK</span>'
    elif level_upper == "MEDIUM":
        return '<span class="badge-med">MEDIUM RISK</span>'
    else:
        return '<span class="badge-low">LOW RISK</span>'


# -------------------------------------------------------------
# PROJECT LOGO: TOPOLOGICAL DEPENDENCY GRAPH 'X'
# -------------------------------------------------------------

def render_logo_svg(size: int = 20, class_name: str = "") -> str:
    """
    Renders the official impactx architecture intelligence logo:
    A topological dependency graph lattice forming the letter 'X'.
    Features interconnected graph nodes (upstream, downstream, core component),
    dependency vector edges, and a central impact ripple hub.
    """
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" class="{class_name}" style="flex-shrink: 0; display: inline-block; vertical-align: middle;">
  <!-- Topological dependency edges forming the 'X' -->
  <line x1="7" y1="7" x2="25" y2="25" stroke="#818CF8" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="25" y1="7" x2="7" y2="25" stroke="#818CF8" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="7" y1="16" x2="25" y2="16" stroke="#4F46E5" stroke-width="1.5" stroke-dasharray="2 2" stroke-linecap="round"/>
  <!-- Corner Dependency Nodes (Code Entities) -->
  <circle cx="7" cy="7" r="3" fill="#312E81" stroke="#A5B4FC" stroke-width="1.8"/>
  <circle cx="25" cy="7" r="3" fill="#312E81" stroke="#A5B4FC" stroke-width="1.8"/>
  <circle cx="7" cy="25" r="3" fill="#312E81" stroke="#A5B4FC" stroke-width="1.8"/>
  <circle cx="25" cy="25" r="3" fill="#312E81" stroke="#A5B4FC" stroke-width="1.8"/>
  <!-- Central Hub Component / Change Trigger Node -->
  <circle cx="16" cy="16" r="4.5" fill="#4F46E5" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="16" cy="16" r="1.5" fill="#FFFFFF"/>
</svg>"""

def render_brand_icon(size: int = 30) -> str:
    """Renders the logo inside a clean, modern matte icon container box."""
    svg_size = int(size * 0.68)
    svg_html = render_logo_svg(size=svg_size)
    return (
        f'<div style="width: {size}px; height: {size}px; border-radius: 8px; '
        f'background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(129, 140, 248, 0.28); '
        f'display: flex; align-items: center; justify-content: center; flex-shrink: 0;">'
        f'{svg_html}'
        f'</div>'
    )

# -------------------------------------------------------------
# VECTOR ICONS FOR ENTERPRISE CARDS
# -------------------------------------------------------------

SVG_ICONS = {
    "code": (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>'
    ),
    "graph": (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="6" cy="6" r="3"></circle><circle cx="18" cy="18" r="3"></circle><circle cx="6" cy="18" r="3"></circle>'
        '<line x1="8.5" y1="7.5" x2="15.5" y2="16.5"></line><line x1="6" y1="9" x2="6" y2="15"></line></svg>'
    ),
    "cpu": (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect>'
        '<line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line>'
        '<line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line>'
        '<line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line>'
        '<line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>'
    ),
    "report": (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
        '<polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line>'
        '<line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>'
    ),
    "zap": (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
    ),
    "scan": (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>'
    ),
    "shield": (
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
    ),
}

def render_pipeline_card(stage: str, title: str, description: str, tags: list = None, icon: str = "") -> str:
    """Renders a modern, professional, glassmorphic pipeline stage card."""
    tags_html = ""
    if tags:
        pills = "".join(f'<span class="pro-tag-pill">{t}</span>' for t in tags)
        tags_html = f'<div class="pro-card-footer">{pills}</div>'

    icon_svg = SVG_ICONS.get(icon, "")
    icon_elem = f'<div class="pro-card-icon">{icon_svg}</div>' if icon_svg else ""

    return f"""
    <div class="pro-card">
        <div class="pro-card-header">
            <div class="stage-badge">{stage}</div>
            <div class="pro-card-title">{title}</div>
            <div style="margin-left: auto;">{icon_elem}</div>
        </div>
        <div class="pro-card-body">{description}</div>
        {tags_html}
    </div>
    """

def render_capability_card(title: str, description: str, tag: str = "", icon: str = "") -> str:
    """Renders a sleek capability card with vector icon anchor and tech badge."""
    icon_svg = SVG_ICONS.get(icon, "")
    icon_elem = f'<div class="pro-card-icon">{icon_svg}</div>' if icon_svg else ""
    tag_elem = f'<div class="pro-card-footer"><span class="pro-tag-pill">{tag}</span></div>' if tag else ""

    return f"""
    <div class="pro-card">
        <div class="pro-card-header">
            {icon_elem}
            <div class="pro-card-title">{title}</div>
        </div>
        <div class="pro-card-body">{description}</div>
        {tag_elem}
    </div>
    """

# Structured, non-hardcoded data models for platform documentation
PIPELINE_STAGES_DATA = [
    {
        "stage": "01",
        "title": "Code Ingestion & AST Parsing",
        "description": "Uploaded ZIP archives are safely unpacked in an isolated local sandbox. Multi-language AST parsers extract imports, exports, functions, and classes across Python, JS, TS, HTML, and CSS.",
        "tags": ["Zip-Slip Traversal Guard", "AST Tokenizer"],
        "icon": "code",
    },
    {
        "stage": "02",
        "title": "Topology Compilation & Metrics",
        "description": "A directed NetworkX graph is generated to map every dependency relationship. Computes PageRank centrality, in/out degrees, architectural hubs, and detects circular dependency cycles.",
        "tags": ["NetworkX DiGraph", "Tarjan Cycles", "PageRank"],
        "icon": "graph",
    },
    {
        "stage": "03",
        "title": "Machine Learning Inference",
        "description": "Engineered topological features feed into ML models: XGBoost predicts downstream blast radius probability, while Random Forest scores non-use confidence for dead code detection.",
        "tags": ["XGBoost Classifier", "Random Forest"],
        "icon": "cpu",
    },
    {
        "stage": "04",
        "title": "Interactive Dashboard & Audit Reports",
        "description": "Interactively simulate change scenarios, inspect architectural hubs, filter dead code, and generate compliance-ready audit reports exportable to PDF, DOCX, and CSV.",
        "tags": ["PDF Audit Reports", "Word DOCX", "CSV Export"],
        "icon": "report",
    },
]

CORE_CAPABILITIES_DATA = [
    {
        "title": "Change Impact Prediction",
        "description": "Evaluates graph distance hops, coupling degrees, and XGBoost machine learning probabilities to calculate downstream ripple cascade.",
        "tag": "XGBoost Classifier",
        "icon": "zap",
    },
    {
        "title": "Dead Code Detection",
        "description": "Identifies unreferenced files, classes, and functions using topological PageRank centrality, in-degree coupling, and Random Forest classification.",
        "tag": "Random Forest",
        "icon": "scan",
    },
    {
        "title": "Multi-Language AST Engine",
        "description": "Parses code structures across Python AST, JavaScript and TypeScript ES6 / CommonJS modules, HTML DOM, and CSS stylesheets.",
        "tag": "AST Tokenizer",
        "icon": "code",
    },
    {
        "title": "Executive Audit Reports",
        "description": "Generates formal compliance and architecture documentation in PDF, Word (.docx), and CSV formats for pull request reviews.",
        "tag": "PDF & DOCX Export",
        "icon": "report",
    },
    {
        "title": "100% Local Sandboxing",
        "description": "Archive extraction, graph compilation, and ML inference execute entirely offline inside your local sandbox with zero data telemetry.",
        "tag": "Zip-Slip Protection",
        "icon": "shield",
    },
]

UPLOAD_FEATURES_DATA = [
    {
        "title": "1. Sandboxed Extraction",
        "description": "Archives are strictly validated with Zip-Slip traversal protection and extracted into an isolated local sandbox.",
        "tag": "Zip-Slip Protection",
        "icon": "shield",
    },
    {
        "title": "2. Multi-Language AST",
        "description": "Parsers scan files to catalog imports, exports, functions, and classes across polyglot repositories without running code.",
        "tag": "AST Tokenizer",
        "icon": "code",
    },
    {
        "title": "3. ML Topology Inference",
        "description": "Compiles NetworkX graph models to compute PageRank centrality, predict XGBoost blast radius, and detect dead code.",
        "tag": "XGBoost & Random Forest",
        "icon": "graph",
    },
]
