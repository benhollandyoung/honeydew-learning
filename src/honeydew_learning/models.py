from pydantic import BaseModel, Field


class WindowInfo(BaseModel):
    id: int = Field(ge=0, le=2**32-1)
    application: str
    bundleID: str

