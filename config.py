import os
from datetime import datetime

class Config:
    # Основные настройки
    SECRET_KEY = 'your-secret-key-here'
    APP_NAME = "Neon Steganography"
    CURRENT_YEAR = datetime.now().year

    # Настройки загрузки файлов
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

    # Настройки кодирования
    END_MARKER = b'\xff\xfe'  # Маркер конца сообщения
    DEFAULT_ENCODING = 'utf-8'

    @staticmethod
    def init_app(app):
        # Создаем папку для загрузок при запуске
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}