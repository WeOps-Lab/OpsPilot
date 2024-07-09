from langserve import CustomUserType


class DrainEntity(CustomUserType):
    cluster_id: int
    template: str
    size: int
