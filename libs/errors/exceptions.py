from enum import Enum, IntFlag
from typing import Optional

class ErrorCode(IntFlag):
    NO_ERROR          = 0x000
    
    CALL_ERROR        = 0x0100
    NOT_FOUND         = CALL_ERROR | 0x0001
    INVALID_ARGUMENTS = CALL_ERROR | 0x0002
    INVALID_CONTENT   = CALL_ERROR | 0x0003
    ALREADY_EXISTS    = CALL_ERROR | 0x0004
    NETWORK_ERROR     = CALL_ERROR | 0x0005
    TIMEOUT           = CALL_ERROR | 0x0006
    
    BACK_OFFICE_ERROR = CALL_ERROR | 0x0400
    BACK__OFFICE_GATE_WAY_UNHANDLED_ERROR = BACK_OFFICE_ERROR | 0x0001
    BACK_OFFICE_PATIENT_CREATION_ERROR = BACK_OFFICE_ERROR | 0x0002
    BACK_OFFICE_PATIENT_MEDICAL_RECORDBIND_ERROR = BACK_OFFICE_ERROR | 0x0003
    BACK_OFFICE_PATIENT_UPDATE_ERROR = BACK_OFFICE_ERROR | 0x0004
    BACK_OFFICE_APPEND_ANAMNES_IS_ERROR = BACK_OFFICE_ERROR | 0x0005
    BACK_OFFICE_ANAMNESIS_UPDATE_ERROR = BACK_OFFICE_ERROR | 0x0006

    DATABASE_ERROR = 0x0400
    DATABASE_INSERT_ERROR = DATABASE_ERROR | 0x0001
    DATABASE_UPDATE_ERROR = DATABASE_ERROR | 0x0002
    DATABASE_DELETE_ERROR = DATABASE_ERROR | 0x0003
    DATABASE_QUERY_ERROR = DATABASE_ERROR | 0x0004
    
    IDENTITY_ERROR = 0x0500
    IDENTITY_API_SERVICES_UNAVAILABLE = IDENTITY_ERROR | 0x0001
    IDENTITY_API_CALL_ERROR = IDENTITY_ERROR | 0x0002
    
    UNDEFINED_ERROR = 0xFF00
    NOT_IMPLEMENTED = 0xFF01
    GLOBAL_UNHADLED_ERROR = 0xFF02
    DISCONNECTED = 0xFF03
    UNHANDLED = 0xFF04
    UNSUPPORTED = 0xFF04

    GENERIC_ERROR      = 0x001
    VALIDATION_ERROR   = 0x003
    UNAUTHORIZED       = 0x004
    CONFLICT           = 0x005
    EXTRACTION_ERROR   = 0x006

class APIError(Exception):
    """
    Exceção base que carrega exatamente os campos do seu ResultError:
      - code:       ErrorCode (enum)
      - code_alias: string (vai ser .value ou .name do enum)
      - system_code: string arbitrário para identificar sistema/subsistema
      - description: string legível para o cliente
      - about_link: string (URL opcional com mais info sobre o erro)
      - details:    string (ou JSON serializado) com informações adicionais
      - status_code: int (código HTTP)
    """
    def __init__(
        self,
        code: ErrorCode,
        system_code: str,
        description: str,
        code_alias: str,
        *,
        status_code: int = 400,
        about_link: Optional[str] = None,
        details: Optional[str] = None
    ):
        super().__init__(description)
        self.code: ErrorCode = code
        self.code_alias: str = f"{system_code} {str(code)}"  
        self.system_code: str = system_code
        self.description: str = description
        self.about_link: Optional[str] = about_link
        self.details: Optional[str] = details
        self.status_code: int = status_code

class NotFoundError(APIError):
    def __init__(self, resource_name: str, resource_id: str):
        super().__init__(
            code=ErrorCode.NOT_FOUND.value,
            code_alias=f"{resource_name.upper()}_NOT_FOUND {ErrorCode.NOT_FOUND.value}",
            system_code=f"{resource_name.upper()}_NOT_FOUND",
            description=f"{resource_name} com ID {resource_id} não foi encontrado.",
            status_code=404,
            about_link=None,
            details=None
        )

class ValidationError(APIError):
    def __init__(self, field_errors: dict):
        import json
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR.value,
            system_code="VALIDATION_FAILED",
            description="Erro de validação nos dados de entrada.",
            status_code=422,
            about_link=None,
            details=json.dumps(field_errors, ensure_ascii=False)
        )


class UnauthorizedError(APIError):
    def __init__(self, message: str = "Não autorizado"):
        super().__init__(
            code=ErrorCode.UNAUTHORIZED.value,
            system_code="UNAUTHORIZED_ACCESS",
            description=message,
            status_code=401,
            about_link=None,
            details=None
        )

class ConflictError(APIError):
    def __init__(self, message: str = "Conflito de dados"):
        super().__init__(
            code=ErrorCode.CONFLICT.value,
            system_code="RESOURCE_CONFLICT",
            description=message,
            status_code=409,
            about_link=None,
            details=None
        )

class ExtractionError(APIError):
    def __init__(
        self,
        message: str = "Erro na extração de dados",
        *,
        code: ErrorCode = ErrorCode.EXTRACTION_ERROR.value,
        code_alias: str = f"EXTRACTION_FAILED {ErrorCode.EXTRACTION_ERROR.value}",
        system_code: str = "EXTRACTION_FAILED",
        status_code: int = 409,
        about_link: Optional[str] = None,
        details: Optional[str] = None
    ):
        super().__init__(
            code=code,
            code_alias=code_alias,
            system_code=system_code,
            description=message,
            status_code=status_code,
            about_link=about_link,
            details=details,
        )
