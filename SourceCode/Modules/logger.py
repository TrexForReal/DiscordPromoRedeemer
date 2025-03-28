from colorama import Fore, Style, Back, init
from threading import Lock
from datetime import datetime
from SourceCode.Modules.config_scr import *
import ctypes
lock = Lock()

bright = Style.BRIGHT
reset = Style.RESET_ALL
green = Fore.GREEN
red = Fore.RED
yellow = Fore.YELLOW
blue = Fore.BLUE
cyan = Fore.CYAN
magenta = Fore.MAGENTA
white = Fore.WHITE
black = Fore.BLACK

valid,invalid=0,0
class TL:
    def timestamp():
        return datetime.now().strftime("%H:%M:%S")

    def log(tag: str, content, color):
      se = parseConfig()["TerminalLogging"]["ShowEmojis"]
      ts = TL.timestamp()
    
      if 's' in tag.lower() or 'r' in tag.lower():
        c = Fore.GREEN
        p = '+'
        e = '' if not se else "✅"
      elif 'e' in tag.lower() or 'w' in tag.lower():
        c = Fore.YELLOW
        p = '!'
        e = '' if not se else "❌"
      elif 'i' in tag.lower():
        c = Fore.BLUE
        p = '%'
        e = '' if not se else "🔔"
      else:
        c = Fore.BLUE
        p = '#'
        e = '' if not se else "🔔"

      with lock:
        init()
        return print(
            f"{bright}{white}[{blue}{ts}{white}] [{color}{tag.upper()[:4]}{white}] [{c}{p}{white}] {magenta}- {white}{content}{reset}"
        )

    def remove_content(filename: str, delete_line: str) -> None:
        with open(filename, "r+") as io:
            content = io.readlines()
            io.seek(0)
            for line in content:
                if not (delete_line in line):
                    io.write(line)
            io.truncate()
    
    def add_content(file:str,content:str)->None:
      with open(file,'a') as f:
        f.write(content+'\n')
    
    def update_console_title(new_title):
      hwnd = ctypes.windll.kernel32.GetConsoleWindow()
      ctypes.windll.kernel32.SetConsoleTitleW(new_title)