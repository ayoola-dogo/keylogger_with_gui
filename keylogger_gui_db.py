import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from gui_database import key_logger_entry
import re


class KeyLoggerGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.iconbitmap('image.ico')
        self.root.geometry('600x600')
        self.root.title('Keylogger')
        self.create_widgets()

    def read_from_file(self):
        with open('keyfile.txt', 'r') as r_file:
            content = r_file.read()
            return content

    def write_scroll(self):
        self.scr_text.delete(1.0, 'end')
        content = self.read_from_file()
        if content:
            self.scr_text.insert(tk.INSERT, content)
        else:
            pass

    # Get content from widgets
    def content_widgets(self):
        item_text = self.scr_text.get(1.0, 'end')
        t_id = self.id_text.get(1.0, 'end')
        title = self.title_text.get(1.0, 'end')
        pattern = re.compile(r'(.*)\s')
        t_id = pattern.sub(r'\1', t_id)
        title = pattern.sub(r'\1', title)
        return t_id, title, item_text

    def clear_widgets(self):
        self.id_text.delete(1.0, 'end')
        self.title_text.delete(1.0, 'end')
        self.scr_text.delete(1.0, tk.END)

    # DATABASE SECTION
    # Save to database
    def insert_into_database(self):
        _id, _title, _text = self.content_widgets()
        mode = 'i'
        date = datetime.now()
        key_logger_entry(mode, _id, _title, _text, date)
        self.clear_widgets()

    # Write into widgets
    def write_into_widgets(self, details):
        if details:
            id, title, entry_text, date = details
            self.id_text.insert(tk.INSERT, id)
            self.title_text.insert(tk.INSERT, title)
            self.scr_text.insert(tk.INSERT, entry_text)
        else:
            pass

    # From Main Window
    def retrieve_from_database(self):
        _id, _title, _text = self.content_widgets()
        mode = 'r'
        date = ''
        details = key_logger_entry(mode, _id, _title, _text, date)
        self.clear_widgets()
        self.write_into_widgets(details)

    # FOR EDIT/TOP LEVEL WINDOW
    def clear_widgets_edit(self):
        self.id_text.delete(1.0, 'end')
        self.title_text.delete(1.0, 'end')
        self.scr_text.delete(1.0, tk.END)
        self.id_in_edit.delete(1.0, 'end')
        self.date_in_edit.delete(1.0, 'end')
        self.title_in_edit.delete(1.0, 'end')
        self.scr_text_edit.delete(1.0, 'end')

    def content_widgets_edit(self):
        item_text = self.scr_text_edit.get(1.0, 'end')
        t_id = self.id_in_edit.get(1.0, 'end')
        title = self.title_in_edit.get(1.0, 'end')
        pattern = re.compile(r'(.*)\s')
        t_id = pattern.sub(r'\1', t_id)
        title = pattern.sub(r'\1', title)
        return t_id, title, item_text

    def insert_database_from_edit(self):
        _id, _title, _text = self.content_widgets_edit()
        mode = 'i'
        date = datetime.now()
        key_logger_entry(mode, _id, _title, _text, date)
        self.clear_widgets_edit()

    # Write to all widgets from top level window
    def write_into_widgets_edit(self, details):
        if details:
            id, title, entry_text, date = details
            self.id_text.insert(tk.INSERT, id)
            self.title_text.insert(tk.INSERT, title)
            self.scr_text.insert(tk.INSERT, entry_text)
            self.id_in_edit.insert(tk.INSERT, id)
            _date = date.strftime('%d-%B-%Y')
            self.date_in_edit.insert(tk.INSERT, _date)
            self.title_in_edit.insert(tk.INSERT, title)
            self.scr_text_edit.insert(tk.INSERT, entry_text)
        else:
            pass

    # From edit/top level window
    def retrieve_from_database_edit(self):
        _id, _title, _text = self.content_widgets_edit()
        mode = 'r'
        date = ''
        details = key_logger_entry(mode, _id, _title, _text, date)
        self.clear_widgets_edit()
        self.write_into_widgets_edit(details)

    def delete(self):
        _id, _title, _text = self.content_widgets_edit()
        mode = 'd'
        date = ''
        key_logger_entry(mode, _id, _title, _text, date)
        self.clear_widgets_edit()

    def delete_all(self):
        mode = 'd_all'
        key_logger_entry(mode, '', '', '', '')
        self.clear_widgets_edit()

    def table_layout(self):
        mode = 'c'
        result = key_logger_entry(mode, '', '', '', '')
        self.scr_text_edit.insert(tk.INSERT, result)

    def edit_top_level(self):
        self.edit_win = tk.Toplevel()
        self.edit_win.title('Edit Database Contents')
        self.edit_win.geometry('+100+100')
        # Frame
        edit_frame = tk.Frame(self.edit_win, bg='purple4')
        edit_frame.pack(expand=1, fill=tk.BOTH)
        # Top Level LabelFrame on Frame
        edit_tpl_lf = tk.LabelFrame(edit_frame, bd=0, bg='purple4')
        edit_tpl_lf.grid(column=0, row=0)
        # labels and Widgets on LabelFrame
        id_label = tk.Label(edit_tpl_lf, text='ID', bd=0, bg='purple4', font='Aerial 10 bold', width=4)
        id_label.grid(column=0, row=0, padx=2, pady=2, sticky=tk.W)
        date_label = tk.Label(edit_tpl_lf, text='Date', bd=0, bg='purple4', font='Aerial 10 bold', width=7)
        date_label.grid(column=1, row=0, padx=2, pady=2, sticky=tk.W)
        title_label = tk.Label(edit_tpl_lf, text='Title', bd=0, bg='purple4', font='Aerial 10 bold', width=25)
        title_label.grid(column=2, row=0, padx=2, pady=2)
        # edit_win widgets
        self.id_in_edit = tk.Text(edit_tpl_lf, width=4, height=2, font=("Helvetica", 11))
        self.id_in_edit.grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
        self.date_in_edit = tk.Text(edit_tpl_lf, width=12, height=2, font=("Helvetica", 11))
        self.date_in_edit.grid(column=1, row=1, padx=8, pady=5)
        self.title_in_edit = tk.Text(edit_tpl_lf, width=48, height=2, font=("Helvetica", 11, "bold"))
        self.title_in_edit.grid(column=2, row=1, padx=10, pady=5)
        # Create Label for ScrolledText
        scr_text_lbl = tk.Label(edit_frame, bg='purple4')
        scr_text_lbl.grid(column=0, row=1, padx=0, pady=10)
        self.scr_text_edit = ScrolledText(scr_text_lbl, width=70, height=18, font=("Helvetica", 11), wrap=tk.WORD)
        self.scr_text_edit.grid(column=0, row=0)

        # Button Labels for Buttons on Frame
        button_lb = tk.Label(edit_frame, bg='purple4')
        button_lb.grid(column=0, row=2)
        button_names = ['Insert', 'Retrieve', 'Delete', 'Delete All', 'Table Layout']
        commands = [self.insert_database_from_edit, self.retrieve_from_database_edit, self.delete, self.delete_all,
                    self.table_layout]
        button_widgets = list()
        n = 0
        for i in button_names:
            button_widgets.append(
                tk.Button(button_lb, text=i, width=10, bg='firebrick4', font='Aerial 9 bold', command=commands[n]).grid
                (column=button_names.index(i), row=1, padx=17, pady=15)
            )
            n += 1

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=1, fill=tk.BOTH)
        m_lf = tk.LabelFrame(main_frame, bg='SlateBlue4')
        m_lf.grid(column=0, row=0)
        # m_lf.grid_columnconfigure(0, weight=1)
        # m_lf.grid_rowconfigure(0, weight=1)
        m_lf.pack(expand=1, fill=tk.BOTH)
        scroll_w = 72
        scroll_h = 25
        self.scr_text = ScrolledText(m_lf, width=scroll_w, height=scroll_h, wrap=tk.WORD, font=("Helvetica", 11))
        self.scr_text.grid(column=0, row=0)
        self.write_scroll()

        # Text and Entry Box Label
        text_entry_lb = tk.Label(m_lf, bg='SlateBlue3')
        text_entry_lb.grid(column=0, row=1)
        text_entry_lb.grid_rowconfigure(0, weight=1)
        text_entry_lb.grid_columnconfigure(0, weight=1)
        # Create Text and Entry Box widgets
        self.id_text = tk.Text(text_entry_lb, width=8, height=2, font=("Helvetica", 11))
        self.id_text.grid(column=0, row=0, padx=10, pady=10)
        self.title_text = tk.Text(text_entry_lb, width=60, height=2, font=("Helvetica", 11, "bold"))
        self.title_text.grid(column=1, row=0, padx=10, pady=10)

        # Button Label on the m_lf
        button_lbl = tk.Label(m_lf, bg='SlateBlue4')
        button_lbl.grid(column=0, row=2)
        # First Buttons row
        edit_button = tk.Button(button_lbl, text='Edit', bg='firebrick4', font='Aerial 10 bold', width=15,
                                command=self.edit_top_level)
        edit_button.grid(column=0, row=0, padx=20, pady=25, sticky=tk.W)
        save_button = tk.Button(button_lbl, text='Save', bg='firebrick4',
                                font='Aerial 10 bold', width=15, command=self.insert_into_database)
        save_button.grid(column=1, row=0, padx=20, pady=25, sticky=tk.W)
        retrieve_button = tk.Button(button_lbl, text='Retrieve', bg='firebrick4', font='Aerial 10 bold', width=15,
                                    command=self.retrieve_from_database)
        retrieve_button.grid(column=2, row=0, padx=20, pady=25, sticky=tk.W)
        # Clear Button
        clear_button = tk.Button(button_lbl, text='Clear', bg='firebrick4', font='Aerial 10 bold', width=15,
                                 command=self.clear_widgets)
        clear_button.grid(column=1, row=1, padx=20, pady=7, sticky=tk.W)

        self.root.protocol('WM_DELETE_WINDOW', self._quit)

    def _quit(self):
        self.root.quit()
        self.root.destroy()


def c_gui():
    key_logger_gui = KeyLoggerGui()
    key_logger_gui.root.mainloop()
