from __future__ import annotations

from typing import Iterable

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.utils import generate_unique_slug
from app.models import Ingredient, Recipe, RecipeIngredient
from app.schemas.recipe import RecipeCreate, RecipeIngredientCreate, RecipeUpdate


class CRUDRecipe:
    def get(self, db: Session, recipe_id: int) -> Recipe | None:
        return db.scalar(
            select(Recipe)
            .where(Recipe.id == recipe_id)
            .options(
                selectinload(Recipe.ingredient_links).selectinload(RecipeIngredient.ingredient)
            )
        )

    def get_by_slug(self, db: Session, slug: str) -> Recipe | None:
        return db.scalar(
            select(Recipe)
            .where(Recipe.slug == slug)
            .options(
                selectinload(Recipe.ingredient_links).selectinload(RecipeIngredient.ingredient)
            )
        )

    def get_multi(self, db: Session, skip: int = 0, limit: int = 20) -> list[Recipe]:
        statement = (
            select(Recipe)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(Recipe.ingredient_links).selectinload(RecipeIngredient.ingredient)
            )
            .order_by(Recipe.created_at.desc())
        )
        return list(db.scalars(statement))

    def create(self, db: Session, obj_in: RecipeCreate) -> Recipe:
        slug = self._build_unique_slug(db, obj_in.title)
        recipe = Recipe(
            title=obj_in.title,
            slug=slug,
            summary=obj_in.summary,
            instructions=obj_in.instructions,
            prep_time_minutes=obj_in.prep_time_minutes,
            cook_time_minutes=obj_in.cook_time_minutes,
            servings=obj_in.servings,
        )
        db.add(recipe)
        db.flush()
        recipe.ingredient_links = self._build_ingredient_links(db, recipe, obj_in.ingredients)
        db.commit()
        return self.get(db, recipe.id)

    def update(self, db: Session, db_obj: Recipe, obj_in: RecipeUpdate) -> Recipe:
        data = obj_in.model_dump(exclude_unset=True, exclude={"ingredients"})
        new_title = data.pop("title", None)

        for field, value in data.items():
            setattr(db_obj, field, value)

        if new_title is not None and new_title != db_obj.title:
            db_obj.title = new_title
            db_obj.slug = self._build_unique_slug(db, new_title, exclude_id=db_obj.id)

        if obj_in.ingredients is not None:
            db_obj.ingredient_links.clear()
            db.flush()
            db_obj.ingredient_links.extend(self._build_ingredient_links(db, db_obj, obj_in.ingredients))

        db.add(db_obj)
        db.commit()
        return self.get(db, db_obj.id)

    def remove(self, db: Session, recipe_id: int) -> Recipe:
        recipe = self.get(db, recipe_id)
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        db.delete(recipe)
        db.commit()
        return recipe

    def _build_unique_slug(self, db: Session, title: str, *, exclude_id: int | None = None) -> str:
        base = generate_unique_slug(title)
        slug = base
        counter = 2
        while self._slug_exists(db, slug, exclude_id=exclude_id):
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    def _slug_exists(self, db: Session, slug: str, *, exclude_id: int | None) -> bool:
        query = select(func.count()).select_from(Recipe).where(Recipe.slug == slug)
        if exclude_id is not None:
            query = query.where(Recipe.id != exclude_id)
        return db.scalar(query) > 0

    def _build_ingredient_links(
        self,
        db: Session,
        recipe: Recipe,
        ingredients: Iterable[RecipeIngredientCreate],
    ) -> list[RecipeIngredient]:
        links: list[RecipeIngredient] = []
        for payload in ingredients:
            ingredient = self._resolve_ingredient(db, payload)
            links.append(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    amount=payload.amount,
                    ingredient=ingredient,
                )
            )
        return links

    def _resolve_ingredient(self, db: Session, payload: RecipeIngredientCreate) -> Ingredient:
        if payload.ingredient_id is not None:
            ingredient = db.get(Ingredient, payload.ingredient_id)
            if ingredient is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
            return ingredient

        if payload.name:
            normalized = payload.name.strip().lower()
            ingredient = db.scalar(
                select(Ingredient).where(func.lower(Ingredient.name) == normalized)
            )
            if ingredient:
                return ingredient
            ingredient = Ingredient(name=payload.name.strip())
            db.add(ingredient)
            db.flush()
            return ingredient

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ingredient requires either an id or a name",
        )
recipe = CRUDRecipe()
