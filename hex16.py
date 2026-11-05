import flet as ft
from deep_translator import MyMemoryTranslator

def main(page: ft.Page):
                                                                # --- НАСТРОЙКА ОКНА (Классический синтаксис Flet) ---
    page.title = "HEX16"
    page.window_width = 550
    page.window_height = 640
    page.window_min_width = 540
    page.window_min_height = 620
    page.theme_mode = ft.ThemeMode.DARK

    lang_mapping = {
        "Французский 🇫🇷": "french",
        "Английский 🇬🇧": "english"
    }

                                                                # --- СИСТЕМНЫЕ ФУНКЦИИ ---
    def copy_to_clipboard(element):
        if element.value and element.value != "...":
            page.set_clipboard(element.value)
            page.open(ft.SnackBar(ft.Text("✨ Текст успешно скопирован!"), show_close_icon=True))

    def paste_from_clipboard(element):
        element.value = page.get_clipboard()
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            btn_theme.text = "Тёмная тема"
            btn_theme.icon = ft.icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            btn_theme.text = "Светлая тема"
            btn_theme.icon = ft.icons.LIGHT_MODE
        page.update()

                                                                # --- ЛОГИКА: ЗАКОДИРОВАТЬ ---
    def process_text(e):
        user_input = entry_ru.value.strip() if entry_ru.value else ""
        if not user_input:
            page.open(ft.SnackBar(ft.Text("⚠️ Пожалуйста, введите текст!")))
            return
        
        try:
            try:
                key = int(entry_key.value)
                if not (1 <= key <= 255):
                    raise ValueError
            except ValueError:
                page.open(ft.SnackBar(ft.Text("❌ Ключ должен быть числом от 1 до 255!")))
                return

            target_lang = lang_mapping[combo_lang.value]
            translator = MyMemoryTranslator(source='russian', target=target_lang)
            translated_text = translator.translate(user_input)

            raw_bytes = translated_text.encode('utf-8')
            encrypted_bytes = bytes([b ^ key for b in raw_bytes])
            hex_encoded = encrypted_bytes.hex()

            entry_result.value = translated_text
            entry_hex_result.value = hex_encoded
            page.update()
            
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"❌ Ошибка перевода: {ex}")))

                                                                # --- ЛОГИКА: РАСШИФРОВАТЬ ---
    def deprocess_text(e):
        hex_input = entry_hex_in.value.strip() if entry_hex_in.value else ""
        if not hex_input:
            page.open(ft.SnackBar(ft.Text("⚠️ Введите HEX-код!")))
            return

        if len(hex_input) % 2 != 0:
            page.open(ft.SnackBar(ft.Text("❌ Длина HEX-кода должна быть чётной (каждый байт — это 2 символа)!")))
            return

        try:
            try:
                key = int(entry_key_dec.value)
                if not (1 <= key <= 255):
                    raise ValueError
            except ValueError:
                page.open(ft.SnackBar(ft.Text("❌ Введите числовой ключ от 1 до 255!")))
                return

            encrypted_bytes = bytes.fromhex(hex_input)
            decrypted_bytes = bytes([b ^ key for b in encrypted_bytes])
            decoded_text = decrypted_bytes.decode('utf-8')

            source_lang = lang_mapping[combo_lang_dec.value]
            translator = MyMemoryTranslator(source=source_lang, target='russian')
            russian_text = translator.translate(decoded_text)

            entry_text_out.value = decoded_text
            entry_ru_out.value = russian_text
            page.update()
            
        except ValueError:
            page.open(ft.SnackBar(ft.Text("❌ Некорректный HEX-код или неверный ключ!")))
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"❌ Не удалось расшифровать (неверный ключ или язык)")))

                                                                # --- ИНТЕРФЕЙС ВКЛАДКИ 1 ---
    entry_ru = ft.TextField(label="Введите текст на русском", expand=True)
    entry_key = ft.TextField(label="Ключ (1-255)", value="12", width=120, text_align=ft.TextAlign.CENTER)
    combo_lang = ft.Dropdown(
        label="Выберите язык перевода",
        options=[ft.dropdown.Option(k) for k in lang_mapping.keys()],
        value="Французский 🇫🇷",
        expand=True
    )
    entry_result = ft.TextField(label="Результат перевода", read_only=True, value="...", text_align=ft.TextAlign.CENTER, expand=True)
    entry_hex_result = ft.TextField(label="16-ричный код (HEX)", read_only=True, value="...", text_align=ft.TextAlign.CENTER, expand=True)

    tab_encrypt_content = ft.Column([
        ft.Text("Шифрование текста", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([entry_ru]),
        ft.Row([ft.Container(combo_lang, expand=3), ft.Container(entry_key, expand=1)]),
        ft.Text("Результаты:", size=14, weight=ft.FontWeight.W_500),
        ft.Row([entry_result, ft.IconButton(ft.icons.COPY, on_click=lambda _: copy_to_clipboard(entry_result))]),
        ft.Row([entry_hex_result, ft.IconButton(ft.icons.COPY, on_click=lambda _: copy_to_clipboard(entry_hex_result))]),
        ft.ElevatedButton("Перевести и закодировать", on_click=process_text, bgcolor=ft.colors.GREEN_700, color=ft.colors.WHITE, height=45)
    ], spacing=15, scroll=ft.ScrollMode.AUTO)

                                                                    # --- ИНТЕРФЕЙС ВКЛАДКИ 2 ---
    entry_hex_in = ft.TextField(label="Вставьте 16-ричный код (HEX)", expand=True)
    entry_key_dec = ft.TextField(label="Ключ (1-255)", value="12", width=120, text_align=ft.TextAlign.CENTER)
    combo_lang_dec = ft.Dropdown(
        label="Какой язык закодирован в HEX?",
        options=[ft.dropdown.Option(k) for k in lang_mapping.keys()],
        value="Французский 🇫🇷",
        expand=True
    )
    entry_text_out = ft.TextField(label="Расшифрованный иностранный текст", read_only=True, value="...", text_align=ft.TextAlign.CENTER, expand=True)
    entry_ru_out = ft.TextField(label="Перевод на русский язык", read_only=True, value="...", text_align=ft.TextAlign.CENTER, expand=True)

    tab_decrypt_content = ft.Column([
        ft.Text("Дешифрование HEX", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([entry_hex_in, ft.IconButton(ft.icons.PASTE, on_click=lambda _: paste_from_clipboard(entry_hex_in))]),
        ft.Row([ft.Container(combo_lang_dec, expand=3), ft.Container(entry_key_dec, expand=1)]),
        ft.Text("Результаты:", size=14, weight=ft.FontWeight.W_500),
        ft.Row([entry_text_out, ft.IconButton(ft.icons.COPY, on_click=lambda _: copy_to_clipboard(entry_text_out))]),
        ft.Row([entry_ru_out, ft.IconButton(ft.icons.COPY, on_click=lambda _: copy_to_clipboard(entry_ru_out))]),
        ft.ElevatedButton("Расшифровать и перевести", on_click=deprocess_text, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE, height=45)
    ], spacing=15, scroll=ft.ScrollMode.AUTO)

                                                                 # --- ВЕРХНЯЯ ПАНЕЛЬ И ВКЛАДКИ ---
    btn_theme = ft.TextButton("Светлая тема", icon=ft.icons.LIGHT_MODE, on_click=toggle_theme)
    
    top_bar = ft.Row([
        ft.Text("HEX16", size=22, weight=ft.FontWeight.BOLD),
        ft.Row([
            btn_theme, 
            ft.IconButton(
                icon=ft.icons.CLOSE, 
                icon_color=ft.colors.RED_400, 
                tooltip="Выйти", 
                on_click=lambda e: page.window_close() 
            )
        ], spacing=5)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=250,
        tabs=[
            ft.Tab(text="🔒 Закодировать", content=ft.Container(tab_encrypt_content, padding=ft.padding.only(top=15))),
            ft.Tab(text="🔓 Расшифровать", content=ft.Container(tab_decrypt_content, padding=ft.padding.only(top=15)))
        ],
        expand=True
    )

    page.add(top_bar, tabs)
ft.app(target=main)