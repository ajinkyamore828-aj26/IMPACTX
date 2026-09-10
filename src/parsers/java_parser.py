"""
Java source code parser for impactx.
Extracts packages, imports, classes, interfaces, methods, and calls.
"""

import re
from src.parsers.base_parser import (
    BaseParser,
    ParsedModule,
    FunctionEntity,
    ClassEntity,
    ImportEntity,
)
from src.utils.file_utils import count_lines
from src.utils.logger import get_logger

logger = get_logger("java_parser")

class JavaParser(BaseParser):
    def __init__(self):
        super().__init__(language="Java")

    def parse(self, file_path: str, content: str) -> ParsedModule:
        total_lines, code_lines, comment_lines = count_lines(content)
        module = ParsedModule(
            file_path=file_path,
            language="Java",
            lines_of_code=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
        )

        try:
            self._extract_imports(content, module)
            self._extract_classes_and_methods(content, module, file_path)
            self._extract_calls(content, module)
        except Exception as e:
            logger.error(f"Error parsing Java file {file_path}: {e}")
            module.parse_error = str(e)

        return module

    def _extract_imports(self, content: str, module: ParsedModule) -> None:
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            if line_str.startswith("import "):
                match = re.search(r'import\s+(?:static\s+)?([a-zA-Z0-9_.*]+);', line_str)
                if match:
                    full_import = match.group(1)
                    symbol = full_import.split(".")[-1]
                    module.imports.append(
                        ImportEntity(
                            source=full_import,
                            module=".".join(full_import.split(".")[:-1]),
                            names=[symbol],
                            is_relative=False,
                            line_number=i,
                        )
                    )

    def _extract_classes_and_methods(self, content: str, module: ParsedModule, file_path: str) -> None:
        lines = content.splitlines()
        class_regex = re.compile(
            r'(?:public|protected|private)?\s*(?:static\s+)?(?:final\s+)?(?:abstract\s+)?(class|interface|enum)\s+([a-zA-Z0-9_]+)(?:\s+extends\s+([a-zA-Z0-9_]+))?(?:\s+implements\s+([a-zA-Z0-9_,\s]+))?'
        )
        method_regex = re.compile(
            r'(?:public|protected|private)?\s*(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?([a-zA-Z0-9_<>[\]]+)\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*(?:throws\s+[a-zA-Z0-9_,\s]+)?\s*\{?'
        )
        
        current_class = None
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            # Class match
            c_match = class_regex.search(line_str)
            if c_match:
                kind = c_match.group(1)
                name = c_match.group(2)
                extends = [c_match.group(3)] if c_match.group(3) else []
                current_class = name
                module.classes.append(
                    ClassEntity(
                        name=name,
                        file_path=file_path,
                        line_start=i,
                        line_end=min(i + 50, len(lines)),
                        base_classes=extends,
                        length=50,
                    )
                )
                continue

            # Method match
            m_match = method_regex.search(line_str)
            if m_match and not line_str.startswith(("if", "for", "while", "catch", "switch", "return", "new")):
                ret_type = m_match.group(1)
                fn_name = m_match.group(2)
                raw_params = m_match.group(3)
                params = [p.strip() for p in raw_params.split(",") if p.strip()]
                if fn_name not in ("if", "for", "while", "catch", "switch"):
                    module.functions.append(
                        FunctionEntity(
                            name=fn_name,
                            file_path=file_path,
                            line_start=i,
                            line_end=min(i + 20, len(lines)),
                            parameters=params,
                            return_type=ret_type,
                            is_method=(current_class is not None),
                            class_name=current_class,
                            length=20,
                        )
                    )

    def _extract_calls(self, content: str, module: ParsedModule) -> None:
        call_regex = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
        reserved = {"if", "for", "while", "switch", "catch", "new", "super", "this", "return", "System"}
        calls = set()
        for line in content.splitlines():
            line_str = line.strip()
            for m in call_regex.finditer(line_str):
                name = m.group(1)
                if name not in reserved:
                    calls.add(name)
        module.raw_calls = list(calls)
