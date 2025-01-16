import sqlite3
import os
import json

def load_recipes_to_database():
    try:
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, 'recipes.db')
        json_path = os.path.join(current_dir, 'recipes1219.json')
        
        print(f"当前目录: {current_dir}")
        print(f"数据库路径: {db_path}")
        print(f"JSON文件路径: {json_path}")
        
        # 首先删除现有的数据库文件（如果存在）
        if os.path.exists(db_path):
            os.remove(db_path)
            print("已删除旧的数据库文件")
        
        # 连接数据库
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # 创建表
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                main_ingredients TEXT NOT NULL,
                secondary_ingredients TEXT NOT NULL,
                nutrition TEXT NOT NULL,
                cooking_link TEXT
            )
            ''')
            
            # 从JSON文件加载数据
            print("\n开始加载JSON数据...")
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                recipes = json_data['recipes']
                print(f"从JSON文件读取到 {len(recipes)} 条数据")
                
                # 准备数据用于插入
                for recipe in recipes:
                    try:
                        cursor.execute('''
                        INSERT INTO recipes 
                        (name, category, main_ingredients, secondary_ingredients, nutrition, cooking_link)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            recipe['name'], 
                            recipe['category'], 
                            recipe['main_ingredients'],
                            recipe['secondary_ingredients'],
                            recipe['nutrition'],
                            recipe['cooking_link']
                        ))
                    except sqlite3.Error as e:
                        print(f"插入数据时出错 ({recipe['name']}): {e}")
                
                conn.commit()
            
            # 显示数据库统计信息
            cursor.execute("SELECT COUNT(*) FROM recipes")
            total_count = cursor.fetchone()[0]
            print(f"\n成功导入数据！数据库中共有 {total_count} 条菜品数据")
            
            # 显示所有数据类别统计
            cursor.execute("SELECT category, COUNT(*) FROM recipes GROUP BY category")
            categories = cursor.fetchall()
            print("\n各类别菜品数量：")
            for category, count in categories:
                print(f"{category}: {count}道菜")
            
            # 显示部分数据示例
            print("\n数据示例（前5条）：")
            cursor.execute("SELECT name, category, nutrition FROM recipes LIMIT 20")
            samples = cursor.fetchall()
            for sample in samples:
                print(f"菜名: {sample[0]}, 类别: {sample[1]}, 营养: {sample[2]}")
            
    except FileNotFoundError:
        print(f"错误：找不到JSON文件，请确保 {json_path} 文件存在")
    except json.JSONDecodeError as e:
        print(f"错误：JSON文件格式不正确: {e}")
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_recipes_to_database()