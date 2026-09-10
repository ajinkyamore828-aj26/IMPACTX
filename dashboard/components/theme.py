"""
Glassmorphism Dark Theme Engine for impactx.
Provides futuristic frosted glass UI styling (translucent surfaces, backdrop blur,
cosmic ambient mesh gradients, micro-borders, glowing metrics, and floating glass pills).
"""

from typing import Dict, Any

GLASS_DARK_CSS = """
<style>
/* -------------------------------------------------------------
   IMPACTX GLASSMORPHISM DESIGN SYSTEM (DARK EDITION)
   ------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background: #090C15 !important;
    color: #F8FAFC !important;
}

/* Header bar styling - Hidden to allow sleek top navbar */
header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    visibility: hidden !important;
}

.block-container,
[data-testid="stMainBlockContainer"],
.main .block-container {
    padding-top: 0.75rem !important;
    padding-bottom: 2.5rem !important;
    padding-left: 1.75rem !important;
    padding-right: 1.75rem !important;
    max-width: 1400px !important;
}

/* Sidebar styling - Frosted Glass Panel */
section[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background: rgba(10, 13, 24, 0.82) !important;
    backdrop-filter: blur(24px) saturate(190%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(190%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
}

/* Typography & Headings */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[data-testid="stText"] {
    color: #CBD5E1 !important;
}

[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

[data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] span,
small {
    color: #64748B !important;
}

label[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* Sidebar Brand Card */
.sidebar-brand-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.09);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    margin-bottom: 20px;
}

.sidebar-brand-logo {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.28);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.sidebar-brand-title {
    font-size: 16px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.3px;
    line-height: 1.2;
}

.sidebar-brand-sub {
    font-size: 11px;
    color: #818CF8;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-top: 2px;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #10B981;
    margin-right: 6px;
    box-shadow: 0 0 10px #10B981, 0 0 4px #10B981;
}

/* Frosted Glass Containers (border=True) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(14, 18, 34, 0.6) !important;
    backdrop-filter: blur(18px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.38), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(255, 255, 255, 0.16) !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
}

/* Glassmorphic Metric Cards */
.metric-card {
    background: #0E131F;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    transition: border-color 0.15s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 98px;
}

.metric-card:hover {
    border-color: rgba(255, 255, 255, 0.16);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
}

.metric-title {
    font-size: 11px;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.1;
    letter-spacing: -0.02em;
}

.metric-subtext {
    font-size: 11px;
    color: #64748B;
    margin-top: 5px;
}

/* Native Streamlit Metrics */
div[data-testid="stMetric"] {
    background: rgba(16, 21, 40, 0.58) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}

div[data-testid="stMetricLabel"] * {
    color: #A5B4FC !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

div[data-testid="stMetricValue"] * {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 24px !important;
}

/* Enterprise Expanders & Report Container */
div[data-testid="stExpander"],
details[data-testid="stExpander"] {
    background: #0E131F !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    margin-bottom: 14px !important;
    overflow: hidden !important;
}

summary[data-testid="stExpanderSummary"],
details[data-testid="stExpander"] > summary {
    background-color: transparent !important;
    color: #F8FAFC !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
}

summary[data-testid="stExpanderSummary"]:hover {
    background-color: rgba(255, 255, 255, 0.03) !important;
}

summary[data-testid="stExpanderSummary"] p,
summary[data-testid="stExpanderSummary"] span {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
}

div[data-testid="stExpanderDetails"] {
    background: rgba(10, 14, 26, 0.5) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
    color: #CBD5E1 !important;
    padding: 20px 24px !important;
    font-size: 13px !important;
    line-height: 1.65 !important;
}

div[data-testid="stExpanderDetails"] h1,
div[data-testid="stExpanderDetails"] h2,
div[data-testid="stExpanderDetails"] h3,
div[data-testid="stExpanderDetails"] h4 {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
    margin-top: 16px !important;
    margin-bottom: 8px !important;
    letter-spacing: -0.01em !important;
}

div[data-testid="stExpanderDetails"] h1 { font-size: 16px !important; }
div[data-testid="stExpanderDetails"] h2 { font-size: 15px !important; }
div[data-testid="stExpanderDetails"] h3 { font-size: 14.5px !important; }
div[data-testid="stExpanderDetails"] h4 { font-size: 14px !important; color: #818CF8 !important; }

div[data-testid="stExpanderDetails"] p {
    font-size: 13px !important;
    color: #94A3B8 !important;
    line-height: 1.65 !important;
    margin-bottom: 10px !important;
}

div[data-testid="stExpanderDetails"] ul,
div[data-testid="stExpanderDetails"] ol {
    margin-left: 20px !important;
    padding-left: 0 !important;
    margin-bottom: 12px !important;
}

div[data-testid="stExpanderDetails"] li {
    font-size: 13px !important;
    color: #94A3B8 !important;
    line-height: 1.6 !important;
    margin-bottom: 6px !important;
}

div[data-testid="stExpanderDetails"] strong,
div[data-testid="stExpanderDetails"] b {
    color: #F1F5F9 !important;
    font-weight: 600 !important;
}

/* Selectboxes & Dropdowns */
div[data-baseweb="select"] > div {
    background-color: rgba(18, 24, 46, 0.65) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="select"] > div:focus,
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"] > div:focus-visible,
div[data-baseweb="select"] > div[aria-expanded="true"] {
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="select"] * {
    color: #FFFFFF !important;
}

/* Multiselect tags — simple, compact, small neutral styling */
div[data-testid="stMultiSelect"] [data-baseweb="tag"],
div[data-baseweb="select"] [data-baseweb="tag"],
.stMultiSelect [data-baseweb="tag"],
[data-baseweb="tag"],
span[data-baseweb="tag"],
div[data-baseweb="tag"] {
    background: rgba(255, 255, 255, 0.05) !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 4px !important;
    color: #CBD5E1 !important;
    height: auto !important;
    min-height: 20px !important;
    max-height: 22px !important;
    padding: 1px 6px !important;
    margin: 1px 2px !important;
    box-shadow: none !important;
}

div[data-testid="stMultiSelect"] [data-baseweb="tag"] span,
div[data-baseweb="select"] [data-baseweb="tag"] span,
[data-baseweb="tag"] span,
[data-baseweb="tag"] div,
[data-baseweb="tag"] {
    color: #CBD5E1 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    line-height: 1.2 !important;
    letter-spacing: 0.2px !important;
}

div[data-testid="stMultiSelect"] [data-baseweb="tag"] svg,
div[data-baseweb="select"] [data-baseweb="tag"] svg,
[data-baseweb="tag"] svg,
[data-baseweb="tag"] [role="button"] svg {
    fill: #64748B !important;
    color: #64748B !important;
    width: 9px !important;
    height: 9px !important;
    cursor: pointer !important;
}

div[data-testid="stMultiSelect"] [data-baseweb="tag"]:hover svg,
[data-baseweb="tag"] [role="button"]:hover svg {
    fill: #CBD5E1 !important;
    color: #CBD5E1 !important;
}

div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"] {
    background-color: rgba(12, 16, 30, 0.96) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6) !important;
}

li[role="option"] {
    background-color: transparent !important;
    color: #E2E8F0 !important;
    font-size: 13px !important;
    padding: 9px 14px !important;
    border-radius: 6px !important;
}

li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background: rgba(255, 255, 255, 0.07) !important;
    color: #FFFFFF !important;
}

/* Text Inputs — no red border */
div[data-baseweb="input"] > div {
    background-color: rgba(18, 24, 46, 0.65) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="input"] > div:focus,
div[data-baseweb="input"] > div:focus-within {
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="input"] input {
    background-color: transparent !important;
    color: #FFFFFF !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #64748B !important;
}

/* Primary Glass Button */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.88) 0%, rgba(99, 102, 241, 0.88) 100%) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: -0.1px !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 9px !important;
    padding: 8px 16px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.15s ease !important;
    white-space: nowrap !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, rgba(67, 56, 202, 0.95) 0%, rgba(79, 70, 229, 0.95) 100%) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* Secondary Frosted Glass Button */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"],
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    color: #CBD5E1 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    letter-spacing: -0.1px !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 9px !important;
    padding: 8px 16px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.15s ease !important;
    white-space: nowrap !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="baseButton-secondary"]:hover,
.stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.18) !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:disabled,
.stButton > button[disabled] {
    background: rgba(255, 255, 255, 0.02) !important;
    color: #64748B !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
    transform: none !important;
    opacity: 0.5 !important;
}

/* Download Buttons */
div[data-testid="stDownloadButton"] > button {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #F8FAFC !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.15s ease !important;
}

div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255, 255, 255, 0.09) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

/* Dashboard Tabs — zero red underline, clean matte active state */
[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"],
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"],
[data-testid="stTabsHeader"] [data-baseweb="tab-highlight"],
div[role="tablist"] [data-baseweb="tab-highlight"],
div[data-baseweb="tab-highlight"],
div[data-baseweb="tab-highlight"] *,
div[data-baseweb="tab-border"] * {
    display: none !important;
    height: 0 !important;
    width: 0 !important;
    max-height: 0 !important;
    opacity: 0 !important;
    visibility: hidden !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-bottom: none !important;
    box-shadow: none !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"],
.stTabs [data-baseweb="tab-list"] {
    background: #0A0E1A !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 9px !important;
    padding: 4px !important;
    gap: 4px !important;
    box-shadow: none !important;
    margin-bottom: 20px !important;
    width: fit-content !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"],
.stTabs [data-baseweb="tab"],
button[role="tab"] {
    border-radius: 6px !important;
    color: #94A3B8 !important;
    padding: 7px 18px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border: 1px solid transparent !important;
    border-bottom: 1px solid transparent !important;
    background: transparent !important;
    outline: none !important;
    box-shadow: none !important;
    transition: color 0.15s ease, background 0.15s ease !important;
    position: relative !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"]::after,
button[role="tab"]::after {
    display: none !important;
    content: none !important;
}

div[data-testid="stTabs"] button[data-baseweb="tab"]:hover,
.stTabs [data-baseweb="tab"]:hover,
button[role="tab"]:hover {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: transparent !important;
    border-bottom-color: transparent !important;
}

div[data-testid="stTabs"] button[aria-selected="true"],
.stTabs [aria-selected="true"],
button[role="tab"][aria-selected="true"] {
    background: rgba(255, 255, 255, 0.09) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Glassmorphic Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    background: rgba(14, 18, 34, 0.65) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
}

/* Code Blocks & Inline Code */
pre, div[data-testid="stCodeBlock"] {
    background: rgba(10, 13, 24, 0.8) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
}

code, :not(pre) > code {
    background: rgba(255, 255, 255, 0.06) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 1px 5px !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
    font-size: 0.85em !important;
    font-weight: 500 !important;
    vertical-align: baseline !important;
}

h1 code, h2 code, h3 code, h4 code, h5 code, h6 code {
    font-size: 0.82em !important;
    font-weight: 600 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    vertical-align: 1px !important;
}

/* Dividers */
hr, div[data-testid="stDivider"] {
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* JSON Viewer */
div[data-testid="stJson"] {
    background: rgba(12, 16, 30, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
}

/* Badges */
.badge-high {
    background: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border: 1px solid rgba(239, 68, 68, 0.3);
    padding: 3px 10px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
}

.badge-med {
    background: rgba(245, 158, 11, 0.15);
    color: #FDE68A;
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 3px 10px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
}

.badge-low {
    background: rgba(16, 185, 129, 0.15);
    color: #6EE7B7;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 3px 10px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
}

/* Force Streamlit columns to stretch children to equal height */
div[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    display: flex !important;
    flex-direction: column !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;
    height: 100% !important;
}

/* Professional Feature & Pipeline Cards (Clean Enterprise - Zero Vibe Glow) */
.pro-card {
    background: #0E131F !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 20px 22px 18px 22px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35) !important;
    transition: border-color 0.15s ease, background 0.15s ease !important;
    display: flex !important;
    flex-direction: column !important;
    height: 190px !important;
    margin-bottom: 14px !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

.pro-card:hover {
    background: #111726 !important;
    border-color: rgba(255, 255, 255, 0.16) !important;
}

.pro-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}

.stage-badge {
    width: 26px;
    height: 26px;
    min-width: 26px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #CBD5E1;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

.pro-card-icon {
    width: 30px;
    height: 30px;
    min-width: 30px;
    border-radius: 7px;
    background: rgba(129, 140, 248, 0.08);
    border: 1px solid rgba(129, 140, 248, 0.15);
    color: #818CF8;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.pro-card-title {
    font-size: 14px;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: -0.01em;
    line-height: 1.25;
    margin: 0;
}

.pro-card-body {
    font-size: 12.5px;
    color: #94A3B8;
    line-height: 1.6;
    margin: 0;
    flex-grow: 1;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}

.pro-card-footer {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.pro-tag-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 500;
    color: #94A3B8;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 3px 8px;
    border-radius: 5px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
}

/* Streamlit File Uploader Centered Dropzone Styling (Solid Matte - Zero Glow) */
div[data-testid="stFileUploader"] {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 auto !important;
}

div[data-testid="stFileUploader"] > label {
    display: none !important;
}

div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"],
div[data-testid="stFileUploader"] section {
    background: #0E131F !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 28px 20px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: 10px !important;
    min-height: 120px !important;
    transition: border-color 0.15s ease, background 0.15s ease !important;
    cursor: pointer !important;
    box-shadow: none !important;
}

div[data-testid="stFileUploader"] section:hover {
    border-color: rgba(255, 255, 255, 0.18) !important;
    background: #111726 !important;
    box-shadow: none !important;
}

div[data-testid="stFileUploader"] section [data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: 4px !important;
    width: 100% !important;
}

div[data-testid="stFileUploader"] section [data-testid="stFileUploaderDropzoneInstructions"] div {
    color: #F8FAFC !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="stFileUploader"] section [data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #64748B !important;
    font-size: 11px !important;
}

div[data-testid="stFileUploader"] section button {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #F8FAFC !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 7px 18px !important;
    margin: 6px auto 0 auto !important;
    order: 2 !important;
    box-shadow: none !important;
    transition: all 0.15s ease !important;
}

div[data-testid="stFileUploader"] section button:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.22) !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}

/* Hide uploaded file name chip (the green "● filename" badge shown after upload) */
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFileData"],
div[data-testid="stFileUploader"] ul,
div[data-testid="stFileUploader"] li {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Radio Group Centering for Ingestion Switcher */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 16px !important;
    flex-wrap: wrap !important;
}

div[data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 8px 18px !important;
    border-radius: 8px !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}

div[data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: rgba(255, 255, 255, 0.16) !important;
}
</style>
"""

def get_theme_css(theme: str = "dark") -> str:
    return GLASS_DARK_CSS

def get_plotly_layout(theme: str = "dark") -> Dict[str, Any]:
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Plus Jakarta Sans, Inter, sans-serif",
            "color": "#F8FAFC",
            "size": 12,
        },
        "margin": dict(l=30, r=30, t=40, b=30),
    }

def get_axis_layout(theme: str = "dark") -> Dict[str, Any]:
    return {
        "gridcolor": "rgba(255, 255, 255, 0.07)",
        "linecolor": "rgba(255, 255, 255, 0.12)",
        "tickcolor": "rgba(255, 255, 255, 0.12)",
        "tickfont": {"color": "#94A3B8", "family": "Plus Jakarta Sans, sans-serif", "size": 11},
        "title_font": {"color": "#C7D2FE", "family": "Plus Jakarta Sans, sans-serif", "size": 12},
    }
