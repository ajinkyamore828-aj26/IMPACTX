"""
CSS parser for impactx.
Extracts @import statements and stylesheet dependencies.
"""

import re
from src.parsers.base_parser import (
    BaseParser,
    ParsedModule,
    ImportEntity,
)
from src.utils.file_utils import count_lines
from src.utils.logger import get_logger

logger = get_logger("css_parser")

class CssParser(BaseParser):
    def __init__(self):
        super().__init__(language="CSS")

    def parse(self, file_path: str, content: str) -> ParsedModule:
        total_lines, code_lines, comment_lines = count_lines(content)
        module = ParsedModule(
            file_path=file_path,
            language="CSS",
            lines_of_code=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
        )

        try:
            # Match @import url("...") or @import "..."
            import_pattern = re.compile(r'@import\s+(?:url\([\'"]?([^\'")]+)[\'"]?\)|[\'"]([^\'"]+)[\'"]);')
            for i, line in enumerate(content.splitlines(), 1):
                match = import_pattern.search(line)
                if match:
                    src = match.group(1) or match.group(2)
                    if src and not src.startswith(("http://", "https://", "//")):
                        module.imports.append(
                            ImportEntity(
                                source=src,
                                module=src,
                                names=["css_import"],
                                is_relative=src.startswith("."),
                                line_number=i,
                            )
                        )
        except Exception as e:
            logger.error(f"Error parsing CSS file {file_path}: {e}")
            module.parse_error = str(e)

        return module
