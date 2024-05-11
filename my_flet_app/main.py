import flet as ft


class Task(ft.UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Checkbox(value=False,
                                        label=self.task_name,
                                        on_change=self.status_changed)
        self.edit_name = ft.TextField(expand=1)
        self.display_view = ft.Row(
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Редактировать задачу",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Удалить задачу",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.edit_name,
                ft.IconButton(
                    ft.icons.DONE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Обновить задачу",
                    on_click=self.save_clicked,
                ),
            ],
        )

        return ft.Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self,e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self,e):
        self.completed =self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)


class TodoApp(ft.UserControl):
    def build(self):
        self.new_task = ft.TextField(hint_text="Что нужно сделать", expand=True)
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text="Все задачи"), ft.Tab(text="Активные задачи"), ft.Tab(text="Выполненные задачи")
            ],
        )

        self.item_left = ft.Text("0 Активных задач")

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD,
                            on_click=self.add_clicked,
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.item_left,
                                ft.OutlinedButton(
                                    text="Очистить список не выполненных задач",
                                    on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    def add_clicked(self, e):
        task = Task(self.new_task.value, self.task_status_change, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self,task):
        self.tasks.controls.remove(task)
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def update(self):
        count = 0
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible=(
                status == "Все задачи"
                or (status == "Активные задачи" and task.completed == False)
                or (status == "Выполненные задачи" and task.completed)
            )
            if not task.completed:
                count += 1
        self.item_left.value = f"{count} активных задач осталось."
        super().update()

    def tabs_changed(self, e):
        self.update()

def main(page: ft.Page):
    page.title = "Приложение задачник"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    app = TodoApp()
    page.add(app)

ft.app(target=main)



