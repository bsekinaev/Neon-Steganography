from PIL import Image
import warnings

def encode_image(image_path, secret_text, output_path="encoded.png"):
    # Открываем изображение с игнорированием предупреждений о палитре
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        img = Image.open(image_path)
    
    # Конвертируем в RGB, если изображение не в этом режиме
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    width, height = img.size
    # Преобразуем текст в бинарный вид (UTF-8)
    binary_secret = ''.join(format(byte, '08b') for byte in secret_text.encode('utf-8'))
    # Добавляем маркер конца сообщения
    binary_secret += '1111111111111110'  # 0xFFFE в бинарном виде

    # Проверяем, поместится ли текст
    max_bits = width * height * 3
    if len(binary_secret) > max_bits:
        raise ValueError(f"Текст слишком большой! Максимум: {max_bits//8} символов")

    data_index = 0
    pixels = img.load()  # Загружаем пиксели для быстрого доступа
    
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            # Меняем последний бит в каждом цветовом канале (R, G, B)
            for color_channel in range(3):  # Только первые 3 канала (RGB)
                if data_index < len(binary_secret):
                    pixel[color_channel] = (pixel[color_channel] & 0xFE) | int(binary_secret[data_index])
                    data_index += 1
            pixels[x, y] = tuple(pixel)

    # Сохраняем результат
    img.save(output_path)
    print(f"Сообщение сохранено в {output_path}")

if __name__ == "__main__":
    try:
        encode_image("input.png", "Тестовое сообщение")
    except Exception as e:
        print(f"Ошибка: {e}")