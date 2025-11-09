import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from pathlib import Path
import os


class RegisterScreen:
    def __init__(self, app):
        self.app = app
        current_dir = Path(os.path.dirname(__file__))
        self.box = self.create_register_screen(current_dir)

    def create_register_screen(self, current_dir):
        self.register_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                background_color="#F0F5E6",
                align_items=CENTER,
                flex=1
            )
        )

        back_btn_box = toga.Box(style=Pack(direction=ROW, width=300))
        back_btn = toga.Button(
            "← Voltar para Login",
            on_press=lambda widget: self.app.show_screen("login"),
            style=Pack(
                background_color="transparent",
                color="#184C2F",
                font_size=12
            )
        )
        back_btn_box.add(back_btn)
        self.register_box.add(back_btn_box)

        self.register_box.add(
            toga.Label(
                "Green Way",
                style=Pack(
                    font_size=28,
                    font_weight="bold",
                    margin_bottom=10,
                    margin_top=10,
                    color="#184C2F",
                    text_align="center"
                )
            )
        )

        logo_container = toga.Box(
            style=Pack(direction=COLUMN, align_items=CENTER, margin_bottom=20)
        )
        logo_path = current_dir / ".." / ".." / ".." / ".." / ".." / ".." / "resources" / "images" / "logo.png"
        if logo_path.exists():
            logo = toga.Image(str(logo_path))
            img_view = toga.ImageView(logo, style=Pack(width=70, height=70, margin_bottom=10))
            logo_container.add(img_view)
        self.register_box.add(logo_container)

        forms_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                margin=10,
                background_color="#F0F5E6",
                align_items=CENTER,
            )
        )
        self.register_box.add(forms_box)

        self.nome_input = toga.TextInput(
            placeholder="Nome Completo",
            style=Pack(background_color="#FFFFFB", color="#757575", margin=5, width=250, height=40)
        )
        self.apelido_input = toga.TextInput(
            placeholder="Apelido",
            style=Pack(background_color="#FFFFFB", color="#757575", margin=5, width=250, height=40)
        )
        self.email_input = toga.TextInput(
            placeholder="E-mail",
            style=Pack(background_color="#FFFFFB", color="#757575", margin=5, width=250, height=40)
        )
        self.senha_input = toga.PasswordInput(
            placeholder="Senha",
            style=Pack(background_color="#FFFFFB", color="#757575", margin=5, width=250, height=40)
        )
        self.confirmar_senha_input = toga.PasswordInput(
            placeholder="Confirmar Senha",
            style=Pack(background_color="#FFFFFB", color="#757575", margin=5, width=250, height=40)
        )

        self.sexo_selection = toga.Selection(
            items=["Selecione...", "Masculino", "Feminino"],
            style=Pack(margin=10, width=150)
        )
        sexo_box = toga.Box(
            children=[
                toga.Label(
                    "Sexo:",
                    style=Pack(color="#133C1F", margin_right=10, font_weight="bold")
                ),
                self.sexo_selection
            ],
            style=Pack(direction=ROW, align_items=CENTER, width=250)
        )

        self.terms_switch = toga.Switch("", style=Pack(width=40, height=20))
        terms_box = toga.Box(
            children=[
                self.terms_switch,
                toga.Label(
                    "Aceito os Termos de Uso e Política\n de Privacidade dos Dados",
                    style=Pack(flex=1, text_align="left", font_size=7, color="#133C1F")
                )
            ],
            style=Pack(direction=ROW, width=250)
        )

        forms_box.add(self.nome_input)
        forms_box.add(self.apelido_input)
        forms_box.add(self.email_input)
        forms_box.add(self.senha_input)
        forms_box.add(self.confirmar_senha_input)
        forms_box.add(sexo_box)
        forms_box.add(terms_box)

        content_spacer = toga.Box(style=Pack(flex=1))
        self.register_box.add(content_spacer)

        btn_cadastro_box = toga.Box(
            children=[
                toga.Button(
                    "CADASTRAR",
                    on_press=self.processar_cadastro,
                    style=Pack(
                        background_color="#184C2F",
                        color="#EDF4E1",
                        font_size=16,
                        font_weight="bold",
                        padding=15,
                        width=200
                    )
                )
            ],
            style=Pack(direction=ROW, align_items="center", padding=5, background_color="#EDF4E1")
        )
        self.register_box.add(btn_cadastro_box)

        return self.register_box

    def processar_cadastro(self, widget):
        nome = self.nome_input.value.strip()
        apelido = self.apelido_input.value.strip()
        email = self.email_input.value.strip()
        senha = self.senha_input.value
        confirmar_senha = self.confirmar_senha_input.value
        sexo = self.sexo_selection.value
        aceitou_termos = self.terms_switch.value

        if not nome or not email or not senha or not apelido:
            print("Por favor, preencha todos os campos obrigatórios")
            return
        elif senha != confirmar_senha:
            print("As senhas não coincidem")
            return
        elif not aceitou_termos:
            print("Você deve aceitar os termos de uso")
            return
        elif not sexo or sexo == "Selecione...":
            print("Por favor, selecione o sexo")
            return

        dados_usuario = {
            "nome": nome,
            "nickName": apelido,
            "email": email,
            "senha": senha,
            "kg": 0,
            "score": 0,
            "missao": 0
        }

        print("Tentando cadastrar usuário:", dados_usuario)

        sucesso = self.app.repository.create_user(dados_usuario)

        if sucesso:
            print("Usuário cadastrado com sucesso!")
            self.limpar_campos_cadastro()
            self.app.show_screen("login") 
        else:
            print("Erro: Este email já está cadastrado!")

    def limpar_campos_cadastro(self):
        self.nome_input.value = ""
        self.apelido_input.value = ""
        self.email_input.value = ""
        self.senha_input.value = ""
        self.confirmar_senha_input.value = ""
        self.sexo_selection.value = "Selecione..."
        self.terms_switch.value = False
