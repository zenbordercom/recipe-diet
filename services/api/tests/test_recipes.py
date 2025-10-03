from fastapi.testclient import TestClient


def test_create_and_list_recipes(client: TestClient) -> None:
    payload = {
        "title": "Spicy Chickpea Stew",
        "summary": "A warming stew packed with protein and fiber.",
        "instructions": "Saute aromatics, simmer chickpeas, finish with greens.",
        "prep_time_minutes": 15,
        "cook_time_minutes": 30,
        "servings": 4,
        "ingredients": [
            {"name": "Chickpeas", "amount": "2 cups"},
            {"name": "Spinach", "amount": "2 cups"},
        ],
    }

    response = client.post("/api/v1/recipes/", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["slug"] == "spicy-chickpea-stew"
    assert len(created["ingredients"]) == 2
    assert {item["ingredient"]["name"] for item in created["ingredients"]} == {
        "Chickpeas",
        "Spinach",
    }

    list_response = client.get("/api/v1/recipes/")
    assert list_response.status_code == 200
    recipes = list_response.json()
    assert len(recipes) == 1
    assert recipes[0]["id"] == created["id"]


def test_update_recipe(client: TestClient) -> None:
    create_payload = {
        "title": "Quick Oats Bowl",
        "summary": "Breakfast ready in minutes.",
        "ingredients": [{"name": "Rolled oats", "amount": "1 cup"}],
    }

    create_response = client.post("/api/v1/recipes/", json=create_payload)
    recipe_id = create_response.json()["id"]

    update_payload = {
        "title": "Quick Oatmeal Bowl",
        "summary": "Breakfast ready in minutes.",
        "ingredients": [
            {"name": "Rolled oats", "amount": "1 cup"},
            {"name": "Banana", "amount": "1"},
        ],
    }

    update_response = client.put(f"/api/v1/recipes/{recipe_id}", json=update_payload)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["slug"] == "quick-oatmeal-bowl"
    assert len(updated["ingredients"]) == 2
    assert {item["ingredient"]["name"] for item in updated["ingredients"]} == {
        "Rolled oats",
        "Banana",
    }

    delete_response = client.delete(f"/api/v1/recipes/{recipe_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/recipes/{recipe_id}")
    assert get_response.status_code == 404
