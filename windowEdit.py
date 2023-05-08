from tkinter import *
import requests
from io import BytesIO
from PIL import Image, ImageTk, ImageGrab
import win32api
import win32con
import win32gui
import win32com.client

VKC = {'backspace': 8, 'tab': 9, 'clear': 254, 'enter': 13, 'shift': 16, 'ctrl': 17, 'alt': 18, 'pause': 19, 'caps_lock': 20, 'esc': 27, 'spacebar': 32, 'page_up': 33, 'page_down': 34, 'end': 35, 'home': 36, 'left arrow': 37, 'up arrow': 38, 'right arrow': 39, 'down arrow': 40, 'select': 41, 'print': 42, 'execute': 43, 'print_screen': 44, 'ins': 45, 'del': 46, 'help': 47, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57, 'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90, 'n 0': 96, 'n 1': 97, 'n 2': 98, 'n 3': 99, 'n 4': 100, 'n 5': 101, 'n 6': 102, 'n 7': 103, 'n 8': 104, 'n 9': 105, 'multiply': 106, 'plus': 107, 'separator key': 108, 'minus': 109, 'decimal key': 110, 'divide': 111, 'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119, 'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127, 'F17': 128, 'F18': 129, 'F19': 130, 'F20': 131, 'F21': 132, 'F22': 133, 'F23': 134, 'F24': 135, 'num_lock': 144, 'scroll_lock': 145, 'left_shift': 160, 'right_shift ': 161, 'left_control': 162, 'right_control': 163, 'left_menu': 164, 'right_menu': 165, 'browser_back': 166, 'browser_forward': 167, 'browser_refresh': 168, 'browser_stop': 169, 'browser_search': 170, 'browser_favorites': 171, 'browser_start_and_home': 172, 'volume_mute': 173, 'volume_Down': 174, 'volume_up': 175, 'next_track': 176, 'previous_track': 177, 'stop_media': 178, 'play/pause_media': 179, 'start_mail': 180, 'select_media': 181, 'start_application_1': 182, 'start_application_2': 183, 'attn': 246, 'crsel': 247, 'exsel': 248, 'play': 250, 'zoom': 251, '+': 187, ',': 188, '-': 189, '.': 190, '/': 191, '`': 192, ';': 186, '[': 219, '\\': 220, ']': 221, "'": 222}

def get_window_state(window_handle: int) -> str:
    """
    Returns the current state of a window based on its window handle.

    Args:
        window_handle (int): The handle to the window.

    Returns:
        str: The window state, which can be "maximized", "minimized", or "normal".
    """
    window_placement = win32gui.GetWindowPlacement(window_handle)
    if window_placement[1] == win32con.SW_SHOWMAXIMIZED:
        return "maximized"
    elif window_placement[1] == win32con.SW_SHOWMINIMIZED:
        return "minimized"
    elif window_placement[1] == win32con.SW_SHOWNORMAL:
        return "normal"

def set_foreground(window_handle: int) -> None:
    """
    Brings a window to the foreground and restores it if it is minimized.

    Args:
        window_handle (int): The handle to the window.

    Returns:
        None
    """
    if get_window_state(window_handle) == "minimized":
        win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
    else:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        win32gui.SetForegroundWindow(window_handle)

def get_window_info(window_handle: int, info_type: str = None) -> tuple[str, int]:
    """
    Returns the window handle and window text (if available) of a window.

    Args:
        window_handle (int): The handle to the window.
        info_type (str): Optional. The type of information to return. Can be "hwnd" to return only the window handle,
            "names" to return only the window text, or None (default) to return both.

    Returns:
        tuple[str, int]: A tuple containing the window handle (as an integer) and window text (as a string).
            If info_type is "hwnd", only the window handle is returned. If info_type is "names", only the window text
            is returned. Otherwise, both values are returned as a tuple.
    """
    if info_type == "names":
        window_text = win32gui.GetWindowText(window_handle)
        return window_text
    elif info_type == "hwnd":
        return window_handle
    else:
        window_text = win32gui.GetWindowText(window_handle)
        return window_handle, window_text


def find_all_windows(info_type: str = None, n: int = None) -> list[tuple[str, int]]:
    """
    Finds all visible windows and returns their window handle and window text (if available).

    Args:
        info_type (str): Optional. The type of information to return. Can be "hwnd" to return only the window handle,
            "names" to return only the window text, or None (default) to return both.
        n (int): Optional. The maximum number of windows to return. If not specified, all visible windows are returned.

    Returns:
        list[tuple[str, int]]: A list of tuples, where each tuple contains the window handle (as an integer) and window text
            (as a string). If info_type is "hwnd", only the window handle is included in the tuple. If info_type is "names",
            only the window text is included. Otherwise, both values are included in the tuple.
    """
    result = []

    def win_enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            if n and len(result) >= n:
                return False
            if info_type == "names":
                window_info = (win32gui.GetWindowText(hwnd),)
            elif info_type == "hwnd":
                window_info = (hwnd,)
            else:
                window_info = (hwnd, win32gui.GetWindowText(hwnd))
            result.append(window_info)
        return True

    win32gui.EnumWindows(win_enum_handler, None)
    return result


def find_window_by_name(name: str) -> int:
    """
    Finds a visible window with a specific name and returns its window handle.

    Args:
        name (str): The name (or a substring of the name) of the window to find.

    Returns:
        int: The handle to the window, if found. Otherwise, returns 0.
    """
    windows = find_all_windows(info_type="names", n=None)
    for window in windows:
        if name.upper() in window[1].upper():
            return window[0]
    return 0


def set_foreground_window_by_name(name: str) -> None:
    """
    Brings a window with a specific name to the foreground, if it is found.

    Args:
        name (str): The name (or a substring of the name) of the window to bring to the foreground.
    """
    window_handle = find_window_by_name(name)
    if window_handle:
        set_foreground(window_handle)



def run(app):
    win32api.WinExec(app)


            
class window:
    def __init__(self, name):
        a = find_all_windows(info_type=None, n=None)
        self.handle = 0
        for i in a:
            if name.upper() in i[1].upper():
                self.handle = i[0]
                self.name = i[1]

    def SetForeground(self):
        set_foreground(self.handle)

    def IsForeground(self):
        if win32gui.GetForegroundWindow() == self.handle:
            return True
        else:
            return False

    def Minimize(self):
        win32gui.ShowWindow(self.handle, 11)

    def Maximize(self):
        win32gui.ShowWindow(self.handle, 3)

    def Restore(self):
        win32gui.ShowWindow(self.handle, 1)



class TkWindow:
    """
    A class to create a new Tkinter window.

    Attributes:
        root (Tk): The root window.
        geometry (str): The geometry of the window.
        title (str): The title of the window.

    Methods:
        show: Displays the window.
        label: Adds a label widget to the window.
        image: Adds an image widget to the window.
    """

    def __init__(self, geometry=None, title='Tkinter'):
        """
        Initializes a new instance of the TkWindow class.

        Args:
            geometry (str): The geometry of the window.
            title (str): The title of the window.
        """
        self.root = Tk()
        self.geometry = geometry
        self.title = title

        if self.geometry:
            self.root.geometry(self.geometry)
        self.root.title(self.title)

    def show(self, always_on_top=False):
        """
        Displays the window.

        Args:
            always_on_top (bool): If True, the window is always on top of other windows.
        """
        if always_on_top:
            self.root.attributes("-topmost", True)
            self.root.overrideredirect(True)
            self.root.wm_attributes('-transparentcolor', self.root['bg'])

        self.root.after(5000, lambda: self.root.destroy())
        self.root.mainloop()

    def label(self, text, font=("Times New Roman", 15)):
        """
        Adds a label widget to the window.

        Args:
            text (str): The text to display in the label.
            font (tuple): The font to use for the label.
        """
        l = Label(self.root, text=text, font=font, bg="grey", fg="white")
        l.grid(row=0, column=1)

    def image(self, url):
        """
        Adds an image widget to the window.

        Args:
            url (str): The URL of the image to display.
        """
        url = requests.get(url).content
        im = Image.open(BytesIO(url))
        im = im.resize(size=(100, 100))
        photo = ImageTk.PhotoImage(im)
        label = Label(self.root, image=photo)
        label.image = photo
        label.grid(row=0, column=0)
        