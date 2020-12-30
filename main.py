import tkinter as tk
import os, glob
from pathlib import Path
import vlc
import json
from PIL import ImageTk, Image

class Main:

    def __init__(self):
        self.root = tk.Tk()

        #canvas/labelframe one
        self.root.configure(bg='#073642')
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

        self.playing = False
        self.paused = False
        self.buttons = []
        self.current_background_path = ""
        self.volume = 50

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
        if len(self.buttons) > 0:
            self.delete_buttons()

        local_path = Path(self.path + foldername)

        for file in local_path.glob("**/*.mp3"):
            filename = str(file).split(self.path + foldername + "/")[1]
            button = tk.Button(self.root, text=filename, width=40,
            command=lambda filename=filename: self.play_song(self.path +
            foldername + "/" + filename)).pack()
            self.file_names.append(filename)
            self.buttons.append(button)

        # for file in local_path.glob("**/*.jpg"):
        #     print(str(file))
        #     self.current_background_path = str(file)
        #     canvas = tk.Canvas(width=600, height=800)
        #     canvas.pack(expand=tk.YES, fill=tk.BOTH)
        #     image = ImageTk.PhotoImage(Image.open(self.current_background_path))
        #     canvas.create_image(10, 10, image=image, anchor=tk.NW)

    def delete_buttons(self):
        for child in self.root.winfo_children():
            if str(child).startswith(".!button"):
                child.destroy()

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

    def play_song(self, song_path):
        if self.playing == False:
            self.playing = True
            self.currrnt_song = vlc.MediaPlayer(song_path)
            self.currrnt_song.play()
        elif self.playing == True:
            self.stop_song()
            self.currrnt_song = vlc.MediaPlayer(song_path)
            self.currrnt_song.play()

    def set_volume(self, scale_up_down):
        if scale_up_down == "up":
            self.volume += 5
        elif scale_up_down == "down":
            self.volume -= 5
        self.currrnt_song.audio_set_volume(self.volume)


    def stop_song(self):
        self.currrnt_song.stop()

if __name__=="__main__":
    main = Main()
