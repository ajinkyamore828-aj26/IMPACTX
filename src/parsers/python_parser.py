"""
AST-based Python code parser.
"""

import ast
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

logger = get_logger("python_parser")

class ComplexityVisitor(ast.NodeVisitor):
    """Calculates approximate cyclomatic complexity for an AST node."""
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)

class PythonParser(BaseParser):
    def __init__(self):
        super().__init__(language="Python")

    def parse(self, file_path: str, content: str) -> ParsedModule:
        total_lines, code_lines, comment_lines = count_lines(content)
        module = ParsedModule(
            file_path=file_path,
            language="Python",
            lines_of_code=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
        )

        try:
            tree = ast.parse(content, filename=file_path)
        except SyntaxError as e:
            logger.warning(f"Syntax error parsing {file_path}: {e}")
            module.parse_error = f"SyntaxError: {e.msg} (line {e.lineno})"
            return module
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            module.parse_error = str(e)
            return module

        # Traverse AST
        self._extract_imports(tree, module)
        self._extract_classes(tree, module, file_path)
        self._extract_functions(tree, module, file_path)
        self._extract_module_calls(tree, module)

        return module

    def _extract_imports(self, tree: ast.AST, module: ParsedModule) -> None:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module.imports.append(
                        ImportEntity(
                            source=alias.name,
                            module=alias.name,
                            names=[alias.asname or alias.name],
                            alias=alias.asname,
                            is_relative=False,
                            line_number=node.lineno,
                        )
                    )
            elif isinstance(node, ast.ImportFrom):
                mod_name = "." * node.level + (node.module or "")
                names = [a.name for a in node.names]
                module.imports.append(
                    ImportEntity(
                        source=mod_name,
                        module=mod_name,
                        names=names,
                        is_relative=(node.level > 0),
                        line_number=node.lineno,
                    )
                )

    def _extract_classes(self, tree: ast.AST, module: ParsedModule, file_path: str) -> None:
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                bases = []
                for b in node.bases:
                    if isinstance(b, ast.Name):
                        bases.append(b.id)
                    elif isinstance(b, ast.Attribute):
                        bases.append(b.attr)

                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)

                line_end = getattr(node, "end_lineno", node.lineno)
                docstring = ast.get_docstring(node)
                class_entity = ClassEntity(
                    name=node.name,
                    file_path=file_path,
                    line_start=node.lineno,
                    line_end=line_end,
                    methods=methods,
                    base_classes=bases,
                    docstring=docstring,
                    length=max(1, line_end - node.lineno + 1),
                )
                module.classes.append(class_entity)

    def _extract_functions(self, tree: ast.AST, module: ParsedModule, file_path: str) -> None:
        # Module-level functions
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn = self._build_function_entity(node, file_path, is_method=False, class_name=None)
                module.functions.append(fn)

        # Class methods
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        fn = self._build_function_entity(item, file_path, is_method=True, class_name=node.name)
                        module.functions.append(fn)

    def _build_function_entity(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        file_path: str,
        is_method: bool,
        class_name: Optional[str],
    ) -> FunctionEntity:
        params = [arg.arg for arg in node.args.args]
        return_type = None
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return_type = node.returns.id
            elif isinstance(node.returns, ast.Constant):
                return_type = str(node.returns.value)

        # Decorators
        decorators = []
        for d in node.decorator_list:
            if isinstance(d, ast.Name):
                decorators.append(d.id)
            elif isinstance(d, ast.Attribute):
                decorators.append(d.attr)
            elif isinstance(d, ast.Call):
                if isinstance(d.func, ast.Name):
                    decorators.append(d.func.id)
                elif isinstance(d.func, ast.Attribute):
                    decorators.append(d.func.attr)

        # In-function calls
        calls = []
        for inner in ast.walk(node):
            if isinstance(inner, ast.Call):
                if isinstance(inner.func, ast.Name):
                    calls.append(inner.func.id)
                elif isinstance(inner.func, ast.Attribute):
                    calls.append(inner.func.attr)

        # Complexity
        cv = ComplexityVisitor()
        cv.visit(node)
        complexity = float(cv.complexity)

        line_end = getattr(node, "end_lineno", node.lineno)
        return FunctionEntity(
            name=node.name,
            file_path=file_path,
            line_start=node.lineno,
            line_end=line_end,
            parameters=params,
            return_type=return_type,
            calls=calls,
            decorators=decorators,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_method=is_method,
            class_name=class_name,
            docstring=ast.get_docstring(node),
            complexity_score=complexity,
            length=max(1, line_end - node.lineno + 1),
        )

    def _extract_module_calls(self, tree: ast.AST, module: ParsedModule) -> None:
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
        module.raw_calls = calls
