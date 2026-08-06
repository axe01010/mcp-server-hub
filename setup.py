#!/usr/bin/env python3
"""Packaging for mcp-server-hub.

Install in dev mode:  pip install -e .
Installs console scripts ``mcp-browse``, ``mcp-install``, ``mcp-manage``,
``mcp-validate``.
"""
from setuptools import setup

setup(
    name="mcp-server-hub",
    version="0.3.0",
    description="Curated, validated catalog of MCP (Model Context Protocol) servers.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="axe01010",
    license="MIT",
    python_requires=">=3.9",
    py_modules=["hub_common", "browse", "install", "manage"],
    install_requires=["requests>=2.31"],
    entry_points={
        "console_scripts": [
            "mcp-browse=browse:main",
            "mcp-install=install:main",
            "mcp-manage=manage:main",
            "mcp-validate=install:main",
        ],
    },
    include_package_data=True,
)