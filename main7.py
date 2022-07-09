# https://github.com/vipinjangra/KivyMD

## VERSION 5

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.list import IconRightWidget

from kivy.properties import ObjectProperty

from picker_modificado import MDDatePicker 
#from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem
from kivymd.uix.list import ILeftBodyTouch, TwoLineRightIconListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons

from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import random
from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
from kivy.factory import Factory
from kivy.uix.image import Image
from kivymd.uix.list import IRightBodyTouch, ILeftBody
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFlatButton
from kivy.uix.popup import Popup
from kivy.metrics import dp

# Base de datos
import csv
from info_materias import obtener_materias
from info_materias import vaciar_feedback
from info_materias import estatus_feedback

# Web scrapping
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from plataformaSuayed_CSV_DB import Feedback

import datetime
from datetime import date



class LoginPage(Screen):
    username = ObjectProperty()
    password = ObjectProperty()
    login_cb = ObjectProperty()


    def on_pre_enter(self, *args):
        Clock.schedule_once(self.remember_)

    def remember_(self,*args):
        archivo = r'assests\BD\usuarioData.csv'
        with open(archivo, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            user = myList[1][0]
            pass_ = myList[1][1]
            remember = myList[1][2]
            if remember == 'True':
                self.login_cb.active = True
                self.username.text = user
                self.password.text = pass_
            else:
                self.login_cb.active = False
                self.username.text = ""
                self.password.text = ""

    def remember_me(self):
        archivo = r'assests\BD\usuarioData.csv'
        obtener_materias(archivo).remember_status()

    def login(self):
        archivo = r'assests\BD\usuarioData.csv'
        with open(archivo, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            user = myList[1][0]
            pass_ = myList[1][1]
            self.ids.User.text = user
            self.ids.Pass.text = pass_


            if self.username.text == user and self.password.text == pass_:
                sm.current = "firstwindow"
                self.username.text = ""
                self.password.text = ""
            else:
                print("Not here!")

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        # self.root.ids.date_label.text = str(value)
        self.ids.enviado_el.text = str(value)

    #
    # Click Cancel
    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        archivo = r'assests\BD\materias.csv'
        current_month = date.today().month
        obtener_materias(archivo).dias_con_pendientes(modo=3, month=current_month,año='2022')
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

        

class FirstWindow(Screen):pass



activity_name = ""
class SecondWindow(Screen):
    def __init_(self,**kwargs):
        super(SecondWindow,self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.update_screen()

    def definir_semestre(self):
        archivo_aux = "assests\BD\semestres_materias.csv"
        archivo = "assests\BD\materias.csv"
        semestre = self.text
        obtener_materias(archivo).define_semester(semestre,archivo_aux)


    def update_screen(self):
        # Limpiando las materias de la pantalla
        self.ids.list_one.clear_widgets()

        ## Rellenando las materias del menú
        materias = obtener_materias("assests\BD\materias.csv").extracción_materias()
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": materia,
                "height": dp(56),
                "on_release": lambda x=materia: self.on_select_item_menu(x),
            } for materia in materias
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        archivo = 'assests\BD\materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name()
        actividades = obtener_materias(archivo).total_actividades(subject_name)

        self.ids.nombre_materia.title = subject_name

        lista = obtener_materias(archivo).list_type()

        if lista == 'TwoLineRightIconListItem':
            for k, v in actividades.items():
                self.ids.list_one.add_widget(
                    ListItemWithCheckbox(text=k, secondary_text=v)
                )
        elif lista == 'TwoLineListItem':
            for k, v in actividades.items():
                self.ids.list_one.add_widget(
                    ListItemWithoutCheckbox(text=k, secondary_text=v)
                )

        subject_name = obtener_materias(archivo).obtener_materia_name()  # consulta
        estados = ['por entregar', 'entregadas con atraso', 'atrasadas', 'entregadas a tiempo']
        num_act_estado = dict()
        for estado in estados:
            obtener_materias(archivo).estado_actividad(estado, 'TwoLineRightIconListItem')
            num_actividades = len(obtener_materias(archivo).total_actividades(subject_name))
            num_act_estado[estado] = num_actividades

        self.ids.por_entregar_text.text = str(num_act_estado['por entregar'])
        self.ids.Entregas_con_retraso_text.text = str(num_act_estado['entregadas con atraso'])
        self.ids.Atrasada_text.text = str(num_act_estado['atrasadas'])
        self.ids.Entregas_a_tiempo_text.text = str(num_act_estado['entregadas a tiempo'])
        obtener_materias(archivo).estado_actividad('por entregar', 'TwoLineRightIconListItem')



    def press_actividad(self):  # Abre la ventana donde se muestran los detalles de la actividad
        activity_name = obtener_materias('assests\BD\materias.csv').define_activity(self.text)
        sm.current = 'thirdwindow'


    def activity_check(self,*args):  # Se indica que se entregó una actividad
        archivo = 'assests\BD\materias.csv'
        activity_name = self.text
        materia = obtener_materias(archivo).obtener_materia_name()
        obtener_materias(archivo).actualizar_DB(materia, activity_name)
        sm.current ="firstwindow"
        sm.current = "secondwindow"


    def abrir_menu(self, button):  # Abre el menú con las materias
        self.menu.caller = button
        self.menu.open()

    def on_select_item_menu(self, text_item):  # Carga la ventana con la materia seleccionada
        self.menu.dismiss()
        archivo = 'assests\BD\materias.csv'
        obtener_materias(archivo).define_subject(text_item)
        subject_name = obtener_materias(archivo).obtener_materia_name()  # consulta
        estados = ['por entregar', 'entregadas con atraso', 'atrasadas', 'entregadas a tiempo']
        num_act_estado = dict()
        for estado in estados:
            obtener_materias(archivo).estado_actividad(estado, 'TwoLineRightIconListItem')
            num_actividades = len(obtener_materias(archivo).total_actividades(subject_name))
            num_act_estado[estado] = num_actividades
        obtener_materias(archivo).estado_actividad('por entregar', 'TwoLineRightIconListItem')
        self.update_screen()


    def consultar_calificaciones(self):  # Extrae el feedback de internet
        archivo = 'assests\BD\materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name()
        subject_clave = obtener_materias(archivo).obtener_materia_clave(subject_name)
        actividades = obtener_materias(archivo).total_actividades(subject_name)
        opts = Options()
        opts.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

        driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver.exe', options=opts)
        activity_feedback = Feedback([subject_clave], actividades, driver).extraccion_feedback()
        vaciar_feedback(archivo, subject_name, activity_feedback)
        register_feedback = vaciar_feedback('assests\BD\materias.csv', subject_name,
                                            activity_feedback).vaciar_resultados()

    def entregas_a_tiempo(self, *args):
        archivo = 'assests\BD\materias.csv'
        obtener_materias(archivo).estado_actividad('entregadas a tiempo', 'TwoLineListItem')

        subject_name = obtener_materias(archivo).obtener_materia_name()  # consulta
        actividades = obtener_materias(archivo).total_actividades(subject_name)  # consulta
        self.update_screen()


    def entregas_con_atraso(self, *args):
        archivo = 'assests\BD\materias.csv'
        obtener_materias(archivo).estado_actividad('entregadas con atraso', 'TwoLineListItem')

        subject_name = obtener_materias(archivo).obtener_materia_name()  # consulta
        actividades = obtener_materias(archivo).total_actividades(subject_name)  # consulta
        self.update_screen()


    def atrasadas(self, *args):
        archivo = 'assests\BD\materias.csv'
        obtener_materias(archivo).estado_actividad('atrasadas', 'TwoLineRightIconListItem')
        subject_name = obtener_materias(archivo).obtener_materia_name()  # consulta
        actividades = obtener_materias(archivo).total_actividades(subject_name)  # consulta
        self.update_screen()


    def por_entregar(self, *args):
        archivo = 'assests\BD\materias.csv'
        obtener_materias(archivo).estado_actividad('por entregar', 'TwoLineRightIconListItem')
        subject_name = obtener_materias(archivo).obtener_materia_name()  # consulta
        actividades = obtener_materias(archivo).total_actividades(subject_name)  # consulta
        self.update_screen()


class ThirdWindow(Screen):
    def on_enter(self, *args):
        activity_name = obtener_materias('assests\BD\materias.csv').obtener_activity_name()
        subject_name = obtener_materias('assests\BD\materias.csv').obtener_materia_name()
        activity_status = estatus_feedback('assests\BD\materias.csv', subject_name, activity_name).resultados()

        self.ids.nombre_actividad.title = activity_name
        self.ids.enviado_el.text = f' Enviada el : {activity_status[0]}'
        self.ids.estatus_entrega.text = f' Status : {activity_status[1]}'
        self.ids.calificacion.text = f' Calificación :  {activity_status[2]}'
        self.ids.calificado_el.text = f' Calificada el : {activity_status[3]}'
        self.ids.scroll_lable.ids.comentarios.text = f' {activity_status[4]}'
        self.ids.ponderacion.text = f' Valor : {"{0:.0f}%".format(float(activity_status[5]) * 100)}'


    #Click OK
    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        # self.root.ids.date_label.text = str(value)
        self.ids.enviado_el.text = str(value)

    #
    # Click Cancel
    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        # date_dialog = MDDatePicker(year=2000, month=2, day=14)
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


class FourthWindow(Screen): pass


class WindowManager(ScreenManager):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    nav_drawer = ObjectProperty()
    sm2 = ScreenManager()
    screen_two = SecondWindow

class ListItemWithCheckbox(TwoLineRightIconListItem):
    '''Custom list item.'''
    icon = StringProperty("")
    screen_two = SecondWindow


class ListItemWithoutCheckbox(TwoLineListItem):
    '''Custom list item.'''
    screen_two = SecondWindow


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''
    screen_login = LoginPage

class ScrolllabelLabel(ScrollView):
    text = StringProperty('')
    comentarios = ObjectProperty()



class MyPopup_tasks(Popup):
    pass


class PopupWindow_tasks(BoxLayout):
    def open_popup(self):
        popup = MyPopup_tasks()
        popup.open()
    


sm = ScreenManager()
class TestNavigationDrawer(MDApp):
    def build(self):
        Window.size = (350, 600)
        self.title = "Gestor de tareas"
        sm2 = ScreenManager()
        Builder.load_file('main7.kv')
        sm.add_widget(LoginPage(name='login_page'))
        sm.add_widget(FirstWindow(name='firstwindow'))
        sm.add_widget(SecondWindow(name='secondwindow'))
        sm.add_widget(ThirdWindow(name='thirdwindow'))
        sm.add_widget(FourthWindow(name='fourthwindow'))
        return sm

    def go_back(self,pantalla):
        if pantalla == 1:
            sm.transition.direction = 'right'
            sm.current = "firstwindow"
        else:
            sm.transition.direction = 'right'
            sm.current = "secondwindow"

TestNavigationDrawer().run()
