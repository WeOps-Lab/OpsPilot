from user_types.base_chunk_request import BaseChunkRequest


class WebPageChunkRequest(BaseChunkRequest):
    url: str
    max_depth: int = 1
