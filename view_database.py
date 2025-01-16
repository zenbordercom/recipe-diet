import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("数据库查看器")
        self.root.geometry("600x400")
        
        self.create_widgets()
        
    def create_widgets(self):
        # 打开数据库按钮
        open_button = ttk.Button(self.root, text="打开数据库", command=self.open_database)
        open_button.pack(pady=10)
        
        # 数据库内容显示区
        self.text_area = tk.Text(self.root, wrap=tk.WORD, width=70, height=20)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
    def open_database(self):
        # 打开文件对话框选择数据库文件
        file_path = filedialog.askopenfilename(
            title="选择数据库文件",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.view_database(file_path)
    
    def view_database(self, db_path):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # 获取所有表名
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                self.text_area.delete(1.0, tk.END)
                for table_name in tables:
                    self.text_area.insert(tk.END, f"表: {table_name[0]}\n")
                    
                    # 获取表结构
                    cursor.execute(f"PRAGMA table_info({table_name[0]})")
                    columns = cursor.fetchall()
                    self.text_area.insert(tk.END, "结构:\n")
                    for col in columns:
                        self.text_area.insert(tk.END, f"  {col[1]} ({col[2]})\n")
                    
                    # 获取表数据
                    cursor.execute(f"SELECT * FROM {table_name[0]} LIMIT 50")
                    rows = cursor.fetchall()
                    self.text_area.insert(tk.END, "数据:\n")
                    for row in rows:
                        self.text_area.insert(tk.END, f"  {row}\n")
                    
                    self.text_area.insert(tk.END, "-" * 40 + "\n")
        
        except sqlite3.Error as e:
            messagebox.showerror("数据库错误", f"无法读取数据库: {e}")

def main():
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 