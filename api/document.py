import json
import logging
import os

from flask import request
from werkzeug.datastructures import FileStorage

from data_types import DocumentData
from decorator import auth_required
from repository.users import Users
from util.crypto_util import hash_content
from util.file_util import file_exists, save_file
from util.path_util import content_path, bucket
from worker.worker_decorator import document_convert_channel
from workflow.message_channel import RoutingKeys

logger = logging.getLogger(__name__)


@auth_required
@document_convert_channel
def upload(uid, msg_channel):
    if "file" in request.files:
        files = request.files.getlist("file")
        documents: list[DocumentData] = []
        for file in files:
            file_data, file_name = read_file(file)
            file_extension = os.path.splitext(file_name)[1].replace('.', '')
            file_hash = hash_content(file_data)
            if file_data is not None:
                file_key = f'{content_path()}/{file_hash}.{file_extension}'
                if not file_exists(bucket=bucket(), file_key=file_key):
                    save_file(bucket=bucket(), file_key=file_key, file_data=file_data)
                documents.append(DocumentData(name=file_name, hash_name=f'{file_hash}__{file_extension}'))
            else:
                logger.error(f'Error reading file {file_name}')
        Users(uid=uid).create_if_not_exists()
        msg_channel.basic_publish(exchange="document_convert_process_exchange",
                                  routing_key=RoutingKeys.convert_document_topic,
                                  body=json.dumps({'user_id': uid, 'document_data': documents}))
        print(str({'user_id': uid, 'document_data': documents}))
    return {'message': 'success'}, 200


def read_file(file: FileStorage) -> (bytes, str):
    file_name = file.filename
    try:
        return file.read(), file_name
    except Exception as e:
        logger.error(f'Error reading file {file_name}: {e}')
    return None, None
