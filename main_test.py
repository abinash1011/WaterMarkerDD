import imageio
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox, ttk
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

        self.light_mode = True
        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("400x400")

        # Style
        s = ttk.Style()
        s.configure('TButton', font=('Arial', 10))
        s.configure('TLabel', font=('Arial', 10))
        s.configure('TRadiobutton', font=('Arial', 10))
        s.configure('TFrame', background='#f0f0f0')
        s.map('TButton', foreground=[('!disabled', 'black'), ('disabled', 'gray50')])
        s.map('TRadiobutton', foreground=[('!disabled', 'black'), ('disabled', 'gray50')])

        # Toggle button
        self.light_mode_button = ttk.Button(self.root, text="Dark Mode" if self.light_mode else "Light Mode", command=self.toggle_mode)
        self.light_mode_button.pack(side=TOP, pady=10)

        # Video selection
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack(pady=5)
        self.video_button = ttk.Button(self.video_frame, text="Select Video", command=self.select_video)
        self.video_button.grid(row=0, column=0, padx=5)
        self.video_label = ttk.Label(self.video_frame, text="No video selected", width=30)
        self.video_label.grid(row=0, column=1)

        # Watermark selection
        self.watermark_frame = ttk.Frame(self.root)
        self.watermark_frame.pack(pady=5)
        self.watermark_button = ttk.Button(self.watermark_frame, text="Select Watermark", command=self.select_watermark)
        self.watermark_button.grid(row=0, column=0, padx=5)
        self.watermark_label = ttk.Label(self.watermark_frame, text="No watermark selected", width=30)
        self.watermark_label.grid(row=0, column=1)

        # Transparency slider
        self.transparency_label = ttk.Label(self.root, text="Transparency")
        self.transparency_label.pack()
        self.transparency_slider = ttk.Scale(self.root, from_=0, to=1, command=self.set_transparency)
        self.transparency_slider.set(0.5)
        self.transparency_slider.pack()

        # Size preset dropdown
        self.size_preset_label = ttk.Label(self.root, text="Watermark Size Preset")
        self.size_preset_label.pack()
        self.size_preset_var = StringVar(self.root)
        self.size_preset_var.set('Medium')
        self.size_preset_dropdown = ttk.Combobox(self.root, textvariable=self.size_preset_var, values=list(self.size_presets.keys()), state='readonly')
        self.size_preset_dropdown.pack()

        # Placement options dropdown
        self.placement_label = ttk.Label(self.root, text="Watermark Placement")
        self.placement_label.pack()
        self.placement_var = StringVar(self.root)
        self.placement_var.set(self.placement_options[0])
        self.placement_dropdown = ttk.Combobox(self.root, textvariable=self.placement_var, values=self.placement_options, state='readonly')
        self.placement_dropdown.pack()

        # Process button
        self.process_button = ttk.Button(self.root, text="Process", command=self.process_video)
        self.process_button.pack(pady=10)

    def toggle_mode(self):
        self.light_mode = not self.light_mode
        self.root['bg'] = '#f0f0f0' if self.light_mode else '#1f1f1f'
        self.light_mode_button['text'] = "Dark Mode" if self.light_mode else "Light Mode"
        self.light_mode_button['style'] = 'TButton' if self.light_mode else 'Disabled.TButton'

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
        self.video_label.config(text=self.video_path if self.video_path else "No video selected")

    def select_watermark(self):
        self.watermark_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.watermark_label.config(text=self.watermark_path if self.watermark_path else "No watermark selected")

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
