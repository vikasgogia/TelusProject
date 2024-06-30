####
# importing packages
####
import os
import cv2
import base64
import random
import requests
import numpy as np
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from utils.constants import *
from utils.util import *
from config.CameraConnectorConfig import CameraConnectorConfig


config = CameraConnectorConfig()


task_bp = Blueprint('task', __name__)


####
# api for receiving the processed tasks from the remote server
####
@task_bp.route('/receive-task', methods=["POST"])
def rec_task():
    for idx, image in request.files.items():
        image_bytes = image.read()
        img_bytes = base64.b64decode(image_bytes)
        filename = secure_filename(f"imageToSave_{idx}.jpeg")
        print(img_bytes)
        # with open(os.path.join(r'C:\Users\vikas\Downloads\driver-distraction-mec\meta', filename), "wb") as fh:
        #     fh.write(img_bytes)
    return jsonify({'message': 'Task saved successfully'})


####
# api for creating a task from a video file and sending it to the remote/ local server
####
@task_bp.route('/send-task', methods=["POST"])
def send_task():
    if not request.method == "POST":
        return generateResponse(Constants.ERROR_KEY, "Only POST requests are allowed."), 400
    
    video_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'vid.mp4')
    cap = cv2.VideoCapture(video_path)
    frames = {}

    scale = 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    num_frames_to_capture = int(np.random.exponential(scale))
    num_frames_to_capture = max(1, min(num_frames_to_capture, total_frames)) 

    for i in range(num_frames_to_capture):
        ret, frame = cap.read()
        if not ret:
            return generateResponse(Constants.ERROR_KEY, "Failed to capture an image."), 400
        _, image_data = cv2.imencode(Constants.JPG, frame)

        frames[f'image_{i}'] = ("captured_image.jpg", image_data.tobytes(), "image/jpeg")

    try:
        # decision = 1 if config.isTotalRemote else make_decision()
        # url = f'{config.localExecutorEndpoint}/task-upload' if decision == 0 else f'{config.remoteExecutorEndpoint}/task-upload'

        response = requests.post(f'{config.remoteExecutorEndpoint}/task-upload', files=frames)
        response.raise_for_status()
        return generateResponse(Constants.SUCCESS_KEY, f"Pass"), 200
    
    except requests.exceptions.RequestException as e:
        return generateResponse(Constants.FAIL_KEY, f"Issue with sending the image - {e}."), 400
