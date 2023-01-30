import pdfplumber
import xlwings as xw
import pandas as pd
import re
import datetime
from time import sleep
from aux_scripts.info_materias import DB_admin
#from info_materias import DB_admin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import requests

class Planes_de_trabajo():
  def __init__(self,semestre=None):
    self.semestre = semestre
    self.semestre_info = self.semestre.split('-')
    self.resta = 0 if self.semestre_info[1] == '2' else 1
    self.año = '20' + (str(int(self.semestre_info[0])-self.resta))
    self.semestre_num = self.semestre_info[1]

  def define_driver_opts(self):
    opts = Options()
    opts.add_argument(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36.")
    opts.add_experimental_option("prefs", {
        "download.default_directory": r"C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\suayedApp\assests\files\planes_de_trabajo",
    })
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),options=opts)
    return driver

  def get_fca_subjects(self):
    list_url = [f'https://planes-trabajo.fca.unam.mx/distancia/2012/{num}' for num in range(1,9)]
    materias_ = []
    for index,url in enumerate(list_url):
        driver = self.define_driver_opts()
        driver.get(url)
        materias = driver.find_elements(By.XPATH,"//table[@class='table table-striped']//td[@style='width:10%']")
        materias_name = [x.text for x in driver.find_elements(By.XPATH,"//th[@class='table-primary']")]
        clave_carrera = []
        for i in range(0,len(materias),6):
            clave = materias[i].text
            carrera = materias[i+2].text
            clave_carrera.append(clave+'_'+carrera)
        lista_clave_carrera =[]
        for x in clave_carrera:
            if x not in lista_clave_carrera:
                lista_clave_carrera.append(x)
        
        #juntar materias_name y clave_carrera en una lista
        for i in range(len(lista_clave_carrera)):
            materias_.append(materias_name[i]+'_'+lista_clave_carrera[i]+'_'+str(index+1))
    #pasar la lista a un dataframe
    df = pd.DataFrame(materias_,columns=['Materia'])
    df['clave_materia'] = df['Materia'].apply(lambda x: x.split('_')[1])
    df['carrera'] = df['Materia'].apply(lambda x: x.split('_')[2])
    df['materia'] = df['Materia'].apply(lambda x: x.split('_')[0]) 
    df['semestre'] = df['Materia'].apply(lambda x: x.split('_')[3])
    df.drop('Materia',axis=1,inplace=True)
    #pasar las carreras a columnas con pivot
    df = df.pivot(index=['clave_materia','materia','semestre'],columns='carrera',values='carrera').reset_index()
    #guardar el df en un csv
    df.to_csv('assests/files/materias_fca.csv',index=True)

  def descargaPlanes(self,modalidad=None,materias=None):
    driver = self.define_driver_opts()
    if modalidad =="d":
        materias = DB_admin().materias_por_semestre(self.semestre,usuario='1') if materias == None else materias
        for materia in materias:
            materia_name = materia['materia']
            grupo = materia['grupo']
            semestre_num = str(grupo)[1:2]
            clave_materia = materia['clave_materia']
            url = f'https://planes-trabajo.fca.unam.mx/distancia/2012/{semestre_num}'
            driver.get(url)
            links_descarga = driver.find_elements(By.XPATH,'//a[@role="button"]')
            links_descarga = [link_descarga.get_attribute('href') for link_descarga in links_descarga]
            link_buscado = f'https://planes-trabajo.fca.unam.mx/pdf/{clave_materia}/{grupo}/ED'
            local_filename = 'assests/files/planes_de_trabajo/plan_{}_{}_ED.pdf'.format(clave_materia,grupo)
            if link_buscado in links_descarga:
                #descargar el pdf
                r = requests.get(link_buscado, stream=True)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
            else:
                list_url = [f'https://planes-trabajo.fca.unam.mx/distancia/2012/{num}' for num in range(1,9)]
                for url in list_url:    
                    driver.get(url)
                    links_descarga = driver.find_elements(By.XPATH,'//a[@role="button"]')
                    links_descarga = [link_descarga.get_attribute('href') for link_descarga in links_descarga]
                    link_buscado = f'https://planes-trabajo.fca.unam.mx/pdf/{clave_materia}/{grupo}/ED'

                    if link_buscado in links_descarga:
                        #descargar el pdf
                        r = requests.get(link_buscado, stream=True)
                        with open(local_filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024): 
                                if chunk: # filter out keep-alive new chunks
                                    f.write(chunk)
                    else:
                        print('no se encontro el plan de trabajo de la materia {} en el semestre {}'.format(materia_name,self.semestre))
            self.parse(local_filename)
        self.call_macro()

  def mes_digit(self,mes,monthNameEnSp):
      if mes == 'enero':
          if monthNameEnSp == 1:
              return "01"
          else:
              return "January"
      elif mes == 'febrero':
          if monthNameEnSp == 1:
              return "02"
          else:
              return "February"
      elif mes == 'marzo':
          if monthNameEnSp == 1:
              return "03"
          else:
              return "March"
      elif mes == 'abril':
          if monthNameEnSp == 1:
              return "04"
          else:
              return "April"
      elif mes == 'mayo':
          if monthNameEnSp == 1:
              return "05"
          else:
              return "May"
      elif mes == 'junio':
          if monthNameEnSp == 1:
              return "06"
          else:
              return "June"
      elif mes == 'julio':
          if monthNameEnSp == 1:
              return "07"
          else:
              return "July"
      elif mes == 'agosto':
          if monthNameEnSp == 1:
              return "08"
          else:
              return "August"
      elif mes == 'septiembre':
          if monthNameEnSp == 1:
              return "09"
          else:
              return "September"
      elif mes == 'octubre':
          if monthNameEnSp == 1:
              return "10"
          else:
              return "October"
      elif mes == 'noviembre':
          if monthNameEnSp == 1:
              return "11"
          else:
              return "November"
      elif mes == 'diciembre':
          if monthNameEnSp == 'Sp':
              return "12"
          else:
              return "December"
      else:
          return mes

  def pdf_text(self,archivo=None):
    pdf = pdfplumber.open(archivo)
    paginas = pdf.pages
    linea_gigante = ""
    for page in paginas:
        text = page.extract_text()
        for line in text.split('\n'):
            linea_gigante = linea_gigante + line
    return linea_gigante

  def Dates_dataFrame(self,archivo=None):
    try:
        fechas2 = list()
        text = self.pdf_text(archivo=archivo)
        text_extracion = re.findall('(CALENDARIO DE ACTIVIDADES.+VII.+Sistema.+FACTORES)', text)
        fechas = re.findall('(\d{2}\sde\s(agosto|septiembre|octubre|noviembre|diciembre))', text_extracion[0]) if self.semestre_num== '1' else re.findall('(\d{2}\sde\s(enero|febrero|marzo|abril|mayo|junio|julio))', text_extracion[0])
        fechas = [fecha[0] for fecha in fechas if fecha[0] != '']
        fechas = fechas

        for bb in range(0, len(fechas)):
            fecha = fechas[bb].replace(' ', '').replace('de', " ") + ' ' + self.año
            fechas[bb] = fecha


        long_fechas = len(fechas)
        for bb in range(0, long_fechas):
            if bb+1 < len(fechas):
                try:
                    fecha1 = fechas[bb].replace(fechas[bb].split(' ')[1],
                                                self.mes_digit(fechas[bb].split(' ')[1], 2))
                    fecha2 = fechas[bb + 1].replace(fechas[bb + 1].split(' ')[1],
                                                    self.mes_digit(fechas[bb + 1].split(' ')[1], 2))
                    
                    date1 = datetime.datetime.strptime(fecha1, '%d %B %Y')
                    date2 = datetime.datetime.strptime(fecha2, '%d %B %Y')
                    diffDates = (date2 - date1).days
                    fech = fechas[bb].replace(fechas[bb].split(' ')[1],
                            self.mes_digit(fechas[bb].split(' ')[1], 1)).replace(" ", "/")

                    fechas2.append(fech)
                    if diffDates < 0.0:
                        fechas.remove(fechas[bb + 1])
                        fechas2.remove(fechas2[bb + 1])
                except Exception as e:
                    pass
            else:

                fech = fechas[bb].replace(" ", "/").replace(fechas[bb].split(' ')[1],
                                                    self.mes_digit(fechas[bb].split(' ')[1], 1))
                fechas2.append(fech)
    except Exception as e:
        pass
    unidad = [0 for i in range(len(fechas2))]
    act = [0 for i in range(len(fechas2))]
    ponderacion = [0 for i in range(len(fechas2))]
    #dataframe con fechas2, unidad, act, ponderacion
    df = pd.DataFrame(list(zip(fechas2, unidad, act, ponderacion)), columns =['Fecha','Unidad','Actividad','Ponderacion'])
    return df
    
  def clave_materia(self,archivo=None):
    text = self.pdf_text(archivo=archivo)
    text_datos_materia = re.findall('(III.+)IV. Contenido', text)
    clave_materia = re.findall('Clave (\d{4})', text_datos_materia[0])
    return clave_materia[0]
   
  def grupo(self,archivo=None):
    text = self.pdf_text(archivo=archivo)
    text_datos_materia = re.findall('(III.+)IV. Contenido', text)
    clave_materia = re.findall('Grupo (\d{4})', text_datos_materia[0])
    return clave_materia[0]

  def call_macro(self,archivo=None):
    app = xw.App(visible=False)
    wb = xw.Book('assests/files/actividades_por_materia/1.juntar_act.xlsm')
    macro1 = wb.macro('Juntar_materias.create_sheets')
    macro1()

  def parse(self,archivo=None):
    pdf = pdfplumber.open(archivo)
    meses = {'agosto':'08','septiembre':'09','octubre':'10','noviembre':'11','diciembre':'12'} if self.semestre_num == '1' else {'febrero':'02','marzo':'03','abril':'04','mayo':'05','junio':'06'} 
    paginas = pdf.pages
    inicio = False
    final = False
    act_table = []
    for index,pagina in enumerate(paginas):
      text = pagina.extract_text()

      if "CALENDARIO DE ACTIVIDADES" in text:
        inicio = True
      
      if inicio == True and final ==False:
        tables = pagina.extract_tables()
        for table in tables:
          act_table.append([row for row in table if len(row)==5])

      if "VII. Sistema de evaluación" in text:
        final = True
    #eliminar listas vacias
    act_table = [x for x in act_table if x != []]


    #convertir a dataframes y concatenar
    table = pd.DataFrame(act_table[0],columns = ['Fecha','Unidad','Actividad','Descripción','Ponderacion'])
    for i in range(1,len(act_table)):
      df2 = pd.DataFrame(act_table[i],columns = ['Fecha','Unidad','Actividad','Descripción','Ponderacion'])
      table = pd.concat([table,df2],axis=0)


    num_filas = table.shape[0]
    for i in range(num_filas):
        celda = table.iloc[i,0]
        tipo = type(celda)
        if type(celda) != str:
          continue
        target_months = '|'.join(meses.keys())
        my_regex = "(\d{2}\sde\s("  + target_months + "))"                               
        fecha = re.findall(my_regex, celda)
        unidad = re.findall('(UNIDAD.+\d{1,2})', celda)
        ponderacion = re.findall('(\d{1,2}\s%)', celda)
        if len(fecha)>0 and len(unidad)>0 and len(ponderacion)>0:
            table.iloc[i,0] = fecha[0][0]
            table.iloc[i,1] = unidad[0]
            table.iloc[i,4] = ponderacion[0]
    df2 = self.Dates_dataFrame(archivo=archivo)
    table = self.df_formating(table,self.año,self.semestre,meses)
    table = pd.merge(table,df2,how='outer',on='Fecha')
    #cambiar el formato de la columna fecha de dd/mm/yyyy a yyyy/mm/dd
    table['Fecha'] = pd.to_datetime(table['Fecha'],format='%d/%m/%Y')
    table['Fecha'] = table['Fecha'].dt.strftime('%Y/%m/%d')
    table = table.drop(columns=['Unidad_y','Actividad_y','Ponderacion_y'])
    table = table.rename(columns={'Unidad_x':'Unidad','Actividad_x':'Actividad','Ponderacion_x':'Ponderacion'})
    table = table.drop_duplicates(subset=['Fecha','Actividad'],keep='first')
    #ordenar el df por fecha
    table = table.sort_values(by='Fecha')
    table['Semestre'] = "'"+self.semestre
    table['Clave'] = self.clave_materia(archivo=archivo)
    table['Grupo'] = self.grupo(archivo=archivo)
    self.df_to_csv(table,self.clave_materia(archivo=archivo))
    
    
  def df_formating(self,table,año,semestre,meses):
    '''dataframe fromat prepareation '''
    table['Unidad'] = table['Unidad'].str.slice(0,8)
    table['Unidad'] = table['Unidad'].str.replace('UNIDAD ','')
    replacements = {'\n':' ','Act. de aprendizaje':'apren','Cuestionario de reforzamiento':'refor','Act. complementaria':'com',
                    'Foros':'foro','Act. lo que aprendí':'loque','Act. lo que aprendí':'loque'}
    for k,v in replacements.items():
        table['Actividad'] = table['Actividad'].str.replace(k,v)
    #concatenar el año a la fecha
    table['Fecha'] = table['Fecha'].str.replace('\n',' ')
    table['Ponderacion'] = table['Ponderacion'].str.replace(' %',' ')
    for mes,mes_num in meses.items():
      table['Fecha'] = table['Fecha'].str.replace(' de '+mes,'/'+ mes_num +'/'+año)
    text_to_replace = ' de {}'.format(self.año)
    table['Fecha'] = table['Fecha'].str.replace(text_to_replace,'')
    table = table[table['Fecha'].str.contains('\d{2}/\d{2}/\d{4}')]
    table = table.reset_index(drop=True)
    table = table.drop(columns=['Descripción'])
    return table

  def df_to_csv(self,df,clave_materia):
    clave_materia = clave_materia[1:] if clave_materia[0:1] == '0' else clave_materia
    nombre_materia = DB_admin().obtener_materia_name_(modo=5,clave_materia=clave_materia)
    df.to_csv(f'assests/files/actividades_por_materia/{nombre_materia}.csv',index=False)
     
 
#df1 = Planes_de_trabajo(r"C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Documents\Administracion\Ivan\5. Semestre 23-1\COACHING\1. Materiales/plan_285_8451_ED.pdf",'23-1').parse()
#df1.clave_materia()


#c = Planes_de_trabajo(semestre ='23-2').descargaPlanes(modalidad='d',materias = [{'materia':'PRESUPUESTOS','grupo':'8451','clave_materia':'1454'}])

#c = Planes_de_trabajo().get_fca_subjects()


