import subprocess

def add_watermark(input_video, watermark, output_video, position='10:10'):
    """
    Add a watermark to a video using ffmpeg.
    
    Args:
        input_video (str): Path to the input video file.
        watermark (str): Path to the watermark image file.
        output_video (str): Path to the output video file.
        position (str): Position of the watermark (optional). Default is '10:10'.
    """
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-i', watermark,
        '-filter_complex', f'overlay={position}',
        output_video
    ]
    
    subprocess.run(cmd)

# Example usage:
input_video = 'v1.mp4'
watermark = 'leaf.png'
output_video = 'output_video_with_watermark.mp4'
add_watermark(input_video, watermark, output_video)
