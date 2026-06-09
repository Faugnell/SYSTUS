from gpiozero import Button

class ButtonController:
    def __init__(self, on_mode_toggle, on_action):
        self.mode_button = Button(
            5,
            bounce_time=0.3
        )
        self.action_button = Button(
            6,
            bounce_time=0.3
        )

        self.mode_button.when_pressed = on_mode_toggle
        self.action_button.when_pressed = on_action

    def cleanup(self):
        self.mode_button.close()
        self.action_button.close()