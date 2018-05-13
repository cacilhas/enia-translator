from argparse import Namespace
import asyncio
from contextlib import closing
import os.path as path
from threading import Thread
import tkinter as tk
from tkinter import messagebox
import tkml
from typing import Tuple
from .. import __AUTHOR__, __VERSION__

from enia_translator.multisearch import search as enia_search
from enia_translator.settings import load_settings

__all__ = ['entrypoint']


def entrypoint() -> None:
    root = create_root()
    win, menubar = create_toplevel(root)
    build_menus(menubar)
    app = GUIApplication(win)
    win.wm_attributes('-topmost', 1)
    win.focus_force()
    app.mainloop()


def create_root() -> tk.Tk:
    root = tk.Tk(className='EniaTransaltor')
    root.title('EN-IA Translator {}'.format(__VERSION__))
    root.option_add('*tearOff', False)
    root.withdraw()
    return root


def create_toplevel(root: tk.Tk) -> Tuple[tk.Toplevel, tk.Menu]:
    win = tk.Toplevel(root) #, class_='EniaTransaltor')
    win.protocol('WM_DELETE_WINDOW', root.quit)
    menubar = tk.Menu(win)
    win['menu'] = menubar
    return win, menubar


def build_menus(menubar: tk.Menu) -> None:
    win = menubar.master
    main_menu = tk.Menu(menubar)
    main_menu.add_command(label='Quit', command=win.master.quit)

    help_menu = tk.Menu(menubar)
    help_menu.add_command(
        label='Author',
        command=lambda: messagebox.showinfo('Author', __AUTHOR__),
    )

    menubar.add_cascade(menu=main_menu, label=win.title())
    menubar.add_cascade(menu=help_menu, label='Help')


class GUIApplication:

    __slots__ = ('result', 'toplevel', 'words')

    def __init__(self, master=None):
        tree_file = path.realpath(path.join(path.dirname(__file__),
                                  'gui.yaml'))
        master.bind('<Return>', lambda evt: self.search())
        self.words = tk.StringVar()
        self.result = None

        with open(tree_file) as fp:
            self.toplevel = tkml.load_fp(
                fp, master,
                context=Namespace(
                    words=self.words,
                    search=self.search,
                    set_text=lambda widget: setattr(self, 'result', widget),
                )
            )
        assert self.result

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
