import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import json
import os

def fetch_data():
    post_id = entry.get()
    if not post_id.isdigit():
        messagebox.showerror("Ошибка", "ID должен быть числом")
        return

    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        text.delete("1.0", tk.END)
        text.insert(tk.END, json.dumps(data, indent=4))
        status_label.config(text="Статус: Успешно")
    except Exception as e:
        status_label.config(text="Статус: Ошибка")
        messagebox.showerror("Ошибка запроса", str(e))

def save_data():
    content = text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Нет данных", "Сначала получите данные")
        return

    folder = filedialog.askdirectory(title="Выберите папку для сохранения")
    if folder:
        file_path = os.path.join(folder, f"post_{entry.get()}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Сохранено", f"Файл сохранён: {file_path}")

root = tk.Tk()
root.title("jsonplaceholder-gui-parser-and-json-saver")
root.geometry("500x400")

tk.Label(root, text="Введите ID(число от 1 до 100):").pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

tk.Button(root, text="Получить данные", command=fetch_data).pack(pady=5)

text = tk.Text(root, height=15, width=60)
text.pack(pady=5)

tk.Button(root, text="Сохранить в файл", command=save_data).pack(pady=5)

status_label = tk.Label(root, text="Статус: Ожидание")
status_label.pack(pady=5)

root.mainloop()
