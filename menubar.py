import tkinter as tk
import os
import re
from tkinter.colorchooser import askcolor
from syntax_highlighting import SyntaxHighlighting
from time import sleep


class Menubar():
    # initialising the menu bar of editor
    def __init__(self, parent):
        self._parent = parent
        self.syntax = parent.syntax_highlighter
        self.ptrn = r'[^\/]+$'
        font_specs = ('Droid Sans Fallback', 12)

        # setting up basic features in menubar
        menubar = tk.Menu(
          parent.master,
          font=font_specs,
          fg=parent.menu_fg,
          bg=parent.menu_bg,
          activeforeground= parent.menubar_fg_active,
          activebackground= parent.menubar_bg_active,
          activeborderwidth=0,
          bd=0)

        parent.master.config(menu=menubar)
        self._menubar = menubar
        # adding features file dropdown in menubar
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(
          label='Load Previous File',
          accelerator='Ctrl+P',
          command=parent.load_previous_file)
        # new file creation feature
        file_dropdown.add_command(
          label='New File',
            accelerator='Ctrl+N',
            command=parent.new_file)
        # open file feature
        file_dropdown.add_command(
          label='Open File',
            accelerator='Ctrl+O',
            command=parent.open_file)
        # save file feature
        file_dropdown.add_command(
          label='Save',
            accelerator='Ctrl+S',
            command=parent.save)
        # Save as feature
        file_dropdown.add_command(
          label='Save As',
            accelerator='Ctrl+Shift+S',
            command=parent.save_as)
        # exit feature
        file_dropdown.add_separator()
        file_dropdown.add_command(
          label='Exit',
          command=parent.on_closing)

        # adding featues to settings dropdown in menubar
        # Edit settings feature
        settings_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        settings_dropdown.add_command(
          label='Edit Settings',
          command=parent.open_settings_file)
        # reset settings feature
        settings_dropdown.add_command(
          label='Reset Settings to Default',
          command=parent.reset_settings_file)

        #view dropdown menu
        view_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        view_dropdown.add_command(
          label='Toggle Menu Bar',
          accelerator='Alt',
          command=self.hide_menu)
        view_dropdown.add_command(
          label='Hide Status Bar',
          command=parent.hide_status_bar)
        view_dropdown.add_command(
          label='Toggle Line Numbers',
          accelerator='Ctrl+Shift+L',
          command=parent.toggle_linenumbers)
        view_dropdown.add_command(
          label='Enter  Mode',
          accelerator='Ctrl+Q',
          command=self.enter__mode)

        #tools dropdown menu
        tools_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        tools_dropdown.add_command(
          label='Find and Replace',
          accelerator='Ctrl+F',
          command=parent.show_find_window)
        tools_dropdown.add_command(
          label='Open Color Selector',
          accelerator='Ctrl+M',
          command=self.open_color_picker)

        #theme dropdown menu
        theme_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        theme_dropdown.add_command(
          label='Dark',
          command=self.syntax.syntax_and_themes.load_dark)
        theme_dropdown.add_command(
          label='Desert',
          command=self.syntax.syntax_and_themes.load_desert)
        theme_dropdown.add_command(
          label='Monokai',
          command=self.syntax.syntax_and_themes.load_monokai)

        syntax_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        
        syntax_dropdown.add_command(
          label='C',
          command=self.syntax.syntax_and_themes.load_c_syntax)
        syntax_dropdown.add_command(
          label='C++',
          command=self.syntax.syntax_and_themes.load_cpp_syntax)
        syntax_dropdown.add_command(
          label="C#",
          command=self.syntax.syntax_and_themes.load_csharp_syntax)
        syntax_dropdown.add_command(
          label='CSS',
          command=self.syntax.syntax_and_themes.load_css_syntax)
        
        syntax_dropdown.add_command(
          label='HTML/Django',
          command=self.syntax.syntax_and_themes.load_html_syntax)
        syntax_dropdown.add_command(
          label='JavaScript',
          command=self.syntax.syntax_and_themes.load_javascript_syntax)
        syntax_dropdown.add_command(
          label='Java',
          command=self.syntax.syntax_and_themes.load_java_syntax)
        syntax_dropdown.add_command(
          label='Python3',
          command=self.syntax.syntax_and_themes.load_python3_syntax)

        build_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        build_dropdown.add_command(
          label='Build',
          command=self.build)
        build_dropdown.add_command(
          label='Run',
          accelerator='Ctrl+R',
          command=self.run)
        build_dropdown.add_command(
          label='Build+Run',
          command=self.build_run)

        # menubar add buttons
        menubar.add_cascade(label='File', menu=file_dropdown)
        menubar.add_cascade(label='View', menu=view_dropdown)
        menubar.add_cascade(label='Settings', menu=settings_dropdown)
        menubar.add_cascade(label='Tools', menu=tools_dropdown)
        menubar.add_cascade(label='Syntax', menu=syntax_dropdown)
        menubar.add_cascade(label='Themes', menu=theme_dropdown)
        menubar.add_cascade(label='Build Options', menu=build_dropdown)
        
        self.menu_fields = [field for field in (
            file_dropdown, view_dropdown, syntax_dropdown, build_dropdown,
            settings_dropdown, tools_dropdown, theme_dropdown)]

    # Settings reconfiguration function
    def reconfigure_settings(self):
        settings = self._parent.loader.load_settings_data()
        for field in self.menu_fields:
            field.configure(
                bg=self._parent.menu_bg,
                fg=self._parent.menu_fg,
                activeforeground=self._parent.menubar_fg_active,
                activebackground=self._parent.menubar_bg_active,
                background = self._parent.bg_color,
            )

        self._menubar.configure(
            bg=self._parent.menu_bg,
            fg=self._parent.menu_fg,
            background = self._parent.bg_color,
            activeforeground= self._parent.menubar_fg_active,
            activebackground = self._parent.menubar_bg_active,
          )

    # color to different text tye can be set here
    def open_color_picker(self):
        return askcolor(title='Color Menu', initialcolor='#d5c4a1')[1]

    def toggle_text_border(self):
        settings = self._parent.loader.load_settings_data()
        border_status = settings['textarea_border']
        if border_status == 0:
          self._parent.textarea.configure(bd=0.5)
          settings['textarea_border'] = 0.5
        elif border_status > 0:
          self._parent.textarea.configure(bd=0)
          settings['textarea_border'] = 0
        self._parent.loader.store_settings_data(settings)

    def toggle_scroll_x(self):
        settings = self._parent.loader.load_settings_data()
        scrollx_width = settings['horizontal_scrollbar_width']
        if scrollx_width > 0:
          self._parent.scrollx.configure(width=0)
          settings['horizontal_scrollbar_width'] = 0
        elif scrollx_width == 0:
          self._parent.scrollx.configure(width=8)
          settings['horizontal_scrollbar_width'] = 8
        self._parent.loader.store_settings_data(settings)

    def toggle_scroll_y(self):
        settings = self._parent.loader.load_settings_data()
        scrolly_width = settings['vertical_scrollbar_width']
        if scrolly_width > 0:
          self._parent.scrolly.configure(width=0)
          settings['vertical_scrollbar_width'] = 0
        elif scrolly_width == 0:
          self._parent.scrolly.configure(width=8)
          settings['vertical_scrollbar_width'] = 8
        self._parent.loader.store_settings_data(settings)

    #  mode is defined here
    def enter__mode(self):
        self._parent.enter__mode()

    # hiding the menubar
    def hide_menu(self):
        self._parent.master.config(menu='')

    # display the menubar
    def show_menu(self):
        self._parent.master.config(menu=self._menubar)

    def base_cmd(self, command):
      cmd = None
      if self._parent.operating_system == 'Windows':
          cmd = f'start cmd.exe @cmd /k {command}'
      elif self._parent.operating_system == 'Linux':
          cmd = f"gnome-terminal -- bash -c '{command}; read'"
      file_from_path = re.search(self.ptrn, self._parent.filename)
      filename = file_from_path.group(0)
      file_path = self._parent.filename[:-len(filename)]
      os.chdir(file_path)
      if cmd:
        os.system(cmd)
      else:
        print('cmd went unassigned!')

    def build(self):
        try:
            file_from_path = re.search(self.ptrn, self._parent.filename)
            filename = file_from_path.group(0)
            if filename[-2:] == '.c':
                compiled_name = filename[:-2]
                self.base_cmd(f'gcc {filename} -o {compiled_name}')
            elif filename[-4:] == '.cpp':
                compiled_name = filename[:-4]
                self.base_cmd(f'g++ -o {compiled_name} {filename}')
            elif filename[-5:] == '.java':
                compiled_name = filename[:-5]
                self.base_cmd(f'javac {filename}')
            else:
                self._parent.statusbar.update_status('cant build')
        except TypeError:
            self._parent.statusbar.update_status('cant build')

    def run(self, *args):
        try:
            file_from_path = re.search(self.ptrn, self._parent.filename)
            filename = file_from_path.group(0)
            if filename[-3:] == '.py':
                self.base_cmd(f'python {self._parent.filename}')
            elif filename[-5:] == '.html':
                self.base_cmd(f'{self._parent.browser} {filename}')
            elif filename[-3:] == '.js':
                self.base_cmd(f'node {self._parent.filename}')
            elif filename[-2:] == '.c':
                compiled_name = filename[:-2]
                self.base_cmd(f'{compiled_name}')
            elif filename[-4:] == '.cpp':
                compiled_name = filename[:-4]
                self.base_cmd(f'{compiled_name}')
            elif filename[-5:] == '.java':
                compiled_name = filename[:-5]
                self.base_cmd(f'java {compiled_name}')
            else:
                self._parent.statusbar.update_status('no python')
        except TypeError as e:
            print(e)
            self._parent.statusbar.update_status('no file run')

    def build_run(self):
        self.build()
        sleep(.5)
        self.run()