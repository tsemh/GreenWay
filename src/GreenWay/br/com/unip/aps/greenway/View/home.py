import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from pathlib import Path
import os


class HomeScreen:
    def __init__(self, app):
        self.app = app
        self.repository = app.repository
        self.current_user = app.current_user
        current_dir = Path(os.path.dirname(__file__))
        self.box = self.create_home_screen(current_dir)

    def create_home_screen(self, current_dir):
        if self.current_user:
            user = self.current_user
            score = user['score']
            kg_reunidos = user['kg']
            tarefas_realizadas = user['missao']
            ranking_position = self.repository.get_user_ranking_position(user['email'])
        else:
            score = 0
            kg_reunidos = 0
            tarefas_realizadas = 0
            ranking_position = 0

        menu_path = current_dir / ".." / ".." / ".." / ".." / ".." / ".." / "resources" / "images" / "menu"

        self.home_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                background_color='#F0F5E6',
                align_items=CENTER,
                flex=1
            )
        )

        menu_superior = toga.Box(
            style=Pack(
                direction=ROW,
                padding=5,
                height=30,
                align_items=CENTER,
                margin_top=20,
                margin_bottom=20,
                background_color='#F0F5E6',
            )
        )
        spacer = toga.Box(style=Pack(flex=1))
        menu_superior.add(spacer)

        menu_superior.add(
            toga.Button(
                icon=str(menu_path / 'config_green.png'),
                on_press=lambda widget: self.btn_switchScreen(widget, 'config'),
                style=Pack(
                    height=40,
                    width=50,
                    margin=5,
                    margin_left=10,
                    background_color='#F0F5E6',
                )
            )
        )
        menu_superior.add(
            toga.Button(
                icon=str(menu_path / 'perfil_green.png'),
                on_press=lambda widget: self.btn_switchScreen(widget, 'perfil'),
                style=Pack(
                    height=40,
                    width=50,
                    margin=5,
                    margin_left=10,
                    background_color='#F0F5E6',
                )
            )
        )

        self.home_box.add(menu_superior)

        self.home_box.add(toga.Label(
            "Green Way",
            style=Pack(
                font_size=28,
                font_weight='bold',
                margin_bottom=10,
                margin_top=10,
                color='#184C2F',
                text_align='center'
            )
        ))

        score_container = toga.Box(
            style=Pack(
                direction=COLUMN,
                align_items=CENTER,
                margin_bottom=20
            )
        )

        gradient_path = current_dir / ".." / ".." / ".." / ".." / ".." / ".." / "resources" / "images" / "gradient.png"
        gradient = toga.Image(str(gradient_path))
        img_view = toga.ImageView(gradient)
        img_view.style = Pack(width=210)
        score_container.add(img_view)

        score_container.add(toga.Label(
            str(score),
            style=Pack(
                font_size=26,
                color=self.scoreColor(score),
                text_align='center',
                margin_top=-70,
                width=80,
                background_color='#F0F5E600',
                font_weight='bold'
            )
        ))

        self.home_box.add(score_container)

        kg_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=15,
                align_items=CENTER,
                margin=20,
                background_color="#184C2F",
            )
        )
        kg_box.add(toga.Label(
            f"{kg_reunidos} kg",
            style=Pack(
                font_size=24,
                color='#FFFFFF',
                text_align='center',
                font_weight='bold'
            )
        ))
        self.home_box.add(kg_box)

        rankReali_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=10,
                align_items=CENTER,
                margin_top=20,
                margin_bottom=20,
                background_color="#F0F5E6",
            )
        )

        ranking_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                align_items=CENTER,
                background_color="#184C2F",
                margin=5,
                flex=1
            )
        )
        ranking_box.add(toga.Label(
            "Posição no \n ranking",
            style=Pack(
                font_size=18,
                color='#FFFFFF',
                text_align='center',
            )
        ))
        ranking_box.add(toga.Label(
            str(ranking_position),
            style=Pack(
                font_size=24,
                color='#FFFFFF',
                text_align='center',
                font_weight='bold'
            )
        ))
        rankReali_box.add(ranking_box)

        realizadas_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                align_items=CENTER,
                background_color="#184C2F",
                margin_right=5,
                flex=1
            )
        )
        realizadas_box.add(toga.Label(
            "Tarefas \n realizadas",
            style=Pack(
                font_size=18,
                color='#FFFFFF',
                text_align='center',
            )
        ))
        realizadas_box.add(toga.Label(
            str(tarefas_realizadas),
            style=Pack(
                font_size=24,
                color='#FFFFFF',
                text_align='center',
                font_weight='bold',
            )
        ))
        rankReali_box.add(realizadas_box)

        self.home_box.add(rankReali_box)

        content_spacer = toga.Box(style=Pack(flex=1))
        self.home_box.add(content_spacer)

        menu_inferior = toga.Box(
            style=Pack(
                direction=ROW,
                padding=15,
                align_items=CENTER,
                background_color='#F0F5E6',
                height=70
            )
        )

        btn_menu = ['Tarefas', 'Ranking', 'Home', 'Convide um amigo']
        for btn in btn_menu:
            icon_name = f"{btn.lower().replace(' ', '_')}.png"
            icon_path = menu_path / icon_name

            if Path(icon_path).exists():
                menu_inferior.add(self.btn_addition(str(icon_path), btn))
            else:
                menu_inferior.add(toga.Button(
                    btn[:3],
                    on_press=lambda widget, screen=btn: self.btn_switchScreen(widget, screen),
                    style=Pack(
                        height=40,
                        width=50,
                        margin=5,
                        margin_left=8,
                        margin_right=8,
                        background_color='#F0F5E6'
                    )
                ))

        self.home_box.add(menu_inferior)

        return self.home_box

    def btn_switchScreen(self, widget, screen):
        print(f"Mudando para tela: {screen}")

    def btn_addition(self, icon_path, screen_name):
        return toga.Button(
            icon=icon_path,
            on_press=lambda widget: self.btn_switchScreen(widget, screen_name),
            style=Pack(
                height=40,
                width=50,
                margin=5,
                margin_left=8,
                margin_right=8,
                background_color='#F0F5E6'
            )
        )

    def scoreColor(self, score: int) -> str:
        colors = [
            (333, '#FFA500'),
            (445, '#FFC300'),
            (557, '#FFFF00'),
            (668, "#ACFF2F"),
            (1000, "#00FF00")
        ]
        return next((color for limit, color in colors if score <= limit), '#133C1F')
