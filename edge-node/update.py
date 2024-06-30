####
# importing packages
####
import threading
import requests
from config.CameraConnectorConfig import CameraConnectorConfig


# update_bp = Blueprint('update', __name__)
config = CameraConnectorConfig()


lock_1 = threading.Lock()
lock_2 = threading.Lock()

queue_size_local = 0
processing_time_local = 0

queue_size_remote = 0
processing_time_remote = 0


def update_qsize_local():
    '''
        function to fetch local queue metadata
    '''
    global queue_size_local
    try:
        response = requests.post(f"{config.localExecutorEndpoint}/queue-metadata")
        response_data = response.json()
        with lock_1:
            queue_size_local = response_data.get('qsize', 0)
            print(f"local queue size: {queue_size_local}")
    except Exception as e:
        print(f"Error updating local queue size: {e}")


def update_qsize_remote():
    '''
        function to fetch remote queue metadata
    '''
    global queue_size_remote
    try:
        response = requests.post(f"{config.remoteExecutorEndpoint}/queue-metadata")
        response_data = response.json()
        with lock_2:
            queue_size_remote = response_data.get('qsize', 0)
            print(f"remote queue size: {queue_size_remote}")
    except Exception as e:
        print(f"Error updating remote queue size: {e}")
