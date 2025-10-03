"""Import SQLAlchemy models here for Alembic autogeneration and Base metadata."""

from app.db.base_class import Base  # noqa: F401
from app.models.ingredient import Ingredient, RecipeIngredient  # noqa: F401
from app.models.recipe import Recipe  # noqa: F401
