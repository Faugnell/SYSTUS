from gpiozero import Button


class ButtonController:
    def __init__(self, on_mode_toggle):
        self.mode_button = Button(5)
        self.mode_button.when_pressed = on_mode_toggle

    def cleanup(self):
        self.mode_button.close()