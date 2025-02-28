#!/usr/bin/env python3

import tkinter as tk
import subprocess
from pynput import keyboard
from pynput.keyboard import Controller, Key
import threading

clipboard_history = []
history_lock = threading.Lock()

last_text = None
last_image = None

# Cria a instância principal do Tkinter (oculta)
root = tk.Tk()
root.withdraw()

# Controller para simular o atalho de colagem (Ctrl+V)
keyboard_controller = Controller()

def simulate_paste():
    keyboard_controller.press(Key.ctrl)
    keyboard_controller.press('v')
    keyboard_controller.release('v')
    keyboard_controller.release(Key.ctrl)

def monitor_clipboard():
    global last_text, last_image
    try:
        content = root.clipboard_get()
        if content != last_text:
            last_text = content
            with history_lock:
                clipboard_history.append({"type": "text", "data": content})
    except tk.TclError:
        try:
            image_bytes = subprocess.check_output(
                ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
                stderr=subprocess.DEVNULL
            )
            if image_bytes != last_image:
                last_image = image_bytes
                with history_lock:
                    clipboard_history.append({"type": "image", "data": image_bytes})
        except subprocess.CalledProcessError:
            pass
    root.after(500, monitor_clipboard)

def show_clipboard_window():
    win = tk.Toplevel(root)
    win.title("Histórico do Clipboard")
    win.attributes("-topmost", True)
    win.focus_force()

    # Define o fundo preto para a janela
    win.configure(bg="black")

    # Fecha a janela ao perder o foco ou ao apertar Esc
    win.bind("<FocusOut>", lambda e: win.destroy())
    win.bind("<Escape>", lambda e: win.destroy())

    # Cria um Listbox com fundo preto, fonte branca e highlight claro
    listbox = tk.Listbox(
        win,
        width=50,
        height=10,
        bg="black",
        fg="white",
        selectbackground="light gray",
        selectforeground="black",
        relief="flat"
    )
    listbox.pack(fill=tk.BOTH, expand=True)

    with history_lock:
        items = list(clipboard_history)
    for item in reversed(items):
        if item["type"] == "text":
            display_text = item["data"][:50].replace('\n', ' ')
        else:
            display_text = "[Imagem]"
        listbox.insert(tk.END, display_text)

    def select_item(event=None):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            with history_lock:
                orig_index = len(clipboard_history) - 1 - index
                item = clipboard_history[orig_index]
            if item["type"] == "text":
                root.clipboard_clear()
                root.clipboard_append(item["data"])
            else:
                p = subprocess.Popen(
                    ["xclip", "-selection", "clipboard", "-t", "image/png", "-i"],
                    stdin=subprocess.PIPE
                )
                p.communicate(input=item["data"])
            win.destroy()
            # Após selecionar, simula o paste na aplicação ativa
            root.after(100, simulate_paste)

    listbox.bind("<Double-Button-1>", select_item)
    listbox.bind("<Return>", select_item)
    listbox.bind("<space>", select_item)
    listbox.focus_set()

    # Atualiza a geometria e posiciona a janela acima do cursor
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x, y = win.winfo_pointerxy()
    win.geometry(f"+{x}+{y - height}")

def on_activate():
    root.after(0, show_clipboard_window)

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse("<ctrl>+<alt>+v"), on_activate
)

def on_press(key):
    hotkey.press(key)

def on_release(key):
    hotkey.release(key)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

root.after(500, monitor_clipboard)
root.mainloop()
