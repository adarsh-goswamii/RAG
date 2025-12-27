from typing import Any, Optional


class Response:
    @staticmethod
    def success(
        message: str,
        data: Optional[Any] = None,
        meta: Optional[dict] = None,
    ) -> dict:
        return {
            "success": True,
            "message": message,
            "data": data,
            "meta": meta,
        }

    @staticmethod
    def error(
        message: str,
        data: Optional[Any] = None,
    ) -> dict:
        return {
            "success": False,
            "message": message,
            "data": data,
        }
