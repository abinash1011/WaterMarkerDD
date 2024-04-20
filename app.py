import imageio
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance

class VideoWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Watermarking App")

        self.video_path = None
        self.watermark_path = None
        self.transparency = 0.5
        self.placement_options = ['Top-Left', 'Top-Right', 'Bottom-Left', 'Bottom-Right', 'Center']
        self.size_presets = {'Mini': 0.25, 'Small': 0.5, 'Medium': 1, 'Large': 2}
        self.watermark = None

        self.create_widgets()

    def create_widgets(self):
        # Configure style
        self.root.geometry("400x350")
        self.root.configure(bg="#f0f0f0")

        style = {"font": ("Arial", 10)}

        # Video selection button
        self.video_button = Button(self.root, text="Select Video", command=self.select_video, **style)
        self.video_button.pack(pady=5)

        # Watermark selection button
        self.watermark_button = Button(self.root, text="Select Watermark", command=self.select_watermark, **style)
        self.watermark_button.pack(pady=5)

        # Transparency slider
        self.transparency_label = Label(self.root, text="Transparency", **style)
        self.transparency_label.pack()
        self.transparency_slider = Scale(self.root, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, command=self.set_transparency, **style)
        self.transparency_slider.set(0.5)
        self.transparency_slider.pack()

        # Size preset dropdown
        self.size_preset_label = Label(self.root, text="Watermark Size Preset", **style)
        self.size_preset_label.pack()
        self.size_preset_var = StringVar(self.root)
        self.size_preset_var.set('Medium')
        self.size_preset_dropdown = OptionMenu(self.root, self.size_preset_var, *self.size_presets.keys(), command=self.set_size_preset)
        self.size_preset_dropdown.pack()

        # Placement options dropdown
        self.placement_label = Label(self.root, text="Watermark Placement", **style)
        self.placement_label.pack()
        self.placement_var = StringVar(self.root)
        self.placement_var.set(self.placement_options[0])
        self.placement_dropdown = OptionMenu(self.root, self.placement_var, *self.placement_options)
        self.placement_dropdown.pack()

        # Process button
        self.process_button = Button(self.root, text="Process", command=self.process_video, **style)
        self.process_button.pack(pady=10)

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])

    def select_watermark(self):
        self.watermark_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])

    def set_transparency(self, value):
        self.transparency = float(value)

    def set_size_preset(self, preset):
        size_factor = self.size_presets[preset]
        if self.watermark_path is not None:
            self.update_watermark_size(size_factor)

    def update_watermark_size(self, size_factor):
        if self.watermark_path is not None:
            watermark = Image.open(self.watermark_path)
            watermark = watermark.convert("RGBA")
            new_width = int(watermark.width * size_factor)
            new_height = int(watermark.height * size_factor)
            self.watermark = watermark.resize((new_width, new_height))

    def process_video(self):
        if self.video_path is None or self.watermark_path is None:
            messagebox.showerror("Error", "Please select video and watermark!")
            return

        placement = self.placement_var.get()

        reader = imageio.get_reader(self.video_path)
        fps = reader.get_meta_data()['fps']

        output_path = 'output_video.avi'
        writer = imageio.get_writer(output_path, fps=fps)

        for frame in reader:
            pil_frame = Image.fromarray(frame)
            position = self.calculate_position(pil_frame.size, self.watermark.size, placement)
            pil_frame = self.apply_watermark(pil_frame, self.watermark, position)
            frame = np.array(pil_frame)
            writer.append_data(frame)

        writer.close()
        messagebox.showinfo("Success", "Video processing complete!")

    def calculate_position(self, frame_size, watermark_size, placement):
        if placement == 'Top-Left':
            return (0, 0)
        elif placement == 'Top-Right':
            return (frame_size[0] - watermark_size[0], 0)
        elif placement == 'Bottom-Left':
            return (0, frame_size[1] - watermark_size[1])
        elif placement == 'Bottom-Right':
            return (frame_size[0] - watermark_size[0], frame_size[1] - watermark_size[1])
        else:  # Center
            return ((frame_size[0] - watermark_size[0]) // 2, (frame_size[1] - watermark_size[1]) // 2)

    def apply_watermark(self, frame, watermark, position):
        # Extract alpha channel
        r, g, b, alpha = watermark.split()
        # Apply transparency
        alpha = ImageEnhance.Brightness(alpha).enhance(self.transparency)
        # Paste watermark onto the frame
        frame.paste(watermark, position, mask=alpha)
        return frame

# Create the Tkinter window
root = Tk()
app = VideoWatermarkApp(root)
root.mainloop()
