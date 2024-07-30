from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.app import App
import os


class SetupScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.float_layout = FloatLayout()
        self.background_image = Image(source='setupbg.png', allow_stretch=True,
                                      keep_ratio=False)
        self.float_layout.add_widget(self.background_image)

        self.box_layout = MDBoxLayout(orientation='vertical', size_hint=(0.6, 0.4),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.packet_cost_input = MDTextField(hint_text='Cost of a packet', input_filter='float')
        self.packet_size_input = MDTextField(hint_text='Number of cigarettes in the packet', input_filter='int')

        self.box_layout.add_widget(self.packet_cost_input)
        self.box_layout.add_widget(self.packet_size_input)

        self.float_layout.add_widget(self.box_layout)

        self.submit_button = MDRaisedButton(text='Submit', md_bg_color=(0.2, 0.6, 0.86, 1), size_hint=(0.6, None),
                                            pos_hint={'center_x': 0.5, 'y': 0.1})
        self.submit_button.bind(on_press=self.submit)

        self.float_layout.add_widget(self.submit_button)
        self.add_widget(self.float_layout)

    def submit(self, instance):
        if not self.packet_size_input.text or not self.packet_cost_input.text:
            # Optionally show an error message
            return

        try:
            packet_size = int(self.packet_size_input.text)
            packet_cost = float(self.packet_cost_input.text)
        except ValueError:
            # Optionally show an error message
            return

        if packet_size <= 0 or packet_cost <= 0:
            # Optionally show an error message
            return

        with open('settings.txt', 'w') as f:
            f.write(f"{packet_size}\n{packet_cost}")

        # Create a setup complete flag
        with open('setup_complete.txt', 'w') as f:
            f.write("setup_complete")

        app = App.get_running_app()
        app.root.current = 'main'
