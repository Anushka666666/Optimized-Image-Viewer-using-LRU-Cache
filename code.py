import os
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

class ImageViewer:
    def __init__(self, master, cache_size=5):
        self.master = master
        master.title("LRU Cached Image Viewer")

        self.label = Label(master)
        self.label.pack()

        self.next_button = Button(master, text="Next", command=self.show_next_image)
        self.next_button.pack(side="right")

        self.prev_button = Button(master, text="Previous", command=self.show_prev_image)
        self.prev_button.pack(side="left")

        self.select_button = Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack()

        self.images = []
        self.index = 0
        self.cache = LRUCache(cache_size)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                           if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
            self.index = 0
            if self.images:
                self.show_image(self.images[self.index])

    def load_image(self, path):
        cached_img = self.cache.get(path)
        if cached_img:
            return cached_img
        img = Image.open(path)
        img = img.resize((500, 500), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        self.cache.put(path, tk_img)
        return tk_img

    def show_image(self, path):
        tk_img = self.load_image(path)
        self.label.config(image=tk_img)
        self.label.image = tk_img

    def show_next_image(self):
        if self.images:
            self.index = (self.index + 1) % len(self.images)
            self.show_image(self.images[self.index])

    def show_prev_image(self):
        if self.images:
            self.index = (self.index - 1) % len(self.images)
            self.show_image(self.images[self.index])

if __name__ == "__main__":
    root = Tk()
    viewer = ImageViewer(root, cache_size=5)  # cache last 5 images
    root.mainloop()
