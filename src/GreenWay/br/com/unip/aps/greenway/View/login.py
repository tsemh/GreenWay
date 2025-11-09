import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from pathlib import Path
import os


class LoginScreen:
    def __init__(self, app):
        self.app = app
        current_dir = Path(os.path.dirname(__file__))
        self.box = self.create_login_screen(current_dir)

    def create_login_screen(self, current_dir):
        self.login_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                margin=10,
                background_color='#F0F5E6',
                align_items=CENTER,
                flex=1
            )
        )

        logo_container = toga.Box(
            style=Pack(
                direction=COLUMN,
                align_items=CENTER,
                margin_bottom=30,
                margin_top=50
            )
        )

        logo_path = current_dir / '..' / '..' / '..' / '..' / '..' / '..' / 'resources' / 'images' / 'logo.png'
        if logo_path.exists():
            logo = toga.Image(str(logo_path))
            img_view = toga.ImageView(logo)
            img_view.style = Pack(width=100, height=100)
            logo_container.add(img_view)

        logo_container.add(
            toga.Label(
                "Green Way",
                style=Pack(
                    font_size=28,
                    font_weight='bold',
                    margin_bottom=10,
                    margin_top=10,
                    color='#184C2F',
                    text_align='center'
                )
            )
        )
        self.login_box.add(logo_container)

        forms_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                margin=20,
                align_items=CENTER,
                width=300
            )
        )

        self.email_input = toga.TextInput(
            placeholder="E-mail",
            style=Pack(
                background_color='#FFFFFF',
                color='#333333',
                margin_bottom=10,
                padding=10,
                width=280,
                height=45
            )
        )

        self.senha_input = toga.PasswordInput(
            placeholder="Senha",
            style=Pack(
                background_color='#FFFFFF',
                color='#333333',
                margin_bottom=15,
                padding=10,
                width=280,
                height=45
            )
        )

        forms_box.add(self.email_input)
        forms_box.add(self.senha_input)

        login_btn = toga.Button(
            "ENTRAR",
            on_press=self.do_login,
            style=Pack(
                background_color='#184C2F',
                color='#FFFFFF',
                margin_top=5,
                padding=15,
                font_size=16,
                font_weight='bold',
                width=200
            )
        )
        forms_box.add(login_btn)

        cadastro_link = toga.Button(
            "Não tem conta? Cadastre-se",
            on_press=lambda w: self.app.show_screen('register'),
            style=Pack(
                background_color='transparent',
                color='#184C2F',
                margin_top=15,
                font_size=12
            )
        )
        forms_box.add(cadastro_link)

        self.login_box.add(forms_box)
        return self.login_box

    def do_login(self, widget):
        email = self.email_input.value.strip()
        senha = self.senha_input.value

        if not email or not senha:
            print("Por favor, preencha email e senha.")
            return

        user = self.app.repository.authenticate_user(email, senha)
        if user:
            self.app.current_user = user
            self.email_input.value = ''
            self.senha_input.value = ''
            from .home import HomeScreen
            self.app.views["home"] = HomeScreen(self.app)
            self.app.show_screen("home")
        else:
            print("Email ou senha incorretos.")
