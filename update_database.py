import sqlite3
import json
import os

def update_database():
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, 'recipes.db')
        json_path = os.path.join(current_dir, 'recipes_data.json')
        
        # 连接数据库
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # 检查是否已存在cooking_link列
            cursor.execute("PRAGMA table_info(recipes)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'cooking_link' not in columns:
                # 添加cooking_link列
                cursor.execute("ALTER TABLE recipes ADD COLUMN cooking_link TEXT")
                print("成功添加cooking_link列")
                
            # 从JSON文件更新数据
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                recipes = data['recipes']
                
            # 更新现有记录的cooking_link
            for recipe in recipes:
                cursor.execute("""
                    UPDATE recipes 
                    SET cooking_link = ? 
                    WHERE name = ?
                """, (recipe['cooking_link'], recipe['name']))
            
            print("成功更新烹饪链接数据")
            conn.commit()

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
        print(f"当前目录: {current_dir}")
        print(f"尝试访问的JSON文件路径: {json_path}")
    except json.JSONDecodeError:
        print("JSON文件格式错误")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    update_database()
