"""
JavaScript and TypeScript parser for impactx.
Extracts ES6 and CommonJS imports, exports, functions, classes, methods, and calls.
"""

import re
from typing import List, Optional, Set
from src.parsers.base_parser import (
    BaseParser,
    ParsedModule,
    FunctionEntity,
    ClassEntity,
    ImportEntity,
)
from src.utils.file_utils import count_lines
from src.utils.logger import get_logger

logger = get_logger("javascript_parser")

class JavaScriptParser(BaseParser):
    def __init__(self):
        super().__init__(language="JavaScript")

    def parse(self, file_path: str, content: str) -> ParsedModule:
        total_lines, code_lines, comment_lines = count_lines(content)
        module = ParsedModule(
            file_path=file_path,
            language="JavaScript",
            lines_of_code=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
        )

        try:
            self._extract_imports(content, module)
            self._extract_exports(content, module)
            self._extract_classes(content, module, file_path)
            self._extract_functions(content, module, file_path)
            self._extract_calls(content, module)
        except Exception as e:
            logger.error(f"Error parsing JS file {file_path}: {e}")
            module.parse_error = str(e)

        return module

    def _extract_imports(self, content: str, module: ParsedModule) -> None:
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            # 1. ES6: import { a, b } from './path' OR import x from './path'
            es6_match = re.search(r'import\s+(?:(\*\s+as\s+[\w$]+|\{[\s\w$,]+\}|[\w$]+)\s+from\s+)?[\'"]([^\'"]+)[\'"]', line_str)
            if es6_match:
                clause = es6_match.group(1) or ""
                source = es6_match.group(2)
                names = []
                if "{" in clause:
                    inner = clause.replace("{", "").replace("}", "")
                    names = [n.strip().split(" as ")[0].strip() for n in inner.split(",") if n.strip()]
                elif clause:
                    names = [clause.strip()]
                
                module.imports.append(
                    ImportEntity(
                        source=source,
                        module=source,
                        names=names,
                        is_relative=source.startswith("."),
                        line_number=i,
                    )
                )
                continue

            # 2. CommonJS: const x = require('./path')
            cjs_match = re.search(r'(?:const|let|var)\s+(\{[\s\w$,]+\}|[\w$]+)\s*=\s*require\([\'"]([^\'"]+)[\'"]\)', line_str)
            if cjs_match:
                clause = cjs_match.group(1)
                source = cjs_match.group(2)
                names = []
                if "{" in clause:
                    inner = clause.replace("{", "").replace("}", "")
                    names = [n.strip().split(":")[0].strip() for n in inner.split(",") if n.strip()]
                else:
                    names = [clause.strip()]
                module.imports.append(
                    ImportEntity(
                        source=source,
                        module=source,
                        names=names,
                        is_relative=source.startswith("."),
                        line_number=i,
                    )
                )

    def _extract_exports(self, content: str, module: ParsedModule) -> None:
        for line in content.splitlines():
            line_str = line.strip()
            exp_match = re.search(r'export\s+(?:default\s+)?(?:class|function|const|let|var)?\s*([\w$]+)', line_str)
            if exp_match:
                name = exp_match.group(1)
                if name not in ("default", "class", "function", "const", "let", "var"):
                    module.exports.append(name)
            elif "module.exports" in line_str:
                module.exports.append("module.exports")

    def _extract_classes(self, content: str, module: ParsedModule, file_path: str) -> None:
        lines = content.splitlines()
        class_regex = re.compile(r'class\s+([\w$]+)(?:\s+extends\s+([\w$]+))?\s*\{')
        for i, line in enumerate(lines, 1):
            m = class_regex.search(line)
            if m:
                class_name = m.group(1)
                base = [m.group(2)] if m.group(2) else []
                # Find methods inside class
                methods = []
                module.classes.append(
                    ClassEntity(
                        name=class_name,
                        file_path=file_path,
                        line_start=i,
                        line_end=min(i + 30, len(lines)),
                        methods=methods,
                        base_classes=base,
                        length=30,
                    )
                )

    def _extract_functions(self, content: str, module: ParsedModule, file_path: str) -> None:
        lines = content.splitlines()
        # 1. function name(...) or async function name(...)
        fn_decl = re.compile(r'(?:async\s+)?function\s+([\w$]+)\s*\(([^)]*)\)')
        # 2. const/let/var name = (async\s*)?(?:\([^)]*\)|[\w$]+)\s*=>
        arrow_decl = re.compile(r'(?:const|let|var)\s+([\w$]+)\s*=\s*(?:async\s*)?(?:\(([^)]*)\)|[\w$]+)\s*=>')
        # 3. Method inside class: methodName(...) {
        method_decl = re.compile(r'^\s*(?:async\s+)?([\w$]+)\s*\(([^)]*)\)\s*\{')

        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            # Ignore control keywords
            if line_str.startswith(("if", "for", "while", "switch", "catch")):
                continue

            m = fn_decl.search(line_str)
            if m:
                name = m.group(1)
                params = [p.strip() for p in m.group(2).split(",") if p.strip()]
                is_async = "async " in line_str
                module.functions.append(
                    FunctionEntity(
                        name=name,
                        file_path=file_path,
                        line_start=i,
                        line_end=min(i + 15, len(lines)),
                        parameters=params,
                        is_async=is_async,
                        length=15,
                    )
                )
                continue

            m_arrow = arrow_decl.search(line_str)
            if m_arrow:
                name = m_arrow.group(1)
                params = [p.strip() for p in (m_arrow.group(2) or "").split(",") if p.strip()]
                is_async = "async " in line_str
                module.functions.append(
                    FunctionEntity(
                        name=name,
                        file_path=file_path,
                        line_start=i,
                        line_end=min(i + 10, len(lines)),
                        parameters=params,
                        is_async=is_async,
                        length=10,
                    )
                )

    def _extract_calls(self, content: str, module: ParsedModule) -> None:
        # Match function calls: word(...)
        call_regex = re.compile(r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(')
        reserved = {"if", "for", "while", "switch", "catch", "function", "import", "require", "return", "typeof"}
        calls = set()
        for line in content.splitlines():
            line_str = line.strip()
            for m in call_regex.finditer(line_str):
                name = m.group(1)
                if name not in reserved:
                    calls.add(name)
        module.raw_calls = list(calls)
