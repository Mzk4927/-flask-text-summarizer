# ---------- app.py ----------
import os
import re
import requests
from flask import Flask, request, render_template

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from bs4 import BeautifulSoup
from docx import Document
import PyPDF2

# ---------- spaCy ----------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise SystemExit("spaCy model 'en_core_web_sm' not found.  Run: python -m spacy download en_core_web_sm")

# ---------- helpers ----------
def load_url_text(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return re.sub(r"\s+", " ", soup.get_text(" ")).strip()

def load_local_text(path: str) -> str:
    path = path.strip('"')
    _, ext = os.path.splitext(path.lower())
    if ext == ".txt":
        with open(path, encoding="utf-8") as f:
            return f.read()
    if ext == ".docx":
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    if ext == ".pdf":
        text = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)
    raise ValueError("Unsupported file type.")

def load_and_extract_text(source: str) -> str | None:
    source = source.strip()
    if not source:
        return None
    if source.startswith("http"):
        try:
            return load_url_text(source)
        except Exception:
            return None
    if os.path.isfile(source):
        try:
            return load_local_text(source)
        except Exception:
            return None
    return source

def summarize_text_textrank(text: str, num_sentences: int) -> list[str]:
    if not text or not text.strip():
        return []
    doc = nlp(text)
    sentences = [s.text.strip() for s in doc.sents if s.text.strip()]
    if len(sentences) <= num_sentences:
        return sentences
    try:
        vectorizer = TfidfVectorizer(
            stop_words=list(nlp.Defaults.stop_words),
            lowercase=True,
            max_features=5000
        )
        tfidf = vectorizer.fit_transform(sentences)
        sim = cosine_similarity(tfidf)
    except ValueError:
        return sentences
    graph = nx.from_numpy_array(sim)
    try:
        scores = nx.pagerank(graph, alpha=0.85)
    except nx.PowerIterationFailedConvergence:
        return []
    ranked = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    selected = [s for _, s in ranked[:num_sentences]]
    idx_map = {sent: i for i, sent in enumerate(sentences)}
    selected.sort(key=lambda s: idx_map[s])
    return selected

# ---------- Flask ----------
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    source = request.form.get("source", "")
    num_sentences = int(request.form.get("num_sentences", 5))

    raw_text = load_and_extract_text(source)
    if not raw_text:
        return "❌ Could not extract text.", 400

    summary = summarize_text_textrank(raw_text, num_sentences)
    if not summary:
        return "❌ Could not summarize.", 400

    bullets = "<br>".join(f"• {s}" for s in summary)
    return f"<h2>Summary</h2>{bullets}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    app.run(host="0.0.0.0", port=port)