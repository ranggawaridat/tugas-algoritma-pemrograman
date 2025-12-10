class AppError(Exception):
    """Base custom exception"""
    pass

class DataNotFound(AppError):
    def __init__(self, message="Data tidak ditemukan"):
        self.message = message
        super().__init__(self.message)

class FileEmpty(AppError):
    def __init__(self, message="File kosong"):
        self.message = message
        super().__init__(self.message)

class FileFormatError(AppError):
    def __init__(self, message="Format file tidak valid"):
        self.message = message
        super().__init__(self.message)
