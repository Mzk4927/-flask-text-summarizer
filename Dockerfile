FROM python:3.11-slim

# install spaCy model once
RUN python -m pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir spacy && \
    python -m spacy download en_core_web_sm

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code
ENV PORT=7860
EXPOSE 7860
CMD ["python", "app.py", "--host=0.0.0.0", "--port=7860"]