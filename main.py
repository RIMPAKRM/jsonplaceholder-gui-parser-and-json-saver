import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import json
import os

class JsonPlaceholderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("jsonplaceholder-gui-parser-and-json-saver")
        self.root.geometry("500x400")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Введите ID (число от 1 до 100):").pack(pady=5)

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)

        tk.Button(self.root, text="Получить данные", command=self.fetch_data).pack(pady=5)

        self.text = tk.Text(self.root, height=15, width=60)
        self.text.pack(pady=5)

        tk.Button(self.root, text="Сохранить в файл", command=self.save_data).pack(pady=5)

        self.status_label = tk.Label(self.root, text="Статус: Ожидание")
        self.status_label.pack(pady=5)

    def fetch_data(self):
        post_id = self.entry.get()
        if not post_id.isdigit():
            messagebox.showerror("Ошибка", "ID должен быть числом")
            return

        url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, json.dumps(data, indent=4))
            self.status_label.config(text="Статус: Успешно")
        except Exception as e:
            self.status_label.config(text="Статус: Ошибка")
            messagebox.showerror("Ошибка запроса", str(e))

    def save_data(self):
        content = self.text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Нет данных", "Сначала получите данные")
            return

        folder = filedialog.askdirectory(title="Выберите папку для сохранения")
        if folder:
            file_path = os.path.join(folder, f"post_{self.entry.get()}.json")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Сохранено", f"Файл сохранён: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка сохранения", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonPlaceholderApp(root)
    root.mainloop()
