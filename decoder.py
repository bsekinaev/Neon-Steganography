from PIL import Image
import warnings
import re
import os
import sys

def decode_image(image_path):
    """Декодирует сообщение из изображения"""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            # Открываем изображение
            try:
                with Image.open(image_path) as img:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    width, height = img.size
                    binary_data = []
                    pixels = img.load()
                    
                    # Собираем биты из изображения
                    for y in range(height):
                        for x in range(width):
                            pixel = pixels[x, y]
                            if isinstance(pixel, int):
                                pixel = (pixel, pixel, pixel)
                            for channel in range(3):
                                binary_data.append(str(pixel[channel] & 1))

                    binary_str = ''.join(binary_data)
                    
                    # ИСПРАВЛЕННЫЙ вариант без list comprehension
                    bytes_list = []
                    for i in range(0, len(binary_str), 8):
                        if i+8 <= len(binary_str):
                            bytes_list.append(binary_str[i:i+8])
                    
                    # Декодируем сообщение
                    message = bytearray()
                    for byte in bytes_list:
                        message.append(int(byte, 2))
                        # Проверяем маркер конца сообщения
                        if len(message) >= 2 and message[-2:] == b'\xff\xfe':
                            return message[:-2].decode('utf-8', errors='ignore')
                    
                    # Пытаемся декодировать как текст
                    try:
                        decoded = message.decode('utf-8')
                        return decoded if decoded.strip() else "Сообщение не найдено"
                    except UnicodeDecodeError:
                        return "Обнаружены бинарные данные (не текст)"
            
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл {image_path} не найден")
            
    except Exception as e:
        raise ValueError(f"Ошибка декодирования: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Использование: python decoder.py <путь_к_изображению>")
        sys.exit(1)
        
    try:
        result = decode_image(sys.argv[1])
        print("Результат:", result)
    except Exception as e:
        print("Ошибка:", str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()