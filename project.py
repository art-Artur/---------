import tkinter as tk
import sqlite3
import random

class EcoTamagotchiDB:
    def __init__(self, db_file='eco_tamagotchi.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                task_points INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completed_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                FOREIGN KEY (task_id) REFERENCES tasks(task_id)
            )
        ''')

        self.conn.commit()

    def insert_task(self, task_name, task_points):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('INSERT INTO tasks (task_name, task_points) VALUES (?, ?)', (task_name, task_points))
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting task: {e}")
            return None

    def insert_completed_task(self, task_id):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('INSERT INTO completed_tasks (task_id) VALUES (?)', (task_id,))
        except sqlite3.Error as e:
            print(f"Error inserting completed task: {e}")

    def get_completed_tasks(self):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('''
                    SELECT tasks.task_name
                    FROM tasks
                    INNER JOIN completed_tasks ON tasks.task_id = completed_tasks.task_id
                ''')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving completed tasks: {e}")
            return []

    def close_connection(self):
        self.conn.close()

class EcoTamagotchiApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ЭкоТамагочи")
        self.master.geometry("400x400")
        self.master.configure(bg="#F7E8DA")

        self.db = EcoTamagotchiDB()

        self.pet_hunger = 0
        self.completed_tasks = 0

        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self.master, text="Прогресс: 0%", font=("Verdana", 12), bg="#F7E8DA")
        self.status_label.pack(pady=(10, 5))

        button_width = 50

        button_frame = tk.Frame(self.master, bg="#F7E8DA")
        button_frame.pack(pady=10)

        buttons = [
            ("Отсортировал отходы", 20),
            ("Использовал тканевую сумку, при покупке продуктов", 20),
            ("Отказался от одноразовых пластиковых изделий", 20),
            ("Сократил энергопотребление в течение дня", 20),
            ("День без автомобиля", 20)
        ]

        for button_text, points in buttons:
            button = tk.Button(button_frame, text=button_text, command=lambda p=points: self.perform_task(p),
                               width=button_width, bg="#E9BBB5", font=("Verdana", 10))
            button.pack(pady=5)

        self.canvas = tk.Canvas(self.master, bg="#F7E8DA", height=200, width=200)
        self.canvas.pack(pady=10)

        self.draw_tree()

    def draw_tree(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(90, 150, 110, 200, fill="#8E6A4B", outline="#000000", width=2)
        self.canvas.create_oval(70, 100, 130, 160, fill="#5F6F52", outline="#000000", width=2)

    def draw_circle_on_tree(self):
        x = 100 + random.randint(-20, 20)
        y = 120 + random.randint(-10, 10)
        self.canvas.create_oval(x, y, x + 10, y + 10, fill="#ff0000", outline="#000000", width=2)

    def perform_task(self, points):
        self.pet_hunger += points
        if self.pet_hunger >= 100:
            self.pet_hunger = 100
            text_window = tk.Toplevel()
            text_window.title("Уведомление")
            text_label = tk.Label(text_window, text="Поздравляю, Ты выполнил задачу на сегодня!")
            text_label.pack(padx=20, pady=20)

        task_id = self.db.insert_task("Task", points)  
        self.db.insert_completed_task(task_id)  

        self.completed_tasks += 1
        self.update_status()
        self.draw_circle_on_tree()

    def update_status(self):
        self.status_label.config(text=f"Прогресс: {self.pet_hunger}%\nВыполнено заданий: {self.completed_tasks}")

def main():
    root = tk.Tk()
    app = EcoTamagotchiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
