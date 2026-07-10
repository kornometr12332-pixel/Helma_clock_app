from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Rectangle
import math
import datetime

# حروف دور ساعت به‌جای اعداد ۱ تا ۱۲
# ۱=H ۲=E ۳=L ۴=M ۵=A ۶=S ۷=H ۸=A ۹=H ۱۰=R ۱۱=A ۱۲=M
CLOCK_LETTERS = ["H", "E", "L", "M", "A", "S", "H", "A", "H", "R", "A", "M"]

GOLD = (0.85, 0.65, 0.13, 1)
PINK = (1, 0.75, 0.8, 1)
WHITE = (1, 1, 1, 1)
DARK = (0.2, 0.1, 0.05, 1)


class ClockFace(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.redraw, pos=self.redraw)
        Clock.schedule_interval(self.update_clock, 1)

    def redraw(self, *args):
        self.update_clock()

    def update_clock(self, *args):
        self.canvas.clear()
        cx = self.center_x
        cy = self.center_y
        radius = min(self.width, self.height) / 2 - 20

        with self.canvas:
            # زمینه صورتی صفحه ساعت
            Color(*PINK)
            Ellipse(pos=(cx - radius, cy - radius), size=(radius * 2, radius * 2))

            # رینگ طلایی دور صفحه
            Color(*GOLD)
            Line(circle=(cx, cy, radius), width=4)
            Line(circle=(cx, cy, radius - 10), width=2)

            # خط‌های ساعت (۱۲ خط بزرگ)
            for i in range(12):
                angle = math.radians(i * 30 - 90)
                x1 = cx + (radius - 15) * math.cos(angle)
                y1 = cy + (radius - 15) * math.sin(angle)
                x2 = cx + (radius - 5) * math.cos(angle)
                y2 = cy + (radius - 5) * math.sin(angle)
                Color(*GOLD)
                Line(points=[x1, y1, x2, y2], width=2)

            # حروف بجای اعداد
            for i, letter in enumerate(CLOCK_LETTERS):
                angle = math.radians(i * 30 - 90)
                lx = cx + (radius - 35) * math.cos(angle)
                ly = cy + (radius - 35) * math.sin(angle)
                label = CoreLabel(text=letter, font_size=28, bold=True, color=(0.6, 0.4, 0.1, 1))
                label.refresh()
                texture = label.texture
                Color(1, 1, 1, 1)
                Rectangle(texture=texture, pos=(lx - texture.size[0] / 2, ly - texture.size[1] / 2), size=texture.size)

            # نوشته Helma وسط صفحه
            label2 = CoreLabel(text="Helma", font_size=24, bold=True, color=(0.7, 0.45, 0.15, 1))
            label2.refresh()
            texture2 = label2.texture
            Color(1, 1, 1, 1)
            Rectangle(texture=texture2, pos=(cx - texture2.size[0] / 2, cy + radius * 0.3), size=texture2.size)

            # زمان فعلی
            now = datetime.datetime.now()
            hour = now.hour % 12
            minute = now.minute
            second = now.second

            # عقربه ساعت
            angle_h = math.radians((hour + minute / 60) * 30 - 90)
            Color(*GOLD)
            Line(points=[cx, cy, cx + radius * 0.5 * math.cos(angle_h), cy + radius * 0.5 * math.sin(angle_h)], width=5)

            # عقربه دقیقه
            angle_m = math.radians(minute * 6 - 90)
            Color(*GOLD)
            Line(points=[cx, cy, cx + radius * 0.75 * math.cos(angle_m), cy + radius * 0.75 * math.sin(angle_m)], width=3)

            # عقربه ثانیه
            angle_s = math.radians(second * 6 - 90)
            Color(0.8, 0.2, 0.3, 1)
            Line(points=[cx, cy, cx + radius * 0.85 * math.cos(angle_s), cy + radius * 0.85 * math.sin(angle_s)], width=1.5)

            # نقطه مرکز
            Color(*DARK)
            Ellipse(pos=(cx - 6, cy - 6), size=(12, 12))


class HelmaClockApp(App):
    def build(self):
        return ClockFace()


if __name__ == "__main__":
    HelmaClockApp().run()
