import psutil
import tkinter as tk
from tkinter import ttk, messagebox

# 获取指定端口的占用进程信息
def find_process_by_port(port):
    results = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr and conn.laddr.port == port:
            pid = conn.pid
            if pid:
                try:
                    p = psutil.Process(pid)
                    info = f"PID: {pid} | Name: {p.name()} | Status: {p.status()} | Cmdline: {' '.join(p.cmdline())}"
                    results.append((pid, info))
                except Exception:
                    results.append((pid, f"PID: {pid} | <Access Denied>"))
    return results

# 查询按钮点击事件
def on_search():
    port_input = port_entry.get()
    if not port_input.isdigit():
        messagebox.showerror("错误", "请输入合法的端口号")
        return

    port = int(port_input)
    result_list.delete(0, tk.END)

    results = find_process_by_port(port)
    if not results:
        result_list.insert(tk.END, f"端口 {port} 未被占用")
        return

    global current_results
    current_results = results
    for i, (_, info) in enumerate(results):
        result_list.insert(tk.END, f"{i+1}. {info}")

# 结束选中进程
def on_kill():
    if not current_results:
        messagebox.showwarning("提示", "没有可结束的进程")
        return

    selection = result_list.curselection()
    if not selection:
        messagebox.showwarning("提示", "请选中一个进程")
        return

    index = selection[0]
    pid, _ = current_results[index]

    try:
        p = psutil.Process(pid)
        p.terminate()
        messagebox.showinfo("成功", f"已结束 PID={pid} 的进程")
        on_search()
    except Exception as e:
        messagebox.showerror("错误", f"无法结束进程：{e}")

# 创建窗口
root = tk.Tk()
root.title("端口占用释放工具")
root.geometry("850x500")
root.configure(bg="#f2f2f2")  # 背景色

# 字体定义
font_title = ("微软雅黑", 16, "bold")
font_normal = ("微软雅黑", 12)

# 标题
title_label = tk.Label(root, text="端口占用查看与释放工具", font=font_title, bg="#f2f2f2", fg="#333")
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# 输入框
port_label = tk.Label(root, text="端口号：", font=font_normal, bg="#f2f2f2")
port_label.grid(row=1, column=0, padx=10, sticky="e")

port_entry = tk.Entry(root, font=font_normal, width=20)
port_entry.grid(row=1, column=1, padx=10, sticky="w")

search_btn = tk.Button(root, text="查询端口", font=font_normal, bg="#4CAF50", fg="white", command=on_search)
search_btn.grid(row=1, column=2, padx=10)

# 结果列表
result_frame = tk.Frame(root)
result_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=20)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_list = tk.Listbox(result_frame, width=110, height=15, font=("Consolas", 11))
result_list.pack(side=tk.LEFT, fill=tk.BOTH)
result_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_list.yview)

# 结束按钮
kill_btn = tk.Button(root, text="结束选中进程", font=font_normal, bg="#f44336", fg="white", command=on_kill)
kill_btn.grid(row=3, column=0, columnspan=3, pady=10)

# 全局变量
current_results = []

# 启动主循环
root.mainloop()
