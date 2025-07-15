# 🤝 Contributing to Mythiq

Welcome to Mythiq — a modular cognitive AI framework. To contribute:

## 🔌 Structure

- All features live in `branches/{module}/routes.py`
- Each module defines a Flask `Blueprint`
- `main.py` injects dynamically via:
  ```python
  ("branches.module.routes", "module_bp", "/api/module")
