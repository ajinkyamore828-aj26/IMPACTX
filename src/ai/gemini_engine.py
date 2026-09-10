"""
AI Intelligence Engine for impactx powered by high-speed Groq inference.
Provides generative architectural intelligence, semantic change impact reasoning,
and safe dead code pruning advisory with resilient multi-model failover and strict grounding.
"""

import os
import re
import logging
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv()

logger = logging.getLogger("impactx.ai")

# Prioritized fast and precise Groq candidate models
GROQ_MODELS = [
    "qwen/qwen3.8-27b",
    "groq/compound",
    "groq/compound-mini",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"


class GeminiEngine:
    """Wrapper for high-speed Groq AI reasoning engine with automatic multi-model failover."""

    @staticmethod
    def get_api_key() -> Optional[str]:
        return os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")

    @classmethod
    def is_available(cls) -> bool:
        key = cls.get_api_key()
        return bool(key and len(key.strip()) > 10)

    @classmethod
    def _generate_with_fallback(
        cls,
        prompt: str,
        system_msg: str = "You are a precise, factual enterprise software architect and code intelligence specialist. You strictly analyze only the files and metrics provided, never hallucinating unmentioned code.",
        error_prefix: str = "AI Copilot",
    ) -> Optional[str]:
        """
        Executes chat completion across prioritized Groq models.
        Automatically falls back to the next model if one encounters transient issues.
        """
        key = cls.get_api_key()
        if not key:
            return None

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "impactx/2.1",
        }

        last_error = None
        for model_name in GROQ_MODELS:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.1,
                "max_tokens": 1500,
            }
            try:
                resp = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=12)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices and "message" in choices[0]:
                        msg = choices[0]["message"]
                        content = msg.get("content", "") or ""
                        if not content.strip():
                            content = msg.get("reasoning", "") or ""
                        
                        content = content.strip()
                        if content:
                            # Clean up think tags, normalize header sizes, and remove strange punctuation spacing
                            clean_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
                            clean_content = re.sub(r'^#{1,3}\s+', '#### ', clean_content, flags=re.MULTILINE)
                            clean_content = re.sub(r'\s+([,.:;?!])', r'\1', clean_content)
                            clean_content = re.sub(r'\s+\)', ')', clean_content)
                            clean_content = re.sub(r'\(\s+', '(', clean_content)
                            if clean_content:
                                return clean_content
                            return content
                elif resp.status_code in (401, 403):
                    return "⚠️ *Groq API authentication failed: please check your GROQ_API_KEY.*"
                else:
                    logger.warning(f"Groq model {model_name} returned status {resp.status_code}: {resp.text[:120]}")
            except Exception as e:
                last_error = e
                logger.warning(f"Groq model {model_name} failed ({e}), falling back...")
                continue

        # Graceful degradation if all candidate models are temporarily unavailable
        logger.error(f"All AI candidate models failed. Last error: {last_error}")
        return (
            f"> ⚠️ **{error_prefix} Temporarily at Capacity**\n\n"
            f"> Upstream AI services are currently experiencing high load. "
            f"All local topological graph calculations, dependencies, and machine learning scores remain 100% operational."
        )

    @classmethod
    def generate_architecture_summary(
        cls,
        scan_info: Dict[str, Any],
        metrics: Dict[str, Any],
        top_hubs: List[Dict[str, Any]],
        cycles: List[List[str]],
    ) -> Optional[str]:
        """Generates high-level executive architectural insights for the scanned codebase."""
        if not cls.is_available():
            return None

        project_name = scan_info.get("project_name", "Uploaded Codebase")
        total_files = scan_info.get("total_files", 0)
        total_loc = scan_info.get("total_code_lines", 0)
        languages = scan_info.get("language_distribution", {})
        lang_str = ", ".join([f"{k} ({v} files)" for k, v in languages.items()]) or "Unknown"

        # Provide actual file inventory for precise grounding
        files_data = scan_info.get("files", [])
        file_list = []
        for f in files_data[:25]:
            file_list.append(f"- `{f.get('path')}` ({f.get('language')}, {f.get('code_lines', 0)} LOC)")
        files_text = "\n".join(file_list) if file_list else "No detailed file list."

        hubs_summary = []
        for h in top_hubs[:5]:
            hubs_summary.append(
                f"- `{h.get('id')}` ({h.get('entity_type')}): PageRank={h.get('pagerank', 0):.4f}, Dependents={h.get('in_degree', 0)}"
            )
        hubs_text = "\n".join(hubs_summary) if hubs_summary else "No prominent architectural hubs detected."

        has_cycles = len(cycles) > 0
        cycle_text = f"Circular Dependencies: {len(cycles)} detected!" if has_cycles else "Circular Dependencies: 0 (Clean DAG)."

        prompt = f"""You are an enterprise software architect analyzing a codebase topology scan.
Strict Ground Truth Directive: Only refer to the actual files and metrics listed below. NEVER invent or assume function names, endpoints, or unmentioned code entities.

Codebase Scan Data:
Project Name: `{project_name}`
Total Files: {total_files} | Total Effective Code LOC: {total_loc}
Languages Detected: {lang_str}
Topology Status: {cycle_text}

Repository File Inventory (sample):
{files_text}

Top Architectural Hubs (Highest Blast Radius Components):
{hubs_text}

Task:
Provide a strictly factual architectural assessment in 3 clear sections:
#### 1. Architectural Pattern & Topology Overview
High-level pattern (e.g. monolithic frontend, layered backend, multi-view web app), dependency direction, and coupling health based solely on the scanned files.

#### 2. Key Architectural Hotspots & Vulnerability Risks
Explain why the identified hub files (`{', '.join([h.get('id', '') for h in top_hubs[:3]])}`) carry the highest change risk, and how alterations to them propagate across dependent files.

#### 3. Developer Action Items
3 concrete, realistic refactoring and isolation recommendations specific to this file structure.
"""
        return cls._generate_with_fallback(
            prompt,
            system_msg="You are a precise, factual enterprise software architect. You strictly analyze only the actual files and graph metrics provided, with zero hallucinations.",
            error_prefix="Architectural Assessment",
        )

    @classmethod
    def explain_impact(
        cls,
        target_component: str,
        impact_res: Dict[str, Any],
    ) -> Optional[str]:
        """Generates natural language reasoning explaining why downstream entities are affected."""
        if not cls.is_available():
            return None

        total_affected = impact_res.get("total_affected", 0)
        direct_count = impact_res.get("direct_count", 0)
        indirect_count = impact_res.get("indirect_count", 0)
        high_risk_count = impact_res.get("high_risk_count", 0)
        affected = impact_res.get("affected_components", [])

        affected_summary = []
        for a in affected[:8]:
            driver = (a.get("explanations") or ["Static dependency"])[0]
            affected_summary.append(
                f"- `{a.get('component')}` ({a.get('type')}): Risk={a.get('risk_level')}, Probability={a.get('probability', 0):.1%}, Distance={a.get('distance')} hops, Driver={driver}"
            )
        aff_text = "\n".join(affected_summary) if affected_summary else "No downstream components affected."

        prompt = f"""You are a code change impact reviewer analyzing the blast radius of modifying: `{target_component}`.
Strict Ground Truth Directive: Only refer to the actual components listed in the results below. Do not assume or invent unmentioned functions.

Impact Analysis Metrics:
- Target File: `{target_component}`
- Total Blast Radius: {total_affected} affected components
- Direct Dependents (Level 1): {direct_count}
- Transitive Ripple Effect (Level 2+): {indirect_count}
- High Risk Entities: {high_risk_count}

Top Downstream Consumers Affected:
{aff_text}

Task:
Provide a strictly factual 2-part impact review:
#### 1. Semantic Blast Radius Breakdown
Explain in plain, technical English the ripple effect of altering `{target_component}` on the specific downstream consumers listed above.

#### 2. Regression Testing & Verification Checklist
List 3 concrete test scenarios to verify before deploying modifications to `{target_component}`.
"""
        return cls._generate_with_fallback(
            prompt,
            system_msg="You are a precise code change impact reviewer. Only reason about the real components provided.",
            error_prefix="Semantic Blast Radius Reasoning",
        )

    @classmethod
    def explain_unused_code(
        cls,
        unused_candidates: List[Dict[str, Any]],
        filter_context: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> Optional[str]:
        """Provides AI-driven dead code pruning guidance by analyzing the full table of candidates."""
        if filter_context is None and "filter_context" in kwargs:
            filter_context = kwargs["filter_context"]

        if not cls.is_available():
            return None

        if not unused_candidates:
            return "No dead code candidates in the current table to analyze."

        total_count = len(unused_candidates)
        table_rows = []
        for i, u in enumerate(unused_candidates[:30], 1):
            name = u.get("name", "Unknown")
            etype = str(u.get("type", "file")).upper()
            fpath = u.get("file_path", "")
            refs = u.get("reference_count", 0)
            prob = u.get("unused_probability", 0.0)
            risk = u.get("risk_level", "LOW")
            reasons = u.get("reasons") or ["Zero static incoming references"]
            evidence = reasons[0] if reasons else "No incoming references"
            table_rows.append(
                f"| {i} | `{name}` | {etype} | `{fpath}` | {refs} | {prob:.1%} | {risk} | {evidence} |"
            )
        table_text = "\n".join(table_rows)

        filter_info = ""
        if filter_context:
            r_levels = ", ".join(filter_context.get("risk_levels", [])) or "All"
            e_types = ", ".join(filter_context.get("entity_types", [])) or "All"
            filter_info = f"Current Table Filters: Risk Tier=[{r_levels}] | Entity Type=[{e_types}]\n"

        prompt = f"""You are a software refactoring safety auditor reviewing candidate unreferenced code.
Strict Ground Truth Directive: Audit ONLY the actual components present in the table below. Do not assume or invent unmentioned components.

{filter_info}Total Components in Audit Table: {total_count} (displaying {min(total_count, 30)} candidates):

| # | Component | Type | File Location | References | Non-Use Prob | Risk Tier | Evidence |
|---|---|---|---|---|---|---|---|
{table_text}

Task:
Perform a structured refactoring safety audit:

#### 1. Framework Entry Points & Critical Roots (DO NOT DELETE)
Identify components in the table that serve as application entry points or root assets (e.g. `index.html`, `server.js`, `main.jsx`, root css). Explain why these have 0 static incoming imports and MUST be preserved.

#### 2. Active Consumers & Shared Dependencies (NOT DEAD CODE)
Identify components with incoming references (reference count >= 1) and confirm they are actively consumed in the topology.

#### 3. True Dead Code & Safe Pruning Candidates
Identify unreferenced non-entry files that represent safe cleanup targets.

#### 4. Safe Verification Protocol
Provide a 3-step verification checklist before deleting any candidate.
"""
        return cls._generate_with_fallback(
            prompt,
            system_msg="You are a principal software refactoring safety auditor. You strictly audit only the real components provided in the table.",
            error_prefix="Dead Code Advisory",
        )
