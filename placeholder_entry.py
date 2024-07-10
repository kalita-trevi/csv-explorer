import ttkbootstrap as ttk

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', bootstyle=None, **kwargs):
        super().__init__(master, bootstyle=bootstyle, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, ttk.END)
            self['foreground'] = self.default_fg_color

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['foreground'] = self.placeholder_color
