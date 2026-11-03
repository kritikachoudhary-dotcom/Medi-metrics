
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from analysis import (
    clean_data,
    calculate_statistics,
    calculate_correlation
)


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("MediMetrics - Health Data Analysis and Visualization System")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg="#F0F7F2")


# ---------------- COLORS ----------------

GREEN = "#176B45"
LIGHT_GREEN = "#DFF3E5"
WHITE = "#FFFFFF"
BG = "#F0F7F2"
DARK = "#263D32"
ACCENT = "#2E8B57"


# ---------------- DATA ----------------

data = clean_data(pd.read_csv("health_data.csv"))


# ---------------- STYLE ----------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=DARK,
    rowheight=30,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=GREEN,
    foreground=WHITE,
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", LIGHT_GREEN)],
    foreground=[("selected", DARK)]
)


# ---------------- MAIN LAYOUT ----------------

sidebar = tk.Frame(root, bg=GREEN, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(root, bg=BG)
content.pack(side="right", fill="both", expand=True)


# ---------------- COMMON FUNCTIONS ----------------

def clear_content():

    for widget in content.winfo_children():
        widget.destroy()


def create_heading(title):

    tk.Label(
        content,
        text=title,
        font=("Arial", 23, "bold"),
        bg=BG,
        fg=GREEN
    ).pack(anchor="w", padx=25, pady=20)


def show_page(page):

    clear_content()

    if page == "Home":
        show_home()

    elif page == "Patient Records":
        show_records()

    elif page == "Data Visualization":
        show_visualization()

    elif page == "Health Analysis":
        show_analysis()

    elif page == "Upload Dataset":
        show_upload()


def show_chart(fig):

    canvas = FigureCanvasTkAgg(fig, master=content)

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


# ---------------- 1. HOME ----------------

def show_home():

    create_heading("Health Data Dashboard")

    stats = calculate_statistics(data)

    cards = tk.Frame(content, bg=BG)
    cards.pack(fill="x", padx=20, pady=15)

    values = [
        ("Total Patients", stats["Total Patients"]),
        ("Average Age", f'{stats["Average Age"]:.1f}'),
        ("Average BP", f'{stats["Average BP"]:.1f}'),
        ("Average Cholesterol",
         f'{stats["Average Cholesterol"]:.1f}')
    ]

    for title, value in values:

        card = tk.Frame(
            cards,
            bg=WHITE,
            padx=15,
            pady=20,
            highlightbackground=LIGHT_GREEN,
            highlightthickness=1
        )

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=7
        )

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=DARK,
            font=("Arial", 11)
        ).pack()

        tk.Label(
            card,
            text=str(value),
            bg=WHITE,
            fg=GREEN,
            font=("Arial", 23, "bold")
        ).pack(pady=10)

    tk.Label(
        content,
        text="Welcome to Medimetrics",
        bg=BG,
        fg=GREEN,
        font=("Arial", 18, "bold")
    ).pack(pady=30)

    tk.Label(
        content,
        text="Analyze patient records, visualize demographics\n"
             "and study health-related information.",
        bg=BG,
        fg=DARK,
        font=("Arial", 13),
        justify="center"
    ).pack()


# ---------------- 2. PATIENT RECORDS ----------------

def show_records():

    create_heading("Patient Records")

    search_frame = tk.Frame(content, bg=BG)
    search_frame.pack(fill="x", padx=25, pady=10)

    tk.Label(
        search_frame,
        text="Search Patient ID:",
        bg=BG,
        fg=DARK,
        font=("Arial", 11)
    ).pack(side="left")

    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 11)
    )
    search_entry.pack(side="left", padx=10)

    table_frame = tk.Frame(content, bg=WHITE)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=15
    )

    columns = list(data.columns)

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for col in columns:

        tree.heading(col, text=col)
        tree.column(
            col,
            width=130,
            anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    def display_records(records):

        tree.delete(*tree.get_children())

        for _, row in records.iterrows():

            tree.insert(
                "",
                "end",
                values=list(row)
            )

    def search_records():

        patient_id = search_entry.get().strip().upper()

        if not patient_id:
            display_records(data)
            return

        result = data[
            data["Patient_ID"].astype(str).str.upper()
            == patient_id
        ]

        display_records(result)

        if result.empty:

            messagebox.showinfo(
                "Search",
                "Patient not found."
            )

    tk.Button(
        search_frame,
        text="Search",
        command=search_records,
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=12
    ).pack(side="left")

    tk.Button(
        search_frame,
        text="Show All",
        command=lambda: display_records(data),
        bg=ACCENT,
        fg=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=12
    ).pack(side="left", padx=8)

    display_records(data)


# ---------------- 3. DATA VISUALIZATION ----------------

def show_visualization():

    create_heading("Patient Data Visualization")

    fig, axes = plt.subplots(
        1, 2,
        figsize=(9, 4)
    )

    fig.patch.set_facecolor(BG)

    axes[0].hist(
        data["Age"],
        bins=8,
        color="#2E8B57",
        edgecolor="black"
    )

    axes[0].set_title(
        "Age Distribution",
        color=GREEN
    )

    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Patients")

    gender = data["Gender"].value_counts()

    axes[1].bar(
        gender.index,
        gender.values,
        color="#2E8B57"
    )

    axes[1].set_title(
        "Gender Distribution",
        color=GREEN
    )

    axes[1].set_xlabel("Gender")
    axes[1].set_ylabel("Patients")

    fig.tight_layout()

    show_chart(fig)

    plt.close(fig)


# ---------------- 4. HEALTH ANALYSIS ----------------

def show_analysis():

    create_heading("Health Analysis")

    fig, axes = plt.subplots(
        1, 2,
        figsize=(9, 4)
    )

    fig.patch.set_facecolor(BG)

    sns.scatterplot(
        data=data,
        x="Age",
        y="Blood_Pressure",
        hue="Gender",
        palette="Greens",
        ax=axes[0]
    )

    axes[0].set_title("Age vs Blood Pressure")

    sns.scatterplot(
        data=data,
        x="Age",
        y="Cholesterol",
        hue="Gender",
        palette="Greens",
        ax=axes[1]
    )

    axes[1].set_title("Age vs Cholesterol")

    fig.tight_layout()

    show_chart(fig)

    plt.close(fig)

    correlation = calculate_correlation(data)

    tk.Label(
        content,
        text="Correlation Between Health Variables",
        font=("Arial", 14, "bold"),
        bg=BG,
        fg=GREEN
    ).pack(pady=10)

    tk.Label(
        content,
        text=correlation.round(2).to_string(),
        font=("Courier New", 11),
        bg=WHITE,
        fg=DARK,
        justify="left",
        padx=15,
        pady=10
    ).pack()


# ---------------- 5. UPLOAD DATASET ----------------

def show_upload():

    create_heading("Upload Health Dataset")

    tk.Label(
        content,
        text="Upload a CSV file containing patient records.",
        bg=BG,
        fg=DARK,
        font=("Arial", 12)
    ).pack(pady=20)

    def upload_file():

        global data

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )

        if file_path:

            try:

                new_data = pd.read_csv(file_path)

                required = [
                    "Patient_ID",
                    "Age",
                    "Gender",
                    "Blood_Pressure",
                    "Cholesterol"
                ]

                if not all(
                    col in new_data.columns
                    for col in required
                ):

                    messagebox.showerror(
                        "Error",
                        "CSV file has incorrect columns."
                    )
                    return

                cleaned = clean_data(new_data)

                if cleaned.empty:

                    messagebox.showerror(
                        "Error",
                        "No valid patient records found."
                    )
                    return

                data = cleaned

                messagebox.showinfo(
                    "Success",
                    "Dataset uploaded successfully!"
                )

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

    tk.Button(
        content,
        text="Choose CSV File",
        command=upload_file,
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 12, "bold"),
        padx=20,
        pady=10,
        relief="flat"
    ).pack(pady=20)

    tk.Button(
        content,
        text="Restore Sample Dataset",
        command=restore_data,
        bg=ACCENT,
        fg=WHITE,
        font=("Arial", 11),
        padx=15,
        pady=8,
        relief="flat"
    ).pack()


def restore_data():

    global data

    data = clean_data(
        pd.read_csv("health_data.csv")
    )

    messagebox.showinfo(
        "Success",
        "Sample dataset restored successfully!"
    )


# ---------------- SIDEBAR ----------------

tk.Label(
    sidebar,
    text="HEALTH ANALYZER",
    bg=GREEN,
    fg=WHITE,
    font=("Arial", 16, "bold")
).pack(pady=30)

pages = [
    "Home",
    "Patient Records",
    "Data Visualization",
    "Health Analysis",
    "Upload Dataset"
]

for page in pages:

    tk.Button(
        sidebar,
        text=page,
        command=lambda p=page: show_page(p),
        bg=GREEN,
        fg=WHITE,
        activebackground=LIGHT_GREEN,
        activeforeground=GREEN,
        font=("Arial", 11),
        relief="flat",
        anchor="w",
        padx=20,
        pady=13
    ).pack(fill="x", padx=10, pady=3)


tk.Label(
    sidebar,
    text="Python Mini Project",
    bg=GREEN,
    fg=WHITE,
    font=("Arial", 10)
).pack(side="bottom", pady=20)


# ---------------- RUN APPLICATION ----------------

show_page("Home")

root.mainloop()
