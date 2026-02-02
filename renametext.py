import os
import re


def shift_filenames(folder_path='Texts'):
    if not os.path.exists(folder_path):
        print(f"Папка '{folder_path}' не знайдена!")
        return

    # 1. Отримуємо всі файли temp_page_N.png
    files = [f for f in os.listdir(folder_path) if re.match(r'temp_page_\d+\.png', f)]

    # Сортуємо їх за номером
    files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

    print(f"Знайдено файлів: {len(files)}")

    # 2. Крок перший: перейменовуємо у тимчасові назви, щоб не було збігів
    # (наприклад, temp_page_4.png -> tmp_1.png)
    temp_changes = []
    for filename in files:
        old_num = int(re.search(r'\d+', filename).group())
        new_num = old_num - 3

        if new_num < 1:
            print(f"Пропуск {filename}: номер стане менше 1")
            continue

        old_path = os.path.join(folder_path, filename)
        tmp_path = os.path.join(folder_path, f"tmp_{new_num}.png")

        os.rename(old_path, tmp_path)
        temp_changes.append((tmp_path, new_num))

    # 3. Крок другий: перетворюємо тимчасові назви на фінальні
    # (tmp_1.png -> temp_page_1.png)
    for tmp_path, num in temp_changes:
        final_path = os.path.join(folder_path, f"temp_page_{num}.png")
        os.rename(tmp_path, final_path)
        print(f"Готово: сторінка {num + 3} тепер стала сторінкою {num}")

    print("\nУсі файли успішно перейменовано!")


if __name__ == "__main__":
    shift_filenames()