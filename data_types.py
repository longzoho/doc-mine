class DocumentData(dict):
    def __init__(self, name, hash_name):
        dict.__init__(self, name=name, hash_name=hash_name)
        self.name = name
        self.hash_name = hash_name


class ProfileData(dict):
    def __init__(self, name, description, hash_names, profile_id):
        dict.__init__(self, name=name, description=description, hash_names=hash_names, profile_id=profile_id)
        self.name = name
        self.description = description
        self.hash_names = hash_names
        self.profile_id = profile_id


class FileStatus(str):
    DOCUMENT_SAVED = "DOCUMENT_SAVED"
    CONTENT_SAVED = "CONTENT_SAVED"
    EMBED_SAVED = "EMBED_SAVED"
    ERROR = "ERROR"


class ProfileStatus(str):
    INIT = "INIT"
    EMBED_SAVED = "EMBED_SAVED"
    ERROR = "ERROR"
