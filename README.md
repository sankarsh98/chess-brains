# How Computers Play Chess

A hands-on mini-course built with Quartz. It builds a tiny alpha-beta chess engine in Python.

Site: https://sankarsh98.github.io/chess-brains/

```bash
npm ci && npx quartz plugin install
npx quartz build -d docs --serve            # preview the site (content lives in docs/)
uv venv && uv pip install chess
.venv/bin/python engine/tiny_engine.py      # run the engine
```
