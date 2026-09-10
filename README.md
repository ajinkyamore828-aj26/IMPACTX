# impactx — ML-Based Code Change Impact and Unused Code Prediction System

> **"Predict the ripple effect before you change the code."**

**impactx** is an enterprise-grade, ML-powered local code analysis system that runs 100% locally on your computer. It provides deterministic answers and calibrated ML probabilities to three critical software engineering questions:
1. **Change Impact Analysis**: *"If I modify this file/function, which other components are likely to be affected?"*
2. **Unused Code Detection**: *"Which functions, classes, and files appear to be dead or unreferenced?"*
3. **Architectural Understanding**: *"How is this software project connected internally, where are the central hubs, and are there circular dependency cycles?"*

---

## 🌟 Key Capabilities

- **100% Local Execution**: Never uploads code to the cloud. Zero external API dependencies. Runs on `http://localhost:8501`.
- **Real Trained ML Models**: Real XGBoost and Random Forest classifiers evaluated with ROC-AUC > 0.98 and F1 > 0.85. No synthetic random numbers.
- **Multi-Language Parsing**:
  - **Python**: Deep AST analysis (classes, methods, async functions, calls, decorators, imports, cyclomatic complexity).
  - **JavaScript / TypeScript**: ES6 modules, CommonJS `require()`, arrow functions, classes, and calls.
  - **Java**: Packages, classes, interfaces, methods, and invocations.
  - **HTML**: Scripts, stylesheets, and page links via BeautifulSoup4.
  - **CSS**: `@import` rules and asset linkages.
- **Graph-Theoretic Engine**: Directed NetworkX graph tracking PageRank, betweenness centrality, in/out degrees, and circular dependency chains.
- **Dual Professional Theme**:
  - **Dark Mode (Default)**: Deep obsidian canvas with glowing Aurora-Electric purple/violet curved backlight matching modern design specifications.
  - **Light Mode**: High-end enterprise slate-white minimalist aesthetic.
  - **Instant Switcher**: One-click theme switcher in the sidebar.
- **Multi-Format Export**: One-click generation of structured JSON, flattened CSV, and self-contained standalone HTML audit reports.

---

## 🚀 Quick Start

### 1. Installation & Setup
```bash
# Ensure Python 3.11+ is installed
cd impactx

# (Optional) Retrain ML models
python training/train_models.py

# Launch the interactive Streamlit Dashboard
streamlit run app.py
```

### 2. Accessing the Dashboard
Open your browser to:
```
http://localhost:8501
```

### 3. Analyzing a Project
- **Upload ZIP**: Drag and drop any software project archive into the sidebar uploader.
- **Load Demo**: Click **"Load & Analyze Demo"** in the sidebar to inspect prepackaged Python, JavaScript, or Fullstack demo projects.

---

## 🏗️ Architecture & Data Flow

```
Upload ZIP / Sample Project
  │
  ▼
[Safe ZIP Extractor] ── Path Traversal & Zip-Bomb Protection
  │
  ▼
[Project Scanner & File Detector] ── Language Detection & Metrics
  │
  ▼
[Multi-Language AST Parsers] ── Python / JS / Java / HTML / CSS
  │
  ▼
[Dependency Analyzer] ── Resolves Cross-File Imports, Calls, Inheritance
  │
  ▼
[NetworkX Dependency Graph] ── Computes PageRank, Degrees, Cycles
  │
  ▼
[Feature Extractor] ── Generates 20+ Structural & Topological Features
  │
  ▼
[ML Inference Engine] ── XGBoost & Random Forest Models
  │
  ├── Impact Predictor (Downstream Ripple Probability & Risk Level)
  └── Unused Code Predictor (Non-Use Confidence & Risk Level)
  │
  ▼
[Interactive Dashboard & Exporters] ── Plotly Graphs & JSON/CSV/HTML Reports
```

---

## 🧪 Automated Testing

Run the comprehensive pytest suite:
```bash
python -m pytest tests/ -v
```

All 18 tests cover safe ZIP handling, AST parsers, graph traversal, cycle detection, feature scaling, model inference, and end-to-end analysis.

---

## 🔒 Security Principles

- **NO Code Execution**: Projects are statically parsed; user code is never evaluated with `exec()` or `eval()`.
- **Zip Bomb Defense**: Validates uncompressed size limits (up to 1.5 GB), compression ratios (< 100x), and file counts (< 10,000).
- **Path Traversal Protection**: Rejects archives with `../` or root directory escape attempts.
- **Binary Screening**: Filters out compiled binaries, DLLs, and executables.
