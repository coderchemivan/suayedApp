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
from pyparsing import FollowedBy

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
import subprocess
from info_materias import obtener_materias
from info_materias import vaciar_feedback
from info_materias import estatus_feedback
from info_materias import goal_file

# Web scrapping
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from plataformaSuayed import Feedback

import datetime
from datetime import date
import mysql.connector


class WindowManager(ScreenManager):
    pass


class LoginPage(Screen):
    username = ObjectProperty()
    password = ObjectProperty()
    login_cb = ObjectProperty()


    def on_pre_enter(self, *args):
        Clock.schedule_once(self.remember_)

    def remember_(self,*args):
        archivo = r'assests\BD\usuarioData.csv'
        remember = obtener_materias(archivo).remember_status(modo=2)  ##listo
        user = '421157110'
        pass_ = '16091997'
        if remember == 1:
            self.login_cb.active = True
            self.username.text = user
            self.password.text = pass_
        else:
            self.login_cb.active = False
            self.username.text = ""
            self.password.text = ""

    def remember_me(self):
        archivo = r'assests\BD\usuarioData.csv'
        obtener_materias(archivo).remember_status(modo = 1) ##listo

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


class FirstWindow(Screen):
    def __init_(self,**kwargs):
        super(FirstWindow,self).__init__(**kwargs)   
    
    def on_enter(self):
        Clock.schedule_once(self.lista_semestres)   

    def lista_semestres(self, dt): # Llena el MDlist del NavigationDrawer
        archivo_aux = r'assests\BD\semestres_materias.csv'
        semestres = obtener_materias(archivo_aux).lista_semester()   #listo
        #Limpiando los semestres anteriores
        self.ids.nav_drawer_content.ids.md_list.clear_widgets()

        for semestre in semestres:
            try:
                self.ids.nav_drawer_content.ids.md_list.add_widget(
                ItemList(text = semestre))
            except:
                pass   

    def definir_semestre(instance):
        archivo_aux = "assests\BD\semestres_materias.csv"
        archivo = "assests\BD\materias.csv"
        semestre = instance.text
        obtener_materias(archivo).define_semester(semestre,archivo_aux) ##listo


    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        # self.root.ids.date_label.text = str(value)
        self.ids.enviado_el.text = str(value)

    # Click Cancel
    def on_cancel(self, instance, value):
        pass


    def show_date_picker(self):
        archivo = r'assests\BD\materias.csv'
        #current_month = date.today().month
        #obtener_materias(archivo).dias_con_pendientes(modo=3, month=current_month,año='2022')
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


activity_name = ""
class SecondWindow(Screen):
    def __init_(self,**kwargs):
        super(SecondWindow,self).__init__(**kwargs)


    def on_pre_enter(self, *args):
        self.conn = mysql.connector.connect(user="root", password="123456",
                                            host="localhost",
                                            database="fca_materias",
                                            port='3306'
                                            )
        self.cur = self.conn.cursor()
        self.por_entregar()
        self.update_screen()

    def update_screen(self):
        # Limpiando las materias de la pantalla
        self.ids.list_one.clear_widgets()

        ## Rellenando las materias del menú
        materias = obtener_materias("assests\BD\materias.csv").extracción_materias()  ##listo  **
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

        subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1) ## listo
        status = obtener_materias(archivo).status(modo=3) ## listo
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3,subject_name_=subject_name[0])  ## listo
        actividades = obtener_materias(archivo).status(modo=2,materia = clave[0],status_=status) ## listo **

        #actividades = obtener_materias(archivo).total_actividades(subject_name)

        self.ids.nombre_materia.title = subject_name[0]

        lista = obtener_materias(archivo).list_type()  ## listo


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

        estados = ['Por entregar', 'Entregada con atraso', 'Atrasada', 'Entregada a tiempo']
        num_act_estado = dict()
        for estado in estados:
            num_actividades = len(obtener_materias(archivo).status(modo=2, materia=clave[0], status_=estado)) ##listo
            num_act_estado[estado] = num_actividades


        self.ids.por_entregar_text.text = str(num_act_estado['Por entregar'])
        self.ids.Entregas_con_retraso_text.text = str(num_act_estado['Entregada con atraso'])
        self.ids.Atrasada_text.text = str(num_act_estado['Atrasada'])
        self.ids.Entregas_a_tiempo_text.text = str(num_act_estado['Entregada a tiempo'])

    def press_actividad(self):  # Abre la ventana donde se muestran los detalles de la actividad
        activity_name = obtener_materias('assests\BD\materias.csv').define_activity(self.text) ##listo
        sm.current = 'thirdwindow'
        sm.transition.direction = "left"


    def activity_check(self,*args):  # Se indica que se entregó una actividad
        archivo = 'assests\BD\materias.csv'
        activity_name = self.text
        materia = obtener_materias(archivo).obtener_materia_name_(modo=1)
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3, subject_name_=materia[0])
        materia = obtener_materias(archivo).obtener_materia_name()
        obtener_materias(archivo).actualizar_DB(clave[0], activity_name)
        sm.current ="firstwindow"
        sm.current = "secondwindow"


    def abrir_menu(self, button):  # Abre el menú con las materias
        self.menu.caller = button
        self.menu.open()

    def on_select_item_menu(self, text_item):  # Carga la ventana con la materia seleccionada
        self.menu.dismiss()
        sm.current = "secondwindow"
        sm.transition.direction = 'right'
        archivo = 'assests\BD\materias.csv'

        self.cur.execute("UPDATE user_settings SET materia_sel = '" + text_item + "' WHERE user_id = 1")
        self.cur.execute("UPDATE user_settings SET status = 'Por entregar' WHERE user_id = 1")
        self.cur.execute("UPDATE user_settings SET tipo_lista = 'TwoLineRightIconListItem' WHERE user_id = 1")
        self.conn.commit()

        obtener_materias(archivo).define_subject(text_item) ##listo
        self.update_screen()

    def entregas_a_tiempo(self, *args):
        archivo = 'assests\BD\materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1)  ## listo
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        obtener_materias(archivo).status(modo=4,status_='Entregada a tiempo')
        actividades = obtener_materias(archivo).status(modo=2,materia=clave[0],status_='Entregada a tiempo') ##listo
        self.update_screen()


    def entregas_con_atraso(self, *args):
        archivo = 'assests\BD\materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1)  ## listo
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        obtener_materias(archivo).status(modo=4,status_='Entregada con atraso') ##listo
        self.update_screen()


    def atrasadas(self, *args):
        archivo = 'assests\BD\materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1)  ## listo
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        obtener_materias(archivo).status(modo=4,status_='Atrasada') ## listo
        self.update_screen()


    def por_entregar(self, *args):
        archivo = 'assests\BD\materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1)  ## listo
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        obtener_materias(archivo).status(modo=4,status_='Por entregar') ## listo
        self.update_screen()


    ##Los métodos del MDBottomNavigation
    def consultar_calificaciones(self):  # Extrae el feedback de internet
        archivo = 'assests\BD\materias.csv'
        archivo_aux = 'assests\BD\semestres_materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1) ## listo
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3, subject_name_=subject_name[0]) ##listo
        actividades = obtener_materias(archivo).status(modo=5,materia=clave[0]) ##listo
        opts = Options()
        opts.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

        driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver.exe', options=opts)
        activity_feedback = Feedback([str(clave[0])], actividades, driver).extraccion_feedback()


    def abrir_plan_trabajo(self):
        archivo = 'assests\BD\materias.csv'
        archivo_clave_grupo = 'assests\BD\materia_grupo.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name_(modo=1) ## listo
        clave = obtener_materias(archivo).obtener_materia_name_(modo=3, subject_name_=subject_name[0]) ##listo
        subject_grupo = obtener_materias(archivo_clave_grupo).obtener_materia_grupo(clave[0])
        carpeta = subject_name[0] + r'\1. Materiales\plan_'+str(clave[0]) +'_'+ subject_grupo +'_'+'ED.pdf'
        path = r"C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Documents\Administracion\Ivan\4.Semestre 22-2" + r'"\"' + carpeta
        path = path.replace('"',"")
        print(path)
        subprocess.Popen([path], shell=True)


    def ver_progreso(self):
        sm.current = "fourthwindow"
        sm.transition.direction = 'left'
        

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


class FourthWindow(Screen):
    def __init_(self,**kwargs):
        super(FourthWindow,self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.imagen)
        archivo = 'assests\BD\materias.csv'
        subject_name = obtener_materias(archivo).obtener_materia_name()
        subject_clave = obtener_materias(archivo).obtener_materia_clave(subject_name)
        archivo_grafica_progreso = r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\suayedApp\assests\materia_dashboard_material\meta.xlsm'
        archivo_meta = 'assests\BD\materia_grupo.csv'
        resultados = goal_file(archivo_grafica_progreso,archivo,archivo_meta,subject_clave,subject_name).change_cell()
        self.ids.acumulado.text = "Acumulado \n" + str(resultados['acumulado'])
        self.ids.meta.text = "Mi meta: \n" + str(resultados['meta'])
    def imagen(self, *args):
       archivo = 'assests\BD\materias.csv'
       subject_name = obtener_materias(archivo).obtener_materia_name()
       subject_clave = obtener_materias(archivo).obtener_materia_clave(subject_name)
       self.ids.materia_progreso.clear_widgets()
       self.ids.materia_progreso.source = f'assests\materia_dashboard_material\{subject_clave}.gif'
    def go_back(self):
       sm.current = "secondwindow"


class ContentNavigationDrawer(MDBoxLayout): #Pertenece a la página principal
    nav_drawer = ObjectProperty()
    sm2 = ScreenManager()
    screen_two = SecondWindow
    screen_one = FirstWindow

class DrawerList(ThemableBehavior, MDList): #Pertenece a la página principal
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class ItemList(TwoLineListItem):  #Pertenece a la página principal
    screen_one = FirstWindow


class ListItemWithCheckbox(TwoLineRightIconListItem): #Pertenece a la pantalla donde se muestran las actividades por materia (se muestra para actividades por entregar o atrasadas)
    '''Custom list item.'''
    icon = StringProperty("")
    screen_two = SecondWindow

class ListItemWithoutCheckbox(TwoLineListItem):  #Pertenece a la pantalla donde se muestran las actividades por materia (se muestra para actividades entregafas)
    '''Custom list item.'''
    screen_two = SecondWindow

class RightCheckbox(IRightBodyTouch, MDCheckbox): #Pertenece a la pantalla donde se muestran las actividades por materia es el checkbox que se muestra para las actividades por entregar o atrasadas
    '''Custom right container.'''
    screen_login = LoginPage

class ScrolllabelLabel(ScrollView):   #Pertenece a la pantalla donde se muestra el feedback de las materias, y es es el scroll que permite hacer scroll a los comentarios del feedback
    text = StringProperty('')
    comentarios = ObjectProperty()

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
            sm.current = "firstwindow"
            sm.transition.direction = 'right'
        else:
            sm.current = "secondwindow"
            sm.transition.direction = 'right'

TestNavigationDrawer().run()
