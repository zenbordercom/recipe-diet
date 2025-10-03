from typing import Iterable

from slugify import slugify


def generate_unique_slug(title: str, existing_slugs: Iterable[str] | None = None) -> str:
    base_slug = slugify(title)
    if not existing_slugs:
        return base_slug

    existing_set = set(existing_slugs)
    if base_slug not in existing_set:
        return base_slug

    counter = 2
    while f"{base_slug}-{counter}" in existing_set:
        counter += 1
    return f"{base_slug}-{counter}"
