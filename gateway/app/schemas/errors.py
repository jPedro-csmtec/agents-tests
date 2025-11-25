from pydantic import BaseModel
from typing import Optional
from enum import Enum

from libs.errors.exceptions import ErrorCode as ErrorCodeEnum

class ErrorCode(int, Enum):
    NO_ERROR         = ErrorCodeEnum.NO_ERROR.value
    
    CALL_ERROR        = ErrorCodeEnum.CALL_ERROR.value
    NOT_FOUND         = ErrorCodeEnum.NOT_FOUND.value
    INVALID_ARGUMENTS = ErrorCodeEnum.INVALID_ARGUMENTS.value
    INVALID_CONTENT   = ErrorCodeEnum.INVALID_CONTENT.value
    ALREADY_EXISTS    = ErrorCodeEnum.ALREADY_EXISTS.value
    NETWORK_ERROR     = ErrorCodeEnum.NETWORK_ERROR.value
    TIMEOUT           = ErrorCodeEnum.TIMEOUT.value
    
    BACK_OFFICE_ERROR = ErrorCodeEnum.BACK_OFFICE_ERROR.value
    BACK__OFFICE_GATE_WAY_UNHANDLED_ERROR = ErrorCodeEnum.BACK__OFFICE_GATE_WAY_UNHANDLED_ERROR.value
    BACK_OFFICE_PATIENT_CREATION_ERROR = ErrorCodeEnum.BACK_OFFICE_PATIENT_CREATION_ERROR.value
    BACK_OFFICE_PATIENT_MEDICAL_RECORDBIND_ERROR = ErrorCodeEnum.BACK_OFFICE_PATIENT_MEDICAL_RECORDBIND_ERROR.value
    BACK_OFFICE_PATIENT_UPDATE_ERROR = ErrorCodeEnum.BACK_OFFICE_PATIENT_UPDATE_ERROR.value
    BACK_OFFICE_APPEND_ANAMNES_IS_ERROR = ErrorCodeEnum.BACK_OFFICE_APPEND_ANAMNES_IS_ERROR.value
    BACK_OFFICE_ANAMNESIS_UPDATE_ERROR = ErrorCodeEnum.BACK_OFFICE_ANAMNESIS_UPDATE_ERROR.value

    DATABASE_ERROR = ErrorCodeEnum.DATABASE_ERROR.value
    DATABASE_INSERT_ERROR = ErrorCodeEnum.DATABASE_INSERT_ERROR.value
    DATABASE_UPDATE_ERROR = ErrorCodeEnum.DATABASE_UPDATE_ERROR.value
    DATABASE_DELETE_ERROR = ErrorCodeEnum.DATABASE_DELETE_ERROR.value
    DATABASE_QUERY_ERROR  = ErrorCodeEnum.DATABASE_QUERY_ERROR.value
    
    IDENTITY_ERROR = ErrorCodeEnum.IDENTITY_ERROR.value
    IDENTITY_API_SERVICES_UNAVAILABLE = ErrorCodeEnum.IDENTITY_API_SERVICES_UNAVAILABLE.value
    IDENTITY_API_CALL_ERROR = ErrorCodeEnum.IDENTITY_API_CALL_ERROR.value
    
    UNDEFINED_ERROR = ErrorCodeEnum.UNDEFINED_ERROR.value
    NOT_IMPLEMENTED = ErrorCodeEnum.NOT_IMPLEMENTED.value
    GLOBAL_UNHADLED_ERROR = ErrorCodeEnum.GLOBAL_UNHADLED_ERROR.value
    DISCONNECTED = ErrorCodeEnum.DISCONNECTED.value
    UNHANDLED = ErrorCodeEnum.UNHANDLED.value
    UNSUPPORTED = ErrorCodeEnum.UNSUPPORTED.value

    GENERIC_ERROR      = ErrorCodeEnum.GENERIC_ERROR.value
    VALIDATION_ERROR   = ErrorCodeEnum.VALIDATION_ERROR.value
    UNAUTHORIZED       = ErrorCodeEnum.UNAUTHORIZED.value
    CONFLICT           = ErrorCodeEnum.CONFLICT.value
    EXTRACTION_ERROR   = ErrorCodeEnum.EXTRACTION_ERROR.value


class ResultErrorSchema(BaseModel):
    code: ErrorCode
    code_alias: str
    system_code: Optional[str]
    description: str
    about_link: Optional[str] = None
    details: Optional[str]    = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "code_alias": "NOT_FOUND",
                "system_code": "USER_NOT_FOUND",
                "description": "Usuário com ID 1234 não foi encontrado.",
                "about_link": "https://docs.myapi.com/errors#USER_NOT_FOUND",
                "details": None
            }
        }
