from typing import List

from fastapi import Request

from app.libs.elasticsearch_db import get_elastic_db
from app.libs.embedding import embedding
from app.libs.response import Response


class IngestController:
    @staticmethod
    def bulk_ingest_documents(request: Request, data: List[str]):
        try:
            vectors = embedding.embed(data)
            elastic_db = get_elastic_db()

            for i in range(len(data)):
                elastic_db.add_vector(
                    embedding=vectors[i],
                    content=data[i]
                )

            return Response.success(f'{len(data)} Documents ingested successfully')

        except Exception as e:
            raise RuntimeError("Bulk ingestion failed") from e