import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("500x500")
root.title("DoS/DDoS Attack")

notebook = ttk.Notebook(root)
dosTab = ttk.Frame(notebook)
dosTab.columnconfigure(0, weight=0)
dosTab.columnconfigure(1, weight=1)
notebook.add(dosTab, text="DOS Attack")
notebook.pack(fill="both", expand=True)

target_label = tk.Label(dosTab, text="Target Ip")
target_inp = tk.Entry(dosTab, background="#333333")
target_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
target_inp.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
target_note = tk.Label(dosTab, text="Target machine's IP address or url")

port_label = tk.Label(dosTab, text="Port Number")
port_inp = tk.Entry(dosTab, background="#333333")
port_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
port_inp.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
 
root.mainloop()