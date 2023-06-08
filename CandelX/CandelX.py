import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import random
from datetime import datetime, timedelta
import string
from PIL import Image, ImageTk

root = tk.Tk()
root.title("CandelX Text Editor")

icon_image = Image.open("icon.ico")
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

class TextEditor(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("CandelX Text Editor")
        self.create_widgets()

    def create_widgets(self):
        # Text area
        self.text = tk.Text(self.master, wrap="word", undo=True)
        self.text.grid(row=0, column=0, sticky="nsew")

        # Menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # File Menu
        file = tk.Menu(self.menu_bar, tearoff=False)
        file.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file.add_command(label="Save As", command=self.save_as, accelerator="Ctrl+S")
        file.add_separator()
        file.add_command(label="Clear", command=self.clear, accelerator="Ctrl+R")
        file.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file)

        # Edit menu
        edit = tk.Menu(self.menu_bar, tearoff=False)
        edit.add_command(label="Find", command=self.find_text)
        edit.add_command(label="Replace", command=self.replace_text)
        edit.add_separator()
        edit.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.menu_bar.add_cascade(label="Edit", menu=edit)

        # Generate Menu
        generate_menu = tk.Menu(self.menu_bar, tearoff=False)

        # Time Section
        time = tk.Menu(generate_menu, tearoff=False)
        time.add_command(label="Random Time", command=self.gen_time)
        time.add_command(label="Current Time", command=self.current_time)
        time.add_separator()
        time.add_command(label="Random Date", command=self.gen_date)
        time.add_command(label="Date In Range", command=self.date_range)
        time.add_command(label="Current Date", command=self.current_date)

        # Name Section
        name = tk.Menu(generate_menu, tearoff=False)
        name.add_command(label="First Name", command=self.first_name)
        name.add_command(label="Middle Name", command=self.middle_name)
        name.add_command(label="Last Name", command=self.last_name)
        name.add_command(label="Full Name", command=self.full_name)

        # Number Section
        number = tk.Menu(generate_menu, tearoff=False)
        number.add_command(label="Generate Number", command=self.gen_num)
        number.add_command(label="Number Range", command=self.num_range)

        # Task Section
        task = tk.Menu(generate_menu, tearoff=False)
        task.add_command(label="Cleaning Task", command=self.clean_task)
        task.add_command(label="Gaming Task", command=self.game_task)
        task.add_command(label="Vlog Task", command=self.vlog_task)
        task.add_command(label="Coding Task", command=self.code_task)

        generate_menu.add_cascade(label="Time", menu=time)
        generate_menu.add_cascade(label="Name", menu=name)
        generate_menu.add_cascade(label="Number", menu=number)
        generate_menu.add_cascade(label="Task", menu=number)

        self.menu_bar.add_cascade(label="Generate", menu=generate_menu)

        # Templates menu
        template_menu = tk.Menu(self.menu_bar, tearoff=False)

        # Backrooms Section
        backrooms = tk.Menu(template_menu, tearoff=False)
        backrooms.add_command(label="Object", command=lambda: self.load_template("info/temps/object.temp"))
        backrooms.add_command(label="Level", command=lambda: self.load_template("info/temps/level.temp"))
        backrooms.add_command(label="Entity", command=lambda: self.load_template("info/temps/entity.temp"))
        backrooms.add_command(label="Phenomena", command=lambda: self.load_template("info/temps/phenomena.temp"))
        backrooms.add_command(label="Group", command=lambda: self.load_template("info/temps/group.temp"))


        # Legal Section
        legal = tk.Menu(template_menu, tearoff=False)
        legal.add_command(label="Cleaning Services Agreement", command=lambda: self.load_template("info/temps/cleaning services agreement.temp"))
        legal.add_command(label="Website Privacy Policy", command=lambda: self.load_template("info/temps/website privacy policy.temp"))
        legal.add_command(label="Resume", command=lambda: self.load_template("info/temps/resume.temp"))
        legal.add_command(label="Contract", command=lambda: self.load_template("info/temps/contract.temp"))
        legal.add_command(label="NDA", command=lambda: self.load_template("info/temps/nda.temp"))
        legal.add_command(label="Employment Agreement", command=lambda: self.load_template("info/temps/empoyment agreement.temp"))

        # Misc. Menu
        misc = tk.Menu(template_menu, tearoff=False)
        misc.add_command(label="Shopping List", command=lambda: self.load_template("temps/shopping list.temp"))

        template_menu.add_cascade(label="Backrooms", menu=backrooms)
        template_menu.add_cascade(label="Legal", menu=legal)
        template_menu.add_cascade(label="Miscelanious", menu=misc)

        self.menu_bar.add_cascade(label="Templates", menu=template_menu)

    def clear(self):
        self.text.delete("1.0", "end")

    def current_time(self):
        current_time = datetime.now().strftime("%I:%M %p")
        self.text.insert("insert", current_time)

    def current_date(self):
        current_date = datetime.now().strftime("%B %d, %Y")
        self.text.insert("insert", current_date)

    def load_template(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf8") as file:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", file.read())
        else:
            messagebox.showerror("Error", "Template not found!")

    def open_file(self, event=None):
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, "r") as f:
                text = f.read()
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", text)
            self.filepath = filepath

    def save_file(self, event=None):
        if self.filepath:
            with open(self.filepath, "w") as f:
                text = self.text.get("1.0", tk.END)
                f.write(text)
        else:
            self.save_file_as()

    def save_as(self, event=None):
        filepath = filedialog.asksaveasfilename()
        if filepath:
            with open(filepath, "w") as f:
                text = self.text.get("1.0", tk.END)
                f.write(text)
                self.filepath = filepath

    def find_text(self):
        query = simpledialog.askstring("Find", "Enter text to find:")
        if query:
            idx = self.text.search(query, "1.0", tk.END)
            if idx:
                self.text.tag_remove("highlight", "1.0", tk.END)
                while idx:
                    end_idx = f"{idx}+{len(query)}c"
                    self.text.tag_add("highlight", idx, end_idx)
                    idx = self.text.search(query, end_idx, tk.END)

            self.text.tag_configure("highlight", background="yellow")

    def replace_text(self):
        query = simpledialog.askstring("Replace", "Enter text to replace:")
        if query:
            replace_with = simpledialog.askstring("Replace", "Replace with:")
            if replace_with:
                idx = self.text.search(query, "1.0", tk.END)
                if idx:
                    answer = messagebox.askyesno(
                        "Replace",
                        f"Replace '{query}' with '{replace_with}'?"
                    )
                    if answer:
                        while idx:
                            end_idx = f"{idx}+{len(query)}c"
                            self.text.delete(idx, end_idx)
                            self.text.insert(idx, replace_with)
                            idx = self.text.search(query, tk.END)

    def undo(self, event=None):
        self.text.edit_undo()

    def redo(self, event=None):
        self.text.edit_redo()

    def gen_date(self):
        start_date = simpledialog.askstring("Set Date Range", "Enter start date (MM/DD/YYYY):")
        end_date = simpledialog.askstring("Set Date Range", "Enter end date (MM/DD/YYYY):")
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.strptime(end_date, "%m/%d/%Y")
            delta = (end_date - start_date).days
            random_days = random.randint(0, delta)
            random_date = start_date + timedelta(days=random_days)
            random_date = max(random_date, start_date)
            random_date = min(random_date, end_date)

        if random_date < start_date or random_date > end_date:
            print(f"Generated date {random_date.strftime('%B %d, %Y')} is not within the given range.")
            self.generate_random_date()
        else:
            self.text.insert("insert", random_date.strftime("%B %d, %Y"))
            print(f"Generated date: {random_date.strftime('%B %d, %Y')}")

    def gen_time(self):
        random_time = f"{random.randint(1, 12):02d}:{random.randint(0, 59):02d}"
        self.text.insert("insert", random_time)

    def full_name(self):
        with open("info/generate/first.name", "r") as file:
            first_names = file.read().splitlines()
            first = random.choice(first_names)

        with open("info/generate/middle.name", "r") as file:
            middle_names = file.read().splitlines()
            middle = random.choice(middle_names)

        with open("info/generate/last.name", "r") as file:
            last_names = file.read().splitlines()
            last = random.choice(last_names)

        random_name = f"{first} {middle} {last}."
        self.text.insert("insert", random_name)

    def first_name(self):
        with open("info/generate/first.name", "r") as file:
            first_names = file.read().splitlines()
            first_name = random.choice(first_names)
            self.text.insert("insert", first_name)

    def middle_name(self):
        with open("generate/middle.name", "r") as file:
            middle_name = file.read().splitlines()
            middle_name = random.choice(middle_name)
            self.text.insert("insert", middle_name)

    def last_name(self):
        with open("info/generate/last.name", "r") as file:
            last_name = file.read().splitlines()
            last_name = random.choice(last_name)
            self.text.insert("insert", last_name)

    def code_task(self):
        with open("generate/coding.task", "r") as file:
            coding_task = file.read().splitlines()
            coding_task = random.choice(coding_task)
            self.text.insert("insert", coding_task)

    def vlog_task(self):
        with open("info/generate/vlog.task", "r") as file:
            coding_task = file.read().splitlines()
            coding_task = random.choice(coding_task)
            self.text.insert("insert", coding_task)

    def clean_task(self):
        with open("info/generate/cleaning.task", "r") as file:
            coding_task = file.read().splitlines()
            coding_task = random.choice(coding_task)
            self.text.insert("insert", coding_task)

    def game_task(self):
        with open("info/generate/gaming.task", "r") as file:
            coding_task = file.read().splitlines()
            coding_task = random.choice(coding_task)
            self.text.insert("insert", coding_task)

    def gen_num(self):
        random_num = random.randint
        self.text.insert(tk.INSERT, str(random_num))

    def num_range(self):
        mn = simpledialog.askinteger("Generate Number Range", "Enter minimum number:")
        mx = simpledialog.askinteger("Generate Number Range", "Enter maximum number:")
        if mn is not None and mx is not None and mn <= mx:
            random_num = random.randint(mn, mx)
            self.text.insert(tk.INSERT, str(random_num))
        else:
            messagebox.showerror("Error", "Invalid range supplied.")

    def date_range(self):
        start = simpledialog.askstring("Set Date Range", "Enter start date (MM/DD/YYYY):")
        if start:
            try:
                start = datetime.strptime(start, "%m/%d/%Y")
                end = simpledialog.askstring("Set Date Range", "Enter end date (MM/DD/YYYY):")
                if end:
                    end = datetime.strptime(end, "%m/%d/%Y")
                    if start > end:
                        raise ValueError("Start date must be earlier than end date")
                    delta = (end - start).days
                    random_days = random.randint(0, delta)
                    gen_date = end - timedelta(days=random_days)
                    self.text.insert("insert", gen_date.strftime("%B %d, %Y"))
                else:
                    messagebox.showerror("Error", "End date is required")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

# Create Window
editor = TextEditor(root)
editor.grid(row=0, column=0, sticky="nsew")

# Text Editor Screen
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Keyboard shortcuts
root.bind("<Control-o>", lambda event: editor.open_file())
root.bind("<Control-s>", lambda event: editor.save_file())
root.bind("<Control-S>", lambda event: editor.save_file_as())
root.bind("<Control-R>", lambda event: editor.clear())

root.update()
root.deiconify()
root.mainloop()
