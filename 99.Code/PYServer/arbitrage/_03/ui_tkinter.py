# -*- coding: utf-8 -*-

from datetime import datetime
import tkinter as tk
from tkinter import ttk
from dal import mssql
import arbitrage._03

class ui_tkinter:
    def __init__(self, root, underlying: str, expire_month: str):
        self.underlying = underlying
        self.expire_month = expire_month
        self.root = root
        self.root.title("持仓delta工具")
        
        # 创建带滚动条的表格框架
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 创建表格视图
        columns = {
            "c_code": ("c_code", 80),
            "c_delta": ("c_delta", 60),
            "c_sell": ("c卖", 50),
            "c_position": ("c持仓", 40),
            "c_buy": ("c买", 50),
            "c_main": ("主", 30),
            "strike_price": ("行权价", 50),
            "p_main": ("主", 30),
            "p_buy": ("p买", 50),
            "p_position": ("p持仓", 40),
            "p_sell": ("p卖", 50),
            "p_delta": ("p_delta", 60),
            "p_code": ("p_code", 80),
        }

        self.tree = ttk.Treeview(self.frame, columns=list(columns.keys()), show="headings")
        for key in columns.keys():
            # 设置列名
            self.tree.heading(key, text=columns[key][0])
            # 设置列宽
            self.tree.column(key, width=columns[key][1], anchor="center")

        # 添加垂直滚动条
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set, selectmode="none")
        
        # 布局组件
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        
        # 设置容器网格布局权重
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # 绑定按钮点击事件（通过事件代理）
        self.tree.bind("<Button-1>", self.on_button_click)



        # 底部固定高度容器
        self.bottom_container = ttk.Frame(root, height=100)
        self.bottom_container.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建文本框及滚动条
        self.text_box = tk.Text(self.bottom_container, wrap=tk.WORD)
        self.bottom_scroll = ttk.Scrollbar(self.bottom_container, orient="vertical", command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=self.bottom_scroll.set)
        
        # 布局文本框组件
        self.bottom_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 强制设置容器高度
        self.bottom_container.pack_propagate(False)



        # 启动定时刷新
        self.schedule_refresh()

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.option_t = arbitrage._03.cal(self.underlying, self.expire_month, self.option_price)
        delta = 0
        for t in self.option_t:
            c_delta = round(t["c_delta"] * 10000)
            p_delta = round(t["p_delta"] * 10000)
            c_lot = (t["cLot"] if t["cLot"] else 0) + (t["cLotTemp"] if t["cLotTemp"] else 0)            
            p_lot = (t["pLot"] if t["pLot"] else 0) + (t["pLotTemp"] if t["pLotTemp"] else 0)
            if c_lot:
                delta += c_delta * c_lot
            if p_lot:
                delta += p_delta * p_lot
            self.tree.insert("", "end", values=(
                t["cCode"],
                c_delta,
                f"【-1】",
                c_lot if c_lot else "",
                f"【+1】",
                t["main"],
                t["strike_price"],
                t["main"],
                f"【+1】",
                p_lot if p_lot else "",
                f"【-1】",
                p_delta,
                t["pCode"]
            ))
        
        self.text_box.delete("1.0", tk.END)
        content = f"组合delta:{delta}"
        self.text_box.insert(tk.END, content)

    def schedule_refresh(self):
        """定时刷新机制"""
        self.option_price = arbitrage._03.get_option_price(self.underlying, self.expire_month)
        self.refresh_data()
        self.root.after(30000, self.schedule_refresh)  # 30秒刷新

    def on_button_click(self, event):
        """处理按钮点击事件"""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            row = self.tree.identify_row(event.y)
            values = self.tree.item(row, "values")
            mid_col_index = int(len(values) / 2)
            strike_price = values[mid_col_index]
            if column == f"#{mid_col_index - 3}":
                self.show_details(values[0], -1)
            elif column == f"#{mid_col_index - 1}":
                self.show_details(values[0], 1)
            elif column == f"#{mid_col_index + 3}":
                self.show_details(values[-1], 1)
            elif column == f"#{mid_col_index + 5}":
                self.show_details(values[-1], -1)

    def show_details(self, code, change):
        sql = ["EXEC P_INSERT_OPTION_DELIVERY_TEMP @time=NULL,@code='%s',@market=NULL,@opname=NULL,@premium=NULL,@lot=%s,@fee=NULL"
            % (code, change)]
        mssql.run(sql)
        
        self.refresh_data()
