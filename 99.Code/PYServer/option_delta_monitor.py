# -*- coding: utf-8 -*-

import tkinter as tk
import option
from arbitrage._03.ui_tkinter import ui_tkinter

if __name__ == "__main__":
    root = tk.Tk()
    app = ui_tkinter(root, "sz159915", option.get_etf_option_expire_day()[0][0:4])
    root.mainloop()
