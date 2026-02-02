import os
import re


def rename_mp3_to_stepped_logic(folder_path='Mp3'):
    if not os.path.exists(folder_path):
        print(f"Папка '{folder_path}' не знайдена!")
        return

    # 1. Отримуємо список усіх mp3 файлів
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp3')]

    # Сортуємо їх за цифрами в назві, щоб "Трек 1" був першим, "Трек 10" останнім
    def extract_number(filename):
        nums = re.findall(r'\d+', filename)
        return int(nums[0]) if nums else 0

    files.sort(key=extract_number)

    print(f"Знайдено файлів: {len(files)}")

    # 2. Перейменовуємо у тимчасові імена, щоб не було конфліктів
    temp_renames = []
    current_track_idx = 0

    for page_num in range(1, 41):
        # Якщо це сторінка Help (4, 8, 12...), пропускаємо її номер
        if page_num % 4 == 0:
            continue

        # Якщо файли ще є в списку, готуємо нове ім'я
        if current_track_idx < len(files):
            old_name = files[current_track_idx]
            new_name = f"{str(page_num).zfill(2)}.mp3"

            old_path = os.path.join(folder_path, old_name)
            temp_path = os.path.join(folder_path, f"temp_{new_name}")

            os.rename(old_path, temp_path)
            temp_renames.append(f"temp_{new_name}")
            print(f"Обробка: {old_name} -> {new_name}")
            current_track_idx += 1

    # 3. Прибираємо префікс "temp_"
    for temp_f in temp_renames:
        final_path = os.path.join(folder_path, temp_f.replace('temp_', ''))
        os.rename(os.path.join(folder_path, temp_f), final_path)

    print("\n✅ Готово! Файли тепер мають імена: 01.mp3, 02.mp3, 03.mp3, 05.mp3, 06.mp3...")


if __name__ == "__main__":
    rename_mp3_to_stepped_logic()