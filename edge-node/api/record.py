####
# importing packages
####
import requests
from flask import Blueprint
from config.CameraConnectorConfig import CameraConnectorConfig


config = CameraConnectorConfig()


record_bp = Blueprint('record', __name__)


####
# send a record request to local/ remote server 
####
@record_bp.route('/record', methods=['GET'])
def record():
    try:
        # if not config.isTotalRemote:
        #     response_local = requests.get(f'{config.localExecutorEndpoint}/record')
        # else:
        #     response_local = None
        response_remote = requests.get(f'{config.remoteExecutorEndpoint}/record')
        # print(response_local, response_remote)
        # if (response_local and response_local == 'success') and response_remote == 'success':
        #     return 'success'
        # elif not response_local and response_remote == 'success':
        #     return 'success'
        # else:
        #     return 'fail'
        return 'success'
    except Exception as e:
        return f'{e}'
