import tkinter as tk
from tkinter import filedialog
import pandas as pd
import ttkbootstrap as ttk
from placeholder_entry import PlaceholderEntry


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")
        self.center_window(800, 600)

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.df = pd.DataFrame()  # Inicializa o DataFrame vazio

        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.load_button = ttk.Button(self.frame, text="Carregar Arquivo .CSV", command=self.load_csv, bootstyle="success")
        self.load_button.pack(side=tk.TOP, pady=10)

        self.filter_frame = ttk.Frame(self.frame)
        self.filter_frame.pack(side=tk.TOP, pady=5)

        self.filter_entry = PlaceholderEntry(self.filter_frame, placeholder="Clique aqui para pesquisar", width=40,
                                             bootstyle="success")
        self.filter_entry.pack(side=tk.LEFT, padx=5)

        self.filter_button = ttk.Button(self.filter_frame, text="Aplicar Filtro", command=self.apply_filter,
                                        bootstyle="success")
        self.filter_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.filter_frame, text="Limpar Filtro", command=self.clear_filter,
                                       bootstyle="success")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.display_data(self.df)

    def display_data(self, df):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        columns = list(df.columns)
        self.treeview = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)

        for index, row in df.iterrows():
            self.treeview.insert("", tk.END, values=list(row))

        self.treeview.pack(fill=tk.BOTH, expand=True)

    def apply_filter(self):
        value = self.filter_entry.get().lower()  # Convert to lowercase
        if value and value != "type here to search...":
            filtered_df = self.df[
                self.df.apply(lambda row: row.astype(str).str.lower().str.contains(value).any(), axis=1)]
            self.display_data(filtered_df)

    def clear_filter(self):
        self.filter_entry.delete(0, tk.END)
        self.filter_entry._add_placeholder()
        self.display_data(self.df)


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")  # Tema claro
    app = App(root)
    root.mainloop()
