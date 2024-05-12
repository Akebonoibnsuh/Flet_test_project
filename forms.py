import flet as ft

from Classes import TinkoffInvestClient

INVEST_TOKEN = "____"

client_r = TinkoffInvestClient(INVEST_TOKEN)


def update_account_data(account_data_container, page):
    account_data_container.controls.clear()  # Очистка предыдущих данных
    account_ids = client_r.get_accounts_id

    for account_id in account_ids:
        positions = client_r.get_positionts(account_id)
        money_positions = client_r.get_money_positions(positions)
        security_positions = client_r.get_security_positions(positions)

        # Создание списка виджетов для отображения денежных позиций
        money_position_widgets = [
            ft.Text(f"{currency}: {amount}") for currency, amount in money_positions.items()
        ]

        # Создание списка виджетов для отображения позиций по бумагам
        security_position_widgets = [
            ft.Text(f"{figi}: {balance}") for figi, balance in security_positions.items()
        ]

        # Создание виджета для отображения данных о счете
        account_data_widget = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Account ID: {account_id}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Money Positions:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Column(money_position_widgets),  # Виджеты денежных позиций
                        ft.Text("Security Positions:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Column(security_position_widgets),  # Виджеты позиций по бумагам
                    ],
                    tight=True
                ),
                padding=10
            ),
            elevation=5,
            margin=10
        )

        # Добавление виджета в контейнер
        account_data_container.controls.append(account_data_widget)

    # Обновление страницы
    page.update()


def form(page: ft.Page):
    # Установка заголовка страницы
    page.title = "Мои счета"

    # Создание контейнера для отображения данных о счетах
    account_data_container = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # Вызов функции для обновления данных о счетах
    update_account_data(account_data_container, page)


    # Добавление контейнера с данными о счетах на страницу
    page.add(account_data_container)

# Запуск приложения
ft.app(target=form)


