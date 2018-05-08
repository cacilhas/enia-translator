import asyncio
from contextlib import closing
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

from enia_translator.multisearch import search as enia_search
from enia_translator.settings import load_settings


def entrypoint() -> None:
    root = tk.Tk()
    root.title('EN-IA Translator')
    app = GUIApplication(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.wm_attributes('-topmost', 1)
    root.focus_force()
    app.mainloop()


class GUIApplication(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        master.bind('<Return>', lambda evt: self.search())
        self.words = tk.StringVar()
        self.create_widgets()

    def create_widgets(self) -> None:
        fr_search = ttk.Frame(self)
        lb_main = ttk.Label(fr_search, text='Word to search:')
        tx_entry = ttk.Entry(fr_search, textvariable=self.words)
        bt_go = ttk.Button(self, text='Search', command=self.search)
        tx_show = self.result = ScrolledText(self, wrap=tk.WORD)

        lb_main.pack(anchor=tk.NW, side=tk.LEFT, expand=False)
        tx_entry.pack(anchor=tk.NE, side=tk.RIGHT, fill=tk.X, expand=True)
        fr_search.pack(anchor=tk.N, fill=tk.X, expand=True)
        bt_go.pack(anchor=tk.S, expand=False)
        tx_show.pack(anchor=tk.S, fill=tk.BOTH, expand=True)

        tx_entry.focus()

    def search(self) -> None:
        value = self.words.get()
        self.result.delete('1.0', tk.END)
        def callback(result: str) -> None:
            self.result.insert(tk.INSERT, result + '\n')

        def target() -> None:
            with closing(asyncio.new_event_loop()) as loop:
                enia_search(value, callback, loop=loop)

        thr = Thread(target=target)
        thr.deamon = True
        thr.start()
