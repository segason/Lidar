import pptk
import pandas as pd
import numpy as np
import os
from time import time
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.factory import Factory
from kivy.graphics import Color, Point
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.config import Config

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '750')

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 1000)

from pprint import pprint

pointSize = 0.001
points = None
viewer = None

# Change Functions
def BackColorChange(self, value):
    viewer.set(bg_color=value)

def GroundColorChange(self, value):
    viewer.set(floor_color=value)

def PointColorChange(self, value):
    selected = viewer.get('selected')
    for x in selected:
        points.loc[x, 'r'] = value[0] * 255
        points.loc[x, 'g'] = value[1] * 255
        points.loc[x, 'b'] = value[2] * 255
    viewer.attributes(points[['r', 'g', 'b']] / 255., points['reflectance'])

def OnPointSizeChange(self, *args):
    pointSize = self.value
    viewer.set(point_size=pointSize)

def OnFloorChange(self, *args):
    floor = self.value
    viewer.set(floor_level=floor)

def gridActive(checkbox, value):
    viewer.set(show_grid =  value)

def infoActive(checkbox, value):
    viewer.set(show_info =  value)

def axisActive(checkbox, value):
    viewer.set(show_axis =  value)

# KV Components
class Separator(BoxLayout):
    pass

class Misc(BoxLayout):
    def __init__(self, **kwargs):
        super(Misc, self).__init__(**kwargs)

        box = CheckBox(active=True)
        label = Label(text='Show Grid')
        self.add_widget(label)
        self.add_widget(box)
        box.bind(active=gridActive)

        box = CheckBox(active=True)
        label = Label(text='Show Info')
        self.add_widget(label)
        self.add_widget(box)
        box.bind(active=infoActive)

        box = CheckBox(active=True)
        label = Label(text='Show Axis')
        self.add_widget(label)
        self.add_widget(box)
        box.bind(active=axisActive)

class PointColor(BoxLayout):
    def __init__(self, **kwargs):
        super(PointColor, self).__init__(**kwargs)
        point_color = ColorPicker()
        self.add_widget(point_color)
        point_color.bind(color=PointColorChange)

class BackColor(BoxLayout):
    def __init__(self, **kwargs):
        super(BackColor, self).__init__(**kwargs)
        back_color = ColorPicker()
        self.add_widget(back_color)
        back_color.bind(color=BackColorChange)

class GroundColor(BoxLayout):
    def __init__(self, **kwargs):
        super(GroundColor, self).__init__(**kwargs)
        ground_color = ColorPicker()
        self.add_widget(ground_color)
        ground_color.bind(color=GroundColorChange)

class Analyzer(BoxLayout):
    def __init__(self, **kwargs):
        super(Analyzer, self).__init__(**kwargs)
        self.ids.s1.bind(value=OnPointSizeChange)
        self.ids.z1.bind(value=OnFloorChange)
        self.file = None
        self.viewer = None
        self.file_name = 0

    def save(self):
        if viewer is not None:
            viewer.capture(str(self.file_name) + ".png")
            file_name = self.file_name + 1

            popup = Popup(title='Saved', content=Label(text='Your viewer image has been saved in the same directory. Press ESC to dismiss.'))
            popup.open()

    def load(self, path, filename):
        global points, viewer

        if not filename:
            print("No file chosen")
        else:
            if self.viewer is not None:
                self.file = None
                self.viewer.clear()
                self.viewer.close()

            self.file = open(os.path.join(path, filename[0]), 'r')
            points = self.read_points()
            viewer = pptk.viewer(points[['x', 'y', 'z']])
            viewer.attributes(points[['r', 'g', 'b']] / 255., points['reflectance'])
            viewer.set(point_size=pointSize)
            viewer.set(bg_color=[1, 1, 1, 1])
            viewer.set(r=1)
            viewer.set(phi=45)
            viewer.set(theta=-200)

            self.file.close()
            self.dismiss_popup()

    def read_points(self):
        # reads Semantic3D .txt file f into a pandas dataframe
        col_names = ['x', 'y', 'z', 'deviation', 'amplitude', 'reflectance', 'r', 'g', 'b']
        col_dtype = {'x': np.float32, 'y': np.float32, 'z': np.float32, 'deviation': np.int32, 'amplitude': np.float32, 'reflectance': np.float32, 'r': np.uint8, 'g': np.uint8, 'b': np.uint8}

        return pd.read_csv(self.file, names=col_names, dtype=col_dtype, header=0, engine='python')

    def dismiss_popup(self):
        self.ids.popup.dismiss()

class PointCloudAnalyzerApp(App):
    def build(self):
        analyzer = Analyzer()
        return analyzer

Factory.register('Root', cls=Analyzer)

if __name__ == '__main__':
    PointCloudAnalyzerApp().run()
