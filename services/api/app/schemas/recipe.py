from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.ingredient import IngredientRead


class RecipeIngredientCreate(BaseModel):
    ingredient_id: int | None = None
    name: str | None = Field(default=None, max_length=255)
    amount: str | None = Field(default=None, max_length=255)


class RecipeIngredientRead(BaseModel):
    ingredient_id: int
    amount: str | None = None
    ingredient: IngredientRead

    model_config = {"from_attributes": True}


class RecipeBase(BaseModel):
    title: str = Field(..., max_length=255)
    summary: str | None = Field(default=None, max_length=500)
    instructions: str | None = None
    prep_time_minutes: int | None = Field(default=None, ge=0)
    cook_time_minutes: int | None = Field(default=None, ge=0)
    servings: int | None = Field(default=None, ge=1)


class RecipeCreate(RecipeBase):
    ingredients: list[RecipeIngredientCreate] = Field(default_factory=list)


class RecipeUpdate(RecipeBase):
    ingredients: list[RecipeIngredientCreate] | None = None


class RecipeRead(RecipeBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RecipeReadWithIngredients(RecipeRead):
    ingredients: list[RecipeIngredientRead]
