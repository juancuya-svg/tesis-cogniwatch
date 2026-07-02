import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="CogniWatch Admin", layout="wide")
st.title("CogniWatch Admin Console")
st.caption("Operational thesis console for internal review.")

metrics_path = Path(__file__).resolve().parents[2] / "ml" / "artifacts" / "nacc_metrics.json"
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    st.json(metrics)
else:
    st.info("No ML metrics found yet. Run the training scripts first.")
