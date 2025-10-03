# nutrition_planner_gui.py
import tkinter as tk
from tkinter import ttk
import json
import sqlite3
from datetime import datetime, timedelta
import webbrowser
import os  # 导入 os 模块以处理文件路径

class NutritionPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("营养搭配计划器")
        self.root.geometry("800x600")
        
        # 设置数据库路径
        self.db_path = os.path.join(os.path.dirname(__file__), 'recipes.db')  # 修改为正确的数据库路径
        print(f"Using database at: {self.db_path}")  # 打印数据库路径以确认
        
        # 从数据库中获取所有可能的营养成分
        self.nutrition_elements = self.get_all_nutrition_elements()
        
        self.create_widgets()
        
    def get_all_nutrition_elements(self):
        # 连接数据库并获取所有独特的营养成分
        nutrition_set = set()
        try:
            with sqlite3.connect(self.db_path) as conn:  # 使用正确的数据库路径
                cursor = conn.cursor()
                cursor.execute("SELECT nutrition FROM recipes")
                for row in cursor.fetchall():
                    elements = row[0].split(',')
                    nutrition_set.update(elements)
        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
        return sorted(list(nutrition_set))
        
    def create_widgets(self):
        # 创建左右分栏
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧：营养成分选择区和结果显示区
        self.create_left_panel(left_frame)
        
        # 右侧：菜品详情显示区
        self.create_right_panel(right_frame)
        
    def create_left_panel(self, frame):
        # 营养成分选择区
        ttk.Label(frame, text="请选择所需营养成分：").pack(anchor=tk.W)
        
        # 创建一个Frame来容纳Checkbuttons
        self.checkbox_frame = ttk.Frame(frame)
        self.checkbox_frame.pack(fill=tk.X, pady=5)
        
        # 创建营养成分的Checkbuttons
        self.nutrition_vars = {}
        row = 0
        col = 0
        buttons_per_row = 4  # 每行显示的按钮数量
        
        for element in self.nutrition_elements:
            var = tk.BooleanVar()
            self.nutrition_vars[element] = var
            ttk.Checkbutton(self.checkbox_frame, text=element, variable=var).grid(
                row=row, column=col, sticky=tk.W, padx=5, pady=2
            )
            
            col += 1
            if col >= buttons_per_row:  # 当达到每行最大数量时换行
                col = 0
                row += 1
        
        # 生成按钮
        ttk.Button(frame, text="生成食谱", command=self.generate_meal_plan).pack(pady=20)
        
        # 结果显示区
        ttk.Label(frame, text="每周食谱安排：").pack(anchor=tk.W)
        self.result_text = tk.Text(frame, wrap=tk.WORD, width=40, height=30)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.tag_configure("clickable", foreground="blue", underline=1)
        self.result_text.tag_bind("clickable", "<Button-1>", self.show_recipe_details)

    def create_right_panel(self, frame):
        ttk.Label(frame, text="菜品详细信息：").pack(anchor=tk.W)
        self.detail_text = tk.Text(frame, wrap=tk.WORD, width=40, height=30)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        # 配置链接样式
        self.detail_text.tag_configure("link", foreground="blue", underline=1)
        self.detail_text.tag_bind("link", "<Button-1>", self.open_link)
        self.detail_text.tag_bind("link", "<Enter>", lambda e: self.detail_text.config(cursor="hand2"))
        self.detail_text.tag_bind("link", "<Leave>", lambda e: self.detail_text.config(cursor=""))

    def open_link(self, event):
        # 获取点击位置的文本
        index = self.detail_text.index(f"@{event.x},{event.y}")
        # 获取链接文本
        url = self.detail_text.get(f"{index} linestart", f"{index} lineend").split("：")[-1].strip()
        # 打开链接
        webbrowser.open(url)

    def generate_meal_plan(self):
        # 获取选中的营养成分
        selected_nutrition = [
            element for element, var in self.nutrition_vars.items() 
            if var.get()
        ]
        
        if not selected_nutrition:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "请至少选择一个营养成分！")
            return
            
        # 生成一周的饮食计划
        meal_plan = self.create_weekly_plan(selected_nutrition)
        
        # 显示结果
        self.display_meal_plan(meal_plan)
        
    def create_weekly_plan(self, selected_nutrition):
        weekly_plan = {}
        days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        meals = ['早餐', '午餐', '晚餐']
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for day in days:
                    daily_meals = {}
                    for meal in meals:
                        # 根据选择的营养成分查询合适的菜品
                        nutrition_condition = " OR ".join(
                            [f"nutrition LIKE '%{n}%'" for n in selected_nutrition]
                        )
                        cursor.execute(f"""
                            SELECT name FROM recipes 
                            WHERE {nutrition_condition}
                            ORDER BY RANDOM() 
                            LIMIT 2
                        """)
                        dishes = [row[0] for row in cursor.fetchall()]
                        daily_meals[meal] = dishes
                    
                    weekly_plan[day] = daily_meals
                    
        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            
        return weekly_plan
        
    def display_meal_plan(self, meal_plan):
        self.result_text.delete(1.0, tk.END)
        
        for day, meals in meal_plan.items():
            self.result_text.insert(tk.END, f"\n{day}:\n")
            for meal_time, dishes in meals.items():
                self.result_text.insert(tk.END, f"{meal_time}: ")
                for i, dish in enumerate(dishes):
                    self.result_text.insert(tk.END, dish, "clickable")
                    if i < len(dishes) - 1:
                        self.result_text.insert(tk.END, ", ")
                self.result_text.insert(tk.END, "\n")
            self.result_text.insert(tk.END, "-" * 40 + "\n")

    def show_recipe_details(self, event):
        # 获取点击的菜品名称
        index = self.result_text.index(f"@{event.x},{event.y}")
        clicked_pos = f"{index} wordstart"
        word_end = f"{index} wordend"
        dish_name = self.result_text.get(clicked_pos, word_end).strip()
        
        # 显示菜品详情
        self.display_recipe_details(dish_name)

    def display_recipe_details(self, dish_name):
        self.detail_text.delete(1.0, tk.END)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, category, main_ingredients, secondary_ingredients, nutrition, cooking_link
                    FROM recipes WHERE name = ?
                """, (dish_name,))
                recipe = cursor.fetchone()
                
                if recipe:
                    self.detail_text.insert(tk.END, f"【{recipe[0]}】\n\n")
                    self.detail_text.insert(tk.END, f"分类：{recipe[1]}\n\n")
                    self.detail_text.insert(tk.END, f"主料：\n{recipe[2]}\n\n")
                    self.detail_text.insert(tk.END, f"辅料：\n{recipe[3]}\n\n")
                    self.detail_text.insert(tk.END, f"营养成分：\n{recipe[4]}\n\n")
                    cooking_links = recipe[5]
                    if cooking_links:
                        links = [link.strip() for link in cooking_links.split("|")]
                        valid_links = [link for link in links if link]
                        if valid_links:
                            self.detail_text.insert(tk.END, f"烹饪链接：\n")
                            for link in valid_links:
                                self.detail_text.insert(tk.END, f"{link}\n", "link")
                else:
                    self.detail_text.insert(tk.END, f"未找到 {dish_name} 的详细信息")
        except sqlite3.Error as e:
            self.detail_text.insert(tk.END, f"数据库错误: {e}")

def main():
    root = tk.Tk()
    app = NutritionPlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()