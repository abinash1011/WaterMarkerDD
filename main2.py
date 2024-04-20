import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Watermarking App")

        self.video_path = None
        self.watermark_path = None
        self.transparency = 0.5
        self.placement_options = ['Top-Left', 'Top-Right', 'Bottom-Left', 'Bottom-Right', 'Center']

        self.create_widgets()

    def create_widgets(self):
        # Video selection button
        self.video_button = Button(self.root, text="Select Video", command=self.select_video)
        self.video_button.pack()

        # Watermark selection button
        self.watermark_button = Button(self.root, text="Select Watermark", command=self.select_watermark)
        self.watermark_button.pack()

        # Transparency slider
        self.transparency_label = Label(self.root, text="Transparency")
        self.transparency_label.pack()
        self.transparency_slider = Scale(self.root, from_=0, to=1, resolution=0.01, orient=HORIZONTAL, command=self.set_transparency)
        self.transparency_slider.pack()

        # Placement options dropdown
        self.placement_label = Label(self.root, text="Watermark Placement")
        self.placement_label.pack()
        self.placement_var = StringVar(self.root)
        self.placement_var.set(self.placement_options[0])
        self.placement_dropdown = OptionMenu(self.root, self.placement_var, *self.placement_options)
        self.placement_dropdown.pack()

        # Process button
        self.process_button = Button(self.root, text="Process", command=self.process_video)
        self.process_button.pack()

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])

    def select_watermark(self):
        self.watermark_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])

    def set_transparency(self, value):
        self.transparency = float(value)

    def process_video(self):
        if self.video_path is None or self.watermark_path is None:
            messagebox.showerror("Error", "Please select video and watermark!")
            return

        placement = self.placement_var.get()

        cap = cv2.VideoCapture(self.video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_path = 'output_video.avi'
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        watermark = Image.open(self.watermark_path)
        watermark = watermark.convert("RGBA")
        watermark = watermark.resize((int(frame_width / 4), int(frame_height / 4)))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            pil_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(pil_frame)

            if placement == 'Top-Left':
                position = (0, 0)
            elif placement == 'Top-Right':
                position = (frame_width - watermark.width, 0)
            elif placement == 'Bottom-Left':
                position = (0, frame_height - watermark.height)
            elif placement == 'Bottom-Right':
                position = (frame_width - watermark.width, frame_height - watermark.height)
            else:  # Center
                position = ((frame_width - watermark.width) // 2, (frame_height - watermark.height) // 2)

            pil_frame.paste(watermark, position, mask=watermark.split()[3])

            final_frame = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
            out.write(final_frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        messagebox.showinfo("Success", "Video processing complete!")

# Create the Tkinter window
root = Tk()
app = VideoWatermarkApp(root)
root.mainloop()
