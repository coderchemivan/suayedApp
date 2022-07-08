
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.snackbar import Snackbar
from kivy.properties import ObjectProperty

KV='''

<DialogContent>
    confirm_check_in_list: confirm_check_in_list
    id: confirm_check_in_dialog
    cols: 1
    spacing: dp(20)
    size_hint_y: None
    size_hint_x: None
    height: self.height
    width: self.width

    AnchorLayout:

        ScrollView:

            MDList:
                id: confirm_check_in_list





'''

class DialogContent(BoxLayout):
    confirm_check_in_list=ObjectProperty()
    def check_conflicts(self, materias):
        c = 0
        for materia in materias[0]:
            self.ids.confirm_check_in_list.add_widget(
                TwoLineListItem(text=f'{materia}',
                    secondary_text=f'{materias[1][c]}',

                )
            )
            c+=1

class pendientes_list():

    dialog=None

    def build(self):

        return Builder.load_string(KV)
    #
    # def close_dialog(self, obj):
    #     self.dialog.dismiss()
    #
    # def confirm_selection(self, obj):
    #     #check number in quantity field
    #
    #     Snackbar(text='Success').open()

    def show_dialog(self,materias_act):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Check products',
                type='custom',
                content_cls=DialogContent(),
                size_hint=(1,1),
            )

        self.dialog.content_cls.check_conflicts(materias_act)
        self.dialog.open()
        #         self.dialog = Popup(
        #             title='Check products',
        #             size_hint=(.7,.6),
        #             content=DialogContent())
        # self.dialog.content.check_conflicts(materias_act)
        # self.dialog.open()















# from kivymd.uix.dialog import MDDialog
# from kivy.uix.popup import Popup
# from kivymd.uix.button import MDRaisedButton, MDFlatButton
# from kivy.lang import Builder
# from kivymd.app import MDApp
# from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
# from kivymd.uix.list import TwoLineListItem
# from kivymd.uix.snackbar import Snackbar
# from kivy.properties import ObjectProperty
#
# KV='''
#
# <DialogContent>
#
#
#     confirm_check_in_list: confirm_check_in_list
#     id: confirm_check_in_dialog
#     size_hint_y: None
#     size_hint_x: None
#     height: self.height
#     width: self.width
#
#     Button:
#         text: "hola"
#         pos_hint:{"x":0.1,"y":0}
#         size_hint:0.8,0.2
#
#     MDList:
#         id: confirm_check_in_list
#         pos_hint:{"x":0.1,"y":0.7}
#         size_hint:0.8,0.8
#
# '''
#
#
#
#
# class DialogContent(FloatLayout):
#     confirm_check_in_list=ObjectProperty()
#     def check_conflicts(self, materias):
#         c = 0
#         for materia in materias[0]:
#             self.ids.confirm_check_in_list.add_widget(
#                 TwoLineListItem(text=f'{materia}',
#                     secondary_text=f'{materias[1][c]}',
#
#                 )
#             )
#             c+=1
#
# class pendientes_list():
#
#     dialog=None
#
#     def build(self):
#
#         return Builder.load_string(KV)
#     #
#     # def close_dialog(self, obj):
#     #     self.dialog.dismiss()
#     #
#     # def confirm_selection(self, obj):
#     #     #check number in quantity field
#     #
#     #     Snackbar(text='Success').open()
#
#     def show_dialog(self,materias_act):
#         if not self.dialog:
#         #     self.dialog = MDDialog(
#         #         type='custom',
#         #         title= 'This is a very long long long text',
#         #         size_hint=(1, 1),
#         #         content_cls=DialogContent(),
#         #     )
#
#         # self.dialog.content_cls.check_conflicts(materias_act)
#         # self.dialog.open()
#                 self.dialog = Popup(
#                     title='Check products',
#                     size_hint=(.7,.6),
#                     content=DialogContent())
#         self.dialog.content.check_conflicts(materias_act)
#         self.dialog.open()