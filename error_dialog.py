# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import Tkinter as tk

class Error:
    def __init__(self, parent, text):
        top = self.top = tk.Toplevel(parent)
        top.title('Error')
        search_lab = tk.Label(top, text=text).grid(row=0, column=0)
        sc_button = tk.Button(top, text="OK", command=self.ok).grid(row=1, column=0)

    def ok(self):
        self.top.destroy()

    @classmethod
    def dialogError(cls, err, root):
        d = Error(root, err)
        root.wait_window(d.top)