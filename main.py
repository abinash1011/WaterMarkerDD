import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")

        # Configure styles
        self.root.configure(bg="#e6e6e6")
        self.title_font = ("Helvetica", 16, "bold")
        self.label_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")

        self.video_path = ""
        self.image_path = ""
        self.watermark_image = None
        self.watermark_alpha = 0.5
        self.watermark_position = (20, 20)

        self.video_label = tk.Label(root, text="Upload Video:", font=self.title_font, bg="#e6e6e6")
        self.video_label.pack(pady=(10, 5))

        self.video_button = tk.Button(root, text="Choose Video", font=self.button_font, command=self.upload_video)
        self.video_button.pack(pady=5)

        self.image_label = tk.Label(root, text="Upload Watermark Image:", font=self.title_font, bg="#e6e6e6")
        self.image_label.pack(pady=(10, 5))

        self.image_button = tk.Button(root, text="Choose Image", font=self.button_font, command=self.upload_image)
        self.image_button.pack(pady=5)

        self.transparency_label = tk.Label(root, text="Transparency:", font=self.title_font, bg="#e6e6e6")
        self.transparency_label.pack(pady=(10, 5))

        self.transparency_slider = tk.Scale(root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_transparency, bg="#e6e6e6")
        self.transparency_slider.set(0.5)
        self.transparency_slider.pack(pady=5)

        self.position_label = tk.Label(root, text="Position (X, Y):", font=self.title_font, bg="#e6e6e6")
        self.position_label.pack(pady=(10, 5))

        self.position_x_entry = tk.Entry(root, font=self.label_font)
        self.position_y_entry = tk.Entry(root, font=self.label_font)
        self.position_x_entry.pack(pady=5)
        self.position_y_entry.pack(pady=5)

        self.position_button = tk.Button(root, text="Set Position", font=self.button_font, command=self.set_position)
        self.position_button.pack(pady=5)

        self.process_button = tk.Button(root, text="Process Video", font=self.button_font, command=self.process_video)
        self.process_button.pack(pady=10)

    def upload_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            try:
                self.watermark_image = Image.open(self.image_path)
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {str(e)}")

    def set_transparency(self, value):
        self.watermark_alpha = float(value)

    def set_position(self):
        x = int(self.position_x_entry.get())
        y = int(self.position_y_entry.get())
        self.watermark_position = (x, y)

    def process_video(self):
        if not self.video_path or not self.image_path:
            messagebox.showerror("Error", "Please upload both video and watermark image.")
            return

        messagebox.showinfo("Processing", "Video processing is in progress...")

root = tk.Tk()
app = WatermarkApp(root)
root.mainloop()
