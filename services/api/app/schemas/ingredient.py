from datetime import datetime

from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = Field(default=None, max_length=500)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    description: str | None = Field(default=None, max_length=500)


class Ingredient(IngredientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IngredientRead(Ingredient):
    pass
