---
title: uv - Package Management
---
# Package Management with `uv

> **Docs:** https://docs.astral.sh/uv/

```python
cd your-project
uv venv                    # Creates .venv in project directory
source .venv/bin/activate  # or: . .venv/bin/activate
uv pip install pandas numpy
```

**Advantages over managing with `conda`:** `conda` can introduce dependency duplication. uv uses aggressive [caching](https://docs.astral.sh/uv/concepts/cache/) to avoid re-downloading (and re-building) dependencies that have already been accessed in prior runs. Let's say two projects are using the same 'pandas' version. Even if you have a separate environments for the projects, uv does not install the dependency twice (like it would do with `conda` environments).

## `uv` commands:

**Install uv (first time):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Setup project:**
```bash
uv init && uv venv --python 3.12
```

**Activate environment:**
```bash
source .venv/bin/activate
```

**Install project in editable mode:**
```bash
uv pip install -e .
```

**Add dependencies:**
```bash
uv add pandas
```

**Add dependencies (`pip` compatibility):**
```bash
uv pip install pandas
```

**Running scripts**
```bash
uv run example.py
```
## Links
- [Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/#using-uv-with-jupyter)
