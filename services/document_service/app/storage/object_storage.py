from shared.config import StorageSettings
from shared.storage import S3ObjectStorage

class ObjectStorage(S3ObjectStorage):
    def __init__(self, settings: StorageSettings) -> None:
        super().__init__(settings)