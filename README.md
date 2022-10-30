# Dependency Heaven
*Deph* is a small script that generates a dependencies file with the used versions.<br>
**This isn't serious, just an experiment with the Python's AST.**

# Installation
```python
pip install git+https://github.com/ZSendokame/depheaven.git
```

# Use
```
              | File with dependencies.
deph --file target.py --output requirements.txt <- Here, it writes the dependencies.
```