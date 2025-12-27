from fastapi import APIRouter, Request
from typing import List
from app.services.ingest.controller import IngestController

router = APIRouter()

@router.post("/bulk")
def upload_documents_in_bulk(request: Request, payload: List[str]):
    return IngestController.bulk_ingest_documents(request, payload)

@router.post("/")
async def upload_document(request: Request, doc):
     return ""