"""
Base parser interface and data structures.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class FunctionEntity:
    name: str
    file_path: str
    line_start: int = 0
    line_end: int = 0
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    calls: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    is_async: bool = False
    is_method: bool = False
    class_name: Optional[str] = None
    docstring: Optional[str] = None
    complexity_score: float = 1.0
    length: int = 0

@dataclass
class ClassEntity:
    name: str
    file_path: str
    line_start: int = 0
    line_end: int = 0
    methods: List[str] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    length: int = 0

@dataclass
class ImportEntity:
    source: str                 # Relative path or module name imported from
    module: Optional[str] = None # E.g., 'auth' in 'from auth import login'
    names: List[str] = field(default_factory=list) # Imported symbols ['login', 'logout']
    alias: Optional[str] = None
    is_relative: bool = False
    line_number: int = 0

@dataclass
class ParsedModule:
    file_path: str
    language: str
    functions: List[FunctionEntity] = field(default_factory=list)
    classes: List[ClassEntity] = field(default_factory=list)
    imports: List[ImportEntity] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    raw_calls: List[str] = field(default_factory=list)
    lines_of_code: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    parse_error: Optional[str] = None

class BaseParser(ABC):
    """Abstract base class for all language-specific parsers."""
    
    def __init__(self, language: str):
        self.language = language

    @abstractmethod
    def parse(self, file_path: str, content: str) -> ParsedModule:
        """Parse source code string and return structured ParsedModule."""
        pass
