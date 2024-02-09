import os
import pygame
import tkinter as tk
from tkinter import filedialog
import random

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Player")
        self.geometry("600x400")
        self.configure(bg="#333333")  # Set background color

        pygame.init()
        pygame.mixer.init()

        self.playlist = []
        self.current_track = 0
        self.paused = False

        self.create_widgets()
        self.pulsate_play_button()
        self.create_animation()

    def create_widgets(self):
        label = tk.Label(self, text="Music Player", font=("Arial", 24), bg="#333333", fg="#ffffff")
        label.pack(pady=15)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, bg="#444444", font=("Arial", 12), height=10, fg="#ffffff", selectbackground="#555555")
        self.listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.play_button = tk.Button(self, text="▶ Play", command=self.play_selected_music, font=("Arial", 14), bg="#4CAF50", fg="#ffffff")
        self.play_button.pack(side=tk.LEFT, padx=20)
        self.play_button.pulsating = False  # Custom attribute to control pulsating effect

        pause_button = tk.Button(self, text="❚❚ Pause", command=self.pause_music, font=("Arial", 14), bg="#FFC107", fg="#333333")
        pause_button.pack(side=tk.LEFT, padx=20)

        resume_button = tk.Button(self, text="► Resume", command=self.resume_music, font=("Arial", 14), bg="#2196F3", fg="#ffffff")
        resume_button.pack(side=tk.LEFT, padx=20)

        stop_button = tk.Button(self, text="■ Stop", command=self.stop_music, font=("Arial", 14), bg="#FF5722", fg="#ffffff")
        stop_button.pack(side=tk.LEFT, padx=20)

        volume_label = tk.Label(self, text="Volume", font=("Arial", 12), bg="#333333", fg="#ffffff")
        volume_label.pack(side=tk.LEFT, padx=10)

        self.volume_scale = tk.Scale(self, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_volume, bg="#333333", fg="#ffffff", highlightbackground="#333333")
        self.volume_scale.set(0.5)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        add_button = tk.Button(self, text="➕ Add Music", command=self.add_music, font=("Arial", 14), bg="#607D8B", fg="#ffffff")
        add_button.pack(side=tk.LEFT, padx=20)

        remove_button = tk.Button(self, text="➖ Remove Music", command=self.remove_music, font=("Arial", 14), bg="#E91E63", fg="#ffffff")
        remove_button.pack(side=tk.LEFT, padx=20)

    def pulsate_play_button(self):
        if self.playlist and hasattr(self, "play_button"):
            if not hasattr(self.play_button, "pulsating") or not self.play_button.pulsating:
                self.play_button.pulsating = True
                self.pulsate_button(self.play_button)
        else:
            self.play_button.pulsating = False
        self.after(500, self.pulsate_play_button)

    def create_animation(self):
        self.canvas = tk.Canvas(self, width=20, height=20, bg="#333333", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=5)
        self.animation_speed = 2  # Change this value to adjust animation speed
        self.bounce_animation()

    def bounce_animation(self):
        x, y = 10, 10
        dx, dy = 0, self.animation_speed

        def animate():
            nonlocal x, y, dx, dy
            self.canvas.delete("all")
            self.canvas.create_oval(x, y, x + 20, y + 20, fill="#4CAF50", outline="#4CAF50")
            x += dx
            y += dy

            if y >= 100 or y <= 0:
                dy *= -1

            self.after(10, animate)

        animate()

    def pulsate_button(self, button, scale_min=1.0, scale_max=1.3, speed=0.005, direction=1):
        if button.pulsating:
            font_config = button.cget("font")
            if font_config:
                font_size = int(font_config.split()[-1])  # Extract font size
                new_font_size = font_size + (speed * direction)
                if new_font_size < scale_min or new_font_size > scale_max:
                    direction *= -1
                font = ("Arial", int(new_font_size))
                button.config(font=font)
                button.config(bg=self.get_random_color(), fg="#ffffff")
                self.after(10, self.pulsate_button, button, scale_min, scale_max, speed, direction)
            else:
                button.pulsating

    def get_random_color(self):
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def add_music(self):
        tk.Tk().withdraw()  # Hide the main window
        music_files = filedialog.askopenfilenames(title="Select Music Files", filetypes=[("Audio Files", "*.mp3")])
        if music_files:
            self.playlist.extend(music_files)
            self.update_listbox()
            if not pygame.mixer.music.get_busy():
                self.play_selected_music()

    def remove_music(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.playlist[index]
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for track in self.playlist:
            self.listbox.insert(tk.END, os.path.basename(track))

    def play_selected_music(self):
        if self.playlist:
            track = self.playlist[self.current_track]
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(self.volume_scale.get())
            pygame.mixer.music.play()
            self.paused = False

    def pause_music(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def resume_music(self):
        if pygame.mixer.music.get_busy() and self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
