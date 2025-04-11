from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TraceMetadata(BaseModel):
    use_case: str
    resource_id: str
    workflow_step: str
    model_version: str
    prompt_version: str

    class Config:
        from_attributes = True


class TraceBase(BaseModel):
    prompt: str
    generation: str
    trace_metadata: TraceMetadata


class TraceCreate(TraceBase):
    user: UserCreate
    ai_model_config: "AIModelConfigCreate"


class TraceResponse(TraceBase):
    id: int
    created_at: datetime
    user: UserResponse
    ai_model_config: "AIModelConfigResponse"

    class Config:
        from_attributes = True


class AIModelConfigBase(BaseModel):
    name: str
    temperature: float


class AIModelConfigCreate(AIModelConfigBase):
    pass


class AIModelConfigResponse(AIModelConfigBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
