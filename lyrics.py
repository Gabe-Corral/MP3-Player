import tkinter as tk
import requests
import json
import lyricsgenius
from PIL import ImageTk,Image
from urllib.request import urlopen
from urllib.error import HTTPError
from io import BytesIO
import wget
import time


class LyricsGui:

    def __init__(self, parent, child, artist, song):
        self.parent = parent
        self.child = child
        self.artist_name = artist
        self.song_name = song
        self.image = ""
        self.lyrics = ""
        self.filename = ""
        self.show_image = True
        self.get_artist_image()

    def get_artist_image(self):
        with open('config.json') as json_file:
            art = json.load(json_file)
            if self.song_name in art['artwork']:
                self.get_lyrics()
            else:
                url = "https://genius.p.rapidapi.com/search"
                querystring = {"q": self.song_name + self.artist_name}
                headers = {
                    'x-rapidapi-key': "",
                    'x-rapidapi-host': "genius.p.rapidapi.com"
                    }
                response = requests.request("GET", url, headers=headers, params=querystring)
                data = json.loads(response.text)
                self.image = data["response"]['hits'][0]['result']['header_image_thumbnail_url']
                try:
                    self.filename = wget.download(self.image, out="artwork/")
                    art['artwork'][self.song_name] = self.filename[9:]

                    with open('config.json', 'w') as json_write:
                            json.dump(art, json_write)
                            self.get_lyrics()
                except HTTPError:
                    print("error")
                    self.show_image = False
                    self.get_lyrics()


    def get_lyrics(self):
        genius = lyricsgenius.Genius("")
        song = genius.search_song(self.song_name, self.artist_name)
        self.lyrics = song.lyrics
        self.create_new_window()

    def create_new_window(self):
        self.child.configure(bg='#073642')
        self.child.wm_title("EPIC MP3 PLAYER")
        self.child.geometry("700x800")

        #frame
        wrapper = tk.LabelFrame(self.child, bg='#073642')
        canvas = tk.Canvas(wrapper, width=680, bg='#073642')
        canvas.pack(side=tk.LEFT)
        y_scroll = tk.Scrollbar(wrapper, orient="vertical",
        command=canvas.yview)
        y_scroll.pack(side=tk.RIGHT, fill="y")
        frame = tk.Frame(canvas)
        canvas.configure(yscrollcommand=y_scroll.set, bg='#073642')
        canvas.bind("<Configure>",
        lambda e: canvas.configure(scrollregion = canvas.bbox('all')))
        canvas.create_window((0, 0), window=frame, width=680, anchor="nw")
        wrapper.pack(fill="y")

        if self.filename != "" or self.show_image:
            with open("config.json") as json_file:
                data = json.load(json_file)

                im = Image.open("artwork/" + data["artwork"][self.song_name]).resize((700, 600))
                photo = ImageTk.PhotoImage(im)
                label = tk.Label(self.child, image=photo)
                label.image = photo
                label.pack()

        tk.Label(frame, text=self.lyrics, bg='#073642', fg='#eee8d5',
        width=100).pack()
