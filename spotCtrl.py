import time
import windowEdit
import win32api as win
import win32gui as gui
import keyboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth

id = 'enter client id'
secret = 'enter client secret'
un = 'enter username'

window = windowEdit.window
tk = windowEdit.TkWindow

VKC = {'backspace': 8, 'tab': 9, 'clear': 254, 'enter': 13, 'shift': 16, 'ctrl': 17, 'alt': 18, 'pause': 19, 'caps_lock': 20, 'esc': 27, 'spacebar': 32, 'page_up': 33, 'page_down': 34, 'end': 35, 'home': 36, 'left arrow': 37, 'up arrow': 38, 'right arrow': 39, 'down arrow': 40, 'select': 41, 'print': 42, 'execute': 43, 'print_screen': 44, 'ins': 45, 'del': 46, 'help': 47, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57, 'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90, 'n 0': 96, 'n 1': 97, 'n 2': 98, 'n 3': 99, 'n 4': 100, 'n 5': 101, 'n 6': 102, 'n 7': 103, 'n 8': 104, 'n 9': 105, 'multiply': 106, 'plus': 107, 'separator key': 108, 'minus': 109, 'decimal key': 110, 'divide': 111, 'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119, 'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127, 'F17': 128, 'F18': 129, 'F19': 130, 'F20': 131, 'F21': 132, 'F22': 133, 'F23': 134, 'F24': 135, 'num_lock': 144, 'scroll_lock': 145, 'left_shift': 160, 'right_shift ': 161, 'left_control': 162, 'right_control': 163, 'left_menu': 164, 'right_menu': 165, 'browser_back': 166, 'browser_forward': 167, 'browser_refresh': 168, 'browser_stop': 169, 'browser_search': 170, 'browser_favorites': 171, 'browser_start_and_home': 172, 'volume_mute': 173, 'volume_Down': 174, 'volume_up': 175, 'next_track': 176, 'previous_track': 177, 'stop_media': 178, 'play/pause_media': 179, 'start_mail': 180, 'select_media': 181, 'start_application_1': 182, 'start_application_2': 183, 'attn': 246, 'crsel': 247, 'exsel': 248, 'play': 250, 'zoom': 251, '+': 187, ',': 188, '-': 189, '.': 190, '/': 191, '`': 192, ';': 186, '[': 219, '\\': 220, ']': 221, "'": 222}
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,client_secret=secret, redirect_uri="http://127.0.0.1:8080", scope="user-read-currently-playing user-modify-playback-state user-read-playback-state user-read-private", username=un))

if sp.current_playback()==None and window('spotify').handle==0:
    windowEdit.run('spotify')

def getname():
    if not window('netflix').handle==0:
        return 'netflix'
    elif not window('watch').handle==0:
        return 'watch'
    elif not window('youtube').handle==0:
        return 'youtube'
    return input('window name: ')

def pause_play():
    if sp.current_playback()['is_playing'] is True:
        sp.pause_playback()
    elif sp.current_playback()['is_playing'] is False:
        sp.start_playback()

def get_artists(artists):
    artist = ''
    for i in range(len(artists)):
        if i == 0:
            artist = artists[i]
        elif i == len(artists)-1:
            artist = artist + f' and {artists[i]}'
        else:
            artist = artist + f', {artists[i]}'
    return artist

def what_song():
    a = sp.current_playback()
    artists = []
    name = a['item']['name']
    for i in a['item']['artists']:
        artists.append(i['name'])
    artist = get_artists(artists)
    return f"'{name}' by {artist}"

def add_artist(track):
    artists = []
    for i in track['artists']:
        artists.append(i['name'])
    return get_artists(artists)



def playlist_songs():
    try:
        if sp.current_user_playing_track()['context']==None:
            current_playlist = sp.current_user_saved_tracks(50)['items']
        else:
            current_playlist = sp.playlist(sp.current_user_playing_track()['context']['uri'].split(':')[-1])
            current_playlist = current_playlist['tracks']['items']
        songs = []
        for i in current_playlist:
            name = i['track']['name']
            artist = add_artist(i['track'])
            songs.append(f"'{name}' by {artist}")
        return songs
    except:
        return []

def volume(l):
    """
    volume +/- 10
    """
    v = sp.current_playback()['device']['volume_percent']
    if l == 0:
        if (v+10) > 100:
            sp.volume(100)
        else:
            sp.volume(v+10)
    if l == 1:
        if (v+10) < 0:
            sp.volume(0)
        else:
            sp.volume(v-10)

def seek(l):
    """
    seek +/- 10 secs
    """
    prog = sp.current_playback()['progress_ms']
    if l == 0:
        if (prog-10000) < 0:
            sp.seek_track(0)
        else:
            sp.seek_track(prog - 10000)
    if l == 1:
        sp.seek_track(prog + 10000)

def watching(w, now):
    """
    Pauses music, goes to tab with video, presses
    the space key in order to play video and disables rest of program.
    If space key is pressed again, video will pause and program will resume.
    """
    if not w.handle == 0:
        w.SetForeground()
        keyboard.press_and_release('space')
        if sp.current_playback()['is_playing'] is True:
            sp.pause_playback()
        while True:
            if keyboard.is_pressed('space'):
                break
        
        window(now).SetForeground()
        sp.start_playback()

def tk_song(ws):
    im = sp.current_playback()['item']['album']['images'][0]
    a = tk()
    a.label(ws)
    a.image(im['url'])
    a.show(1)
    

def previous():
    try:
        sp.previous_track()
    except:
        pass

def show_song():
    """
    Display the current song with its position in the playlist. at the top left corner of screen
    """
    w_s = what_song()
    pl = playlist_songs()
    s_n = 0
    if w_s in pl:
        s_n = pl.index(w_s)+1
    if not s_n==0:
        ws = w_s+' '+str(s_n)+'/'+str(len(pl))
    else:
        ws = w_s
    tk_song(ws)    

def watch_window(wn):
    """
    Monitor the active window and perform the 'watching' action.
    """
    d = gui.GetWindowText(gui.GetForegroundWindow())
    watching(window(wn),d)
    time.sleep(0.5)

    
def manual():
    """
    Main function to monitor and execute key actions in a loop.
    """
    win.keybd_event(VKC['multiply'], 0, windowEdit.win32con.KEYEVENTF_KEYUP, 0)
    wn = getname()

    key_actions = {
        VKC['left arrow']: previous,
        VKC['right arrow']: sp.next_track,
        VKC['n 0']: pause_play,
        VKC['down arrow']: lambda: seek(0),
        VKC['up arrow']: lambda: seek(1),
        VKC['plus']: lambda: volume(0),
        VKC['minus']: lambda: volume(1),
        VKC['/']: show_song,
        VKC['divide']: lambda: watch_window(wn),
    }

    loop = False
    while True:
        if win.GetAsyncKeyState(VKC['multiply']) != 0:
            time.sleep(1)
            loop = not loop

        if loop:
            for key, action in key_actions.items():
                if win.GetAsyncKeyState(key) != 0:
                    action()
                    time.sleep(0.5)
        else:
            time.sleep(0.5)  # small delay to avoid high CPU usage


manual()