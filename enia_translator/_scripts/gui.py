from argparse import Namespace
import asyncio
from contextlib import closing
import os.path as path
from threading import Thread
import tkinter as tk
import tkml

from enia_translator.multisearch import search as enia_search
from enia_translator.settings import load_settings

__all__ = ['entrypoint']


def entrypoint() -> None:
    root = tk.Tk()
    root.title('EN-IA Translator')
    app = GUIApplication(root)
    root.wm_attributes('-topmost', 1)
    root.focus_force()
    app.mainloop()


class GUIApplication:

    def __init__(self, master=None):
        tree_file = path.realpath(path.join(path.dirname(__file__),
                                  'gui.yaml'))
        master.bind('<Return>', lambda evt: self.search())
        self.words = tk.StringVar()
        with open(tree_file) as fp:
            tree = self.toplevel = tkml.load_fp(
                fp, master,
                context=Namespace(words=self.words, search=self.search)
            )
        self.result = tree.children['!frame2'].children['!scrolledtext']

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

    def mainloop(self) -> None:
        self.toplevel.mainloop()
