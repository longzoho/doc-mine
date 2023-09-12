import os


def content_path():
    return os.getenv('CONTENT_PATH') or 'content'


def document_path():
    return os.getenv('DOCUMENT_PATH') or 'document'


def embeddingdb_path():
    return os.getenv('EMBEDDINGDB_PATH') or 'embeddingdb'


def bucket():
    return os.getenv('BUCKET_NAME') or 'doc-mining'


def get_file_info_by_hash(hash_name: str):
    return hash_name.split('__')


def get_content_file_key(hash_name: str):
    [file_name, file_ext] = get_file_info_by_hash(hash_name=hash_name)
    return f'{content_path()}/{file_name}.{file_ext}'


def get_document_file_key(hash_name: str):
    return f'{document_path()}/{hash_name}.json'
