import os
import time
import tkinter as tk
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageTk

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

def adjust_transparency():
    """5. Прозорість зображення (зміна альфа-каналу)"""
    print("\n--- 5. Налаштування прозорості зображення ---")
    path = input("Введіть шлях до зображення: ").strip()
    if not os.path.exists(path):
        print("Файл не знайдено.")
        return
        
    try:
        img = Image.open(path).convert("RGBA")
        opacity_percent = float(input("Введіть рівень прозорості (0-100%, де 100 — повністю непрозоре, 0 — невидиме): ").strip())
        alpha_multiplier = max(0.0, min(1.0, opacity_percent / 100.0))
        
        r, g, b, a = img.split()
        a = a.point(lambda p: int(p * alpha_multiplier))
        img_transparent = Image.merge("RGBA", (r, g, b, a))
        
        out_path = input("Введіть шлях для збереження файлу (рекомендовано .png): ").strip()
        if not out_path.lower().endswith((".png", ".webp")):
            print("Увага: для збереження прозорості використовується формат PNG.")
            out_path = os.path.splitext(out_path)[0] + ".png"
            
        img_transparent.save(out_path, format="PNG")
        print(f"[Успіх] Зображення з прозорістю збережено у {out_path}")
    except Exception as e:
        print(f"[Помилка] Не вдалося змінити прозорість: {e}")

def crop_and_split():
    """6. Кадрування та розділення зображення на частини"""
    print("\n--- 6. Кадрування та розділення зображення ---")
    path = input("Введіть шлях до зображення: ").strip()
    if not os.path.exists(path):
        print("Файл не знайдено.")
        return

    try:
        img = Image.open(path)
        w, h = img.size
        print(f"Поточний розмір зображення: {w}x{h} px")
        
        print("\nОберіть операцію:")
        print("1. Розбити зображення на N x M частин (сітка)")
        print("2. Залишити тільки вибрану область (видалити все ззовні / Crop)")
        print("3. Видалити вибрану область (вирізати фрагмент всередині)")
        choice = input("Ваш вибір (1/2/3): ").strip()

        if choice == "1":
            cols = int(input("Введіть кількість частин по горизонталі (стовпців): "))
            rows = int(input("Введіть кількість частин по вертикалі (рядків): "))
            output_dir = input("Введіть папку для збереження частин: ").strip()
            
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                
            tile_w = w // cols
            tile_h = h // rows
            base_name, ext = os.path.splitext(os.path.basename(path))
            
            count = 0
            for r in range(rows):
                for c in range(cols):
                    left = c * tile_w
                    upper = r * tile_h
                    right = (c + 1) * tile_w if c < cols - 1 else w
                    lower = (r + 1) * tile_h if r < rows - 1 else h
                    
                    part = img.crop((left, upper, right, lower))
                    filename = f"{base_name}_part_{r+1}_{c+1}{ext}"
                    out_path = os.path.join(output_dir, filename) if output_dir else filename
                    part.save(out_path)
                    count += 1
            print(f"[Успіх] Зображення успішно розбито на {count} частин.")

        elif choice in ("2", "3"):
            print("Введіть координати прямокутної області (left, top, right, bottom):")
            left = int(input(f"Left (0 до {w-1}): "))
            top = int(input(f"Top (0 до {h-1}): "))
            right = int(input(f"Right ({left+1} до {w}): "))
            bottom = int(input(f"Bottom ({top+1} до {h}): "))

            if not (0 <= left < right <= w and 0 <= top < bottom <= h):
                print("Помилка: некоректні межі області.")
                return

            if choice == "2":
                cropped_img = img.crop((left, top, right, bottom))
                out_path = input("Введіть шлях для збереження вирізаної області: ").strip()
                cropped_img.save(out_path)
                print(f"[Успіх] Область вирізано і збережено у {out_path}")
            else:
                img_modified = img.convert("RGBA")
                fill_choice = input("Заповнити вирізану ділянку прозорістю (1) чи білим кольором (2)? ").strip()
                fill_color = (0, 0, 0, 0) if fill_choice == "1" else (255, 255, 255, 255)
                
                blank_patch = Image.new("RGBA", (right - left, bottom - top), fill_color)
                img_modified.paste(blank_patch, (left, top))
                
                out_path = input("Введіть шлях для збереження (для прозорості краще .png): ").strip()
                if fill_choice == "1" and not out_path.lower().endswith((".png", ".webp")):
                    out_path = os.path.splitext(out_path)[0] + ".png"
                img_modified.save(out_path)
                print(f"[Успіх] Область видалено, результат збережено у {out_path}")
        else:
            print("Невірний вибір.")
    except Exception as e:
        print(f"[Помилка] Не вдалося виконати кадрування: {e}")

def adjust_contrast():
    """7. Збільшення контрастності зображення"""
    print("\n--- 7. Регулювання контрастності зображення ---")
    path = input("Введіть шлях до зображення: ").strip()
    if not os.path.exists(path):
        print("Файл не знайдено.")
        return

    try:
        img = Image.open(path)
        factor = float(input("Введіть коефіцієнт контрастності (1.0 — без змін, > 1.0 — збільшення, наприклад 1.5 або 2.0): "))
        
        enhancer = ImageEnhance.Contrast(img)
        img_contrast = enhancer.enhance(factor)
        
        out_path = input("Введіть шлях для збереження файлу: ").strip()
        img_contrast.save(out_path)
        print(f"[Успіх] Зображення з підвищеною контрастністю збережено у {out_path}")
    except Exception as e:
        print(f"[Помилка] Не вдалося змінити контрастність: {e}")

def combine_images():
    """8. Об'єднання двох зображень горизонтально або вертикально"""
    print("\n--- 8. Об'єднання двох зображень ---")
    p1 = input("Введіть шлях до першого зображення: ").strip()
    p2 = input("Введіть шлях до другого зображення: ").strip()
    
    if not (os.path.exists(p1) and os.path.exists(p2)):
        print("Помилка: один або обидва файли не знайдено.")
        return

    print("Оберіть напрямок об'єднання:")
    print("1. Горизонтально (поруч одне біля одного)")
    print("2. Вертикально (одне під одним)")
    direction = input("Ваш вибір (1/2): ").strip()

    try:
        img1 = Image.open(p1).convert("RGBA")
        img2 = Image.open(p2).convert("RGBA")

        if direction == "1":
            # Масштабуємо друге зображення під висоту першого для охайного склеювання
            target_h = img1.height
            if img2.height != target_h:
                new_w = int(img2.width * (target_h / img2.height))
                img2 = img2.resize((new_w, target_h), Image.Resampling.LANCZOS)
            
            combined_w = img1.width + img2.width
            combined = Image.new("RGBA", (combined_w, target_h), (0, 0, 0, 0))
            combined.paste(img1, (0, 0))
            combined.paste(img2, (img1.width, 0))

        elif direction == "2":
            # Масштабуємо друге зображення під ширину першого
            target_w = img1.width
            if img2.width != target_w:
                new_h = int(img2.height * (target_w / img2.width))
                img2 = img2.resize((target_w, new_h), Image.Resampling.LANCZOS)
            
            combined_h = img1.height + img2.height
            combined = Image.new("RGBA", (target_w, combined_h), (0, 0, 0, 0))
            combined.paste(img1, (0, 0))
            combined.paste(img2, (0, img1.height))
        else:
            print("Невірний вибір напрямку.")
            return

        out_path = input("Введіть шлях для збереження (наприклад, combined.png): ").strip()
        if not out_path.lower().endswith((".png", ".webp")):
            out_path = os.path.splitext(out_path)[0] + ".png"
        combined.save(out_path)
        print(f"[Успіх] Зображення успішно об'єднано та збережено у {out_path}")
    except Exception as e:
        print(f"[Помилка] Не вдалося об'єднати зображення: {e}")

def add_watermark():
    """9. Створення водяного знаку на зображенні"""
    print("\n--- 9. Створення водяного знаку ---")
    path = input("Введіть шлях до зображення: ").strip()
    if not os.path.exists(path):
        print("Файл не знайдено.")
        return

    try:
        base_img = Image.open(path).convert("RGBA")
        text = input("Введіть текст водяного знаку: ").strip()
        font_size = int(input("Введіть розмір шрифту (наприклад, 36): ").strip() or "36")
        
        print("Введіть колір водяного знаку у форматі R,G,B (наприклад, 255,255,255):")
        color_input = input("Колір (R,G,B): ").strip() or "255,255,255"
        r, g, b = tuple(map(int, color_input.split(",")))
        
        opacity_percent = float(input("Введіть непрозорість (0-100%, наприклад 40): ").strip() or "40")
        alpha = int(max(0.0, min(1.0, opacity_percent / 100.0)) * 255)

        # Спроба завантажити системний шрифт TTF
        font = None
        font_candidates = ["arial.ttf", "DejaVuSans.ttf", "calibri.ttf", "/System/Library/Fonts/Helvetica.ttc"]
        for f in font_candidates:
            try:
                font = ImageFont.truetype(f, font_size)
                break
            except IOError:
                continue
        if font is None:
            font = ImageFont.load_default()

        # Шар для малювання з прозорістю
        txt_layer = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        print("\nОберіть положення водяного знаку:")
        print("1. По центру")
        print("2. Правий нижній кут")
        print("3. Лівий верхній кут")
        print("4. Правий верхній кут")
        print("5. Власні координати (X, Y)")
        pos_choice = input("Ваш вибір (1-5): ").strip()

        padding = 20
        if pos_choice == "1":
            pos = ((base_img.width - text_w) // 2, (base_img.height - text_h) // 2)
        elif pos_choice == "2":
            pos = (base_img.width - text_w - padding, base_img.height - text_h - padding)
        elif pos_choice == "3":
            pos = (padding, padding)
        elif pos_choice == "4":
            pos = (base_img.width - text_w - padding, padding)
        elif pos_choice == "5":
            x = int(input(f"X (0 до {base_img.width}): "))
            y = int(input(f"Y (0 до {base_img.height}): "))
            pos = (x, y)
        else:
            print("Невірний вибір. Використано положення по центру.")
            pos = ((base_img.width - text_w) // 2, (base_img.height - text_h) // 2)

        draw.text(pos, text, fill=(r, g, b, alpha), font=font)
        watermarked = Image.alpha_composite(base_img, txt_layer)

        out_path = input("Введіть шлях для збереження (наприклад, watermarked.png): ").strip()
        if not out_path.lower().endswith((".png", ".webp")):
            out_path = os.path.splitext(out_path)[0] + ".png"
            
        watermarked.save(out_path)
        print(f"[Успіх] Водяний знак нанесено. Збережено у {out_path}")
    except Exception as e:
        print(f"[Помилка] Не вдалося додати водяний знак: {e}")

def slideshow_player():
    """10. Слайд-шоу з відтворенням зображень через Tkinter"""
    print("\n--- 10. Слайд-шоу плеєр ---")
    print("1. Завантажити всі зображення з папки")
    print("2. Вказати перелік файлів через кому")
    choice = input("Ваш вибір (1/2): ").strip()

    images_paths = []
    valid_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    if choice == "1":
        folder = input("Введіть шлях до папки з зображеннями: ").strip()
        if not os.path.isdir(folder):
            print("Папку не знайдено.")
            return
        files = sorted(os.listdir(folder))
        images_paths = [os.path.join(folder, f) for f in files if os.path.splitext(f)[1].lower() in valid_exts]
    elif choice == "2":
        paths_input = input("Введіть шляхи до зображень через кому: ").strip()
        images_paths = [p.strip() for p in paths_input.split(",") if os.path.exists(p.strip())]
    else:
        print("Невірний вибір.")
        return

    if not images_paths:
        print("Не знайдено жодного коректного зображення.")
        return

    delay_sec = float(input("Введіть затримку між слайдами в секундах (наприклад, 2.0): ").strip() or "2.0")
    delay_ms = int(delay_sec * 1000)

    # Запуск вікна відтворення через Tkinter
    root = tk.Tk()
    root.title("Слайд-шоу лабораторних робіт")
    root.geometry("850x650")
    root.configure(bg="#1e1e1e")

    label_img = tk.Label(root, bg="#1e1e1e")
    label_img.pack(expand=True, fill="both")

    info_label = tk.Label(root, text="", font=("Arial", 11), fg="#dddddd", bg="#1e1e1e")
    info_label.pack(side="bottom", pady=5)

    idx = [0]

    def next_slide():
        if not root.winfo_exists():
            return
        img_path = images_paths[idx[0]]
        try:
            pil_img = Image.open(img_path)
            # Підгонка зображення під розмір вікна зі збереженням пропорцій
            win_w = max(400, root.winfo_width() - 40)
            win_h = max(300, root.winfo_height() - 70)
            pil_img.thumbnail((win_w, win_h), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(pil_img)
            label_img.config(image=photo)
            label_img.image = photo
            
            info_label.config(text=f"[{idx[0] + 1}/{len(images_paths)}] {os.path.basename(img_path)} (Закрийте вікно для виходу)")
        except Exception as e:
            info_label.config(text=f"Помилка завантаження {img_path}: {e}")

        idx[0] = (idx[0] + 1) % len(images_paths)
        root.after(delay_ms, next_slide)

    # Перший кадр викликаємо після повної ініціалізації вікна
    root.after(100, next_slide)
    print("Слайд-шоу запущено. Закрийте графічне вікно, щоб повернутися в консоль.")
    root.mainloop()

def main():
    while True:
        print("\n=======================================")
        print(" ЛАБОРАТОРНА РОБОТА: ОБРОБКА ЗОБРАЖЕНЬ ")
        print("=======================================")
        print("1. Конвертація форматів (пакетна/одинична)")
        print("2. Зміна розміру зображень (з пропорціями)")
        print("3. Перетворення (заміна) кольорів")
        print("4. Корекція колірного балансу / каналів")
        print("5. Налаштування прозорості (альфа-канал)")
        print("6. Кадрування та розбиття на частини (Crop/Grid)")
        print("7. Збільшення/зміна контрастності")
        print("8. Об'єднання двох зображень (Горизонтально/Вертикально)")
        print("9. Створення водяного знаку (текст, прозорість, позиція)")
        print("10. Слайд-шоу плеєр (Tkinter)")
        print("0. Вихід")
        
        choice = input("Оберіть пункт меню (0-10): ").strip()
        if choice == "1":
            convert_formats()
        elif choice == "2":
            resize_images()
        elif choice == "3":
            transform_colors()
        elif choice == "4":
            adjust_color_balance()
        elif choice == "5":
            adjust_transparency()
        elif choice == "6":
            crop_and_split()
        elif choice == "7":
            adjust_contrast()
        elif choice == "8":
            combine_images()
        elif choice == "9":
            add_watermark()
        elif choice == "10":
            slideshow_player()
        elif choice == "0":
            print("Вихід з програми. До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()