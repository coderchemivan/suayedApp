from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
import mysql.connector
from info_materias import obtener_materias



class Content(BoxLayout):pass



class insertar_meta(MDApp):
    def __init_(self,**kwargs):
        super(insertar_meta,self).__init__(**kwargs)


    dialog = None

    def show_confirmation_dialog(self):
        kv_file = r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\suayedApp\dialog\dialog_meta.kv'
        Builder.unload_file(kv_file)
        Builder.load_file(kv_file)

        if not self.dialog:
            self.dialog = MDDialog(
                title="",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release= self.closeDialog
                    ),
                    MDFlatButton(
                        text="OK", on_press=self.grabText
                    ),
                ],
            )
        self.dialog.get_normal_height()
        self.dialog.open()


    def grabText(self,int):
        self.conn = mysql.connector.connect(user="root", password="123456",
                                            host="localhost",
                                            database="fca_materias",
                                            port='3306'
                                            )
        self.cur = self.conn.cursor()
        for obj in self.dialog.content_cls.children:
            archivo = ""
            subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1) ## busca la materia que se va a mostrar en la pantalla
            clave = obtener_materias(archivo).obtener_materia_name_(modo=3,subject_name_=subject_name[0])  ## buscando la clave de la materia que se va a mostrar en pantalla
            query = "UPDATE materias_usuario SET meta = '{}' WHERE clave_materia = '{}'".format(obj.text,clave[0])
            self.cur.execute(query)
            self.conn.commit()
            self.dialog.dismiss()

    def closeDialog(self,int):
        self.dialog.dismiss()



# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
#
# from kivymd.app import MDApp
# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.textfield import MDTextField
#
# KV = '''
# <Content>
#     orientation: "vertical"
#     spacing: "12dp"
#     size_hint_y: None
#     height: "120dp"
#
#     MDTextField:
#         hint_text: "City"
#
#     MDTextField:
#         hint_text: "Street"
#
#
# FloatLayout:
#
#     MDFlatButton:
#         text: "ALERT DIALOG"
#         pos_hint: {'center_x': .5, 'center_y': .5}
#         on_release: app.show_confirmation_dialog()
# '''
#
#
# class Content(BoxLayout):
#     pass
#
#
#
# class Example(MDApp):
#     dialog = None
#
#     def build(self):
#         return Builder.load_string(KV)
#
#     def show_confirmation_dialog(self):
#         if not self.dialog:
#             self.dialog = MDDialog(
#                 title="Address:",
#                 type="custom",
#                 content_cls=Content(),
#                 buttons=[
#                     MDFlatButton(
#                         text="CANCEL", text_color=self.theme_cls.primary_color, on_release= self.closeDialog
#                     ),
#                     MDFlatButton(
#                         text="OK", text_color=self.theme_cls.primary_color, on_release=self.grabText
#                     ),
#                 ],
#             )
#         self.dialog.get_normal_height()
#         self.dialog.open()
#
#
#     def grabText(self, inst):
#         for obj in self.dialog.content_cls.children:
#             if isinstance(obj, MDTextField):
#                 print(obj.text)
#         self.dialog.dismiss()
#
#     def closeDialog(self, inst):
#         self.dialog.dismiss()
#
#
# Example().run()

