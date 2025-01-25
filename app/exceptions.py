import uuid
from typing import Any, Dict, Optional

from fastapi import status


class ErrorCode:
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AGENT_NOT_FOUND = "AGENT_NOT_FOUND"
    AGENT_ALREADY_EXISTS = "AGENT_ALREADY_EXISTS"
    CUSTOMER_CONNECTION_ERROR = "CUSTOMER_CONNECTION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class BaseAPIException(Exception):
    def __init__(
            self,
            message: str,
            error_code: str,
            status_code: int = status.HTTP_400_BAD_REQUEST,
            details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        self.request_id = str(uuid.uuid4())
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        error_response = {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "request_id": self.request_id,
                "status_code": self.status_code,
            }
        }
        if self.details:
            error_response["error"]["details"] = self.details
        return error_response


class ValidationError(BaseAPIException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class AgentNotFoundError(BaseAPIException):
    def __init__(self, agent_id: str):
        super().__init__(
            message=f"Agent with ID {agent_id} not found",
            error_code=ErrorCode.AGENT_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )


class DuplicateAgentError(BaseAPIException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"Agent with identifier {identifier} already exists",
            error_code=ErrorCode.AGENT_ALREADY_EXISTS,
            status_code=status.HTTP_409_CONFLICT
        )


class AgentCustomerConnectionError(BaseAPIException):
    def __init__(self, agent_id: str, customer_id: str):
        super().__init__(
            message=f"Agent with id={agent_id} is not connected to customer with id={customer_id}",
            error_code=ErrorCode.CUSTOMER_CONNECTION_ERROR,
            status_code=status.HTTP_404_NOT_FOUND
        )
