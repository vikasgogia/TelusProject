####
# import packages
####
from flask import Flask
# from api.capture import capture_bp
from update import *
# from api.proc_time import proc_time_bp
from api.task import task_bp
from api.record import record_bp
import threading
import time
from config.CameraConnectorConfig import CameraConnectorConfig


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key


# Register Blueprints
# app.register_blueprint(capture_bp)
# app.register_blueprint(update_bp)
# app.register_blueprint(proc_time_bp)
app.register_blueprint(task_bp)
app.register_blueprint(record_bp)

config = CameraConnectorConfig()


def start_threading():
    while True:
        # thread_local = threading.Thread(target=update_qsize_local)
        thread_remote = threading.Thread(target=update_qsize_remote)
        # thread_local.start()
        thread_remote.start()
        # thread_local.join()
        thread_remote.join()
        time.sleep(5)


# if not config.isTotalRemote:
threading.Thread(target=start_threading).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, threaded=True)
