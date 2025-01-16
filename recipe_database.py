import sqlite3
import json

def create_recipe_database():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # 创建菜谱表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        main_ingredients TEXT NOT NULL,
        secondary_ingredients TEXT NOT NULL,
        nutrition TEXT NOT NULL,
        cooking_link TEXT
    )
    ''')
    
    # 示例菜谱数据
    recipes_data = [
        {
            "name": "红烧肉",
            "category": "荤菜",
            "main_ingredients": "五花肉",
            "secondary_ingredients": "葱姜蒜,八角,桂皮",
            "nutrition": "蛋白质,脂肪,铁",
            "cooking_link": "https://www.xiachufang.com/recipe/100395789/"
        },
        {
            "name": "番茄炒蛋",
            "category": "素菜",
            "main_ingredients": "番茄,鸡蛋",
            "secondary_ingredients": "葱花,盐",
            "nutrition": "维生素C,蛋白质,胡萝卜素",
            "cooking_link": "https://www.xiachufang.com/recipe/100395527/"
        },
        # ... 后续可以添加更多菜谱
    ]
    
    # 插入数据
    for recipe in recipes_data:
        cursor.execute('''
        INSERT INTO recipes (name, category, main_ingredients, secondary_ingredients, nutrition, cooking_link)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (recipe['name'], recipe['category'], recipe['main_ingredients'], 
              recipe['secondary_ingredients'], recipe['nutrition'], recipe['cooking_link']))
    
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def search_recipe_by_name(name):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes WHERE name LIKE ?', ('%' + name + '%',))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def search_recipe_by_category(category):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes WHERE category = ?', (category,))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

if __name__ == '__main__':
    create_recipe_database()
