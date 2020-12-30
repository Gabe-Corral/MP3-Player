import tkinter as tk
import os, glob
from pathlib import Path
import vlc

class Main:

    def __init__(self):
        self.root = tk.Tk()

        #canvas one
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

        self.directory = Path("/home/gaubay/Music/music/")
        self.path = "/home/gaubay/Music/music/"
        self.folder_names = []

        self.playing = False
        self.buttons = []

        self.get_folder_name()

    def get_folder_name(self):
        for file in self.directory.glob("**"):
            if len(str(file).split(self.path)) > 1:
                self.folder_names.append(str(file).split(self.path)[1])
        self.start_gui()

    def display_folder_names(self):
        self.folder_names.sort()
        i = 0
        for name in self.folder_names:
            tk.Button(self.frame_one, text=name, width=40,
            bg='#073642', fg='#eee8d5', command=lambda name=name:
            self.display_details(name)).pack()
            i += 30

    def start_gui(self):
        self.root.wm_title("EPIC MP3 PLAYER")
        self.root.geometry("1200x700")

        self.display_folder_names()

        tk.mainloop()

    def display_details(self, foldername):
        if len(self.buttons) > 0:
            self.delete_buttons()

        local_path = Path(self.path + foldername)
        
        for file in local_path.glob("**/*"):
            filename = str(file).split(self.path + foldername + "/")[1]
            button = tk.Button(self.root, text=filename,
            command=lambda filename=filename: self.play_song(self.path + foldername + "/" + filename)).pack()
            self.buttons.append(button)

        tk.Button(self.root, text="Stop", command=self.stop_song).pack()

    def delete_buttons(self):
        for child in self.root.winfo_children():
            if str(child).startswith(".!button"):
                child.destroy()

    def play_song(self, song_path):
        print(song_path)
        self.currrnt_song = vlc.MediaPlayer(song_path)
        self.currrnt_song.play()

    def stop_song(self):
        self.currrnt_song.stop()

if __name__=="__main__":
    main = Main()
