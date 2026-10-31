import flet as ft

def main(page: ft.Page):
    page.title = "IGOS Trading Bot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    status_text = ft.Text("Статус: Ожидание запуска", size=16, color=ft.colors.AMBER_400)
    balance_text = ft.Text("Виртуальный баланс: $1,000.00 USDT", size=18, weight=ft.FontWeight.BOLD)

    def start_bot_click(e):
        status_text.value = "Статус: Сканирование рынка и работа в DRY_RUN..."
        status_text.color = ft.colors.GREEN_400
        page.update()

    start_button = ft.ElevatedButton(
        text="Запустить движок IGOS",
        icon=ft.icons.PLAY_ARROW,
        on_click=start_bot_click,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE_700
    )

    page.add(
        ft.Column([
            ft.Text("🤖 IGOS Mobile", size=28, weight=ft.FontWeight.BOLD),
            balance_text,
            status_text,
            ft.Divider(height=20),
            start_button
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == '__main__':
    ft.app(target=main)
