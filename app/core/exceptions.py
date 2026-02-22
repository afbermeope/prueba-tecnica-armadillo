class BusinessException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class EntityNotFoundException(BusinessException):
    def __init__(self, entity_name: str, entity_id: any):
        super().__init__(f"{entity_name} with id {entity_id} not found", 404)

class IntegrityViolationException(BusinessException):
    def __init__(self, message: str):
        super().__init__(message, 409)
