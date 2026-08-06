# 🔌 MCP Server Hub

<p align="center">
  <img src="https://img.shields.io/badge/MCP-Server-blue?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Agents-purple?style=for-the-badge" />
</p>

> **Discover, install, and manage MCP servers** — a curated directory for AI agent tools.

## ✨ Features

- 📋 Curated directory of 100+ MCP servers
- 🔍 Search by category (browsing, coding, data, etc.)
- 📦 One-command installer
- ⭐ Ratings and reviews
- 🔄 Auto-update checking

## 🚀 Quick Start

```bash
git clone https://github.com/axe01010/mcp-server-hub.git
cd mcp-server-hub

# Browse the directory
python browse.py

# Install a server
python install.py mcp-server-name

# List installed
python manage.py list
```

## 📂 Categories

| Category | Examples |
|----------|----------|
| 🌐 Browsing | Playwright, Puppeteer |
| 💻 Coding | GitHub, GitLab, Jira |
| 📊 Data | PostgreSQL, Redis, BigQuery |
| 📁 Files | S3, Google Drive, Notion |
| 🤖 AI | OpenAI, Anthropic, Ollama |

## 📁 Structure

```
mcp-server-hub/
├── browse.py             # Browse directory
├── install.py            # Install servers
├── manage.py             # Manage installed
├── servers/              # Server configs
│   ├── github.json
│   ├── postgres.json
│   └── ...
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Add new servers via pull request.

## 📜 License

MIT
