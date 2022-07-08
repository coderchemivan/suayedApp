# from kivymd.app import MDApp
# from kivy.uix.popup import Popup
# from kivy.uix.boxlayout import BoxLayout
#
# class PopContent(Popup):
#     pass



#https://stackoverflow.com/questions/65576764/kivymd-custom-list-dialog-cant-insert-changeable-list-in-mddialog
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
#
# from kivymd.app import MDApp
# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.list import OneLineListItem, MDList
#
# KV = '''
# <Content>
#     # name:"content"
#     # draw:container
#     orientation: "vertical"
#     ScrollView:
#
#         MDList:
#             id: container
#
#
# FloatLayout:
#     # mgr:cont
#     # Content:
#     #     id:cont
#
#     MDFlatButton:
#         text: "ALERT DIALOG"
#         pos_hint: {'center_x': .5, 'center_y': .5}
#         on_release: app.show_confirmation_dialog()
# '''
#
#
# class Content(BoxLayout):
#     def __init__(self, *args, **kwargs):
#         super().__init__(**kwargs)
#         container = self.ids.container
#         print("content called")
#
#         def adding(self):
#             for i in range(20):
#                 container.add_widget(OneLineListItem(text=f"Single-line item {i}"))
#             print("adding called")
#
#         adding(self)
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
#             )
#
#         self.dialog.open()
#
#
# Example().run()



# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.button import MDRaisedButton, MDFlatButton
# from kivymd.uix.list import OneLineListItem
# from kivy.lang import Builder
# from kivymd.app import MDApp
# from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.uix.boxlayout import BoxLayout
# from kivymd.uix.label import MDLabel
# from kivymd.uix.list import ThreeLineListItem
# from kivymd.uix.snackbar import Snackbar
# from kivy.properties import ObjectProperty
#
# KV='''
#
#
# <DialogContent>
#     confirm_check_in_list: confirm_check_in_list
#     id: confirm_check_in_dialog
#     orientation: "vertical"
#     spacing: dp(20)
#     size_hint_y: None
#     size_hint_x: None
#     height: self.height
#     width: self.width
#
#     AnchorLayout:
#         adaptive_height: True
#         ScrollView:
#
#             MDList:
#                 id: confirm_check_in_list
# '''
#
# product_dict={'name 1': (1, 2), 'name 2': (3,4), 'name 3':(4,2)}
#
#
#
# class DialogContent(BoxLayout):
#     confirm_check_in_list=ObjectProperty()
#     #def check_conflicts(self, conflicts):
#         #self.add_widget(MDLabel(text = "Namw"))
#         # for name, quantity in conflicts.items():
#         #     self.ids.confirm_check_in_list.add_widget(
#         #         ThreeLineListItem(text=f'{name}',
#         #             secondary_text=f'q1: {quantity[0]}',
#         #             tertiary_text=f'q2: {quantity[1]}',
#         #         )
#         #     )
#
#
# class pendientes_list():
#     def __init__(self,**kwargs):pass
#
#
#     def show_dialog(self):
#
#
#         product_dict = {'name 1': (1, 2), 'name 2': (3, 4), 'name 3': (4, 2)}
#
#
#         my_dialog = MDDialog(
#             title='Check products',
#             type='custom',
#
#
#             items = [
#                 OneLineListItem(text="Callisto"),
#                 OneLineListItem(text="Luna"),],
#
#             buttons=[
#                 MDFlatButton(
#                     text='CANCEL',
#                     theme_text_color="Custom",
#
#                 ),
#                 MDRaisedButton(
#                     text='OK',
#                     theme_text_color="Custom",
#
#
#
#                 )
#             ],
#         )
#
#         my_dialog.open()



from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
<<<<<<< HEAD
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.list import OneLineAvatarIconListItem

=======
>>>>>>> parent of 1cdf1f4 ("Work on calendar")
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.list import OneLineListItem

KV = '''
<ItemConfirm>
    on_release: root.set_icon(check)

<<<<<<< HEAD
KV = '''
<ItemConfirm>
    on_release: root.set_icon(check)

<<<<<<< HEAD
=======
=======
>>>>>>> parent of 1cdf1f4 ("Work on calendar")
    CheckboxLeftWidget:
        id: check
        group: "check"


MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_confirmation_dialog()
'''


<<<<<<< HEAD

=======
>>>>>>> parent of 1cdf1f4 ("Work on calendar")
class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class pendientes_list():
    dialog = None

    def build(self):
        return Builder.load_string(KV)

    def show_dialog(self,fechas):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Phone ringtone",
                type="confirmation",
                items=[ItemConfirm(text=str(i)) for i in range(20)
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



