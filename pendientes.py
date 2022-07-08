from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.list import OneLineAvatarIconListItem

from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import OneLineListItem


KV = '''
<ItemConfirm>
    on_release: root.set_icon(check)


    CheckboxLeftWidget:
        id: check
        group: "check"


MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_confirmation_dialog()
'''



class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
        print("este es una prueba")


class pendientes_list():
    dialog = None

    def build(self):
        return Builder.load_string(KV)

    def show_dialog(self,materias_act):

        if not self.dialog:
            self.dialog = MDDialog(
                title="Phone ringtone",
                type="confirmation",
                items=[ItemConfirm(text=str(materia)) for materia in materias_act[0]
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



