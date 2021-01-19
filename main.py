import tkinter as tk
import os, glob
from pathlib import Path
import vlc
import json
from PIL import ImageTk, Image
from eyed3 import id3
import eyed3
import collections
import time
from lyrics import LyricsGui
import tkinter.ttk as ttk
from ttkthemes import themed_tk as theme

class Main:

    def __init__(self):
        self.root = theme.ThemedTk()
        self.root.configure(bg='#073642')
        self.root.get_themes()
        self.root.set_theme("plastik")

        #canvas/labelframe 1
        self.wrapper_one = tk.LabelFrame(self.root)
        self.canvas = tk.Canvas(self.wrapper_one)
        self.canvas.pack(side=tk.LEFT, fill="y")
        self.y_scroll = tk.Scrollbar(self.wrapper_one, orient="vertical",
        command=self.canvas.yview)
        self.y_scroll.pack(side=tk.RIGHT, fill="y")
        self.frame_one = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.y_scroll.set, bg='#073642')
        self.canvas.bind("<Configure>",
        lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.frame_one, anchor="nw")
        self.wrapper_one.pack(fill="y", side="left")

        #labelframe 2
        self.wrapper_two = tk.LabelFrame(self.root)
        self.canvas_two = tk.Canvas(self.wrapper_two, height=100, width=900)
        self.frame_two = tk.Frame(self.canvas_two)
        self.canvas_two.pack(side=tk.LEFT, fill="x")
        self.canvas_two.create_window((0, 0), window=self.frame_two, anchor="nw",
        height=100, width=900)
        self.wrapper_two.pack(fill="x", side="bottom")

        self.directory = Path("/home/gaubay/Music/music/")
        self.path = "/home/gaubay/Music/music/"
        self.folder_names = []
        self.file_names = []
        self.current_background_path = ""

        #button images
        self.play_button_img = Image.open("/home/gaubay/project/python/MP3-Player/assets/play.png").resize((25,25))
        self.pause_button_img = Image.open("/home/gaubay/project/python/MP3-Player/assets/pause.png").resize((25,25))
        self.skip_button_img = Image.open("/home/gaubay/project/python/MP3-Player/assets/skip.png").resize((25,25))
        self.unskip_button_img = Image.open("/home/gaubay/project/python/MP3-Player/assets/unskip.png").resize((25,25))

        self.pause_btn = ""
        self.play_btn = ""
        self.slider = ""
        self.skip = ""
        self.unskip = ""
        self.current_time = 0
        self.current_sone_name = ""
        self.force_next_song = False

        self.playing = False
        self.paused = False
        self.buttons = []
        self.volume = 50
        self.tag = id3.Tag()
        self.current_working_directory = ""
        self.song_titles = {}
        self.after = 0
        self.index = 0
        self.foldername = ""

        self.get_folder_name()

    def get_folder_name(self):
        for file in self.directory.glob("**"):
            if len(str(file).split(self.path)) > 1:
                self.folder_names.append(str(file).split(self.path)[1])
        self.start_gui()

    def display_folder_names(self):
        self.folder_names.sort()
        for name in self.folder_names:
            tk.Button(self.frame_one, text=name, width=40,
            bg='#073642', fg='#eee8d5', command=lambda name=name:
            self.display_details(name)).pack()

    def start_gui(self):
        self.root.wm_title("EPIC MP3 PLAYER")
        self.root.geometry("1200x700")

        self.display_folder_names()
        self.create_controls()

        tk.mainloop()

    def display_details(self, foldername):
        self.song_titles = {}
        if len(self.buttons) > 0:
            self.delete_buttons()

        local_path = Path(self.path + foldername)

        for file in local_path.glob("**/*.mp3"):
            filename = str(file).split(self.path + foldername + "/")[1]
            self.tag.parse(self.path + foldername + "/" + filename)
            track_num = str(self.tag.track_num).split(",")[0].split("(")[1]
            title = track_num + " " + self.tag.title
            duration = eyed3.load(self.path + foldername + "/" + filename).info.time_secs
            artist = self.tag.artist
            self.song_titles[track_num] = [title, filename, duration, artist]
        self.create_label_frame()
        for i in range(len(self.song_titles) + 1):
            if i > 0:
                button = tk.Button(self.frame_three, text=self.song_titles[str(i)][0],
                width=100, command=lambda i=i: self.play_song(foldername, i,
                self.song_titles[str(i)][2]),
                bg='#073642', fg='#eee8d5').pack()
                self.buttons.append(i)

    def delete_buttons(self):
        self.frame_three.destroy()
        self.wrapper_three.destroy()
        self.canvas_three.destroy()
        self.y_scroll_two.destroy()

    def change_play_pause(self):
        play = ImageTk.PhotoImage(self.play_button_img)
        pause = ImageTk.PhotoImage(self.pause_button_img)
        if self.playing == False:
            self.play_btn.destroy()
            self.pause_btn = tk.Button(self.frame_two, image=pause, command=self.pause_play, borderwidth=0)
            self.pause_btn.image = pause
            self.pause_btn.place(x=30, y=0)
        else:
            self.pause_btn.destroy()
            self.play_btn = tk.Button(self.frame_two, image=play, command=self.pause_play, borderwidth=0)
            self.play_btn.image = play
            self.play_btn.place(x=30, y=0)

    def create_controls(self):
        play = ImageTk.PhotoImage(self.play_button_img)
        pause = ImageTk.PhotoImage(self.pause_button_img)
        skip_img = ImageTk.PhotoImage(self.skip_button_img)
        unskip_img = ImageTk.PhotoImage(self.unskip_button_img)

        self.pause_btn = tk.Button(self.frame_two, image=pause, command=self.pause_play, borderwidth=0)
        self.pause_btn.image = pause
        self.pause_btn.place(x=30, y=0)

        self.skip = tk.Button(self.frame_two, image=skip_img, borderwidth=0,
        command=lambda: self.playing_duration(self.foldername, self.index))
        self.skip.image = skip_img
        self.skip.place(x=60, y=0)

        self.unskip = tk.Button(self.frame_two, image=unskip_img, borderwidth=0,
        command=self.unskip_song)
        self.unskip.image = unskip_img
        self.unskip.place(x=0, y=0)

        self.volume_bar()

        tk.Button(self.frame_two, text="Lyrics",
        command= lambda: self.get_lyrics(self.song_titles[str(self.index)][3],
        self.song_titles[str(self.index)][0]),
        width=20, bg='#073642', fg='#eee8d5').place(x=630, y=0)

    def volume_bar(self):
        volume_label = tk.Label(self.frame_two, text="Volume").place(x=0, y=50)
        self.volume_control = ttk.Scale(self.frame_two, from_=0,to=150,
        command=self.set_volume, value=50)
        self.volume_control.place(x=0, y=75, height=15)

    def set_volume(self, x):
        new_volume = int(self.volume_control.get())
        self.currrnt_song.audio_set_volume(new_volume)

    def pause_play(self):
        if self.playing:
            self.root.after_cancel(self.after)
            self.currrnt_song.pause()
            self.playing = False
            self.paused = True
            self.change_play_pause()
        elif self.paused:
            self.currrnt_song.play()
            self.paused = False
            self.playing = True
            self.force_next_song = True
            self.update_timer()
            self.change_play_pause()

    def play_song(self, foldername, index, duration):
        self.foldername = foldername
        song_name = self.song_titles[str(index)][0][2:]
        self.index = index

        if self.playing == False:
            self.playing = True
            self.change_play_pause()
            self.currrnt_song = vlc.MediaPlayer(self.path
           + foldername + "/" + self.song_titles[str(index)][1])
            self.currrnt_song.play()
            self.create_slider(duration, song_name)

            if self.after != 0 :
                self.root.after_cancel(self.after)

            self.after = self.root.after(int(duration)*1000, lambda:
            self.playing_duration(foldername, index))
        elif self.playing == True:
            self.stop_song()
            self.root.after_cancel(self.after)
            self.currrnt_song = vlc.MediaPlayer(self.path
           + foldername + "/" + self.song_titles[str(index)][1])
            self.currrnt_song.play()
            self.create_slider(duration, song_name)
            self.after = self.root.after(int(duration)*1000, lambda:
            self.playing_duration(foldername, index))

    def unskip_song(self):
        self.index -= 1
        if self.index >= 1:
            duration = duration = eyed3.load(self.path
            + self.foldername + "/" + self.song_titles[str(self.index)][1]).info.time_secs
            self.stop_song()
            self.play_song(self.foldername, self.index, duration)
        else:
            self.stop_song()

    def playing_duration(self, foldername, index):
        index += 1
        if index <= len(self.song_titles):
            duration = duration = eyed3.load(self.path
            + foldername + "/" + self.song_titles[str(index)][1]).info.time_secs
            self.stop_song()
            self.play_song(foldername, index, duration)
        else:
            self.stop_song()

    def create_label_frame(self):
        self.wrapper_three = tk.LabelFrame(self.root, bg='#073642')
        self.canvas_three = tk.Canvas(self.wrapper_three)
        self.canvas_three.pack(side=tk.LEFT, fill="both", expand="yes")
        self.y_scroll_two = tk.Scrollbar(self.wrapper_three, orient="vertical",
        command=self.canvas_three.yview)
        self.y_scroll_two.pack(side=tk.RIGHT, fill="y")
        self.frame_three = tk.Frame(self.canvas_three)
        self.canvas_three.configure(yscrollcommand=self.y_scroll_two.set, bg='#073642')
        self.canvas_three.bind("<Configure>",
        lambda e: self.canvas_three.configure(scrollregion = self.canvas_three.bbox('all')))
        self.canvas_three.create_window((0, 0), window=self.frame_three,
        anchor="nw")
        self.wrapper_three.pack(fill="both", expand="yes")

    def create_slider(self, duration, song):
        self.duration = duration
        self.destroy_slider()
        skip_img = ImageTk.PhotoImage(self.skip_button_img)
        unskip_img = ImageTk.PhotoImage(self.unskip_button_img)
        self.slider = ttk.Scale(self.frame_two, from_=0,to=duration, orient=tk.HORIZONTAL,
        value=0, command=self.slide_song, length=350)
        self.song_label = tk.Label(self.frame_two, text=song)

        self.slider.place(x=200, y=50, height=15)
        self.song_label.place(x=340, y=30)
        self.current_time = 0
        self.update_timer()

    def slide_song(self, label):
        #self.time_label.config(text=int(self.slider.get()))
        self.currrnt_song.set_time(int(self.slider.get())*1000)

    def get_lyrics(self, artist, song):
        song_name = song[2:]
        LyricsGui(self.root, tk.Toplevel(self.root), artist, song_name)

    def update_timer(self, foldername=False):
        self.slider.config(value=self.current_time)
        self.current_time += 1
        if int(self.duration) <= self.current_time and self.force_next_song:
            self.force_next_song = False
            self.playing_duration(self.foldername, self.index)
        elif self.playing:
            self.slider_after = self.slider.after(1000, self.update_timer)

    def destroy_slider(self):
        if self.slider != "":
            self.slider.destroy()
            self.song_label.destroy()

    def stop_song(self):
        self.currrnt_song.stop()

if __name__=="__main__":
    main = Main()
