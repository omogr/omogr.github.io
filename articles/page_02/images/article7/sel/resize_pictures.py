import os
from PIL import Image

def create_thumbnails(file_list_path):
    """Создает уменьшенные копии изображений с размерами 100x100 и 80x80"""
    with open(file_list_path, 'r') as file:
        image_paths = [line.strip() for line in file.readlines()]

    for original_path in image_paths:
        if not os.path.exists(original_path):
            print(f"Файл не найден: {original_path}")
            continue

        try:
            with Image.open(original_path) as img:
                # Создаем базовое имя для новых файлов
                base, ext = os.path.splitext(original_path)
                

                if original_path.endswith("00.png"):
                    # Обработка для 80x80
                    img_copy = img.copy()
                    img_copy.thumbnail((80, 80))
                    new_size = min(img_copy.size[0], img_copy.size[1], 80)
                    img_copy = img_copy.crop((
                        (img_copy.width - new_size) // 2,
                        (img_copy.height - new_size) // 2,
                        (img_copy.width + new_size) // 2,
                        (img_copy.height + new_size) // 2
                    ))
                    img_copy.resize((80, 80), Image.LANCZOS).save(f"{base}_80x80{ext}")
                else:
                    # Обработка для 100x100
                    img_copy = img.copy()
                    img_copy.thumbnail((100, 100))
                    new_size = min(img_copy.size[0], img_copy.size[1], 100)
                    img_copy = img_copy.crop((
                        (img_copy.width - new_size) // 2,
                        (img_copy.height - new_size) // 2,
                        (img_copy.width + new_size) // 2,
                        (img_copy.height + new_size) // 2
                    ))
                    path = f"{base}_100x100{ext}"
                    path1 = path.replace('\\sel\\','\\')
                    img_copy.resize((100, 100), Image.LANCZOS).save(path1)
                    

        except Exception as e:
            print(f"Ошибка обработки {original_path}: {str(e)}")

if __name__ == "__main__":
    # Укажите путь к файлу со списком изображений
    create_thumbnails("png.lst") # путь/к/файлу.txt")