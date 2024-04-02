import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont


class VideoWatermarkApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Watermark App")

        # Create buttons
        self.upload_video_button = QPushButton("Upload Video")
        self.upload_video_button.clicked.connect(self.upload_video)
        self.upload_image_button = QPushButton("Upload Image")
        self.upload_image_button.clicked.connect(self.upload_image)
        self.transparent_button = QPushButton("Make Watermark Transparent")
        self.transparent_button.clicked.connect(self.make_transparent)
        self.position_button = QPushButton("Change Watermark Position")
        self.position_button.clicked.connect(self.change_position)

        # Create label to display video
        self.video_label = QLabel()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.upload_video_button)
        layout.addWidget(self.upload_image_button)
        layout.addWidget(self.transparent_button)
        layout.addWidget(self.position_button)
        layout.addWidget(self.video_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Variables
        self.video_path = None
        self.image_path = None

    def upload_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi)")
        if self.video_path:
            self.process_video()

    def upload_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg)")
        if self.image_path:
            self.process_video()

    def process_video(self):
        if self.video_path and self.image_path:
            cap = cv2.VideoCapture(self.video_path)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, fps, (frame_width, frame_height))

            image = Image.open(self.image_path)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Overlay image onto video frame
                watermark = self.overlay_image(frame, image)
                out.write(watermark)

                # Display the processed frame
                self.display_frame(watermark)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()

    def overlay_image(self, frame, image):
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pil_image.paste(image, (0, 0), image)
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def display_frame(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)
        self.video_label.setAlignment(Qt.AlignCenter)

    def make_transparent(self):
        pass  # Add code to make watermark transparent

    def change_position(self):
        pass  # Add code to change watermark position


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoWatermarkApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
