# TESTING SCRIPT
# FILES & FOLDERS WITH STATS BAR --> PYARABIC(STRIP TASHKEEL) & SEARCH IN (TEXT/TEXT WORDS & DICTIONARY) & ANALYSIS
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import pdfkit
import re
import pandas as pd
from pyarabic.araby import strip_tashkeel
from Lexicon import Lexicon
from analyzer2 import Analyzer
lexicon = Lexicon()

files = []
selected_file_path = None


def create_table_window(word_counts, file_path=None):
    table_window = tk.Toplevel(root)
    table_window.title("Word Count Table")
    table_window.geometry("600x450")
    table_window.transient(root)

    table_frame = tk.Frame(table_window)
    table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    left_table_frame = tk.Frame(table_frame)
    left_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_table_frame = tk.Frame(table_frame)
    right_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    left_table_label = tk.Label(left_table_frame, text="Word Frequency Table")
    left_table_label.pack(side=tk.TOP, padx=10, pady=5)

    left_table_scrollbar = ttk.Scrollbar(left_table_frame)
    left_table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    left_table = ttk.Treeview(
        left_table_frame, columns=("SN", "Word", "Count"))
    left_table.heading("SN", text="SN")
    left_table.heading("Word", text="Word")
    left_table.heading("Count", text="Count")

    left_table.column("#0", width=0, stretch=tk.NO)
    left_table.column("SN", width=20, anchor="center")
    left_table.column("Word", width=50, anchor="center")
    left_table.column("Count", width=20, anchor="center")

    left_table.pack(fill=tk.BOTH, expand=True)
    left_table_scrollbar.config(command=left_table.yview)
    left_table.configure(yscrollcommand=left_table_scrollbar.set)

    right_table_frame.columnconfigure(0, weight=1)
    right_table_frame.rowconfigure(0, weight=0)
    right_table_frame.rowconfigure(1, weight=2)

    right_table_label = tk.Label(right_table_frame, text="Word Details Table")
    right_table_label.grid(row=2, column=0, padx=10, pady=5)

    right_table = ttk.Treeview(right_table_frame, columns=(
        "Left Part", "Word", "Right Part", "Line Number", "File Path"), show="headings")
    right_table.heading("Left Part", text="Left Part")
    right_table.heading("Word", text="Word")
    right_table.heading("Right Part", text="Right Part")
    right_table.heading("Line Number", text="Line Number")
    right_table.heading("File Path", text="File Path")

    right_table.column("Left Part", width=80, anchor="center")
    right_table.column("Word", width=50, anchor="center")
    right_table.column("Right Part", width=80, anchor="center")
    right_table.column("Line Number", width=20, anchor="center")
    right_table.column("File Path", width=100, anchor="center")

    right_table_scrollbar = ttk.Scrollbar(
        right_table_frame, orient=tk.HORIZONTAL)
    right_table_scrollbar.grid(row=4, column=0, sticky='ew')

    right_table.configure(xscrollcommand=right_table_scrollbar.set)
    right_table_scrollbar.config(command=right_table.xview)

    # Configure the xscrollcommand for each column
    for column in right_table["columns"]:
        right_table.column(column, width=100, anchor='center', stretch=True)
        right_table.heading(column, text=column)

    right_table.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

    # Bind the scrollbar to scroll the columns
    right_table_scrollbar.bind("<MouseWheel>", lambda event: right_table.xview_scroll(
        int(-1 * (event.delta / 120)), "units"))

    # Scroll to the last column
    right_table.xview_moveto(1.0)
    search_frame = tk.Frame(right_table_frame)
    search_frame.grid(row=0, column=0, padx=10, pady=5)

    search_label = tk.Label(search_frame, text="Search Word:")
    search_label.pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=10)

    search_button = ttk.Button(
        search_frame, text="OK", command=lambda: perform_search(search_entry.get()))
    search_button.pack(side=tk.BOTTOM, padx=5)

    checkbox_frame = tk.Frame(right_table_frame, bd=1, relief=tk.SOLID)
    checkbox_frame.grid(row=1, column=0, padx=10, pady=5)

    selected_option = tk.StringVar(value="Search in Text")

    search_in_text_checkbox = tk.Checkbutton(
        checkbox_frame, text="Search in Text", variable=selected_option, onvalue="Search in Text")
    search_in_text_checkbox.pack(side=tk.TOP, anchor=tk.W)

    search_in_text_words_checkbox = tk.Checkbutton(
        checkbox_frame, text="Search in Text Words", variable=selected_option, onvalue="Search in Text Words")
    search_in_text_words_checkbox.pack(side=tk.TOP, anchor=tk.W)

    analyze_word_checkbox = tk.Checkbutton(
        checkbox_frame, text="Analyze Word", variable=selected_option, onvalue="Analyze Word")
    analyze_word_checkbox.pack(side=tk.TOP, anchor=tk.W)

    search_in_dictionary_checkbox = tk.Checkbutton(
        checkbox_frame, text="Search in Dictionary", variable=selected_option, onvalue="Search in Dictionary")
    search_in_dictionary_checkbox.pack(side=tk.TOP, anchor=tk.W)

    for i, (word, count) in enumerate(word_counts.items(), start=1):
        left_table.insert("", "end", values=(i, word, count))

    def on_table_select(event):
        global selected_file_path  # Add this line at the beginning of the function
        selected_item = left_table.focus()
        if selected_item:
            selected_word = left_table.item(selected_item, "values")[1]
            search_entry.delete(0, tk.END)
            search_entry.insert(0, selected_word)
            selected_file_path = file_path  # Store the selected file path
            perform_search(selected_word)

    left_table.bind("<<TreeviewSelect>>", on_table_select)

    def get_word_details(selected_word, file_path=None):
        word_details = []
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    words = line.split()
                    for index, word in enumerate(words):
                        if word == selected_word:
                            left_part = " ".join(words[max(0, index-2):index])
                            right_part = " ".join(words[index+1:index+3])
                            word_details.append(
                                (left_part, word, right_part, line_number, file_path))
        else:
            for file_path in files:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_number, line in enumerate(file, start=1):
                        words = line.split()
                        for index, word in enumerate(words):
                            if word == selected_word:
                                left_part = " ".join(
                                    words[max(0, index-2):index])
                                right_part = " ".join(words[index+1:index+3])
                                word_details.append(
                                    (left_part, word, right_part, line_number, file_path))
        return word_details

    def perform_search(search_word):
        global selected_file_path

        selected_option_value = selected_option.get()

        if selected_option_value == "Search in Text" or selected_option_value == "Search in Text Words":
            search_results = get_word_details(search_word, file_path)
            populate_selected_word_table(search_results)
        elif selected_option_value == "Analyze Word":
            analyzed_word = Analyzer.transliterate(search_word)
            analyzed_segments = Analyzer.segment(analyzed_word)
            valid_segments = Analyzer.validateSegments(analyzed_segments)
            analyzed_results = Analyzer.findSolutions(valid_segments)

            results = [
                (
                    Analyzer.deTransliterate(segment[0]),
                    Analyzer.deTransliterate(segment[1]),
                    Analyzer.deTransliterate(segment[2]),
                    Analyzer.deTransliterate(segment[4]),
                    segment[6],
                    segment[5]
                )
                for segment in analyzed_results
            ]

            populate_selected_word_table(results)
        elif selected_option_value == "Search in Dictionary":
            search_results = lexicon.search(search_word, None)
            populate_selected_word_table(search_results)
        elif not selected_option_value:
            selected_option_value = "Search in Text"
            search_results = get_word_details(search_word, file_path)
            populate_selected_word_table(search_results)

    def populate_selected_word_table(selected_word_details):
        right_table.delete(*right_table.get_children())

        if selected_option.get() == "Search in Dictionary":
            # Modify the columns
            right_table["columns"] = ("Word", "Meaning")
            right_table.heading("Word", text="Word")
            right_table.heading("Meaning", text="Meaning")
            right_table.column("Word", width=50, anchor="center")
            right_table.column("Meaning", width=200, anchor="center")
            for word in selected_word_details:
                meaning = lexicon.htLX[word]
                right_table.insert("", tk.END, values=(word, meaning))

        elif selected_option.get() == "Search in Text" or selected_option.get() == "Search in Text Words":
            # Modify the columns
            right_table["columns"] = (
                "Left Part", "Word", "Right Part", "Line Number", "File Path")
            right_table.heading("Left Part", text="Left Part")
            right_table.heading("Word", text="Word")
            right_table.heading("Right Part", text="Right Part")
            right_table.heading("Line Number", text="Line Number")
            right_table.heading("File Path", text="File Path")

            right_table.column("Left Part", width=80, anchor="center")
            right_table.column("Word", width=50, anchor="center")
            right_table.column("Right Part", width=80, anchor="center")
            right_table.column("Line Number", width=20, anchor="center")
            right_table.column("File Path", width=100, anchor="center")
            for details in selected_word_details:
                right_table.insert("", "end", values=details)

        elif selected_option.get() == "Analyze Word":
            # Modify the columns
            right_table["columns"] = (
                "Prefix", "Stem", "Suffix", "Vocabulary", "POS", "Gloss")
            right_table.heading("Prefix", text="Prefix")
            right_table.heading("Stem", text="Stem")
            right_table.heading("Suffix", text="Suffix")
            right_table.heading("Vocabulary", text="Vocabulary")
            right_table.heading("POS", text="POS")
            right_table.heading("Gloss", text="Gloss")

            right_table.column("Prefix", width=50, anchor="center")
            right_table.column("Stem", width=100, anchor="center")
            right_table.column("Suffix", width=50, anchor="center")
            right_table.column("Vocabulary", width=50, anchor="center")
            right_table.column("POS", width=50, anchor="center")
            right_table.column("Gloss", width=50, anchor="center")
            for details in selected_word_details:
                right_table.insert("", "end", values=details)

    stats_bar_frame = tk.Frame(table_window)  # creates the stats bar frame
    stats_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)

    word_forms_label = tk.Label(stats_bar_frame, text="Word Forms:")
    word_forms_label.pack(side=tk.LEFT, padx=5)

    total_words_label = tk.Label(stats_bar_frame, text="Total Words:")
    total_words_label.pack(side=tk.LEFT, padx=5)

    file_path_label = tk.Label(stats_bar_frame, text="File Path:")
    file_path_label.pack(side=tk.LEFT, padx=5)

    size_label = tk.Label(stats_bar_frame, text="Size:")
    size_label.pack(side=tk.LEFT, padx=5)

    if file_path:
        word_forms = len(word_counts)
        total_words = sum(word_counts.values())
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        size_label.config(text=f"Size: {file_size} bytes")
    else:
        word_forms = len(word_counts)
        total_words = sum(word_counts.values())
        folder_path = os.path.dirname(files[0])
        file_name = folder_path
        folder_size = sum(os.path.getsize(file) for file in files)
        size_label.config(text=f"Size: {folder_size} bytes")

    word_forms_label.config(text=f"Word Forms: {word_forms}")
    total_words_label.config(text=f"Total Words: {total_words}")
    file_path_label.config(text=f"Path: {file_name}")

    def save_context():
        selected_word_details = []
        for item in right_table.get_children():
            values = right_table.item(item, 'values')
            selected_word_details.append(values)

        html_table = generate_html_table(selected_word_details)

        # Open file dialog for saving the HTML file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html", filetypes=[("HTML Files", "*.html")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(html_table)
            messagebox.showinfo("Save Successful",
                                "Context saved successfully.")

    def generate_html_table(selected_word_details):
        html = """
        <html>
        <head>
        <style>
        table {
            border-collapse: collapse;
            margin: auto;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
        }
        th {
            background-color: #dddddd;
        }
        </style>
        </head>
        <body>
        <table>
        <tr>
            <th>Left Part</th>
            <th>Word</th>
            <th>Right Part</th>
            <th>Line Number</th>
            <th>File Path</th>
        </tr>
        """

        for details in selected_word_details:
            html += "<tr>"
            for value in details:
                html += f"<td>{value}</td>"
            html += "</tr>"

        html += """
        </table>
        </body>
        </html>
        """

        return html

    def corpus_file_properties():
        if file_path:
            word_forms = len(word_counts)
            total_words = sum(word_counts.values())
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            size_label.config(text=f"Size: {file_size} bytes")
            properties_message = f"File Name: {file_name}\n"
            properties_message += f"Word Forms: {word_forms}\n"
            properties_message += f"Total Words: {total_words}\n"
            properties_message += f"File Size: {file_size} bytes"
        else:
            word_forms = len(word_counts)
            total_words = sum(word_counts.values())
            folder_path = os.path.dirname(files[0])
            file_name = folder_path
            folder_size = sum(os.path.getsize(file) for file in files)
            size_label.config(text=f"Size: {folder_size} bytes")
            properties_message = f"Folder Name: {file_name}\n"
            properties_message += f"Word Forms: {word_forms}\n"
            properties_message += f"Total Words: {total_words}\n"
            properties_message += f"Folder Size: {folder_size} bytes"

        messagebox.showinfo("Corpus File Properties", properties_message)

    def letters_summary():
        word = search_entry.get().strip()

        if not word:
            messagebox.showinfo(
                "Error", "Please enter a word in the search bar.")
            return

        # Calculate letter frequencies
        letter_counts = {}
        total_letters = 0
        for letter in word:
            if letter.isalpha():
                letter_counts[letter] = letter_counts.get(letter, 0) + 1
                total_letters += 1

        if not letter_counts:
            messagebox.showinfo("Error", "No letters found in the word.")
            return

        # Calculate percentages
        letter_percentages = {}
        for letter, count in letter_counts.items():
            percentage = (count / total_letters) * 100
            letter_percentages[letter] = round(percentage, 2)

        # Create the print preview window
        print_preview_window = tk.Toplevel()
        print_preview_window.title("Letters Summary")
        print_preview_window.geometry("400x300")

        # Create a Treeview widget for the print preview
        preview_tree = ttk.Treeview(print_preview_window)
        preview_tree.pack(fill=tk.BOTH, expand=True)

        # Set up the Treeview columns
        preview_tree["columns"] = ("SN", "Letter", "Frequency", "%")

        # Configure column headings
        preview_tree.heading("SN", text="SN")
        preview_tree.heading("Letter", text="Letter")
        preview_tree.heading("Frequency", text="Frequency")
        preview_tree.heading("%", text="%")

        # Remove the empty column with index #0
        preview_tree.column("#0", width=0, stretch=tk.NO)

        # Set the anchor attribute for center alignment in all columns
        preview_tree.column("SN", anchor="center", width=20)
        preview_tree.column("Letter", anchor="center", width=50)
        preview_tree.column("Frequency", anchor="center", width=50)
        preview_tree.column("%", anchor="center", width=50)

        # Add the letter details to the Treeview
        i = 1
        summary_data = []
        for letter, count in letter_counts.items():
            percentage = letter_percentages[letter]
            preview_tree.insert("", tk.END, values=(
                i, letter, count, percentage))
            summary_data.append((i, letter, count, percentage))
            i += 1

        # Set the Treeview to read-only
        preview_tree.configure(takefocus=False)

        # Configure Treeview scrollbar
        tree_scrollbar = ttk.Scrollbar(
            print_preview_window, orient="vertical", command=preview_tree.yview)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        preview_tree.configure(yscrollcommand=tree_scrollbar.set)

        def close_window():
            print_preview_window.destroy()

        # Add Ok button to close the window
        ok_button = ttk.Button(print_preview_window,
                               text="EXIT", command=close_window)
        ok_button.pack(pady=10)
        return summary_data

    def export_context_to_excel():
        selected_word_details = []
        for item in right_table.get_children():
            values = right_table.item(item, 'values')
            selected_word_details.append(values)

        # Create a DataFrame from the word details
        df = pd.DataFrame(selected_word_details, columns=[
                          "Left Part", "Word", "Right Part", "Line Number", "File Path"])

        # Open a file dialog to choose the output Excel file path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if file_path:
            # Save the DataFrame to the Excel file
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Complete",
                                "Word details exported to Excel successfully.")

    def export_words_to_excel():
        selected_word_details = []
        for item in left_table.get_children():
            values = left_table.item(item, 'values')
            selected_word_details.append(values)

        # Create a DataFrame from the word details
        df = pd.DataFrame(selected_word_details, columns=[
                          "SN", "Word", "Frequency"])

        # Open a file dialog to choose the output Excel file path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if file_path:
            # Save the DataFrame to the Excel file
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Complete",
                                "Word details exported to Excel successfully.")

    def export_summary_to_excel():

        # Execute letters_summary function to get the summary data for the current word
        summary_data = letters_summary()

        # Create a DataFrame from the summary data
        df = pd.DataFrame(summary_data, columns=[
                          "SN", "Letter", "Frequency", "%"])

        # Open a file dialog to choose the output Excel file path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if file_path:
            # Save the DataFrame to the Excel file
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Complete",
                                "Summary exported to Excel successfully.")

    def print_context():
        def create_print_preview():
            selected_columns = [column for column,
                                var in column_vars.items() if var.get() == 1]
            selected_option = rows_to_print_option.get()
            print_title = title_entry.get()

            # Get the selected word details from the right table
            selected_word_details = []
            if selected_option == "Selected":
                selected_items = right_table.selection()
                selected_word_details = [
                    [right_table.item(item, "values")[right_table["columns"].index(
                        column)] for column in selected_columns]
                    for item in selected_items
                ]
            else:
                selected_word_details = [
                    [right_table.item(item, "values")[right_table["columns"].index(
                        column)] for column in selected_columns]
                    for item in right_table.get_children()
                ]

            # Create the print preview window
            print_preview_window = tk.Toplevel(root)
            print_preview_window.title("Print Context Selection")
            print_preview_window.geometry("800x600")

            # Create a frame for the print preview content
            print_preview_frame = tk.Frame(print_preview_window)
            print_preview_frame.pack(fill=tk.BOTH, expand=True)

            # Add the title label
            title_label = tk.Label(
                print_preview_frame, text=print_title, font=("Arial", 16, "bold"))
            title_label.pack(pady=10)

            # Create a Treeview widget for the print preview
            preview_tree = ttk.Treeview(print_preview_frame)
            preview_tree.pack(fill=tk.BOTH, expand=True)

            # Set up the Treeview columns
            preview_tree["columns"] = selected_columns

            # Remove the empty column with index #0
            preview_tree.column("#0", width=0, stretch=tk.NO)

            # Configure column headings
            for column in selected_columns:
                preview_tree.heading(column, text=column)

            # Configure column widths
            for column in preview_tree["columns"]:
                preview_tree.column(column, width=100, anchor="center")

            # Add the word details to the Treeview
            for details in selected_word_details:
                preview_tree.insert("", tk.END, values=details)

            # Set the Treeview to read-only
            preview_tree.configure(takefocus=False)

            # Configure Treeview scrollbar
            tree_scrollbar = ttk.Scrollbar(
                print_preview_frame, orient="vertical", command=preview_tree.yview)
            tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            preview_tree.configure(yscrollcommand=tree_scrollbar.set)

            # Fit to width if selected
            preview_tree["displaycolumns"] = selected_columns

            # Add Print button
            print_button = ttk.Button(
                print_preview_frame, text="Print",
                command=lambda: generate_pdf(
                    selected_columns, selected_word_details, print_title)
            )
            print_button.pack(pady=10)

        def on_ok():
            create_print_preview()

        def generate_pdf(columns, data, title):
            # Generate HTML table
            html = "<html><head><meta charset='utf-8'><style>table {border-collapse: collapse; width: 100%; text-align: center;} th, td {border: 1px solid black; padding: 8px;}</style></head><body>"
            html += f"<h1 style='text-align: center;'>{title}</h1>"
            html += "<table><tr>"
            for column in columns:
                html += f"<th>{column}</th>"
            html += "</tr>"
            for row in data:
                html += "<tr>"
                for i, value in enumerate(row):
                    # Check if column is selected
                    if i < len(columns) and columns[i]:
                        html += f"<td>{value}</td>"
                html += "</tr>"
            html += "</table></body></html>"

            # Ask user for file path and name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                # Convert HTML to PDF and save
                pdfkit.from_string(html, file_path)
                messagebox.showinfo(
                    "PDF Generated", "PDF file generated successfully.")

        print_window = tk.Toplevel(root)
        print_window.title("Print Context")
        print_window.geometry("400x300")

        print_frame = tk.Frame(print_window)
        print_frame.pack(fill=tk.BOTH, expand=True)

        # Columns to print
        columns_label = tk.Label(print_frame, text="Columns to print:")
        columns_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        column_vars = {}
        row_count = 1
        for column in right_table["columns"]:
            var = tk.IntVar(value=1)
            column_vars[column] = var
            checkbox = tk.Checkbutton(print_frame, text=column, variable=var)
            checkbox.grid(row=row_count, column=0, sticky="w", padx=20)
            row_count += 1

        # Rows to print
        rows_label = tk.Label(print_frame, text="Rows to print:")
        rows_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 5))

        rows_to_print_option = tk.StringVar(value="All")

        all_rows_radio = tk.Radiobutton(
            print_frame, text="All", variable=rows_to_print_option, value="All")
        all_rows_radio.grid(row=1, column=1, sticky="w", padx=20)

        selected_rows_radio = tk.Radiobutton(
            print_frame, text="Selected", variable=rows_to_print_option, value="Selected")
        selected_rows_radio.grid(row=2, column=1, sticky="w", padx=20)

        # Title of Print
        title_label = tk.Label(print_frame, text="Title of Print:")
        title_label.grid(row=3, column=1, sticky="w", padx=10, pady=(10, 5))

        title_entry = tk.Entry(print_frame)
        title_entry.grid(row=4, column=1, columnspan=2,
                         padx=10, pady=5, sticky="we")

        # OK button
        ok_button = ttk.Button(print_frame, text="OK", command=on_ok)
        ok_button.grid(row=5, column=1, columnspan=2,
                       padx=10, pady=(20, 10), sticky="we")

    def print_words():
        def create_print_preview():
            selected_columns = [column for column,
                                var in column_vars.items() if var.get() == 1]
            selected_option = rows_to_print_option.get()
            print_title = title_entry.get()

            # Get the selected word details from the left table
            selected_word_details = []
            if selected_option == "Selected":
                selected_items = left_table.selection()
                for item in selected_items:
                    values = [left_table.item(item, "values")[left_table["columns"].index(
                        column)] for column in selected_columns]
                    selected_word_details.append(values)
            else:
                for item in left_table.get_children():
                    values = [left_table.item(item, "values")[left_table["columns"].index(
                        column)] for column in selected_columns]
                    selected_word_details.append(values)

            # Create the print preview window
            print_preview_window = tk.Toplevel(root)
            print_preview_window.title("Print Words Selection")
            print_preview_window.geometry("800x600")

            # Create a frame for the print preview content
            print_preview_frame = tk.Frame(print_preview_window)
            print_preview_frame.pack(fill=tk.BOTH, expand=True)

            # Add the title label
            title_label = tk.Label(
                print_preview_frame, text=print_title, font=("Arial", 16, "bold"))
            title_label.pack(pady=10)

            # Create a Treeview widget for the print preview
            preview_tree = ttk.Treeview(print_preview_frame)
            preview_tree.pack(fill=tk.BOTH, expand=True)

            # Set up the Treeview columns
            preview_tree["columns"] = selected_columns

            # Remove the empty column with index #0
            preview_tree.column("#0", width=0, stretch=tk.NO)

            # Configure column headings
            for column in selected_columns:
                preview_tree.heading(column, text=column)

            # Configure column widths
            for column in preview_tree["columns"]:
                preview_tree.column(column, width=100, anchor="center")

            # Add the word details to the Treeview
            for details in selected_word_details:
                preview_tree.insert("", tk.END, values=details)

            # Set the Treeview to read-only
            preview_tree.configure(takefocus=False)

            # Configure Treeview scrollbar
            tree_scrollbar = ttk.Scrollbar(
                print_preview_frame, orient="vertical", command=preview_tree.yview)
            tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            preview_tree.configure(yscrollcommand=tree_scrollbar.set)

            # Fit to width if selected
            preview_tree["displaycolumns"] = selected_columns

            # Add Print button
            print_button = ttk.Button(print_preview_frame, text="Print",
                                      command=lambda: generate_pdf(selected_columns, selected_word_details, print_title))
            print_button.pack(pady=10)

        def on_ok():
            create_print_preview()

        def generate_pdf(columns, data, title):
            # Generate HTML table
            html = "<html><head><meta charset='utf-8'><style>table {border-collapse: collapse; width: 100%; text-align: center;} th, td {border: 1px solid black; padding: 8px;}</style></head><body>"
            html += f"<h1 style='text-align: center;'>{title}</h1>"
            html += "<table><tr>"
            for column in columns:
                html += f"<th>{column}</th>"
            html += "</tr>"
            for row in data:
                html += "<tr>"
                for i, value in enumerate(row):
                    # Check if column is selected
                    if i < len(columns) and columns[i]:
                        html += f"<td>{value}</td>"
                html += "</tr>"
            html += "</table></body></html>"

            # Ask user for file path and name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                # Convert HTML to PDF and save
                pdfkit.from_string(html, file_path)
                messagebox.showinfo(
                    "PDF Generated", "PDF file generated successfully.")

        print_window = tk.Toplevel(root)
        print_window.title("Print Words")
        print_window.geometry("400x300")

        print_frame = tk.Frame(print_window)
        print_frame.pack(fill=tk.BOTH, expand=True)

        # Columns to print
        columns_label = tk.Label(print_frame, text="Columns to print:")
        columns_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        column_vars = {}
        row_count = 1
        for column in left_table["columns"]:
            var = tk.IntVar(value=1)
            column_vars[column] = var
            checkbox = tk.Checkbutton(print_frame, text=column, variable=var)
            checkbox.grid(row=row_count, column=0, sticky="w", padx=20)
            row_count += 1

        # Rows to print
        rows_label = tk.Label(print_frame, text="Rows to print:")
        rows_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 5))

        rows_to_print_option = tk.StringVar(value="All")

        all_rows_radio = tk.Radiobutton(
            print_frame, text="All", variable=rows_to_print_option, value="All")
        all_rows_radio.grid(row=1, column=1, sticky="w", padx=20)

        selected_rows_radio = tk.Radiobutton(
            print_frame, text="Selected", variable=rows_to_print_option, value="Selected")
        selected_rows_radio.grid(row=2, column=1, sticky="w", padx=20)

        # Title of Print
        title_label = tk.Label(print_frame, text="Title of Print:")
        title_label.grid(row=3, column=1, sticky="w", padx=10, pady=(10, 5))

        title_entry = tk.Entry(print_frame)
        title_entry.grid(row=4, column=1, columnspan=2,
                         padx=10, pady=5, sticky="we")

        # OK button
        ok_button = ttk.Button(print_frame, text="OK", command=on_ok)
        ok_button.grid(row=5, column=1, columnspan=2,
                       padx=10, pady=(20, 10), sticky="we")

    def close():
        table_window.destroy()  # Destroy the table window

        # Remove the additional file menu options
        file_menu.delete(0, tk.END)
        file_menu.add_command(label="Load Corpus", command=load_corpus)
        file_menu.add_command(label="Load Folder", command=load_folder)
        file_menu.add_command(label="Load from URL")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=exit_app)

    def on_closing():
        close()
        table_window.quit()

    table_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Add extra features to the File menu
    file_menu.delete("Exit")
    file_menu.add_command(label="Save Context", command=save_context)
    file_menu.add_command(label="Corpus File Properties",
                          command=corpus_file_properties)
    file_menu.add_command(label="Letters Summary", command=letters_summary)
    file_menu.add_separator()
    file_menu.add_command(label="Export Context to Excel",
                          command=export_context_to_excel)
    file_menu.add_command(label="Export Words to Excel",
                          command=export_words_to_excel)
    file_menu.add_command(label="Export Summary to Excel",
                          command=export_summary_to_excel)
    file_menu.add_separator()
    file_menu.add_command(label="Print Context", command=print_context)
    file_menu.add_command(label="Print Words", command=print_words)
    file_menu.add_separator()
    file_menu.add_command(label="Close", command=close)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit)

    table_window.mainloop()


def load_corpus():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        word_counts = load_file(file_path)
        if word_counts:
            create_table_window(word_counts, file_path)
        else:
            messagebox.showinfo(
                "Error", "The selected file is empty or does not exist.")


def load_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        global files
        files = get_text_files(folder_path)
        if files:
            word_counts = load_folder_files()
            if word_counts:
                create_table_window(word_counts)
            else:
                messagebox.showinfo(
                    "Error", "No words found in the selected folder.")
        else:
            messagebox.showinfo(
                "Error", "No text files found in the selected folder.")


def load_folder_files():
    word_counts = {}
    for file_path in files:
        counts = load_file(file_path)
        for word, count in counts.items():
            word_counts[word] = word_counts.get(word, 0) + count
    return word_counts


def get_text_files(folder_path):
    text_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                text_files.append(os.path.join(root, file))
    return text_files


def load_file(file_path):
    word_counts = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line)
            for word in words:
                stripped_word = strip_tashkeel(word)
                if stripped_word.isalpha():
                    word_counts[stripped_word] = word_counts.get(
                        stripped_word, 0) + 1
    return word_counts


'''
def font_settings():
    # Implement font settings functionality here
    messagebox.showinfo("Font Settings", "Font Settings")

def language_settings():
    # Implement language settings functionality here
    messagebox.showinfo("Language Settings", "Language Settings")

def number_of_words():
    # Implement number of words functionality here
    messagebox.showinfo("Number of Words", "Number of Words")

def number_of_lines():
    # Implement number of lines functionality here
    messagebox.showinfo("Number of Lines", "Number of Lines")
'''


def show_status_bar():
    # Implement show status bar functionality here
    if view_show_statusbar.get():
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    else:
        status_bar.pack_forget()


def show_about():
    about_message = "Al Khaleel V3.0\n\nDevelopment Group:\n\n" \
                    "Dr. Harmain M. Harmain, PI\n" \
                    "Associate Professor\n" \
                    "harmain@uaeu.ac.ae\n\n" \
                    "Mr. Shadi N. Salah, RA\n" \
                    "snaser@uaeu.ac.ae"
    messagebox.showinfo("About", about_message)


def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.quit()


root = tk.Tk()
root.title("Al Khaleel V3.0")
root.geometry("700x600")

# Create Menubar
menubar = tk.Menu(root)

# Create File menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Load Corpus", command=load_corpus)
file_menu.add_command(label="Load Folder", command=load_folder)
#file_menu.add_command(label="Load from URL")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

'''
# Create Settings menu
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Font Settings", command=font_settings)
settings_menu.add_command(label="Language", command=language_settings)
settings_menu.add_command(label="Number of Words", command=number_of_words)
settings_menu.add_command(label="Number of Lines", command=number_of_lines)
menubar.add_cascade(label="Settings", menu=settings_menu)
'''

# Create View menu
view_menu = tk.Menu(menubar, tearoff=0)
view_show_statusbar = tk.BooleanVar(value=True)
view_menu.add_checkbutton(label="Show Status Bar", onvalue=True,
                          offvalue=False, variable=view_show_statusbar, command=show_status_bar)
menubar.add_cascade(label="View", menu=view_menu)

# Create Help menu
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

# Configure Menubar
root.config(menu=menubar)

# Create Status Bar
status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
