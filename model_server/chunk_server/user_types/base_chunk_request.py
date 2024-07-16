from langserve import CustomUserType
from langchain.pydantic_v1 import Field


class BaseChunkRequest(CustomUserType):
    enable_recursive_chunk_parse: bool = Field(True)
    recursive_chunk_size: int = Field(128)
    recursive_chunk_overlap: int = Field(0)

    enable_semantic_chunck_parse: bool = Field(False)
    semantic_embedding_address: str = Field("http://fast-embed-server-zh.ops-pilot:8101")

    ocr_provider_address: str = Field("http://ocr-server.ops-pilot:8109")
    enable_ocr_parse: bool = Field(False)

    excel_header_row_parse: bool = Field(False)
    excel_full_content_parse: bool = Field(True)

    custom_metadata: dict = Field({})
