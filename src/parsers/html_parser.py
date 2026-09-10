"""
HTML parser for impactx using BeautifulSoup4.
Extracts script references, stylesheets, linked pages, and endpoints.
"""

from bs4 import BeautifulSoup
from src.parsers.base_parser import (
    BaseParser,
    ParsedModule,
    ImportEntity,
)
from src.utils.file_utils import count_lines
from src.utils.logger import get_logger

logger = get_logger("html_parser")

class HtmlParser(BaseParser):
    def __init__(self):
        super().__init__(language="HTML")

    def parse(self, file_path: str, content: str) -> ParsedModule:
        total_lines, code_lines, comment_lines = count_lines(content)
        module = ParsedModule(
            file_path=file_path,
            language="HTML",
            lines_of_code=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
        )

        try:
            soup = BeautifulSoup(content, "html.parser")

            # 1. Scripts (<script src="...">)
            for script in soup.find_all("script", src=True):
                src = script["src"]
                if src and not src.startswith(("http://", "https://", "//")):
                    module.imports.append(
                        ImportEntity(
                            source=src,
                            module=src,
                            names=["script"],
                            is_relative=src.startswith("."),
                        )
                    )

            # 2. Stylesheets (<link rel="stylesheet" href="...">)
            for link in soup.find_all("link", href=True):
                rel = link.get("rel", [])
                if isinstance(rel, list):
                    rel = " ".join(rel)
                if "stylesheet" in rel.lower():
                    href = link["href"]
                    if href and not href.startswith(("http://", "https://", "//")):
                        module.imports.append(
                            ImportEntity(
                                source=href,
                                module=href,
                                names=["stylesheet"],
                                is_relative=href.startswith("."),
                            )
                        )

            # 3. Internal page links (<a href="...">)
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href and not href.startswith(("http://", "https://", "#", "mailto:", "tel:")):
                    module.raw_calls.append(href)

        except Exception as e:
            logger.error(f"Error parsing HTML file {file_path}: {e}")
            module.parse_error = str(e)

        return module
