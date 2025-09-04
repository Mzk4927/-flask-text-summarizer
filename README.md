## TextRank Summarizer (Flask)

A simple, production-ready Flask web app that extracts the most important sentences from text using the classic TextRank algorithm (PageRank over TF‑IDF cosine similarity). Paste raw text, provide a local file path (.txt, .docx, .pdf), or submit a URL — get a concise summary instantly.

### Features
- **Multiple input sources**: raw text, local files (.txt/.docx/.pdf), or URLs
- **Language processing**: sentence segmentation via spaCy
- **Ranking**: TF‑IDF + cosine similarity + NetworkX PageRank
- **Lightweight UI**: basic HTML form served by Flask
- **Container-ready**: Dockerfile included

### Tech Stack
- **Backend**: Python, Flask
- **NLP**: spaCy (`en_core_web_sm`), scikit‑learn (TF‑IDF), NetworkX (PageRank)
- **Parsing**: BeautifulSoup (HTML), python‑docx, PyPDF2

---

### Live Demo (optional)
If you’re hosting on Hugging Face Spaces or elsewhere, add your link here:

`https://huggingface.co/spaces/<your-username>/textrank-flask`

---

### Project Structure
```
.
├─ app.py                  # Flask app with TextRank pipeline
├─ templates/
│  └─ index.html          # Minimal form UI
├─ requirements.txt        # Python dependencies
├─ Dockerfile              # Container build
└─ README.md               # This file
```

---

### Quick Start (Local)

Prereqs: Python 3.9+ recommended.

```bash
# 1) Create and activate a virtualenv (recommended)
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3) Run the app
python app.py
# App runs on http://127.0.0.1:7860 (or PORT from env)
```

Open your browser to `http://127.0.0.1:7860/` and paste text, a file path, or a URL.

---

### API

- **POST** `/summarize`
  - Form fields:
    - `source` (string): raw text, local file path, or URL
    - `num_sentences` (int, default 5): number of sentences to return
  - Responses:
    - `200 OK`: HTML snippet containing bullet-point summary
    - `400 Bad Request`: error message if extraction or summarization fails

Example (curl):
```bash
curl -X POST http://127.0.0.1:7860/summarize \
  -F "source=Your raw text goes here" \
  -F "num_sentences=5"
```

---

### Docker

Build and run locally:
```bash
docker build -t textrank-flask .
docker run --rm -p 7860:7860 textrank-flask
```

---

### Deployment Notes

- **Port**: The app reads `PORT` from the environment (default `7860`).
- **spaCy model**: Ensure `en_core_web_sm` is available at runtime (install during build or first start).
- **File inputs**: When providing a local path via the UI, the file must be readable from the server’s filesystem.

#### Hugging Face Spaces
1) Push this repo to your Space (Gradio/Static not required; this is a Flask app).
2) Set the Space to use the `Dockerfile` or a custom command that runs `python app.py`.
3) Confirm port exposure (use the default 7860 or set `PORT`).

#### Render/Heroku/Fly.io/etc.
- Use the Dockerfile or a Procfile-style command: `python app.py`.
- Configure environment variable `PORT` if required by the platform.

---

### How It Works (Brief)
1) spaCy segments text into sentences.
2) TF‑IDF vectorization over sentences (with spaCy stopwords).
3) Cosine similarity matrix becomes a graph (nodes = sentences, edges = similarity).
4) PageRank scores sentences; top‑k are selected and re‑ordered to preserve readability.

---

### Troubleshooting
- "spaCy model not found": run `python -m spacy download en_core_web_sm`.
- "Could not extract text": for URLs ensure the page is reachable; for files ensure the server can access the path and the extension is one of `.txt`, `.docx`, `.pdf`.
- PDF extraction quality depends on the source PDF; some PDFs have limited or no extractable text.

---

### License
This project is licensed under the terms of the `LICENSE` file in this repository.


