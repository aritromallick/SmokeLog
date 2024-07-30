from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from setup_screen import SetupScreen
from main_screen import MainScreen
import os


class MainAppLauncher(MDApp):
    def build(self):
        sm = ScreenManager()

        # Check if setup is complete
        if os.path.exists('setup_complete.txt'):
            sm.add_widget(MainScreen(name='main'))
            sm.current = 'main'
        else:
            sm.add_widget(SetupScreen(name='setup'))
            sm.add_widget(MainScreen(name='main'))

        return sm


if __name__ == '__main__':
    MainAppLauncher().run()
