import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from pathlib import Path
import os

from .br.com.unip.aps.greenway.Repository.greenWayRepository import GreenWayRepository
from .br.com.unip.aps.greenway.View.login import LoginScreen
from .br.com.unip.aps.greenway.View.register import RegisterScreen
from .br.com.unip.aps.greenway.View.home import HomeScreen


class GreenWay(toga.App):
    def __init__(self):
        super().__init__()
        self.repository = GreenWayRepository()
        self.current_screen = None
        self.current_user = None
        self.views = {}

    def startup(self):
        self.main_container = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_container

        self.views = {
            "login": LoginScreen(self),
            "register": RegisterScreen(self)
        }

        self.show_screen("login")
        self.main_window.show()

    def show_screen(self, name):
        if self.current_screen:
            self.main_container.remove(self.current_screen)

        if name == "home":
            self.views["home"] = HomeScreen(self)

        self.current_screen = self.views[name].box
        self.main_container.add(self.current_screen)

    def login_user(self, user_data):
        self.current_user = user_data
        self.show_screen("home")


def main():
    return GreenWay()
