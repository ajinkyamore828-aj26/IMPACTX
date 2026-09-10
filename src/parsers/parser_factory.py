"""
Parser factory for impactx.
Routes files to the appropriate language parser based on extension.
"""

from pathlib import Path
from typing import Optional, Dict
from src.parsers.base_parser import BaseParser
from src.parsers.python_parser import PythonParser
from src.parsers.javascript_parser import JavaScriptParser
from src.parsers.java_parser import JavaParser
from src.parsers.html_parser import HtmlParser
from src.parsers.css_parser import CssParser

class ParserFactory:
    _parsers: Dict[str, BaseParser] = {}

    @classmethod
    def get_parser(cls, file_path: str | Path) -> Optional[BaseParser]:
        """Returns the appropriate parser instance for a given file extension."""
        ext = Path(file_path).suffix.lower()
        
        if ext in cls._parsers:
            return cls._parsers[ext]

        parser: Optional[BaseParser] = None
        if ext == ".py":
            parser = PythonParser()
        elif ext in (".js", ".jsx", ".ts", ".tsx"):
            parser = JavaScriptParser()
        elif ext == ".java":
            parser = JavaParser()
        elif ext in (".html", ".htm"):
            parser = HtmlParser()
        elif ext == ".css":
            parser = CssParser()

        if parser:
            cls._parsers[ext] = parser
        return parser

    @classmethod
    def is_supported(cls, file_path: str | Path) -> bool:
        ext = Path(file_path).suffix.lower()
        return ext in {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".html", ".htm", ".css"}
