import time
import logging
from elasticsearch8 import Elasticsearch
from typing import List, Dict, Any

from app.config import get_settings

# Setup basic logging to see retry attempts in your terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = get_settings()


class ElasticVectorDB:
    def __init__(
            self,
            index_name: str,
            embedding_dim: int = config.embedding_dims,
            host: str = f"http://{config.db_host}:{config.db_port}",
    ):
        self.index_name = index_name
        self.embedding_dim = embedding_dim
        # Using hosts list format for better compatibility
        self.client = Elasticsearch('http://localhost:9200', basic_auth=None, meta_header=False,  verify_certs=False,  # Explicitly no auth
                                    headers={"Accept": "application/json"})

        # Attempt to connect before proceeding
        self.check_connection()
        self._ensure_index()

    def check_connection(self):
        """Attempts to ping Elasticsearch with retries."""
        max_retries = 10
        delay = 5  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                if self.client.ping():
                    logger.info("Successfully connected to Elasticsearch.")
                    return
                else:
                    logger.warning(f"Connection attempt {attempt}/{max_retries}: Ping failed.")
            except Exception as e:
                logger.warning(f"Connection attempt {attempt}/{max_retries}: {e}")

            if attempt < max_retries:
                time.sleep(delay)

        # If we exit the loop, all retries failed
        raise ConnectionError(
            f"Could not connect to Elasticsearch at {config.db_host}:{config.db_port} after {max_retries} attempts."
        )

    # -------------------------
    # internal
    # -------------------------
    def _ensure_index(self):
        if self.client.indices.exists(index=self.index_name):
            return

        mapping = {
            "mappings": {
                "properties": {
                    "embedding": {
                        "type": "dense_vector",
                        "dims": self.embedding_dim,
                        "index": True,
                        "similarity": "cosine",
                    },
                    "content": {"type": "text"},
                    "metadata": {
                        "properties": {
                            "source": {"type": "keyword"},
                        }
                    },
                }
            }
        }

        self.client.indices.create(
            index=self.index_name,
            body=mapping,
        )

    # ... (rest of your add_vector and search methods remain the same)

    def add_vector(self, embedding: List[float], content: str, metadata: Dict[str, Any] | None = None, source: str | None = None):
        meta = dict(metadata or {})
        if source:
            meta["source"] = source
        doc = {"embedding": embedding, "content": content, "metadata": meta}
        self.client.index(index=self.index_name, document=doc)

    def search(self, query_embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
        query = {
            "knn": {
                "field": "embedding",
                "query_vector": query_embedding,
                "k": k,
                "num_candidates": 100,
            }
        }
        response = self.client.search(index=self.index_name, body={"size": k, "query": query})
        return [
            {
                "score": hit["_score"],
                "content": hit["_source"]["content"],
                "metadata": hit["_source"]["metadata"],
            }
            for hit in response["hits"]["hits"]
        ]

    def list_docs(self) -> List[Dict[str, Any]]:
        if not self.client.indices.exists(index=self.index_name):
            return []
        resp = self.client.search(
            index=self.index_name,
            body={
                "size": 0,
                "aggs": {
                    "by_source": {
                        "terms": {"field": "metadata.source", "size": 10000},
                        "aggs": {
                            "first_chunk": {
                                "top_hits": {"size": 1, "_source": ["content"]}
                            }
                        },
                    }
                },
            },
        )
        out: List[Dict[str, Any]] = []
        for bucket in resp["aggregations"]["by_source"]["buckets"]:
            source: str = bucket["key"]
            chunks: int = bucket["doc_count"]
            hits = bucket["first_chunk"]["hits"]["hits"]
            summary: str | None = None
            if hits:
                content: str = hits[0]["_source"].get("content", "")
                first_line = content.split("\n", 1)[0].strip()
                summary = first_line[:120] if first_line else None
            out.append({
                "file": source.split("/")[-1],
                "path": source,
                "chunks": chunks,
                "summary": summary,
            })
        return sorted(out, key=lambda x: x["path"])

    def delete_database(self):
        if self.client.indices.exists(index=self.index_name):
            self.client.indices.delete(index=self.index_name)


elastic_db: ElasticVectorDB | None = None


def get_elastic_db() -> ElasticVectorDB:
    global elastic_db
    if elastic_db is None:
        # Note: Index creation is now handled inside __init__ via _ensure_index()
        elastic_db = ElasticVectorDB("rabbits_v1")
    return elastic_db
