"""
Dependency analyzer: parses project files, resolves imports and calls, and builds DependencyGraph.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.parsers.parser_factory import ParserFactory
from src.parsers.base_parser import ParsedModule
from src.graph.dependency_graph import DependencyGraph
from config.constants import EdgeType, EntityType
from src.utils.file_utils import read_file_safe, normalize_rel_path
from src.utils.logger import get_logger

logger = get_logger("dependency_analyzer")

# Cap how many files we parse to keep analysis fast
_MAX_PARSE_FILES = 500


def _parse_one(f: Dict[str, Any]) -> tuple[str, "ParsedModule"] | None:
    """Parse a single file and return (rel_path, parsed) or None on failure."""
    rel_path = f["path"]
    abs_path = Path(f["abs_path"])
    parser = ParserFactory.get_parser(abs_path)
    if not parser:
        return None
    try:
        content = read_file_safe(abs_path)
        parsed = parser.parse(rel_path, content)
        return rel_path, parsed
    except Exception:
        return None


class DependencyAnalyzer:
    """Orchestrates parsing and dependency resolution across a project codebase."""

    def __init__(self, root_dir: str | Path):
        self.root_dir = Path(root_dir)
        self.parsed_modules: Dict[str, ParsedModule] = {}
        self.dep_graph = DependencyGraph()

    def analyze(self, files_list: List[Dict[str, Any]]) -> DependencyGraph:
        """
        Parses all supported files in parallel, resolves inter-file relationships,
        and constructs the full DependencyGraph.
        """
        supported = [f for f in files_list if f.get("is_supported", False)]

        # Cap total files to avoid extremely long runs
        if len(supported) > _MAX_PARSE_FILES:
            logger.warning(f"Capping parse to {_MAX_PARSE_FILES} files (project has {len(supported)}).")
            supported = supported[:_MAX_PARSE_FILES]

        # ── Step 1: Parse all supported files in parallel ──────────────────
        max_workers = min(8, len(supported) or 1)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(_parse_one, f) for f in supported]
            for future in as_completed(futures):
                result = future.result()
                if result is None:
                    continue
                rel_path, parsed = result
                self.parsed_modules[rel_path] = parsed

        # ── Step 1b: Build graph nodes (single-threaded, fast) ──────────────
        for rel_path, parsed in self.parsed_modules.items():
            self.dep_graph.add_node(
                rel_path,
                entity_type=EntityType.FILE,
                name=rel_path,
                file_path=rel_path,
                language=parsed.language,
                lines_of_code=parsed.lines_of_code,
                code_lines=parsed.code_lines,
                function_count=len(parsed.functions),
                class_count=len(parsed.classes),
                import_count=len(parsed.imports),
            )

            for fn in parsed.functions:
                fn_id = f"{rel_path}/{fn.name}"
                self.dep_graph.add_node(
                    fn_id,
                    entity_type=EntityType.FUNCTION,
                    name=fn.name,
                    file_path=rel_path,
                    language=parsed.language,
                    line_start=fn.line_start,
                    line_end=fn.line_end,
                    lines_of_code=fn.length,
                    complexity_score=fn.complexity_score,
                    is_async=fn.is_async,
                    is_method=fn.is_method,
                    class_name=fn.class_name,
                )
                self.dep_graph.add_edge(rel_path, fn_id, edge_type=EdgeType.INCLUDES, weight=0.5)

            for cls_entity in parsed.classes:
                cls_id = f"{rel_path}/{cls_entity.name}"
                self.dep_graph.add_node(
                    cls_id,
                    entity_type=EntityType.CLASS,
                    name=cls_entity.name,
                    file_path=rel_path,
                    language=parsed.language,
                    line_start=cls_entity.line_start,
                    line_end=cls_entity.line_end,
                    lines_of_code=cls_entity.length,
                )
                self.dep_graph.add_edge(rel_path, cls_id, edge_type=EdgeType.INCLUDES, weight=0.5)

        # ── Step 2: Build symbol lookup tables ─────────────────────────────
        known_files = set(self.parsed_modules.keys())
        function_lookup: Dict[str, List[str]] = {}
        class_lookup: Dict[str, List[str]] = {}

        for mod_path, mod in self.parsed_modules.items():
            for fn in mod.functions:
                function_lookup.setdefault(fn.name, []).append(f"{mod_path}/{fn.name}")
            for cls_entity in mod.classes:
                class_lookup.setdefault(cls_entity.name, []).append(f"{mod_path}/{cls_entity.name}")

        # ── Step 3: Resolve imports and calls ──────────────────────────────
        for mod_path, mod in self.parsed_modules.items():
            current_dir = Path(mod_path).parent

            for imp in mod.imports:
                target_file = self._resolve_import_target(imp.source, current_dir, known_files)
                if target_file:
                    self.dep_graph.add_edge(mod_path, target_file, edge_type=EdgeType.IMPORTS, weight=1.0)
                    for name in imp.names:
                        fn_target = f"{target_file}/{name}"
                        if self.dep_graph.graph.has_node(fn_target):
                            self.dep_graph.add_edge(mod_path, fn_target, edge_type=EdgeType.REFERENCES, weight=1.0)

            for fn in mod.functions:
                fn_id = f"{mod_path}/{fn.name}"
                for called_name in fn.calls:
                    local_fn_id = f"{mod_path}/{called_name}"
                    if self.dep_graph.graph.has_node(local_fn_id) and local_fn_id != fn_id:
                        self.dep_graph.add_edge(fn_id, local_fn_id, edge_type=EdgeType.CALLS, weight=1.0)
                    elif called_name in function_lookup:
                        for candidate_id in function_lookup[called_name]:
                            if candidate_id != fn_id:
                                self.dep_graph.add_edge(fn_id, candidate_id, edge_type=EdgeType.CALLS, weight=0.8)

            for cls_entity in mod.classes:
                cls_id = f"{mod_path}/{cls_entity.name}"
                for base in cls_entity.base_classes:
                    local_base = f"{mod_path}/{base}"
                    if self.dep_graph.graph.has_node(local_base):
                        self.dep_graph.add_edge(cls_id, local_base, edge_type=EdgeType.INHERITS, weight=1.0)
                    elif base in class_lookup:
                        for candidate_id in class_lookup[base]:
                            self.dep_graph.add_edge(cls_id, candidate_id, edge_type=EdgeType.INHERITS, weight=1.0)

        logger.info(f"Built dependency graph: {self.dep_graph.number_of_nodes} nodes, {self.dep_graph.number_of_edges} edges.")
        return self.dep_graph

    def _resolve_import_target(self, source: str, current_dir: Path, known_files: Set[str]) -> Optional[str]:
        """Resolves an import source string to a relative project file path."""
        cleaned = source.replace("\\", "/").strip()
        if not cleaned:
            return None

        # 1. Direct match
        if cleaned in known_files:
            return cleaned

        current_abs_dir = self.root_dir / current_dir
        check_bases = [current_abs_dir, self.root_dir]

        for base in check_bases:
            try:
                target = (base / cleaned).resolve()
                rel = normalize_rel_path(target, self.root_dir)
                if rel in known_files:
                    return rel

                for ext in (".js", ".jsx", ".ts", ".tsx", ".py", ".html", ".css", ".json", ".java"):
                    target_ext = (base / f"{cleaned}{ext}").resolve()
                    rel_ext = normalize_rel_path(target_ext, self.root_dir)
                    if rel_ext in known_files:
                        return rel_ext

                    index_target = (base / cleaned / f"index{ext}").resolve()
                    rel_index = normalize_rel_path(index_target, self.root_dir)
                    if rel_index in known_files:
                        return rel_index
            except Exception:
                pass

        # 3. Python dot-notation
        dot_path = cleaned.replace(".", "/")
        for base in check_bases:
            try:
                for ext in (".py", ".js", ".ts"):
                    target_dot = (base / f"{dot_path}{ext}").resolve()
                    rel_dot = normalize_rel_path(target_dot, self.root_dir)
                    if rel_dot in known_files:
                        return rel_dot
            except Exception:
                pass

        # 4. Exact filename match
        target_name = Path(cleaned).name.lower()
        exact_matches = [f for f in known_files if Path(f).name.lower() == target_name]
        if len(exact_matches) == 1:
            return exact_matches[0]
        elif len(exact_matches) > 1:
            for f in exact_matches:
                if str(current_dir).replace("\\", "/") in f:
                    return f
            return exact_matches[0]

        # 5. Stem fallback
        target_stem = Path(cleaned).stem.lower()
        if target_stem:
            stem_matches = [f for f in known_files if Path(f).stem.lower() == target_stem]
            if len(stem_matches) == 1:
                return stem_matches[0]
            elif len(stem_matches) > 1:
                for f in stem_matches:
                    if str(current_dir).replace("\\", "/") in f:
                        return f
                return stem_matches[0]

        return None
