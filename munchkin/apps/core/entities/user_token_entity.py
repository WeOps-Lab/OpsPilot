from typing import Optional

from pydantic import BaseModel, Field


class UserTokenEntity(BaseModel):
    token: Optional[str] = Field(None, description='用户令牌')
    error_message: Optional[str] = Field(None, description='认证失败信息')
    success: bool = Field(description='是否成功认证')
