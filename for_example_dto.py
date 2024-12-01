from pydantic import BaseModel, Field, ValidationError, validator

class ProfileDto(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool