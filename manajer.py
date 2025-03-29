import os
import csv
import json
from tkinter import *
from tkinter import filedialog, messagebox

class SimpleDocApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Manager")
        self.root.geometry("600x400")
        
        # Data storage
        self.docs = []
        self.current_file = None
        
        # GUI Setup
        self.setup_ui()
        
        # Load existing data
        self.load_data()

    def setup_ui(self):
        # Main Frame
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Text Editor
        self.text_editor = Text(main_frame, wrap=WORD, font=('Arial', 12))
        self.text_editor.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        # Buttons Frame
        btn_frame = Frame(main_frame)
        btn_frame.pack(fill=X)
        
        Button(btn_frame, text="New", command=self.new_doc).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Open", command=self.open_file).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Save", command=self.save_file).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Export CSV", command=self.export_csv).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Export JSON", command=self.export_json).pack(side=RIGHT, padx=5)

    def new_doc(self):
        self.text_editor.delete(1.0, END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", ".txt"), ("CSV Files", ".csv"), ("All Files", ".")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    if file_path.endswith('.csv'):
                        reader = csv.reader(file)
                        content = "\n".join([",".join(row) for row in reader])
                    else:
                        content = file.read()
                
                self.text_editor.delete(1.0, END)
                self.text_editor.insert(END, content)
                self.current_file = file_path
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        content = self.text_editor.get(1.0, END)
        
        if self.current_file:
            try:
                with open(self.current_file, 'w') as file:
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", ".txt"), ("CSV Files", ".csv"), ("All Files", ".")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.text_editor.get(1.0, END))
                self.current_file = file_path
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def export_csv(self):
        content = self.text_editor.get(1.0, END).strip()
        lines = content.split("\n")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    for line in lines:
                        writer.writerow([line])
                messagebox.showinfo("Success", "CSV exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")

    def export_json(self):
        content = self.text_editor.get(1.0, END).strip()
        data = {
            "content": content,
            "metadata": {
                "lines": len(content.split("\n")),
                "chars": len(content)
            }
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                messagebox.showinfo("Success", "JSON exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export JSON: {str(e)}")

    def load_data(self):
        # Load from JSON if exists (optional)
        if os.path.exists("docs.json"):
            try:
                with open("docs.json", 'r') as file:
                    self.docs = json.load(file)
            except:
                pass

if __name__ == "__main__":
    root = Tk()
    app = SimpleDocApp(root)
    root.mainloop()