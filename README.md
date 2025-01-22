# EnhanceVision

EnhanceVision is a FastAPI-based application designed to enhance video quality by adjusting parameters such as sharpness, contrast, brightness, saturation, and color boost. The application processes an input video file and returns the path to the enhanced video.

## Features

- **Video Enhancement**: Adjust sharpness, contrast, brightness, saturation, and color boost.
- **FastAPI Endpoint**: Easy-to-use REST API for video enhancement.
- **Efficient Processing**: Utilizes OpenCV and MoviePy for efficient video processing.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zebracatai/EnhanceVision.git
   cd EnhanceVision
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   uvicorn app:app --reload --port 8006
   ```

   The application will be available at `http://127.0.0.1:8006`.

## Usage

### API Endpoint

- **Endpoint**: `/enhance`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "video_path": "path/to/input/video.mp4",
    "sharpness": 1.0,
    "contrast": 1.0,
    "brightness": 0.0,
    "saturation": 1.0,
    "color_boost": 1.0
  }
  ```
- **Response**:
  ```json
  {
    "output_video_path": "path/to/output/video_enhanced.mp4"
  }
  ```

### Example Request

You can use the provided `test_request.py` script to test the API:

```bash
python test_request.py
```

### Example Response

```json
{
  "output_video_path": "/home/ubuntu/projects/research/bc_remover/result_voice_enhanced.mp4"
}
```

## File Structure

```
EnhanceVision/
├── app.py                # Main FastAPI application
├── test_request.py       # Script to test the API
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Configuration

You can adjust the default values for the enhancement parameters in the `VideoEnhancementRequest` dataclass within the `app.py` file.

## Dependencies

The required dependencies are listed in `requirements.txt`. Install them using:

```bash
sudo apt update
sudo apt install ffmpeg=7:4.4.2-0ubuntu0.22.04.1
pip install -r requirements.txt
```

