import subprocess
import time
from pathlib import Path
import yaml
import threading
import logging

cfg = yaml.safe_load(open('config.yaml'))
photo_dir = Path(cfg['paths']['photos'])
photo_dir.mkdir(exist_ok=True)

def capture_photo():
    # Start in a separate thread
    threading.Thread(target=_capture_photo_task).start()
    return True  # Return immediately

def _capture_photo_task():
    try:
        timestamp = int(time.time())
        filename = f"./photos/photo_{timestamp}.jpg"
        
        # Use libcamera-still with increased timeout and simpler settings
        cmd = [
            "libcamera-still", 
            "-o", filename,
            "--width", "1920",
            "--height", "1080",
            "--nopreview",
            "--immediate"  # Take picture immediately without delay
        ]
        
        # Increase timeout to 10 seconds
        subprocess.run(cmd, check=True, timeout=10)
        
        # Update display once the capture is complete
        from display import update_display
        update_display(state_text="Foto tirada!", show_camera_icon=True)
        
    except subprocess.TimeoutExpired:
        logging.error("Camera capture timed out - trying alternative method")
        
    except Exception as e:
        logging.error(f"Error taking photo: {e}")
        from display import update_display
        update_display(state_text="Erro com camera", show_error_icon=True)

def capture_gif():
    try:
        timestamp = int(time.time())
        gif_path = photo_dir / f'gif_{timestamp}.gif'
        
        # Kill any lingering processes
        try:
            subprocess.run(["pkill", "-f", "libcamera"], timeout=1, check=False)
            time.sleep(0.5)
        except:
            pass
        
        # Capture HIGH QUALITY video for better GIFs
        cmd = [
            "libcamera-vid",
            "--timeout", "5000",        # 5 seconds recording
            "--framerate", "10",        # Smoother framerate
            "--width", "1280",          # Good balance of size vs performance
            "--height", "720",
            "--nopreview",              # Don't show preview
            "-o", "/tmp/video.h264"
        ]
        
        # Use Popen for better process control
        logging.info("Starting video capture for GIF")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        try:
            process.wait(timeout=15)  # Longer timeout for reliability
        except subprocess.TimeoutExpired:
            logging.warning("Video process taking too long, terminating")
            process.terminate()
            time.sleep(1)
        
        # Check if video file exists and has content
        if not Path("/tmp/video.h264").exists() or Path("/tmp/video.h264").stat().st_size < 1000:
            raise Exception("Video capture failed or file is too small")
            
        logging.info("Converting to large GIF")
        # Convert to LARGE gif with high quality settings
        cmd_ffmpeg = [
            "ffmpeg",
            "-y",
            "-i", "/tmp/video.h264",
            "-vf", "fps=10,scale=1024:-1:flags=lanczos",  # LARGER SIZE: 1024px width
            "-loop", "0",               # Make GIF loop continuously  
            "-max_delay", "5",          # Faster frame display
            "/tmp/out.gif"
        ]
        subprocess.run(cmd_ffmpeg, check=True, timeout=20)  # Longer timeout for larger GIF

        # Move gif to photos folder
        subprocess.run(["mv", "/tmp/out.gif", str(gif_path)], check=True)
        
        logging.info(f"Large GIF created successfully at {gif_path}")
        from display import update_display
        update_display(state_text="GIF criado!", show_gif_icon=True)
        
        return gif_path
    except Exception as e:
        logging.error(f"Error creating GIF: {e}")
        from display import update_display
        update_display(state_text="Erro GIF", show_error_icon=True)
        return None
