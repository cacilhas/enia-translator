import asyncio
from contextlib import closing
from functools import partial
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import tkml

from enia_translator import __AUTHOR__, __VERSION__
from enia_translator.multisearch import search as enia_search

__all__ = ['entrypoint']


def entrypoint() -> None:
    load = tkml.fixtures()
    title = 'EN-IA Translator {}'.format(__VERSION__)
    root = load('root.yaml')
    words = tk.StringVar()
    stext = None

    def add_cascade(widget: tk.Misc, menu: tk.Menu, label: str) -> None:
        widget.add_cascade(menu=menu, label=label)

    def search(evt=None) -> None:
        value = words.get()
        stext.delete('1.0', tk.END)
        def callback(result: str) -> None:
            stext.insert(tk.INSERT, result + '\n')

        def target() -> None:
            with closing(asyncio.new_event_loop()) as loop:
                enia_search(value, callback, loop=loop)

        thr = Thread(target=target)
        thr.deamon = True
        thr.start()

    def get_stext(widget: scrolledtext.ScrolledText) -> None:
        nonlocal stext
        stext = widget

    quit = lambda: root.quit()
    show_author = partial(messagebox.showinfo, 'Author', __AUTHOR__)

    win = load('main.yaml', root)
    win['menu'] = win.nametowidget('!menu')
    root.mainloop()


if __name__ == '__main__':
    entrypoint()
