# DocuMind AI

DocuMind AI is a document intelligence MVP. Upload a text-based PDF, extract its pages, split the text into overlapping chunks, retrieve relevant passages, and ask questions with page-level source references.

## What works today

- FastAPI backend with interactive OpenAPI docs
- PDF upload validation and text extraction using PyMuPDF
- SQLite persistence by default (PostgreSQL can be configured)
- Chunk storage and transparent lexical retrieval
- Optional OpenAI-compatible chat completion integration
- Retrieval-only fallback when no AI API key is configured
- Streamlit user interface
- Basic automated tests and Docker packaging

## Important limitations

This is an MVP, not a production-ready multi-tenant service. Retrieval currently uses keyword overlap rather than vector embeddings. Scanned PDFs need OCR, which is not included. Authentication, authorization, rate limiting, malware scanning, robust migrations, and production storage are future engineering tasks. Do not upload confidential documents to an untrusted deployment.

## Quick start (Python 3.11+)

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API.

In a second terminal, activate the same environment and run:

```bash
streamlit run streamlit_app.py
```

Open http://localhost:8501.

## Optional AI answers

Set `OPENAI_API_KEY` in `.env` to enable synthesized answers from retrieved passages. `OPENAI_BASE_URL` and `OPENAI_MODEL` support compatible providers. Without a key, the app returns retrieved excerpts and clearly labels the mode as `retrieval_only`.

Never commit `.env` or API keys.

## API

- `GET /health` — health check
- `POST /documents` — upload a PDF as multipart form field `file`
- `GET /documents` — list uploaded documents
- `DELETE /documents/{id}` — delete a document and its chunks
- `POST /ask` — JSON body: `{"question": "...", "document_id": 1}`; omit `document_id` to search all documents

## Run tests

```bash
pytest -q
```

## Docker

Copy `.env.example` to `.env`, then:

```bash
docker compose up --build
```

API: http://localhost:8000/docs  
UI: http://localhost:8501

## Suggested next engineering milestones

1. Add database migrations with Alembic.
2. Add vector embeddings and a vector index; evaluate retrieval quality with a small benchmark.
3. Add authentication, per-user document ownership, and authorization tests.
4. Add OCR as an opt-in processing pipeline for scanned PDFs.
5. Add file lifecycle management, observability, structured logs, and rate limiting.
6. Add CI with linting, type checking, and test execution.

## Project ownership

Build on this code, understand it, run the tests, make meaningful changes, and document your design decisions before presenting it as your own work.
