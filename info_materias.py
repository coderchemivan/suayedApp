import csv

import datetime
from datetime import date
import chardet
import pandas as pd
import xlwings as xw
from openpyxl import load_workbook
import re


class obtener_materias():

    def __init__(self, archivo_materias):
        self.archivo_materias = archivo_materias

    def lista_semester(self):  # Devuelve una lista con los semestres disponibles
        with open(self.archivo_materias, 'rb') as rawdata:
            result = chardet.detect(rawdata.read(100000))
        df = pd.read_csv(self.archivo_materias, encoding=result['encoding'])
        semestres = df['Semestre'].unique()
        return semestres

    def define_semester(self, semestre, archivo_aux):
        with open(archivo_aux, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            semester_list = list()

            myList[1][16] = "TwoLineRightIconListItem"
            first_subject_semester = False

            for x, row in enumerate(myList):
                if x == 0:
                    semester_list.append(row[2:])

                elif x > 0:
                    if first_subject_semester is False and row[1] == semestre:
                        myList[1][12] = row[3]
                        materia = row[3]
                        first_subject_semester = True
                    if myList[x][1] == semestre:
                        if len(semester_list) == 1:
                            row = row[2:]
                            row[10] = materia
                            semester_list.append(row)
                        else:
                            semester_list.append(row[2:])

            my_new_list = open(self.archivo_materias, 'w', newline='')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(semester_list)
            first_subject_semester = False

    def dias_con_pendientes(self, modo, month=None, año=None, fecha=None):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)

        if modo == 1:
            lista_dias = list()
            for x, line in enumerate(myList):
                if x > 0:
                    fecha_entrega = myList[x][3]
                    fecha_split = fecha_entrega.split('/')
                    mes_ = fecha_split[1]
                    año_ = fecha_split[2]
                    if month == mes_ and año_ == año:
                        lista_dias.append(fecha_split[0])

            return lista_dias
        elif modo == 2:
            mes_trabajado = myList[1][15]
            return mes_trabajado
        elif modo == 3:  # Se pone el mes actual en la BD
            myList[1][15] = month
            my_new_list = open(self.archivo_materias, 'w', newline='')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(myList)

        elif modo == 4:
            lista_dias = list()
            materias = list()
            actividades = list()
            estados = list()
            materia_actividad = list()
            for x, line in enumerate(myList):
                if x > 0:
                    materia = myList[x][1]
                    actividad = myList[x][2]
                    fecha_entrega = myList[x][3]
                    estado = myList[x][5]
                    materia_act = dict()
                    if fecha_entrega == fecha:
                        lista_dias.append(fecha_entrega)
                        materias.append(materia)
                        actividades.append(actividad)
                        estados.append(estado)
            materia_actividad.append(materias)
            materia_actividad.append(actividades)
            materia_actividad.append(estados)
            return materia_actividad

    def remember_status(self):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            if myList[1][2] == 'True':
                myList[1][2] = 'False'
            else:
                myList[1][2] = 'True'
            my_new_list = open(self.archivo_materias, 'w', newline='')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(myList)

    def extracción_materias(self):
        with open(self.archivo_materias, 'r') as file:
            tabla_info_materias = csv.reader(file)
            materias = list()
            c = 0
            for row in tabla_info_materias:
                materia = row[1]
                if not materia in materias and c != 0:
                    materias.append(row[1])
                c += 1
        return materias

    def subject_actividades(self, subject):
        with open(self.archivo_materias, 'r') as file:
            tabla_info_materias = csv.reader(file)
            actividades = list()
            for row in tabla_info_materias:
                materia = row[1]
                if materia == subject:
                    actividades.append(row[2])
        return actividades

    def total_actividades(self, materia):
        with open(self.archivo_materias, 'r') as file:
            tabla_info_materias = csv.reader(file)
            reader = csv.reader(file)
            myList = list(reader)

            estado = myList[1][12]

            actividades = list()
            dates = list()
            activity_date = dict()
            c = 0
            for row in myList:
                if c > 0:
                    partes = row[3].split('/')
                    fecha_de_entrega = partes[0] + "-" + partes[1] + "-" + partes[2]
                    fecha_de_entrega = datetime.datetime.strptime(fecha_de_entrega, '%d-%m-%Y')

                    if row[4] != "":
                        a = (row[4])
                        partes = row[4].split('/')
                        fecha_entregada = partes[0] + "-" + partes[1] + "-" + partes[2]
                        fecha_entregada = datetime.datetime.strptime(fecha_entregada, '%d-%m-%Y')
                        diff = (fecha_de_entrega - fecha_entregada).days
                        diff_fechaEntregada_Hoy = abs((fecha_entregada - datetime.datetime.today()).days)


                    else:
                        diff = (fecha_de_entrega - datetime.datetime.today()).days
                        diff_fechaEntrega_Hoy = abs((fecha_de_entrega - datetime.datetime.today()).days)

                    if estado == 'todas' and row[1] == materia:
                        actividades.append(row[2])
                        d = row[5]
                        if diff >= 0 and 'Entregada' not in row[5]:
                            activity_date[row[2]] = f'Due to {row[3]}'
                        elif 'Entregada' in row[5]:
                            activity_date[row[2]] = f'Delivered {diff_fechaEntregada_Hoy} days ago'
                        elif diff < 0 and row[4] == "":
                            activity_date[row[2]] = f'{diff_fechaEntrega_Hoy} days delayed'

                    elif estado == 'por entregar' and diff >= 0 and row[1] == materia and row[5] == 'Por entregar':
                        actividades.append(row[2])
                        activity_date[row[2]] = f'Due to {row[3]}'
                    elif estado == 'entregadas a tiempo' and diff >= 0 and row[1] == materia and row[
                        5] == 'Entregada a tiempo':
                        actividades.append(row[2])
                        activity_date[row[2]] = f'Delivered {diff_fechaEntregada_Hoy} days ago'
                    elif estado == 'entregadas con atraso' and diff < 0 and row[1] == materia and row[
                        5] == "Entregada con atraso":
                        actividades.append(row[2])
                        activity_date[row[2]] = row[3]
                        if diff_fechaEntregada_Hoy != "today":
                            activity_date[row[2]] = f'Delivered {diff_fechaEntregada_Hoy} days ago'
                        else:
                            activity_date[row[2]] = f'Delivered {diff_fechaEntregada_Hoy}'
                    elif estado == 'atrasadas' and row[1] == materia and diff < 0 and row[4] == "":
                        actividades.append(row[2])
                        activity_date[row[2]] = f'{diff_fechaEntrega_Hoy} days delayed'
                c += 1

        return activity_date

    def actualizar_estados(self):  # Actualiza los estados de las actividades en cuanto abre la app
        with open(self.archivo_materias, 'r') as file:
            tabla_info_materias = csv.reader(file)
            reader = csv.reader(file)
            myList = list(reader)
            c = 0
            for row in myList:
                if c > 0:
                    partes = row[3].split('/')
                    fecha_de_entrega = partes[0] + "-" + partes[1] + "-" + partes[2]
                    fecha_de_entrega = datetime.datetime.strptime(fecha_de_entrega, '%d-%m-%Y')

                    if row[4] == "":
                        diff = (datetime.datetime.today() - fecha_de_entrega).days
                        if diff <= 0:
                            estado = 'Por entregar'
                        else:
                            estado = 'Atrasada'
                        myList[c][5] = estado
                        my_new_list = open(self.archivo_materias, 'w', newline='')
                        csv_writer = csv.writer(my_new_list)
                        csv_writer.writerows(myList)
                c += 1

    def obtener_fecha_entrega(self, materia):
        with open(self.archivo_materias, 'r') as file:
            tabla_info_materias = csv.reader(file)
            fechas = list()
            for row in tabla_info_materias:
                if row[1] == materia:
                    # materia = row[0]
                    fechas.append(row[3])
        return fechas


    def define_activity(self, actividad):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            for line in reader:
                myList.append(line)

            myList[1][9] = actividad
            my_new_list = open(self.archivo_materias, 'w', newline='')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(myList)

    def define_subject(self, materia):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            for line in reader:
                myList.append(line)
            myList[1][10] = materia
            my_new_list = open(self.archivo_materias, 'w', newline='')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(myList)

    def estado_actividad(self, estado, list_name):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            for line in reader:
                myList.append(line)
            myList[1][12] = estado
            myList[1][14] = list_name

            my_new_list = open(self.archivo_materias, 'w', newline='')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(myList)

    def obtener_activity_name(self):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            for line in reader:
                myList.append(line)
            actividad = myList[1][9]
            return actividad

    def obtener_materia_name(self):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            for line in reader:
                myList.append(line)
            materia = myList[1][10]
            return materia

    def list_type(self):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)
            for line in reader:
                myList.append(line)
            list_type_ = myList[1][14]
            return list_type_

    def obtener_materia_clave(self, materia):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list()
            for line in reader:

                if line[1] == materia:
                    clave = str(line[0])
                    break
        return clave

    def obtener_materia_grupo(self, clave):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            grupo = ""
            for line in reader:
                if line[0] == clave:
                    grupo = str(line[1])
                    break
        return grupo

    def actualizar_DB(self, materia, actividad):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            myList = list(reader)

            c = 0
            for row in myList:
                if row[1] == materia and row[2] == actividad:
                    hoy = date.today().strftime('%d/%m/%Y')
                    myList[c][4] = hoy
                    partes = row[3].split('/')
                    fecha_de_entrega = partes[0] + "-" + partes[1] + "-" + partes[2]
                    fecha_de_entrega = datetime.datetime.strptime(fecha_de_entrega, '%d-%m-%Y')
                    diff = (fecha_de_entrega - datetime.datetime.today()).days
                    if diff >= 0:
                        myList[c][5] = 'Entregada a tiempo'
                    else:
                        myList[c][5] = 'Entregada con atraso'
                    break
                c += 1
            my_new_list = open(self.archivo_materias, 'w', newline='')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(myList)


class estatus_feedback():
    def __init__(self, archivo_materias, materia, actividad):
        self.archivo_materias = archivo_materias
        self.actividad = actividad
        self.materia = materia

    def resultados(self):
        with open(self.archivo_materias, 'r') as file:
            reader = csv.reader(file)
            activity_status = list()
            for line in reader:

                if line[1] == self.materia and line[2] == self.actividad:
                    fecha_entregada = line[4]
                    status = line[5]
                    calificacion = line[6]
                    calificada_el = line[7]
                    comentarios = line[8]
                    valor = line[13]

                    activity_status.append(fecha_entregada)
                    activity_status.append(status)
                    activity_status.append(calificacion)
                    activity_status.append(calificada_el)
                    activity_status.append(comentarios)
                    activity_status.append(valor)
                    break

            return activity_status


class vaciar_feedback():
    def __init__(self, archivo_materias, materia, actividades_feedback):
        self.archivo_materias = archivo_materias
        self.materia = materia
        self.actividades_feedback = actividades_feedback

    def vaciar_resultados(self):
        with open(self.archivo_materias, 'r') as file:

            reader = csv.reader(file)
            myList = list(reader)
            for line in reader:
                myList.append(line)
            for k, v in self.actividades_feedback.items():
                c = 0
                for row in myList:
                    if row[3] == self.materia and row[4] == k:
                        if v[0]!="" and v[0]!="Sin envío":
                            v[0] = float(v[0].split("/")[0])
                        else:pass
                        myList[c][8] = v[0]  # calificacion
                        myList[c][9] = v[1]  # calificada el
                        myList[c][10] = v[2]  # comentarios
                    c += 1
                    continue

                with open(self.archivo_materias, 'rb') as rawdata:
                    result = chardet.detect(rawdata.read(100000))
                my_new_list = open(self.archivo_materias, 'w', newline='', encoding=result['encoding'])
                csv_writer = csv.writer(my_new_list)
                for line in myList:
                    try:
                        csv_writer.writerow(line)
                    except:
                        line[10] = line[10].encode('utf8').decode('ascii', 'ignore')
                        csv_writer.writerow(line)


class goal_file():
    def __init__(self,archivo_excel,archivo,clave,subject_name):
        self.archivo = archivo
        self.archivo_excel = archivo_excel
        self.clave = clave
        self.subject_name = subject_name
    def change_cell(self):
        with open(self.archivo, 'rb') as rawdata:
            result = chardet.detect(rawdata.read(100000))
        df = pd.read_csv(self.archivo,encoding=result['encoding'])
        try:
            df['Clave'] = df['Clave'].astype(str).apply(lambda x:x[:4])
        except:pass
        df = df[df['Clave'] == self.clave]
        #df_calificacion = df['Calificacion'].apply(lambda x: x.split("/")[0]).astype(float)
        df_calificacion = df['Calificacion'].astype(float)
        df_valor = df['Valor'].astype(float)
        df_ponderacion = ((df_calificacion*df_valor)/10)

        ## Se hace la suma de las calificaciones
        resultados = dict()
        acumulado = df_ponderacion.sum()*10
        resultados['acumulado'] = round(acumulado,2)
        #resultados['max_grade'] = round(max_grade,2)
        print(resultados)

        ## Enviando la suma de calificaciones al libro de excel
        wb = load_workbook(filename=self.archivo_excel,read_only=False,keep_vba=True)
        ws = wb['Hoja1']
        ws['a2'] = self.subject_name
        ws['b2'] = int(self.clave)
        ws['d2'] = resultados['acumulado']
        wb.save(self.archivo_excel)
        app = xw.App(visible=False)
        wb = xw.Book('assests/materia_dashboard_material/meta.xlsm')
        macro1 = wb.macro('modulo.progress')
        macro1()
        wb.save()
        wb.app.quit()
        return resultados


#archivo = r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\suayedApp\assests\BD\semestres_materias.csv'
#archiv = r'C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\suayedApp\assests\materia_dashboard_material\meta.xlsm'
#goal_file(archiv,archivo,'1343','COMPORTAMIENTO EN LAS ORGANIZACIONES').change_cell()

# obtener_materias(archivo).lista_semester()
# obtener_materias(archivo).define_semester('Semestre 22-2',
# r"C:\Users\ivan_\OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO\Desktop\repositorios\suayedApp\assests\BD/semestres_materias.csv")

# print(obtener_materias(archivo).dias_con_pendientes('05'))
# obtener_materias(archivo).actualizar_estados()
# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').definir_lista('TwoLineRightIconListItem')
# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').total_actividades('PRINCIPIOS Y TECNICAS DE LA INVESTIGACION')

# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').actualizar_DB('COSTOS','Unidad 5 / Actividad complementaria 1 /')

# print(obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').subject_actividades('ÉTICA EN LAS ORGANIZACIONES'))

# print(obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').total_actividades("COSTOS"))

# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').define_activity('actividad1')

# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').obtener_activity_name()

# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.xlsx').hjh()


# print(estatus_feedback(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv','PRINCIPIOS Y TECNICAS DE LA INVESTIGACION','U1_Act_aprend_5').resultados())

# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').define_subject('actividad1')

# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').obtener_materia_clave('COSTOS')


# activi = ['Unidad 1 / Actividad complementaria 1 /', 'Unidad 2 / Actividad complementaria 1 /', 'Unidad 2 / Cuestionario de reforzamiento /', 'Unidad 3 / Actividad complementaria 1 /', 'Unidad 4 / Cuestionario de reforzamiento /', 'Unidad 4 / Actividad complementaria 1/', 'Unidad 5 / Actividad complementaria 1 /', 'Unidad 6 / Cuestionario de reforzamiento /', 'Unidad 6 / Actividad complementaria 1 /', 'Unidad 7 / Cuestionario de reforzamiento /', 'Unidad 8 / Actividad complementaria 1 /', 'Unidad 1 / Cuestionario de reforzamiento /', 'Unidad 1 / Actividad complementaria 1 /']

#
# vaciar_feedback(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias-copia.csv','COMPORTAMIENTO EN LAS ORGANIZACIONES',retro).vaciar_resultados()

# btener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').define_activity('fefef')


# obtener_materias(r'C:\Python310\PycharmProjects\kivyGUI\virt\KivyMDNavDrawerAndScreenManager\assests\BD\materias.csv').total_actividades('DESARROLLO SUSTENTABLE Y LAS ORGANIZACIONES')
