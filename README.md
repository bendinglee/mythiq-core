# 🧠 Mythiq — Modular Cognition AI

Mythiq is a self-reflective, adaptive AI system engineered for memory tracking, introspective routing, persona evolution, and multi-branch cognition. Built for free-tier platforms like Railway and GitHub Codespaces, Mythiq doesn’t just respond — it reflects.

---

## 🚀 Live Demo  
[![Launch Mythiq](https://img.shields.io/badge/Open-Mythiq-blue)](https://observant-fascination-production.up.railway.app)

## ⚡ Deploy Instantly  
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/YOUR_TEMPLATE_ID)

---

## 🔍 Key API Endpoints

| Type            | Endpoint                                       | Description                                         |
|-----------------|------------------------------------------------|-----------------------------------------------------|
| 🧠 Identity     | `/api/meta/model/snapshot`                     | Boot signature and module list                      |
|                | `/api/meta/model/fingerprint`                  | Cognitive traits, gradient, module scope            |
| 🧬 Persona      | `/api/persona/self`                            | Mission, style, tone, and learning model            |
|                | `/api/persona/traits`                          | Cognition fingerprint and resilience profile        |
|                | `/api/persona/adapt/reflect`                   | Mood/tone/goals update via POST                     |
| 🧠 Memory       | `/api/memory/explore/summary`                 | Active anchors and trigger trace                    |
|                | `/api/memory/explore/journal`                 | Session-level anchor history                        |
| 📚 Docs         | `/api/docs/contribute/map`                    | Full route hierarchy for developers                 |
| 🔌 Plugins      | `/api/interface/style/plugin/spec`            | External module injection spec                      |
| 🚦 Health       | `/healthcheck`                                | Fast boot response for Railway uptime               |

---

## 🧪 Quick Start (Codespaces or Local)

```bash
git clone https://github.com/bendinglee/mythiq-core
cd mythiq-core
pip install -r requirements.txt

# Run using Railway or locally
export PORT=5000
gunicorn main:app -b 0.0.0.0:$PORT --timeout 120
