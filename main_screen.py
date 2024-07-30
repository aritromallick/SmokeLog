from kivy.app import App
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
import os


class MainScreen(MDScreen):
    cost_per_packet = NumericProperty(0)
    num_cigarettes_per_packet = NumericProperty(0)
    cost_per_cigarette = NumericProperty(0)
    total_cost = NumericProperty(0)
    cigarettes_smoked = NumericProperty(0)
    last_smoked_time = StringProperty('N/A')
    last_smoked_datetime = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_settings()

        # Top bar
        self.top_bar = MDTopAppBar(
            title="SmokeLog",
            pos_hint={"top": 1},
            elevation=0,  # Removed shadow
        )
        self.add_widget(self.top_bar)

        # Timer box
        self.timer_card = MDCard(
            orientation='vertical',
            size_hint=(0.9, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.85},
            padding=10,
            radius=[10, 10, 10, 10],
            md_bg_color='#F0F0F0'
        )

        self.timer_label = MDLabel(
            text='0:00:00',
            font_style='Subtitle1',
            halign='center',
            valign='middle',
            theme_text_color='Primary'
        )

        self.timer_card.add_widget(self.timer_label)
        self.add_widget(self.timer_card)

        # Container for the cost and smoked cards
        self.stats_container = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.7},
            spacing=20
        )

        # Total Cost card
        self.total_cost_card = MDCard(
            orientation='vertical',
            size_hint=(0.45, 1),
            padding=10,
            radius=[10, 10, 10, 10],
            md_bg_color='#F0F0F0'
        )

        self.price_label = MDLabel(
            text=f'Total Cost: {self.total_cost:.2f}',
            font_style='Subtitle1',
            halign='center',
            valign='middle',
            theme_text_color='Primary'
        )

        self.total_cost_card.add_widget(self.price_label)

        # Cigarettes Smoked card
        self.smoked_card = MDCard(
            orientation='vertical',
            size_hint=(0.45, 1),
            padding=10,
            radius=[10, 10, 10, 10],
            md_bg_color='#F0F0F0'
        )

        self.smoked_label = MDLabel(
            text=f'Cigarettes Smoked: {self.cigarettes_smoked}',
            font_style='Subtitle1',
            halign='center',
            valign='middle',
            theme_text_color='Primary'
        )

        self.smoked_card.add_widget(self.smoked_label)

        # Add the cards to the container
        self.stats_container.add_widget(self.total_cost_card)
        self.stats_container.add_widget(self.smoked_card)

        # Add the container to the screen
        self.add_widget(self.stats_container)

        # Smoke Cigarette button
        self.smoke_button = MDRaisedButton(
            text='Smoke Cigarette',
            md_bg_color='#3BA1F2',
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            elevation=2,
            on_release=self.smoke_cigarette,
        )
        self.add_widget(self.smoke_button)

        # Reset Settings button
        self.reset_button = MDRaisedButton(
            text='Reset Settings',
            md_bg_color='#FF0000',
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            elevation=2,
            on_release=self.reset_settings,
        )
        self.add_widget(self.reset_button)

        # Start the live timer update
        Clock.schedule_interval(self.update_timer, 1)

    def on_pre_enter(self, *args):
        self.load_settings()

    def load_settings(self):
        try:
            with open('settings.txt', 'r') as f:
                lines = f.readlines()
                self.num_cigarettes_per_packet = int(lines[0].strip())
                self.cost_per_packet = float(lines[1].strip())
                self.cost_per_cigarette = self.cost_per_packet / self.num_cigarettes_per_packet
                print(f"Cost per cigarette: {self.cost_per_cigarette}")

            # Save the fresh settings to the file
            self.save_settings()
        except (FileNotFoundError, IndexError, ValueError) as e:
            print(f"Error loading settings: {e}")
            self.num_cigarettes_per_packet = 0
            self.cost_per_packet = 0
            self.cost_per_cigarette = 0

    def save_settings(self):
        with open('settings.txt', 'w') as f:
            f.write(f"{self.num_cigarettes_per_packet}\n{self.cost_per_packet}\n{self.cost_per_cigarette}")

    def smoke_cigarette(self, instance):
        # Avoid division by zero or invalid updates
        if self.num_cigarettes_per_packet == 0 or self.cost_per_cigarette == 0:
            return

        self.cigarettes_smoked += 1
        self.total_cost = self.cost_per_cigarette * self.cigarettes_smoked

        now = datetime.now()
        if self.last_smoked_datetime is not None:
            interval = now - self.last_smoked_datetime
            self.last_smoked_time = str(interval).split('.')[0]
        else:
            self.last_smoked_time = 'N/A'

        self.last_smoked_datetime = now

        self.price_label.text = f'Total Cost: {self.total_cost:.2f}'
        self.smoked_label.text = f'Cigarettes Smoked: {self.cigarettes_smoked}'
        # self.timer_label.text = f'Last Cigarette: {self.last_smoked_time}'

    def update_timer(self, dt):
        if self.last_smoked_datetime is not None:
            interval = datetime.now() - self.last_smoked_datetime
            self.timer_label.text = f'{str(interval).split(".")[0]}'
        else:
            self.timer_label.text = '0:00:00'

    def reset_settings(self, instance):
        # Delete settings and flag files
        if os.path.exists('settings.txt'):
            os.remove('settings.txt')
        if os.path.exists('setup_complete.txt'):
            os.remove('setup_complete.txt')

        # Reset properties
        self.num_cigarettes_per_packet = 0
        self.cost_per_packet = 0
        self.cost_per_cigarette = 0
        self.total_cost = 0
        self.cigarettes_smoked = 0
        self.last_smoked_time = 'N/A'
        self.last_smoked_datetime = None

        # Update UI
        self.price_label.text = 'Total Cost: 0.00'
        self.smoked_label.text = 'Cigarettes Smoked: 0'
        self.timer_label.text = '0:00:00'

        # Navigate to setup screen
        app = App.get_running_app()
        app.root.current = 'setup'
