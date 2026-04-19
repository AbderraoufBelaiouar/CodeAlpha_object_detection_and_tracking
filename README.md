# 🚗 Object Detection and Tracking
### CodeAlpha AI Internship — Task 4

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![Platform](https://img.shields.io/badge/Platform-Google%20Colab-orange?logo=googlecolab)

Real-time vehicle detection and tracking on video footage using **YOLOv8** and the **ByteTrack** algorithm. Each detected vehicle is assigned a persistent ID that follows it across all frames.

---

## 📹 Demo

| Input Frame | Output Frame |
|:-----------:|:------------:|
| Raw top-down road footage | Annotated with bounding boxes + tracking IDs |

> Video: `car-detection.mp4` — 768×432, 12.5 fps, 30 seconds, top-down road view

---

## 🧠 How It Works

```
Video File → Frame Extraction → YOLOv8 Detection → ByteTrack Tracking → Annotated Output
```

1. **Video Input** — OpenCV reads the video frame by frame
2. **YOLOv8 Detection** — detects vehicles with bounding boxes and class labels
3. **ByteTrack Tracking** — assigns a persistent ID to each vehicle across frames
4. **Frame Annotation** — draws boxes, labels, and IDs on each frame
5. **Output Writing** — saves the fully annotated video to file

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Ultralytics YOLOv8](https://docs.ultralytics.com) | Object detection + built-in tracking |
| OpenCV (`cv2`) | Video I/O and frame processing |
| ByteTrack | Multi-object tracking algorithm |
| Google Colab | Cloud GPU execution environment |
| ffmpeg | Video format conversion (AVI → MP4) |

---

## 📁 Project Structure

```
CodeAlpha_ObjectDetection/
├── detect_and_track.py     ← main script
├── car-detection.mp4       ← input video
├── output_tracked.mp4      ← annotated output video
└── README.md               ← this file
```

---

## ⚙️ Setup and Usage

### 1. Install dependencies

```bash
pip install ultralytics opencv-python
```

### 2. Upload your video (Google Colab)

```python
from google.colab import files
uploaded = files.upload()   # select your video file
```

### 3. Run detection and tracking

```python
from ultralytics import YOLO
import cv2

# Load model — downloads yolov8n.pt (~6MB) automatically on first run
model = YOLO("yolov8n.pt")

INPUT_VIDEO  = "car-detection.mp4"
OUTPUT_VIDEO = "output_tracked.avi"

cap    = cv2.VideoCapture(INPUT_VIDEO)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS) or 25
out    = cv2.VideoWriter(OUTPUT_VIDEO,
             cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    results   = model.track(frame, persist=True,
                    tracker="bytetrack.yaml", verbose=False)
    annotated = results[0].plot()
    out.write(annotated)

cap.release()
out.release()
print("Done!")
```

### 4. Play result inside Colab

```python
import subprocess
from IPython.display import HTML
from base64 import b64encode

# Convert AVI → MP4 for browser playback
subprocess.run(["ffmpeg", "-y", "-i", "output_tracked.avi",
                "-vcodec", "libx264", "output_tracked.mp4"],
               capture_output=True)

mp4  = open("output_tracked.mp4", "rb").read()
data = b64encode(mp4).decode()
HTML(f'<video width=700 controls autoplay loop>'
     f'<source src="data:video/mp4;base64,{data}"></video>')
```

### 5. Download the output

```python
from google.colab import files
files.download("output_tracked.mp4")
```

---

## ⚠️ Google Colab — Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Error: Could not open camera` | `VideoCapture(0)` looks for a webcam | Use `VideoCapture("file.mp4")` |
| `cv2.imshow() is disabled` | Crashes Jupyter sessions | Save to file, play with `HTML()` |
| `cv2.waitKey()` not working | No live window in Colab | Remove it entirely |

---

## 🤖 Model Details

**YOLOv8 Nano (`yolov8n.pt`)**
- Size: ~6 MB, downloads automatically on first run
- Detects 80 COCO classes including `car`, `truck`, `bus`, `person`
- Fastest YOLO variant — suitable for CPU and GPU inference

**ByteTrack**
- Assigns stable integer IDs to each detected object
- Handles brief occlusions without losing track
- Built into Ultralytics — no extra installation needed

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Input resolution | 768 × 432 |
| Frame rate | 12.5 fps |
| Video duration | 30 seconds |
| Total frames processed | 377 |
| Objects tracked | Cars / vehicles |
| Environment | Google Colab |

---

## 📚 References

- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com)
- [ByteTrack Paper — Zhang et al., 2022](https://arxiv.org/abs/2110.06864)
- [OpenCV Documentation](https://docs.opencv.org)
- [CodeAlpha Internship](https://www.codealpha.tech)

---

> **CodeAlpha AI Internship** | Task 4 — Object Detection and Tracking
