from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.list import OneLineListItem


class ItemConfirm(TwoLineListItem):
    pass


class pendientes_list():
    dialog = None


    def show_dialog(self,fechas):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Phone ringtone",
                type="confirmation",
                items=[ItemConfirm(text=str(fecha)) for fecha in fechas
                ],
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",

                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",

                    ),
                ],
            )
        self.dialog.open()



