# # https://github.com/vipinjangra/KivyMD

# ## VERSION 5
import os

import pandas as pd
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.list import IconRightWidget

from kivy.properties import ObjectProperty
from kivymd.uix.datatables import MDDataTable

from aux_scripts.picker_modificado import MDDatePickerModificado
 
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem
from kivymd.uix.list import ILeftBodyTouch, TwoLineRightIconListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons

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
from aux_scripts.info_materias import DB_admin
from aux_scripts.info_materias import goal_file
from aux_scripts.PT_extraction import Planes_de_trabajo

# Web scrapping
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from aux_scripts.plataformaSuayed import Feedback
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
        remember = DB_admin().remember_status(modo=0)  
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
        
        DB_admin().remember_status(modo = 1) 

    def login(self):
        user_info = DB_admin().user_info(columnas=['username', 'password']) 
        user = user_info['username']
        pass_ = user_info['password']
        self.ids.User.text = user
        self.ids.Pass.text = pass_


        if self.username.text == user and self.password.text == pass_:
            sm.current = "firstwindow"
            self.username.text = ""
            self.password.text = ""
        else:
            print("Not here!")

class FirstWindow(Screen):
    nav_drawer2 = ObjectProperty()
    def __init__(self,**kwargs):
        super(FirstWindow,self).__init__(**kwargs)

    
    def on_pre_enter(self):
        Clock.schedule_once(self.lista_semestres)
        self.nav_drawer2.set_state("close")

    def lista_semestres(self, dt): # Llena el MDlist del NavigationDrawer
        semestres = DB_admin().lista_semester()  
        #Limpiando los semestres anteriores
        self.ids.nav_drawer_content.ids.md_list.clear_widgets()

        for semestre in semestres:
            try:
                self.ids.nav_drawer_content.ids.md_list.add_widget(
                ItemList(text = semestre))
            except:
                pass   
        self.ids.nav_drawer_content.ids.md_list.add_widget(
        ItemList(text = 'Agregar semestre'))
    def definir_semestre(instance):
        if instance.text != 'Agregar semestre':
            semestre = instance.text
            DB_admin().define_semester(semestre) 
            sm.current ="secondwindow"
        else:
            sm.current = "addsemesterwindow"
            DB_admin().semester_añadido_info(semestre='1',accion='update')


    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        # self.root.ids.date_label.text = str(value)
        self.ids.enviado_el.text = str(value)

    # Click Cancel
    def on_cancel(self, instance, value):
        pass


    def show_date_picker(self):
        #current_month = date.today().month
        #DB_admin(archivo).dias_con_pendientes(modo=3, month=current_month,año='2022')
        date_dialog = MDDatePickerModificado()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


activity_name = ""
class SecondWindow(Screen):
    def __init_(self,**kwargs):
        super(SecondWindow,self).__init__(**kwargs)

    def db_connection(self):
        self.conn = mysql.connector.connect(user="root", password="123456",
                                            host="localhost",
                                            database="fca_materias",
                                            port='3306'
                                            )
        self.cur = self.conn.cursor()

    def on_pre_enter(self, *args):
        self.db_connection()
        self.por_entregar()
        #self.update_screen()

    def update_screen(self):
        # Limpiando las materias de la pantalla
        status = DB_admin().status(modo=1)
        self.ids.list_one.clear_widgets()

        ## Rellenando las materias del menú
        materias = DB_admin().extracción_materias()  ##listo  **
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
        ##
        subject_name = DB_admin().obtener_materia_name_(modo=1) ## busca la materia que se va a mostrar en la pantalla
        status = DB_admin().status(modo=3) ## buscando el status del cual se van a buscar las act conformes al él
        clave = DB_admin().obtener_materia_name_(modo=3,subject_name_=subject_name[0])  ## buscando la clave de la materia que se va a mostrar en pantalla
        actividades = DB_admin().status(modo=2,materia = clave[0],status_=status) ## busca las act conforme a la materia y status seleccionados

        #actividades = DB_admin(archivo).total_actividades(subject_name)

        self.ids.nombre_materia.title = subject_name[0]

        ## (TwoLineRightIconListItem) para actividades por entregar y atrasadas (TwoLineListItem) para entregadas
        lista = DB_admin().list_type()
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
        ##

        ## Cuenta cuantas actividades hay de la materia por status para mostrarlo en pantalla
        estados = ['Por entregar', 'Entregada con atraso', 'Atrasada', 'Entregada a tiempo']
        num_act_estado = dict()
        for estado in estados:
            num_actividades = len(DB_admin().status(modo=2, materia=clave[0], status_=estado)) ##listo
            num_act_estado[estado] = num_actividades
        self.ids.por_entregar_text.text = str(num_act_estado['Por entregar'])
        self.ids.Entregas_con_retraso_text.text = str(num_act_estado['Entregada con atraso'])
        self.ids.Atrasada_text.text = str(num_act_estado['Atrasada'])
        self.ids.Entregas_a_tiempo_text.text = str(num_act_estado['Entregada a tiempo'])
        ##

    def press_actividad(self):  # Abre la ventana donde se muestran los detalles de la actividad
        activity_name = DB_admin().define_activity(self.text) 
        sm.current = 'thirdwindow'
        sm.transition.direction = "left"


    def activity_check(self,*args):  # Se indica que se entregó una actividad
        activity_name = self.text
        materia = DB_admin().obtener_materia_name_(modo=1)
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=materia[0])
        DB_admin().actualizar_DB(clave[0], activity_name)
        sm.current ="firstwindow"
        sm.current = "secondwindow"


    def abrir_menu(self, button):  # Abre el menú con las materias
        self.menu.caller = button
        self.menu.open()

    def on_select_item_menu(self, text_item):  # Carga la ventana con la materia seleccionada
        self.menu.dismiss()
        sm.current = "secondwindow"
        sm.transition.direction = 'right'
        archivo = ''

        self.cur.execute("UPDATE user_settings SET materia_sel = '" + text_item + "' WHERE user_id = 1")
        self.cur.execute("UPDATE user_settings SET status = 'Por entregar' WHERE user_id = 1")
        self.cur.execute("UPDATE user_settings SET tipo_lista = 'TwoLineRightIconListItem' WHERE user_id = 1")
        self.conn.commit()
        self.update_screen()

    def entregas_a_tiempo(self, *args):
        subject_name = DB_admin().obtener_materia_name_(modo=1)  ## listo
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        DB_admin().status(modo=4,status_='Entregada a tiempo')
        actividades = DB_admin().status(modo=2,materia=clave[0],status_='Entregada a tiempo') ##listo
        self.update_screen()


    def entregas_con_atraso(self, *args):
        archivo = ''
        subject_name = DB_admin().obtener_materia_name_(modo=1)  
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0])  
        DB_admin().status(modo=4,status_='Entregada con atraso') ##listo
        self.update_screen()


    def atrasadas(self, *args):
        subject_name = DB_admin().obtener_materia_name_(modo=1)  ## listo
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        DB_admin().status(modo=4,status_='Atrasada') ## listo
        self.update_screen()


    def por_entregar(self, *args):
        subject_name = DB_admin().obtener_materia_name_(modo=1)  ## listo
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        DB_admin().status(modo=4,status_='Por entregar') ## listo
        self.update_screen()


    ##Los métodos del MDBottomNavigation
    def consultar_calificaciones(self):  # Extrae el feedback de internet
        subject_name = DB_admin().obtener_materia_name_(modo=1) ## listo
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0]) ##listo
        actividades = DB_admin().status(modo=5,materia=clave[0]) ##listo
        opts = Options()
        opts.add_argument(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36.")
        driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),options=opts)
        # opts.add_argument(
        #     "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")

        # driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver.exe', options=opts)
        activity_feedback = Feedback([str(clave[0])], actividades, driver).extraccion_feedback()


    def abrir_plan_trabajo(self):
        subject_name = DB_admin().obtener_materia_name_(modo=1) 
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0]) 
        subject_grupo = DB_admin().obtener_materia_grupo(clave[0]) 
        semestre_info = DB_admin().fetch_semester_selected_info()
        semestre_name = semestre_info['name']
        semestre_id = semestre_info['id']
        pdf_file = subject_name[0] + '//1. Materiales//plan_'+str(clave[0]) +'_'+ str(subject_grupo) +'_'+'ED.pdf'
        archivo_categorias = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'files', pdf_file))
        path = "C://Users//ivan_//Documents//UNAM//Semestres//{}. {}//{}".format(str(int(semestre_id)+5), semestre_name, pdf_file)
        subprocess.Popen([path], shell=True)


    def ver_progreso(self):
        sm.current = "fourthwindow"
        sm.transition.direction = 'left'
        

class ThirdWindow(Screen):
    def on_pre_enter(self, *args):
        activity_name = DB_admin().obtener_materia_name_(modo=4) 
        activity_name = DB_admin().encode_decode_activity(activity_name, decode=True)
        subject_name = DB_admin().obtener_materia_name_(modo=1) 
        clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0]) 
        activity_status = DB_admin().estado_actividad(clave=clave[0],actividad=activity_name) 


        self.ids.nombre_actividad.title = activity_name
        self.ids.enviado_el.text = f' Enviada el : {activity_status[0]}'
        self.ids.ponderacion.text = f' Valor : {"{0:.0f}%".format(float(activity_status[1]))}'
        self.ids.estatus_entrega.text = f' Status : {activity_status[2]}'
        self.ids.calificacion.text = f' Calificación :  {activity_status[3]}'
        if activity_status[4]!= "":
            date = activity_status[4].split('-')
            date = date[2]+'-'+date[1]+'-'+date[0]
            self.ids.calificado_el.text = f' Calificada el : {date}' 
        else:
            self.ids.calificado_el.text = ""
        self.ids.scroll_lable.ids.comentarios.text = f' {activity_status[5]}'



    #Click OK
    def on_save(self, instance, value, date_range):
        fecha = value.strftime('%d/%m/%Y')
        self.ids.enviado_el.text = str(fecha)
        DB_admin().update_fecha_entregada(value)        

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
        subject_name = DB_admin().obtener_materia_name_(modo=1) ## listo
        subject_clave = DB_admin().obtener_materia_name_(modo=3, subject_name_=subject_name[0])  ## listo
        archivo_grafica_progreso = r'assets\materia_dashboard_material\meta.xlsm'
        semestre_seleccionado = DB_admin().semestre_seleccionado()
        resultados = goal_file(archivo_grafica_progreso,semestre_seleccionado,subject_clave[0],subject_name).progreso()
        self.ids.top_bar_w4.title = subject_name[0]
        self.ids.acumulado.text = "Acumulado \n" + str(resultados['acumulado'])
        self.ids.meta.text = "Mi meta: \n" + str(resultados['meta'])
        self.ids.max_cal.text = "Calificación \n máxima\n" + str(resultados['max_posible'])
        #Clock.schedule_once(self.imagen)
        df = DB_admin().condensado_tareas(subject_clave[0])
        df = df.iloc[:, 0:]
        cols = df.columns.values
        values = df.values
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.9),
            pos_hint = {"x":0.05,"y":0.05},
            use_pagination=True,
            column_data=[
                (col, dp(20))
                for col in cols
            ],
            row_data=values
        )
        self.ids.tabla.add_widget(self.data_tables)
    def imagen(self, *args):
        subject_name = DB_admin().obtener_materia_name_(modo=1)  ## listo
        subject_clave = DB_admin().obtener_materia_name_(modo=3,subject_name_=subject_name[0])  ## listo       self.ids.materia_progreso.clear_widgets()
        self.ids.materia_progreso.source = f'assets\materia_dashboard_material\{subject_clave[0]}.gif'

    def go_back(self):
        sm.current = "secondwindow"

    dialog = None
    def show_confirmation_dialog(self):
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
                        text="OK", on_press=self.setGoal
                    ),
                ],
            )
        self.dialog.get_normal_height()
        self.dialog.open()


    def setGoal(self,int):
        self.conn = mysql.connector.connect(user="root", password="123456",
                                            host="localhost",
                                            database="fca_materias",
                                            port='3306'
                                            )
        self.cur = self.conn.cursor()
        for obj in self.dialog.content_cls.children:
            subject_name = DB_admin().obtener_materia_name_(modo=1) ## busca la materia que se va a mostrar en la pantalla
            clave = DB_admin().obtener_materia_name_(modo=3,subject_name_=subject_name[0])  ## buscando la clave de la materia que se va a mostrar en pantalla
            query = "UPDATE materias_usuario SET meta = '{}' WHERE clave_materia = '{}'".format(obj.text,clave[0])
            self.cur.execute(query)
            self.conn.commit()
            self.ids.meta.text = "Mi meta: \n" + str(float(obj.text))
            obj.text = ""
            self.dialog.dismiss()
    def closeDialog(self,int):
        self.dialog.dismiss()

class AddSemesterWindow(Screen):
    def __init__(self,**kwargs):
        super(AddSemesterWindow,self).__init__(**kwargs)
    def on_pre_enter(self, *args):
        self.ids.top_bar_w5.title = "Añade las materias que cursarás en este semestre"
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.9),
            pos_hint = {"x":0.05,"y":0.05},
            use_pagination=True,
            column_data=[
                ("Materia", dp(60)),
                ("Grupo", dp(30)),
                
            ],
            row_data=[]
        )
        self.ids.add_semester_table.add_widget(self.data_tables)


        menu_semestre_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{str(i)} ° semestre",
                "height": dp(40),
                "on_release": lambda x=i: self.on_select_item_menu(x),
            } for i in range(1,9)
        ]
        self.menu_semestres = MDDropdownMenu(
            caller=self.ids.semestre,
            items=menu_semestre_items,
            width_mult=4,
        )


    def go_back(self):
        sm.current = "firstwindow"
    def on_select_item_menu(self, text_item):
        DB_admin().semester_añadido_info(semestre=text_item,accion='update')
        semestre_a_seleccionar =  DB_admin().semester_añadido_info(accion='select')
        materias = DB_admin().materias_por_semestre(carrera="Administración",semestre=semestre_a_seleccionar)
        materias_name = [x['materia'] for x in materias]
        '''menu de materias'''
        menu_materias_items = [
            {
                "viewclass": "OneLineListItem",
                "text": materia,
                "height": dp(40),
                "on_release": lambda x=materia: self.on_select_item_menu_materias(x),
            } for materia in materias_name
        ]
        self.menu_materias = MDDropdownMenu(
            caller=self.ids.semestre,
            items=menu_materias_items,
            width_mult=4,
        )
        self.menu_semestres.dismiss()
    def on_select_item_menu_materias(self, text_item):
        materia = text_item.title()
        grupo = self.ids.grupo.text
        if grupo != "":
            self.add_materia_a_tabla(materia=materia,grupo=grupo)
            self.menu_materias.dismiss()

    def add_materia_a_tabla(self,materia,grupo):
        self.data_tables.row_data.append((materia,grupo))

    def agregar_materias_DB(self):
        materias = self.data_tables.row_data
        lista_materias = []
        for materia in materias:
            dicc = {}
            dicc['nombre'] = materia[0].upper()
            dicc['grupo'] = materia[1]
            dicc['clave_materia'] = DB_admin().obtener_materia_name_(modo=6,subject_name_=materia[0].upper())
            lista_materias.append(dicc)
        semestre = 'Semestre 23-2'
        DB_admin().semester_añadido_info(semestre=semestre,accion='insertar')
        DB_admin(usuario=1).semester_añadido_info(semestre=semestre,materias=lista_materias,accion='insertar_materias')
        Planes_de_trabajo(semestre =semestre.split(' ')[1]).descargaPlanes(modalidad='d')

        
        
            
class ContentNavigationDrawer(MDBoxLayout): #Pertenece a la página principal
    nav_drawer = ObjectProperty()
    sm2 = ScreenManager()
    screen_two = SecondWindow


class DrawerList(ThemableBehavior, MDList): #Pertenece a la página principal
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
    nav_drawer = ObjectProperty()


class ItemList(TwoLineListItem):  #Pertenece a la página principal
    screen_one = FirstWindow
    nav_drawer2 = ObjectProperty()


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



class Content(BoxLayout):pass

sm = ScreenManager()
class suayedApp(MDApp):
    def build(self):
        Window.size = (350, 600)
        self.title = "MysuayedApp"
        sm2 = ScreenManager()
        Builder.load_file('mysuayedApp.kv')
        sm.add_widget(LoginPage(name='login_page'))
        sm.add_widget(FirstWindow(name='firstwindow'))
        sm.add_widget(SecondWindow(name='secondwindow'))
        sm.add_widget(ThirdWindow(name='thirdwindow'))
        sm.add_widget(FourthWindow(name='fourthwindow'))
        sm.add_widget(AddSemesterWindow(name='addsemesterwindow'))
        return sm

    def go_back(self,pantalla):
        if pantalla == 1:
            sm.current = "firstwindow"
            sm.transition.direction = 'right'
        else:
            sm.current = "secondwindow"
            sm.transition.direction = 'right'

suayedApp().run()

