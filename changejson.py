import json


def transform_json_to_stepped_format(input_file='vocabulary.json', output_file='vocabulary.json'):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        # Отримуємо всі старі словники в порядку зростання
        # (Наприклад, ті що були під номерами 4, 5, 6, 7, 8, 9...)
        sorted_keys = sorted(old_data.keys(), key=lambda x: int(x))

        new_data = {}
        current_old_idx = 0

        # Проходимо по номерах сторінок від 1 до 40
        for page_num in range(1, 41):
            # Якщо номер ділиться на 4 без залишку — це Help Page, пропускаємо
            if page_num % 4 == 0:
                continue

            # Якщо у нас ще є старі дані, беремо наступний доступний словник
            if current_old_idx < len(sorted_keys):
                old_key = sorted_keys[current_old_idx]
                new_data[str(page_num)] = old_data[old_key]
                print(f"Старий словник '{old_key}' -> став ключем '{page_num}'")
                current_old_idx += 1

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

        print(f"\n✅ Готово! Створено файл: {output_file}")
        print(f"Ключі в новому файлі: {', '.join(new_data.keys())}")

    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    transform_json_to_stepped_format()