from typing import List, Union
import ollama

from app.config import get_settings

config = get_settings()

class EmbeddingService:
    def __init__(self):
        """
        model example:
        - nomic-embed-text
        - mxbai-embed-large
        """
        self.model = config.embedding_model

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        Returns:
        - List[List[float]] for batch
        - Always batched (even for single string)
        """
        if isinstance(text, str):
            text = [text]

        response = ollama.embeddings(
            model=self.model,
            prompt=text,
        )

        return [item["embedding"] for item in response["data"]]

    def embed_one(self, text: str) -> List[float]:
        """
        Convenience wrapper for single text
        """
        return self.embed(text)[0]

embedding = EmbeddingService()