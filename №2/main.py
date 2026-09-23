import os
from PIL import Image, ImageEnhance

def convert_formats():
    """1. Конвертація форматів зображень з порівнянням розмірів"""
    print("\n--- 1. Конвертація форматів зображень ---")
    paths_input = input("Введіть шлях до зображення (або кілька шляхів через кому): ").strip()
    paths = [p.strip() for p in paths_input.split(",") if p.strip()]
    
    target_format = input("Введіть вихідний формат (наприклад, PNG, JPEG, WEBP, BMP): ").strip().upper()
    output_dir = input("Введіть шлях до директорії збереження (або натисніть Enter для збереження в тій самій папці): ").strip()
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    for path in paths:
        if not os.path.exists(path):
            print(f"Файл не знайдено: {path}")
            continue
        try:
            original_size = os.path.getsize(path)
            img = Image.open(path)
            
            # Конвертація в RGB для сумісності з форматами на кшталт JPEG (якщо є альфа-канал)
            if target_format == "JPEG" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            base_name = os.path.splitext(os.path.basename(path))[0]
            out_filename = f"{base_name}.{target_format.lower()}"
            out_path = os.path.join(output_dir, out_filename) if output_dir else out_filename
            
            img.save(out_path, format=target_format)
            new_size = os.path.getsize(out_path)
            
            print(f"\n[Успіх] {path} -> {out_path}")
            print(f"  Початковий розмір: {original_size / 1024:.2f} KB")
            print(f"  Новий розмір: {new_size / 1024:.2f} KB")
            diff = new_size - original_size
            percent = (diff / original_size) * 100 if original_size > 0 else 0
            print(f"  Зміна розміру: {diff / 1024:.2f} KB ({percent:+.2f}%)")
        except Exception as e:
            print(f"[Помилка] Не вдалося обробити {path}: {e}")

def resize_images():
    """2. Конвертація розміру зображень (окремо або зі збереженням пропорцій)"""
    print("\n--- 2. Конвертація розміру зображень ---")
    paths_input = input("Введіть шлях до зображення (або кілька шляхів через кому): ").strip()
    paths = [p.strip() for p in paths_input.split(",") if p.strip()]
    
    print("Виберіть режим зміни розміру:")
    print("1. За заданими шириною та висотою (розтягування/деформація)")
    print("2. За шириною (зі збереженням пропорцій)")
    print("3. За висотою (зі збереженням пропорцій)")
    mode = input("Ваш вибір (1/2/3): ").strip()
    
    width, height = None, None
    if mode == "1":
        width = int(input("Введіть ширину (px): "))
        height = int(input("Введіть висоту (px): "))
    elif mode == "2":
        width = int(input("Введіть нову ширину (px): "))
    elif mode == "3":
        height = int(input("Введіть нову висоту (px): "))
    else:
        print("Невірний режим.")
        return

    output_dir = input("Введіть шлях до директорії збереження (або Enter для поточної): ").strip()
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    for path in paths:
        if not os.path.exists(path):
            print(f"Файл не знайдено: {path}")
            continue
        try:
            img = Image.open(path)
            orig_w, orig_h = img.size
            
            if mode == "1":
                new_size = (width, height)
            elif mode == "2":
                ratio = width / orig_w
                new_size = (width, int(orig_h * ratio))
            elif mode == "3":
                ratio = height / orig_h
                new_size = (int(orig_w * ratio), height)
                
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
            
            base_name, ext = os.path.splitext(os.path.basename(path))
            out_filename = f"{base_name}_resized{ext}"
            out_path = os.path.join(output_dir, out_filename) if output_dir else out_filename
            
            img_resized.save(out_path)
            print(f"[Успіх] Збережено: {out_path} (Новий розмір: {new_size[0]}x{new_size[1]})")
        except Exception as e:
            print(f"[Помилка] Не вдалося змінити розмір {path}: {e}")

def transform_colors():
    """3. Перетворення кольорів (заміна певного кольору на інший)"""
    print("\n--- 3. Перетворення кольорів ---")
    path = input("Введіть шлях до зображення: ").strip()
    if not os.path.exists(path):
        print("Файл не знайдено.")
        return
        
    try:
        img = Image.open(path).convert("RGB")
        print("Введіть старий колір у форматі R,G,B (наприклад: 255,255,255):")
        old_rgb = tuple(map(int, input("Старий колір (R,G,B): ").split(",")))
        
        print("Введіть новий колір у форматі R,G,B (наприклад: 0,0,0):")
        new_rgb = tuple(map(int, input("Новий колір (R,G,B): ").split(",")))
        
        tolerance = int(input("Введіть допустиму похибку кольору (0 для точного збігу, наприклад 15): ").strip() or "0")
        
        pixels = img.load()
        width, height = img.size
        
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                if (abs(r - old_rgb[0]) <= tolerance and
                    abs(g - old_rgb[1]) <= tolerance and
                    abs(b - old_rgb[2]) <= tolerance):
                    pixels[x, y] = new_rgb
                    
        out_path = input("Введіть шлях для збереження файлу: ").strip()
        img.save(out_path)
        print(f"[Успіх] Зображення з перетвореними кольорами збережено у {out_path}")
    except Exception as e:
        print(f"[Помилка] Не вдалося перетворити кольори: {e}")

def adjust_color_balance():
    """4. Корекція колірного балансу (канали RGB або загальна яскравість)"""
    print("\n--- 4. Корекція колірного балансу ---")
    path = input("Введіть шлях до зображення: ").strip()
    if not os.path.exists(path):
        print("Файл не знайдено.")
        return
        
    try:
        img = Image.open(path).convert("RGB")
        print("Виберіть тип корекції:")
        print("1. Загальна корекція яскравості")
        print("2. Збільшити/зменшити червоний канал (Red)")
        print("3. Збільшити/зменшити зелений канал (Green)")
        print("4. Збільшити/зменшити синій канал (Blue)")
        choice = input("Ваш вибір (1/2/3/4): ").strip()
        
        if choice == "1":
            factor = float(input("Введіть коефіцієнт (наприклад, 1.2 — збільшити на 20%, 0.8 — зменшити): "))
            enhancer = ImageEnhance.Brightness(img)
            img_adjusted = enhancer.enhance(factor)
        elif choice in ("2", "3", "4"):
            factor = float(input("Введіть коефіцієнт множення каналу (наприклад, 1.3): "))
            r, g, b = img.split()
            if choice == "2":
                r = r.point(lambda i: min(255, int(i * factor)))
            elif choice == "3":
                g = g.point(lambda i: min(255, int(i * factor)))
            elif choice == "4":
                b = b.point(lambda i: min(255, int(i * factor)))
            img_adjusted = Image.merge("RGB", (r, g, b))
        else:
            print("Невірний вибір.")
            return
            
        out_path = input("Введіть шлях для збереження файлу: ").strip()
        img_adjusted.save(out_path)
        print(f"[Успіх] Зображення з відкоригованим балансом збережено у {out_path}")
    except Exception as e:
        print(f"[Помилка] Не вдалося виконати корекцію балансу: {e}")

def main():
    while True:
        print("\n=======================================")
        print(" ЛАБОРАТОРНА РОБОТА: ОБРОБКА ЗОБРАЖЕНЬ ")
        print("=======================================")
        print("1. Конвертація форматів (пакетна/одинична)")
        print("2. Зміна розміру зображень (з пропорціями)")
        print("3. Перетворення (заміна) кольорів")
        print("4. Корекція колірного балансу / каналів")
        print("0. Вихід")
        
        choice = input("Оберіть пункт меню (0-4): ").strip()
        if choice == "1":
            convert_formats()
        elif choice == "2":
            resize_images()
        elif choice == "3":
            transform_colors()
        elif choice == "4":
            adjust_color_balance()
        elif choice == "0":
            print("Вихід з програми. До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()