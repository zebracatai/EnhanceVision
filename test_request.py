import requests

def test_enhance_video():
    """
    Sends a test POST request to the /enhance endpoint.
    Adjust the URL and payload to fit your environment and video file path.
    """
    url = "http://127.0.0.1:8006/enhance"  # Update if your server runs elsewhere
    
    payload = {
        "video_path": "/home/ubuntu/projects/research/bc_remover/result_voice.mp4",
        "sharpness": 1.1,
        "contrast": 1,
        "brightness": 0.1,
        "saturation": 1,
        "color_boost": 1
    }
    
    response = requests.post(url, json=payload)
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    test_enhance_video()
