import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

from enia_translator import EniaWordSearcher
from enia_translator.settings import load_settings


def entrypoint() -> None:
    root = tk.Tk()
    root.title('EN-IA Translator')
    app = GUIApplication(root)
    app.pack()
    root.wm_attributes('-topmost', 1)
    root.focus_force()
    app.mainloop()


class GUIApplication(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        master.bind('<Return>', lambda evt: self.search())
        self.word = tk.StringVar()
        self.create_widgets()

    def create_widgets(self) -> None:
        fr_search = ttk.Frame(self)
        lb_main = ttk.Label(fr_search, text='Word to search:')
        tx_entry = ttk.Entry(fr_search, textvariable=self.word)
        bt_go = ttk.Button(self, text='Search', command=self.search)
        tx_show = self.result = ScrolledText(self, wrap=tk.WORD)

        tx_entry.bind('<Return>', lambda evt: self.search())

        lb_main.pack(anchor=tk.NW, side=tk.LEFT, expand=False)
        tx_entry.pack(anchor=tk.NE, side=tk.RIGHT, fill=tk.X, expand=True)
        fr_search.pack(anchor=tk.N, fill=tk.X, expand=True)
        bt_go.pack(anchor=tk.S, expand=True)
        tx_show.pack(anchor=tk.S, fill=tk.BOTH, expand=True)

        tx_entry.focus()

    def search(self) -> None:
        value = self.word.get()
        searcher = EniaWordSearcher(value, load_settings())
        result = '\n'.join(searcher.search(value))
        self.result.delete('1.0', tk.END)
        self.result.insert(tk.INSERT, result)
