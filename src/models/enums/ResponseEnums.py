from enum import Enum


class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully!"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported!"
    FILE_SIZE_EXCEEDED = "File size exceeded!"
    FILE_UPLOAD_SUCCESS = "File upload success!"
    FILE_UPLOAD_FAILED = "File upload failed"
    PROCESSING_FAILED = "File processing failed"
    PROCESSING_SUCCESS = "File processing success"
