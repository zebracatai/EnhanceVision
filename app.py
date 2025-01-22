"""
FastAPI Application for Video Enhancement

This module defines a FastAPI application that receives a video file path and
enhancement parameters (sharpness, contrast, brightness, saturation, color_boost).
It then processes and returns the path to the enhanced video.
"""

import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from fastapi import FastAPI
from pydantic.dataclasses import dataclass
from typing import Optional

app = FastAPI()


@dataclass
class VideoEnhancementRequest:
    """
    Dataclass that defines the incoming request body for video enhancement.
    """
    video_path: str
    sharpness: Optional[float] = 1.0
    contrast: Optional[float] = 1.0
    brightness: Optional[float] = 0.0
    saturation: Optional[float] = 1.0
    color_boost: Optional[float] = 1.0


@dataclass
class VideoEnhancementResponse:
    """
    Dataclass that defines the outgoing response body after video enhancement.
    """
    output_video_path: str


def enhance_video(
    video_path: str,
    output_path: str,
    sharpness: float = 1.0,
    contrast: float = 1.0,
    brightness: float = 0.0,
    saturation: float = 1.0,
    color_boost: float = 1.0,
) -> None:
    """
    Enhance a video by adjusting sharpness, contrast, brightness, saturation,
    and color boost, then write the processed frames to a new video file.

    Parameters:
    -----------
    video_path: str
        Path to the input video file.
    output_path: str
        Desired path for the enhanced video file.
    sharpness: float, default=1.0
        Sharpness factor (>1 increases sharpness, <1 decreases sharpness).
    contrast: float, default=1.0
        Contrast factor (>1 increases contrast, <1 decreases contrast).
    brightness: float, default=0.0
        Brightness adjustment (positive to increase, negative to decrease).
    saturation: float, default=1.0
        Saturation factor (>1 increases saturation, <1 decreases saturation).
    color_boost: float, default=1.0
        Boosts color intensity (>1 makes colors more vivid, <1 makes colors duller).
    """

    # Load video using MoviePy
    clip = VideoFileClip(video_path)

    def process_frame(frame: np.ndarray) -> np.ndarray:
        """
        Process a single frame, applying the configured transformations.
        
        Parameters:
        -----------
        frame: np.ndarray
            A single video frame in BGR format.

        Returns:
        --------
        np.ndarray
            The transformed frame in BGR format.
        """

        # Convert frame to HSV to adjust saturation and color boost
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Adjust saturation
        hsv[..., 1] *= saturation

        # Adjust color boost
        hsv[..., 1] *= color_boost

        # Clip the values to the valid HSV range
        hsv = np.clip(hsv, 0, 255).astype(np.uint8)

        # Convert back to BGR
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Adjust brightness (beta) and contrast (alpha)
        # Note: brightness in cv2.convertScaleAbs must be an integer
        frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=int(brightness))

        # Adjust sharpness if needed
        if sharpness != 1.0:
            # Construct a kernel for sharpening
            kernel = np.array(
                [
                    [0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0],
                ],
                dtype=np.float32,
            )
            frame = cv2.filter2D(frame, -1, kernel * sharpness)

        return frame

    # Apply the frame processing to each frame of the clip
    enhanced_clip = clip.fl_image(process_frame)

    # Write the result to a new video file
    enhanced_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=4,  # Attempt to speed up encoding
        temp_audiofile="temp_audio.m4a",
        remove_temp=True,
    )


@app.post("/enhance", response_model=VideoEnhancementResponse)
def enhance_video_endpoint(request: VideoEnhancementRequest) -> VideoEnhancementResponse:
    """
    FastAPI endpoint that receives a VideoEnhancementRequest, processes the video,
    and returns a VideoEnhancementResponse with the path of the enhanced video.

    Request Body:
    ------------
    video_path: str
        Path to the input video file.
    sharpness: float (optional)
    contrast: float (optional)
    brightness: float (optional)
    saturation: float (optional)
    color_boost: float (optional)

    Returns:
    --------
    VideoEnhancementResponse
        A dataclass containing the path to the enhanced video.
    """

    # Create output path in the same directory with "_enhanced" suffix
    base_name, ext = os.path.splitext(request.video_path)
    output_path = f"{base_name}_enhanced{ext}"

    # Perform the video enhancement
    enhance_video(
        video_path=request.video_path,
        output_path=output_path,
        sharpness=request.sharpness,
        contrast=request.contrast,
        brightness=request.brightness,
        saturation=request.saturation,
        color_boost=request.color_boost,
    )

    return VideoEnhancementResponse(output_video_path=output_path)
