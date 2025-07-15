# 🧠 Mythiq — Modular Cognition AI

**Mythiq** is a self-reflective AI system built for human-like memory tracking, modular introspection, and persona evolution. Designed to run on free-tier platforms like Railway and GitHub Codespaces.

## 🚀 Features
- Introspective routing with `/api/meta/snapshot`
- Cognitive state summary via `/api/memory/summary`
- Persona engines, reflex triggers, self-learning, and more

## 🧪 Quick Start
```bash
git clone https://github.com/bendinglee/mythiq-core
cd mythiq-core
pip install -r requirements.txt
export PORT=5000
gunicorn main:app -b 0.0.0.0:$PORT --timeout 120
