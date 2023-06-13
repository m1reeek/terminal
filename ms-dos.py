import os
import PySimpleGUI as sg
import pyzipper
import sys
from io import StringIO

class MSDOSTerminal:
    def __init__(self):
        self.initial_dir = os.getcwd()
        self.current_dir = self.initial_dir
        self.username = ""
        self.hostname = ""
        self.password = ""
        self.logged_in = False
        sg.theme('DarkBlack')
        self.layout = [
            [sg.Output(size=(80, 20), font=("Courier New", 10), key='-OUTPUT-', text_color='lime', background_color='black')],
            [sg.Text("", size=(80, 1), font=("Courier New", 10), key='-PROMPT-', text_color='lime', background_color='black')],
            [sg.Input(key='-INPUT-', font=("Courier New", 10)), sg.Button('Execute', key='-EXECUTE-', button_color=('black', 'lime'))],
            [sg.Multiline(size=(80, 10), font=("Courier New", 10), key='-EDITOR-', background_color='black', text_color='lime')],
            [sg.Button('Save', key='-SAVE-', button_color=('black', 'lime')), sg.Button('Save As', key='-SAVEAS-', button_color=('black', 'lime')), sg.Button('Clear Editor', key='-CLEAR-', button_color=('black', 'lime')), sg.Button('Open TMS File', key='-OPENTMS-', button_color=('black', 'lime'))]
        ]
        self.window = sg.Window("Terminal", self.layout, finalize=True)
        self.current_command = ""
        self.stdin_backup = sys.stdin
        self.stdout_backup = sys.stdout
        self.stderr_backup = sys.stderr
        self.stdin_stringio = StringIO()
        self.stdout_stringio = StringIO()
        self.stderr_stringio = StringIO()

    def run(self):
        print(" ________                                 __                      __  \n /        |                               /  |                    /  | \n $$$$$$$$/______    ______   _____  ____  $$/  _______    ______  $$ | \n    $$ | /      \  /      \ /     \/    \ /  |/       \  /      \ $$ | \n    $$ |/$$$$$$  |/$$$$$$  |$$$$$$ $$$$  |$$ |$$$$$$$  | $$$$$$  |$$ | \n    $$ |$$    $$ |$$ |  $$/ $$ | $$ | $$ |$$ |$$ |  $$ | /    $$ |$$ | \n    $$ |$$$$$$$$/ $$ |      $$ | $$ | $$ |$$ |$$ |  $$ |/$$$$$$$ |$$ | \n    $$ |$$       |$$ |      $$ | $$ | $$ |$$ |$$ |  $$ |$$    $$ |$$ | \n    $$/  $$$$$$$/ $$/       $$/  $$/  $$/ $$/ $$/   $$/  $$$$$$$/ $$/  \n                                                                      ")
        if os.path.isfile("userdata.tms"):
            self.load_user_data()
            print(f"Welcome back, {self.username}!")
            self.logged_in = True
            print("Type 'cmd' to list commands.")
            print()
        else:
            print("User Registration, Input Your Name:")
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED:
                break

            if not self.logged_in:
                if event == '-EXECUTE-' or event == '-INPUT-' and values['-INPUT-'] != "":
                    self.process_login(values['-INPUT-'])
                continue

            if event == '-EXECUTE-' or event == '-INPUT-' and values['-INPUT-'] != "":
                self.current_command = values['-INPUT-']
                self.process_command(self.current_command)
                self.window['-INPUT-'].update("")
                self.window['-PROMPT-'].update("")
                continue

            if event == '-SAVE-':
                self.save_file()
                continue

            if event == '-SAVEAS-':
                self.save_file_as()
                continue

            if event == '-CLEAR-':
                self.clear_editor()
                continue

            if event == '-OPENTMS-':
                self.open_tms_file()
                continue

        self.save_user_data()
        self.window.close()

    def load_user_data(self):
        with open("userdata.tms", "r") as file:
            data = file.readlines()
            self.username = data[0].strip()
            self.hostname = data[1].strip()
            self.password = data[2].strip()

    def save_user_data(self):
        with open("userdata.tms", "w") as file:
            file.write(f"{self.username}\n")
            file.write(f"{self.hostname}\n")
            file.write(f"{self.password}\n")

    def process_login(self, input_text):
        if self.username == "":
            self.username = input_text.strip()
            print(f"Hello, {self.username}!")
            print("Now, input your hostname:")
            return

        if self.hostname == "":
            self.hostname = input_text.strip()
            print(f"Hostname set to: {self.hostname}")
            print("Please set a password:")
            return

        if self.password == "":
            self.password = input_text.strip()
            print("User registration complete!")
            self.logged_in = True
            print("Type 'cmd' to list commands.")
            print()
            return

    def process_command(self, command):
        if command.lower() == "cmd":
            self.list_commands()
        elif command.lower() == "help":
            self.print_help_message()
        elif command.lower() == "ls":
            self.list_files()
        elif command.lower().startswith("cd"):
            self.change_directory(command)
        elif command.lower().endswith(".pms"):
            self.run_pms_script(command)
        elif command.lower().startswith("cat"):
            self.read_text_file(command)
        elif command.lower().startswith("rm"):
            self.remove_file(command)
        elif command.lower().startswith("mkdir"):
            self.make_directory(command)
        elif command.lower().startswith("unzip"):
            self.unzip_file(command)
        else:
            print(f"Invalid command: {command}")
            self.print_help_message()

    def list_commands(self):
        print("Available commands:")
        print("cmd\t\tList available commands")
        print("help\t\tDisplay this help message")
        print("ls\t\tList files in the current directory")
        print("cd [dir]\tChange current directory (use '..' for parent directory)")
        print("[script.pms]\tExecute a Python script file")
        print("cat [file]\tDisplay the content of a text file")
        print("rm [file]\tRemove a file")
        print("mkdir [dir]\tCreate a new directory")
        print("unzip [file]\tExtract files from a zip archive")
        print()

    def print_help_message(self):
        print("Welcome to the RetroNet Terminal!")
        print("This is a simple terminal application.")
        print("You can execute commands, navigate directories, and perform basic file operations.")

    def list_files(self):
        files = os.listdir(self.current_dir)
        for file in files:
            print(file)
        print()

    def change_directory(self, command):
        parts = command.split()
        if len(parts) == 1:
            self.current_dir = self.initial_dir
        else:
            target_dir = parts[1]
            if target_dir == "..":
                self.current_dir = os.path.dirname(self.current_dir)
            else:
                new_dir = os.path.join(self.current_dir, target_dir)
                if os.path.isdir(new_dir):
                    self.current_dir = new_dir
                else:
                    print(f"No such directory: {target_dir}")
        os.chdir(self.current_dir)
        print(f"Current directory: {self.current_dir}")
        print()
    
    def run_pms_script(self, command):
        script_file = command.strip()
        if os.path.isfile(script_file):
            try:
                with open(script_file, "r") as file:
                    script_content = file.read()
                self.execute_pms_script(script_content)
            except Exception as e:
                print(f"Error reading script file: {e}")
        else:
            print(f"No such file: {script_file}")
        print()

    def execute_pms_script(self, script_content):
        self.stdin_backup = sys.stdin
        self.stdout_backup = sys.stdout
        self.stderr_backup = sys.stderr
        sys.stdin = self.stdin_stringio
        sys.stdout = self.stdout_stringio
        sys.stderr = self.stderr_stringio
        try:
            exec(script_content, globals(), globals())
        except Exception as e:
            print(f"Error executing script: {e}")
        sys.stdin = self.stdin_backup
        sys.stdout = self.stdout_backup
        sys.stderr = self.stderr_backup
        print(self.stdout_stringio.getvalue())
        self.stdin_stringio.seek(0)
        self.stdin_stringio.truncate(0)
        self.stdout_stringio.seek(0)
        self.stdout_stringio.truncate(0)
        self.stderr_stringio.seek(0)
        self.stderr_stringio.truncate(0)

    def read_text_file(self, command):
        parts = command.split()
        if len(parts) == 1:
            print("Please provide a file name.")
        else:
            file_path = parts[1]
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    print(file.read())
            else:
                print(f"No such file: {file_path}")
        print()

    def remove_file(self, command):
        parts = command.split()
        if len(parts) == 1:
            print("Please provide a file name.")
        else:
            file_path = parts[1]
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File removed: {file_path}")
            else:
                print(f"No such file: {file_path}")
        print()

    def make_directory(self, command):
        parts = command.split()
        if len(parts) == 1:
            print("Please provide a directory name.")
        else:
            dir_path = parts[1]
            os.makedirs(dir_path, exist_ok=True)
            print(f"Directory created: {dir_path}")
        print()

    def unzip_file(self, command):
        parts = command.split()
        if len(parts) == 1:
            print("Please provide a zip file name.")
        else:
            file_path = parts[1]
            if os.path.isfile(file_path) and file_path.endswith(".zip"):
                try:
                    with pyzipper.AESZipFile(file_path) as zf:
                        zf.extractall(pwd=b"infected")
                    print(f"File extracted: {file_path}")
                except Exception as e:
                    print(f"Error extracting file: {e}")
            else:
                print(f"No such file or not a zip file: {file_path}")
        print()

    def save_file(self):
        if not self.current_command.endswith(".tms"):
            print("Please provide a file name with the '.tms' extension.")
            print()
            return

        with open(self.current_command, "w") as file:
            file.write(self.window['-EDITOR-'].get())
        print("File saved.")
        print()

    def save_file_as(self):
        file_name = sg.popup_get_file("Save As", save_as=True, default_extension=".pms")
        if file_name:
            self.current_command = file_name
            self.save_file()

    def clear_editor(self):
        self.window['-EDITOR-'].update("")
        print("Editor cleared.")
        print()

    def open_tms_file(self):
        file_name = sg.popup_get_file("Open TMS File", file_types=(("TMS Files", "*.tms"),))
        if file_name:
            with open(file_name, "r") as file:
                self.window['-EDITOR-'].update(file.read())
            self.current_command = file_name
            print(f"TMS file opened: {file_name}")
            print()

if __name__ == "__main__":
    terminal = MSDOSTerminal()
    terminal.run()