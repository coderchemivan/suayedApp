from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.list import OneLineAvatarIconListItem

from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import ThreeLineAvatarListItem
from kivymd.uix.list import OneLineListItem



class ItemConfirm(ThreeLineAvatarListItem):
    divider = None



class pendientes_list():
    def __init_(self,**kwargs):
        super(pendientes_list,self).__init__(**kwargs)

    def hola(self):
        print("haz chonguitos")

    dialog = None

    #def build(self):
    #    return Builder.load_string(KV)

    def show_dialog(self,materias_act,fecha):

        if not self.dialog:
            self.dialog = MDDialog(
                title=f"Actividades para el \n {fecha}",
                type="confirmation",
                items=[ItemConfirm(text=str(materia),
                                   secondary_text = materias_act[1][i],
                                   tertiary_text = materias_act[0][i],
                                   on_release=lambda x=3: self.hola()
                                   ) for i,materia in enumerate(materias_act[2])
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



