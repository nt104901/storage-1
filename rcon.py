import tkinter as tk
from tkinter import filedialog, messagebox
from mcrcon import MCRcon

def send_commands():
    try:
        ip_port = entry_ip.get()
        password = entry_password.get()

        if ":" not in ip_port:
            messagebox.showerror("Ошибка", "IP должен быть в формате IP:PORT")
            return

        ip, port = ip_port.split(":")
        port = int(port)

        commands = text_commands.get("1.0", tk.END).strip().split("\n")

        with MCRcon(ip, password, port=port) as mcr:
            for cmd in commands:
                if cmd.strip():
                    mcr.command(cmd)

        messagebox.showinfo("Готово", "Команды отправлены")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def save_commands():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_commands.get("1.0", tk.END))
        messagebox.showinfo("Сохранено", "Файл сохранён")


# --- GUI ---
root = tk.Tk()
root.title("Minecraft RCON Sender")
root.geometry("600x500")

tk.Label(root, text="IP:PORT сервера").pack()
entry_ip = tk.Entry(root, width=40)
entry_ip.pack()

tk.Label(root, text="RCON пароль").pack()
entry_password = tk.Entry(root, width=40, show="*")
entry_password.pack()

tk.Label(root, text="Команды (каждая с новой строки)").pack()
text_commands = tk.Text(root, height=15)
text_commands.pack(fill="both", expand=True)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="SEND", width=15, command=send_commands).pack(side="left", padx=5)
tk.Button(frame_buttons, text="SAVE", width=15, command=save_commands).pack(side="left", padx=5)

root.mainloop()
