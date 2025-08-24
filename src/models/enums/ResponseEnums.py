from enum import Enum


class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully!"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported!"
    FILE_SIZE_EXCEEDED = "File size exceeded!"
    FILE_UPLOAD_SUCCESS = "File upload success!"
    FILE_UPLOAD_FAILED = "File upload failed"
    PROCESSING_FAILED = "File processing failed"
    PROCESSING_SUCCESS = "File processing success"
    NO_FILES_ERROR = "no files founded"
    FILE_ID_ERROR = "no file found with this id"
    PROJECT_NOT_FOUND_ERROR = "project not found"
    INSERT_INTO_VECTORDB_ERROR = "insert into vectordb error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert into vectordb success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb collection retrieved"
    VECTORDB_COLLECTION_RETRIEVAL_ERROR = "error while retrieving vectordb collection"
    VECTOR_SEARCH_ERROR = "vector_search_error"
    VECTOR_SEARCH_SUCCESS = "vector_search_success"
