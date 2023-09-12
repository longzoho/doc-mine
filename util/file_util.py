import os


def get_file_path_by_key(bucket: str, file_key: str):
    data_folder = os.getenv('DATA_FOLDER')
    # get file path with ./bucket/path/file_key
    return f'{data_folder}/{bucket}/{file_key}'


def get_file_path_from_root(file_key: str):
    root_folder = os.getenv('ROOT_FOLDER')
    # get file path with ./bucket/path/file_key
    return f'{root_folder}/{file_key}'


def file_exists(bucket: str, file_key: str):
    # check file with ./bucket/path/file_key exists
    return os.path.exists(get_file_path_by_key(bucket=bucket, file_key=file_key))


def get_file_content(bucket: str, file_key: str) -> str:
    # get file text with ./bucket/path/file_key
    with open(get_file_path_by_key(bucket=bucket, file_key=file_key), 'rt') as f:
        return f.read()


def save_file(bucket: str, file_key: str, file_data: bytes | str) -> str:
    file_path = get_file_path_by_key(bucket=bucket, file_key=file_key)
    # create folder if not exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # save file with ./bucket/path/file_key
    if isinstance(file_data, str):
        with open(file_path, 'wt') as f:
            f.write(file_data)
    else:
        with open(file_path, 'wb') as f:
            f.write(file_data)
    return file_path


def copy_file(bucket: str, file_key: str, new_file_key: str):
    file_path = get_file_path_by_key(bucket=bucket, file_key=file_key)
    new_file_path = get_file_path_by_key(bucket=bucket, file_key=new_file_key)
    # create folder if not exists
    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

    # save file with ./bucket/path/file_key
    with open(file_path, 'rb') as f:
        with open(new_file_path, 'wb') as new_f:
            new_f.write(f.read())
