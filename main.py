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

class Main:

    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='#073642')

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
        self.canvas_two = tk.Canvas(self.wrapper_two, height=100)
        self.frame_two = tk.Frame(self.canvas_two)
        self.canvas_two.pack(side=tk.LEFT, fill="x")
        self.canvas_two.create_window((0, 0), window=self.frame_two, anchor="nw")
        self.wrapper_two.pack(fill="x", side="bottom")

        self.directory = Path("/home/gaubay/Music/music/")
        self.path = "/home/gaubay/Music/music/"
        self.folder_names = []
        self.file_names = []
        self.current_background_path = ""

        self.playing = False
        self.paused = False
        self.buttons = []
        self.volume = 50
        self.tag = id3.Tag()
        self.current_working_directory = ""
        self.song_titles = {}
        self.after = 0

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
            self.song_titles[track_num] = [title, filename, duration]
        self.create_label_frame()
        for i in range(len(self.song_titles) + 1):
            if i > 0:
                button = tk.Button(self.frame_three, text=self.song_titles[str(i)][0],
                 width=40, command=lambda i=i: self.play_song(foldername, i,
                self.song_titles[str(i)][2]),
                bg='#073642', fg='#eee8d5').pack()
                self.buttons.append(i)

    def delete_buttons(self):
        self.frame_three.destroy()
        self.wrapper_three.destroy()
        self.canvas_three.destroy()
        self.y_scroll_two.destroy()

    def create_controls(self):
        tk.Button(self.frame_two, text="Pause/Play", command=self.pause_play,
        width=20, bg='#073642', fg='#eee8d5').pack()
        tk.Button(self.frame_two, text="Up",
        width=20, bg='#073642', fg='#eee8d5',
        command=lambda : self.set_volume("up")).pack()
        tk.Button(self.frame_two, text="Down",
        width=20, bg='#073642', fg='#eee8d5',
        command=lambda : self.set_volume("down")).pack()

    def pause_play(self):
        if self.playing:
            self.currrnt_song.pause()
            self.paused = True
        elif self.paused:
            self.currrnt_song.play()
            self.paused = False

    def play_song(self, foldername, index, duration):
        if self.playing == False:
            self.playing = True
            self.currrnt_song = vlc.MediaPlayer(self.path
           + foldername + "/" + self.song_titles[str(index)][1])
            self.currrnt_song.play()

            if self.after != 0 :
                self.root.after_cancel(self.after)

            self.after = self.root.after(int(duration)*1000, lambda:
            self.playing_duration(foldername, index))
        elif self.playing == True:
            self.stop_song()
            self.currrnt_song = vlc.MediaPlayer(self.path
           + foldername + "/" + self.song_titles[str(index)][1])
            self.currrnt_song.play()
            self.after = self.root.after(int(duration)*1000, lambda:
            self.playing_duration(foldername, index))

    def playing_duration(self, foldername, index):
        print("Ended", index)
        index += 1
        duration = duration = eyed3.load(self.path
        + foldername + "/" + self.song_titles[str(index)][1]).info.time_secs
        self.stop_song()
        self.play_song(foldername, index, duration)
        print("playing", index)

    def set_volume(self, scale_up_down):
        if scale_up_down == "up":
            self.volume += 5
        elif scale_up_down == "down":
            self.volume -= 5
        self.currrnt_song.audio_set_volume(self.volume)

    def create_label_frame(self):
        self.wrapper_three = tk.LabelFrame(self.root)
        self.canvas_three = tk.Canvas(self.wrapper_three)
        self.canvas_three.pack(side=tk.LEFT, fill="y")
        self.y_scroll_two = tk.Scrollbar(self.wrapper_three, orient="vertical",
        command=self.canvas_three.yview)
        self.y_scroll_two.pack(side=tk.RIGHT, fill="y")
        self.frame_three = tk.Frame(self.canvas_three)
        self.canvas_three.configure(yscrollcommand=self.y_scroll_two.set, bg='#073642')
        self.canvas_three.bind("<Configure>",
        lambda e: self.canvas_three.configure(scrollregion = self.canvas_three.bbox('all')))
        self.canvas_three.create_window((0, 0), window=self.frame_three, anchor="nw")
        self.wrapper_three.pack(fill="y", side="left")


    def stop_song(self):
        self.currrnt_song.stop()

if __name__=="__main__":
    main = Main()
