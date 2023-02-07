import io
import sys
import os
import pyqrcode
import png
import time

from kivy.app import App  # necessary for the App class
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.videoplayer import VideoPlayer
# from kivy.uix.camera import Camera, CoreCamera
from kivy.uix.image import Image, CoreImage

# Window.maximize()

######################################################################
# Camera needs: opencv-python
# Video needs: ffpyplayer
######################################################################


class AppObjScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(AppObjScreenManager, self).__init__(**kwargs)
        self.statedict = {
            "screen_main":  {
                "seq": 1,
                'inst': 'button_nav_main',
                'down': ['button_nav_main'],
                'normal': ["button_nav_intro"]},
            "screen_intro": {
                "seq": 0,
                'inst': 'button_nav_intro',
                'down': ['button_nav_intro'],
                'normal': ["button_nav_main"]}
            }


class NavBar(BoxLayout):
    """=== Class name: NavBar ==========================================================================================
    This Layout can be used across all screens. Class handles complications of now yet drawn instances.
    It sets appearance for instances only appearing on screen.
    ============================================================================================== by Sziller ==="""

    @ staticmethod
    def on_release_navbar(inst):
        """=== Method name: on_toggle_navbar ===========================================================================
        Method manages multiple screen selection by Toggle button set.
        All Toggle Buttons call this same function. Their Class names are stored in the <buttons> list.
        Only one button of the entire set is down at a given time. Function is extendable.
        Once a given button is 'down', it becomes inactive, all other buttons are activated and set to "normal" state.
        The reason of the logic is as follows:
        Screen manager is the unit taking care of actual screen swaps, also it stores actually shown screen name.
        However, at the itme of instantiation of the Screen Manager's ids are still not accessible.
        So we refer to ScreenManager's id's only on user action.
        :var inst: - the instance (button) activating the Method.
        ========================================================================================== by Sziller ==="""
        old_seq: int = 0
        for k, v in App.get_running_app().root.statedict.items():
            if k == App.get_running_app().root.current_screen.name:
                old_seq = v["seq"]
                break
        new_seq = App.get_running_app().root.statedict[inst.target]["seq"]

        App.get_running_app().change_screen(screen_name=inst.target, screen_direction={True: "left", False: "right"}
        [old_seq - new_seq < 0])
        for buttinst in App.get_running_app().root.current_screen.ids.navbar.ids:
            print(buttinst)
            if buttinst in App.get_running_app().root.statedict[inst.target]['normal']:
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].disabled = False
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].state = "normal"
            if buttinst in App.get_running_app().root.statedict[inst.target]['down']:
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].disabled = True
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].state = "down"


class OperationAreaBox(BoxLayout):
    pass

class OpAreaIntro(OperationAreaBox):
    def on_buttonclick_edittext(self):
        App.get_running_app().change_screen(screen_name="screen_main",
                                            screen_direction="left")

class OpAreaMain(OperationAreaBox):
    def __init__(self, **kwargs):
        super(OpAreaMain, self).__init__(**kwargs)
        self.string_tobe_converted: str = ""
        self.qr_code = None

    def on_textupdate_textinput(self, inst):
        self.string_tobe_converted = inst.text
        print(self.string_tobe_converted)

    def on_buttonclick_generate_qr(self, mode: int = 3, *args, **kwargs):
        """=== Function name: app_qr_generator_init ========================================================================
        :param mode: int -  1 - display as pixels in terminal window
                            2 - display in OS window
                            4 - write to file
        ============================================================================================== by Sziller ==="""

        self.qr_code = pyqrcode.create(content=self.string_tobe_converted, mode="binary")

        if mode in [1, 3, 5, 7]:
            print(self.qr_code.terminal())

        if mode in [2, 3, 6, 7]:
            target = "fing.png"
            self.qr_code.png(target, scale = 10)
            App.get_running_app().root.ids.screen_intro.ids.opareaintro.ids.qr_plot_layout.source = target
            App.get_running_app().root.ids.screen_intro.ids.opareaintro.ids.qr_plot_layout.reload()

        App.get_running_app().change_screen(screen_name="screen_intro",
                                            screen_direction="right")

class AppObj(App):
    """=== Class name: CayMan ========================================================================================
    Child of built in class: App
    This is the Parent application for the Sealed of Kex manager project.
    Instantiation should - contrary to what is used on the net - happen by assigning it to a variable name.
    :param window_content:
    ============================================================================================== by Sziller ==="""
    def __init__(self,
                 window_content: str,
                 app_title: str = "Sziller's App",
                 csm: float = 1.0):
        super(AppObj, self).__init__()
        self.title                      = app_title
        self.window_content             = window_content
        self.content_size_multiplier    = csm

    def change_screen(self, screen_name, screen_direction="left"):
        """=== Method name: change_screen ==============================================================================
        Use this screenchanger instead of the built-in method for more customizability and to enable further
        actions before changing the screen.
        Also, if screenchanging first needs to be validated, use this method!
        ========================================================================================== by Sziller ==="""
        smng = self.root  # 'root' refers to the only one root instance in your App. Here it is the actual ROOT
        smng.current = screen_name
        smng.transition.direction = screen_direction

    def build(self):
        return self.window_content


if __name__ == "__main__":
    from kivy.lang import Builder  # to freely pick kivy files

    display_settings = {0: {'fullscreen': False, 'run': Window.maximize},
                        1: {'fullscreen': False, 'size': (400, 800)},
                        2: {'fullscreen': False, 'size': (600, 400)},
                        3: {'fullscreen': False, 'size': (1000, 500)}}

    style_code = 1

    Window.fullscreen = display_settings[style_code]['fullscreen']
    if 'size' in display_settings[style_code].keys(): Window.size = display_settings[style_code]['size']
    if 'run' in display_settings[style_code].keys(): display_settings[style_code]['run']()



    try:
        content = Builder.load_file(str(sys.argv[1]))
    except IndexError:
        content = Builder.load_file("qr_generator.kv")

    application = AppObj(window_content=content,
                         app_title="QR code generator",
                         csm=1)
    application.run()