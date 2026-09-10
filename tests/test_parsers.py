"""
Unit tests for multi-language AST and code parsers.
"""

from src.parsers.python_parser import PythonParser
from src.parsers.javascript_parser import JavaScriptParser
from src.parsers.java_parser import JavaParser
from src.parsers.html_parser import HtmlParser
from src.parsers.css_parser import CssParser
from src.parsers.parser_factory import ParserFactory

def test_python_parser():
    code = """
import os
from math import sqrt as square_root

class Calculator:
    def add(self, a, b):
        return a + b

def calculate_metric(val):
    c = Calculator()
    return c.add(val, 10)
"""
    parser = PythonParser()
    module = parser.parse("calc.py", code)

    assert len(module.functions) == 2  # add (method) and calculate_metric
    assert len(module.classes) == 1
    assert module.classes[0].name == "Calculator"
    assert len(module.imports) == 2
    assert "add" in module.raw_calls or "Calculator" in module.raw_calls

def test_javascript_parser():
    code = """
import { login } from "./auth.js";
export function init() {
    login("admin", "pass");
}
export class AppService {
    async start() {
        init();
    }
}
"""
    parser = JavaScriptParser()
    module = parser.parse("app.js", code)

    assert len(module.imports) == 1
    assert module.imports[0].source == "./auth.js"
    assert "login" in module.imports[0].names
    assert len(module.functions) >= 1
    assert "init" in module.exports or len(module.classes) >= 1

def test_java_parser():
    code = """
package com.demo;
import java.util.List;

public class OrderService {
    public void processOrder(String orderId) {
        validate(orderId);
    }
}
"""
    parser = JavaParser()
    module = parser.parse("OrderService.java", code)

    assert len(module.imports) == 1
    assert len(module.classes) == 1
    assert module.classes[0].name == "OrderService"
    assert len(module.functions) == 1
    assert module.functions[0].name == "processOrder"

def test_html_parser():
    html = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css">
    <script src="bundle.js"></script>
</head>
<body>
    <a href="about.html">About</a>
</body>
</html>
"""
    parser = HtmlParser()
    module = parser.parse("index.html", html)

    sources = [imp.source for imp in module.imports]
    assert "style.css" in sources
    assert "bundle.js" in sources
    assert "about.html" in module.raw_calls

def test_css_parser():
    css = """
@import url("theme.css");
@import "reset.css";
body { color: red; }
"""
    parser = CssParser()
    module = parser.parse("main.css", css)

    sources = [imp.source for imp in module.imports]
    assert "theme.css" in sources
    assert "reset.css" in sources

def test_parser_factory():
    assert ParserFactory.is_supported("script.py")
    assert ParserFactory.is_supported("ui.jsx")
    assert ParserFactory.is_supported("style.css")
    assert not ParserFactory.is_supported("binary.exe")
