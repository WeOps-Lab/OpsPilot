from langserve import CustomUserType
from pydantic.v1 import Field


class AzureOcrRequest(CustomUserType):
    azure_ocr_endpoint: str = Field(..., extra={"widget": {"type": "text"}})
    azure_ocr_key: str = Field(..., extra={"widget": {"type": "text"}})
    file: str = Field(..., extra={"widget": {"type": "base64file"}})
