"""
Streamlit Community Cloud default entry point for Romankiv Computer Vision Studio.
Delegates execution to app.py so Streamlit Cloud's default 'streamlit_app.py' works out of the box.
"""
from pathlib import Path

app_path = Path(__file__).parent / "app.py"
with open(app_path, "r", encoding="utf-8") as f:
    exec(compile(f.read(), str(app_path), "exec"), globals())
