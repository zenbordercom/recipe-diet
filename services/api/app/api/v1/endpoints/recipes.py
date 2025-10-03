from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.crud import recipe_crud
from app.schemas.recipe import RecipeCreate, RecipeReadWithIngredients, RecipeUpdate

router = APIRouter()


@router.get("/", response_model=list[RecipeReadWithIngredients])
def list_recipes(
    *,
    db: Annotated[Session, Depends(get_session)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[RecipeReadWithIngredients]:
    return recipe_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{recipe_id}", response_model=RecipeReadWithIngredients)
def get_recipe(*, db: Annotated[Session, Depends(get_session)], recipe_id: int) -> RecipeReadWithIngredients:
    recipe = recipe_crud.get(db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.post("/", response_model=RecipeReadWithIngredients, status_code=status.HTTP_201_CREATED)
def create_recipe(
    *, db: Annotated[Session, Depends(get_session)], recipe_in: RecipeCreate
) -> RecipeReadWithIngredients:
    return recipe_crud.create(db, obj_in=recipe_in)


@router.put("/{recipe_id}", response_model=RecipeReadWithIngredients)
def update_recipe(
    *,
    db: Annotated[Session, Depends(get_session)],
    recipe_id: int,
    recipe_in: RecipeUpdate,
) -> RecipeReadWithIngredients:
    db_recipe = recipe_crud.get(db, recipe_id=recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe_crud.update(db, db_obj=db_recipe, obj_in=recipe_in)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(*, db: Annotated[Session, Depends(get_session)], recipe_id: int) -> None:
    recipe_crud.remove(db, recipe_id=recipe_id)
