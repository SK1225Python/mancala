import main
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from kivy.config import Config
Config.set('graphics', 'width', '512')
Config.set('graphics', 'height', '384')

class TextWidget(Widget):
    text = StringProperty()
    
    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = ''

    def buttonClicked(self):
        self.text = 'Good morning'

    def buttonClicked2(self):
        self.text = 'Hello'

    def buttonClicked3(self):
        self.text = 'Good evening'

class DesignApp(App):
    def __init__(self, **kwargs):
        super(DesignApp, self).__init__(**kwargs)
        self.title = 'Mancala'    # ウィンドウの名前を変更

    def build(self):
        return TextWidget()


if __name__ == '__main__':
    DesignApp().run()