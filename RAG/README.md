# 🧠 RAG Backend (FastAPI + Elasticsearch)

A minimal **Retrieval-Augmented Generation (RAG)** backend built with **FastAPI** and **Elasticsearch** for vector similarity search.

Designed as a clean foundation for LLM-powered search and chat systems.

---

## ✨ What this does

- Stores embeddings in Elasticsearch (`dense_vector`)
- Retrieves top-K relevant chunks using cosine similarity
- Automatically creates indices on startup
- Easy to extend for any LLM

---

## 🛠 Tech Stack

- Python 3.11
- FastAPI + Uvicorn
- Elasticsearch 8.x
- Docker Compose
- Pipenv

---

## 🚀 Quick Start

```bash
docker compose up -d
pipenv --python 3.11
pipenv install
pipenv shell
uvicorn app.main:app --reload --port 4000
```
