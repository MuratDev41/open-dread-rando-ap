import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import sys
import os
import logging
import json
from pathlib import Path
from open_dread_rando import dread_patcher

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)
        self.text_widget.after(0, append)

class PatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Metroid Dread Randomizer Patcher")
        self.root.geometry("700x500")
        
        # Configure grid
        self.root.columnconfigure(1, weight=1)
        
        # Romfs path
        tk.Label(root, text="Base RomFS Directory:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.romfs_entry = tk.Entry(root)
        self.romfs_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(root, text="Browse...", command=self.browse_romfs).grid(row=0, column=2, padx=10, pady=10)
        
        # Config path
        tk.Label(root, text="Config JSON:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.config_entry = tk.Entry(root)
        self.config_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(root, text="Browse...", command=self.browse_config).grid(row=1, column=2, padx=10, pady=10)
        
        # Output path
        tk.Label(root, text="Output Directory:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.output_entry = tk.Entry(root)
        self.output_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(root, text="Browse...", command=self.browse_output).grid(row=2, column=2, padx=10, pady=10)
        
        # Patch button
        self.patch_btn = tk.Button(root, text="Run Patcher", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=self.start_patching)
        self.patch_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="ew")
        
        # Log area
        tk.Label(root, text="Log Output:").grid(row=4, column=0, padx=10, pady=(10,0), sticky="w")
        self.log_area = scrolledtext.ScrolledText(root, height=10, state='disabled')
        self.log_area.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.root.rowconfigure(5, weight=1)
        
        # Setup logging redirection
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = TextHandler(self.log_area)
        handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        self.logger.addHandler(handler)

    def browse_romfs(self):
        path = filedialog.askdirectory(title="Select Base RomFS Directory")
        if path:
            self.romfs_entry.delete(0, tk.END)
            self.romfs_entry.insert(0, path)

    def browse_config(self):
        path = filedialog.askopenfilename(title="Select Config JSON", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if path:
            self.config_entry.delete(0, tk.END)
            self.config_entry.insert(0, path)

    def browse_output(self):
        path = filedialog.askdirectory(title="Select Output Directory")
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def start_patching(self):
        romfs = self.romfs_entry.get()
        config = self.config_entry.get()
        output = self.output_entry.get()
        
        if not romfs or not config or not output:
            messagebox.showerror("Error", "Please fill in all paths.")
            return
            
        self.patch_btn.config(state='disabled')
        threading.Thread(target=self.run_patcher, args=(romfs, config, output), daemon=True).start()

    def run_patcher(self, romfs, config_path, output):
        try:
            with open(config_path, 'r') as f:
                configuration = json.load(f)
            
            dread_patcher.patch_extracted(
                Path(romfs),
                Path(output),
                configuration
            )
            
            messagebox.showinfo("Success", "Patching completed successfully!")
        except Exception as e:
            self.logger.exception("Patching failed")
            messagebox.showerror("Error", f"Patching failed: {str(e)}")
        finally:
            self.patch_btn.after(0, lambda: self.patch_btn.config(state='normal'))

if __name__ == "__main__":
    root = tk.Tk()
    PatcherGUI(root)
    root.mainloop()
