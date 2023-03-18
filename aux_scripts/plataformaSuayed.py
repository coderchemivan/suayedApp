#Inicio proyecto 27/05/22


from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import mysql.connector
import datetime
from aux_scripts.info_materias import DB_admin



class Feedback():
    def __init__(self,materias,actividades,driver):
        self.materias = materias
        self.actividades = actividades
        self.driver = driver


        #Abriendo la página
        self.driver.get("https://administracion.suayed.fca.unam.mx/login/index.php")



        # Logeo en la página
        user_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        sleep(2.0)
        user_input.send_keys("421157110")
        password_input.send_keys("16091997")
        password_input.send_keys(Keys.ENTER)

        try:
            menu_btn = self.driver.find_element(By.XPATH, '//button[@aria-expanded="false"]').click()
        except:
            pass

    def extraccion_feedback(self):
        # Seleccionando la materia
        actividad_feedback = dict()
        conn = mysql.connector.connect(user="root", password="123456",
                                       host="localhost",
                                       database="fca_materias",
                                       port='3306'
                                       )
        for materia in self.materias:

            try:
                menu_btn = self.driver.find_element(By.XPATH, '//button[@aria-expanded="false"]').click()
            except:
                pass



            cur = conn.cursor()
            #select_subjet_activities= "SELECT name FROM actividades WHERE clave_materia = " + materia
            #cur.execute(select_subjet_activities)
            #actividades_materia = cur.fetchall()


            #actividades,= list(zip(*actividades_materia))

            #print({materia:actividades})
            #subject = self.driver.find_element(By.XPATH, '//*[contains(text(),"' + materia + '")]').click()

            subject = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"' + materia + '")]'))

            )

            subject = self.driver.find_element(By.XPATH, '//*[contains(text(),"' + materia + '")]').click()


            for activity in self.actividades:
                subject_content = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'region-main'))

                )


                status_calificacion =  "SELECT cal_status FROM actividades " \
                                       "WHERE clave_materia ="+materia+" AND name = '" + str(activity) + "'"

                cur.execute(status_calificacion)
                status_calificacion = cur.fetchall()
                status_calificacion, = list(zip(*status_calificacion))
                status_calificacion = status_calificacion[0]
                
                if status_calificacion == 3:
                    continue

                # Abriendo la actividad
                try:
                    actividad = DB_admin().decode_activity(activity,abbrv=False)
                    actividad = self.driver.find_element(By.XPATH,
                                                         './/span[contains(text(),"' + actividad + '")]').click()
                except:
                    try:
                        actividad = self.driver.find_element(By.XPATH,
                                                            './/span[contains(text(),"' + actividad.replace('//','/') + '")]').click()
                    except:
                        print(actividad)
                        continue


                try:
                    #status de la entrega
                    fecha_entregada = None
                    entrega_status_contendor = self.driver.find_elements(By.XPATH, "//*[@class='submissionstatustable']//*[@class='cell c1 lastcol']")
                    index = 0
                    for status in entrega_status_contendor:
                        if entrega_status_contendor[index].text.startswith("Monday") or entrega_status_contendor[index].text.startswith("Tuesday") or entrega_status_contendor[index].text.startswith("Wednesday") or entrega_status_contendor[index].text.startswith("Thursday") or entrega_status_contendor[index].text.startswith("Friday") or entrega_status_contendor[index].text.startswith("Saturday") or entrega_status_contendor[index].text.startswith("Sunday"):
                            fecha_entregada = entrega_status_contendor[index].text
                            break
                        index += 1
                    fecha_entregada = tranformData.transform_date(fecha_entregada)         
                    fecha_entrega = cur.execute("SELECT fecha_entrega FROM actividades WHERE clave_materia ="+materia+" AND name = '" + str(activity) + "'")
                    fecha_entrega = cur.fetchall()
                    fecha_entrega, = list(zip(*fecha_entrega))
                    fecha_entrega = fecha_entrega[0]
                    
                    if fecha_entregada != None:
                        update_fecha_entregada = "UPDATE actividades SET entregada_el = '" + fecha_entregada + \
                                                    "' WHERE clave_materia = " + materia + " AND name = '" + str(activity) + "'" 
                        #transformando fecha_entregada de str a datetime
                        fecha_entregada = datetime.datetime.strptime(fecha_entregada, '%Y-%m-%d')
                        fecha_entrega = datetime.datetime.strptime(fecha_entrega, '%Y-%m-%d')
                    if fecha_entregada!= None and fecha_entregada > fecha_entrega:
                        update_status = 'Entregada con atraso'
                        update_act_status = "UPDATE actividades SET status =" + '"'+update_status+ '"'+ "WHERE clave_materia = " + materia + " AND name = '" + str(activity) + "'"    
                    elif fecha_entregada!= None and fecha_entregada <= fecha_entrega:
                        update_status = 'Entregada a tiempo'
                        update_act_status = "UPDATE actividades SET status =" + '"'+update_status+ '"'+ "WHERE clave_materia = " + materia + " AND name = '" + str(activity) + "'"  
                        cur.execute(update_act_status)  
                    

                    #feedback
                    feedback_content = self.driver.find_elements(By.XPATH, './/div[@class="feedback"]//td')   
                    calificacion = ""
                    calificado_en= ""
                    if len(feedback_content) > 0:
                        calificacion = feedback_content[0].text.split("/")[0].strip()
                        calificado_en = feedback_content[1].text
                        calificado_en =tranformData.transform_date(calificado_en)
                    
                        update_fecha_calificacion = "UPDATE actividades SET calificada_en = '" + calificado_en + \
                                                    "' WHERE clave_materia ="+materia+" AND name = '" + str(activity) + "'"

                        update_calificacion = "UPDATE actividades SET calificacion =" + calificacion +  \
                                                " WHERE clave_materia ="+materia+" AND name = '" + str(activity) + "'"

                        update_calificacion_status = "UPDATE actividades SET cal_status = 1 " \
                                                        "WHERE clave_materia =" + materia + " AND name = '" + str(activity) + "'"
                        cur.execute(update_calificacion_status)
                        cur.execute(update_fecha_calificacion)
                        cur.execute(update_calificacion)

                    cur.execute(update_fecha_entregada) if fecha_entregada != None else None


                    actividades_materia = cur.fetchall()


                # Obteniendo comentarios de la actividad
                    feedback = ""
                    try:
                        btn_show_more = self.driver.find_element(By.XPATH,
                                                                '//*[contains(@class,"expandsummaryicon expand")]').click()  # btn_show_more = driver.find_element(By.XPATH,'//*[@class="expandsummaryicon expand_assignfeedback_comments_386697"]')
                        comentarios = self.driver.find_elements(By.XPATH,
                            '//*[contains(@class,"box py-3 boxaligncenter full_assignfeedback_comments")]/p')

                    except:
                        comentarios = self.driver.find_elements(By.XPATH,
                            '//*[contains(@class,"assignfeedback_comments")]/p')


                    for comentario in comentarios:
                        feedback += ' ' + comentario.text

                    if feedback =="":
                        feedback = 'Sin comentarios'
                    update_comentarios = "UPDATE actividades SET comentarios ='" + feedback + \
                                        "' WHERE clave_materia =" + materia + " AND name = '" + str(activity) + "'"

                    cur.execute(update_comentarios)
                    conn.commit()
                    actividad_feedback[activity] = [calificacion, calificado_en, feedback]
                    
                except Exception as e:
                    print(e)
                    pass
                self.driver.back()
            self.driver.back()
        self.driver.quit()
        conn.close()
        return actividad_feedback


class tranformData():
    def __init__(self):pass

    def transform_date(date):
        try:
            date = date.split(",")
            date = date[1].split("de")
            dia = date[0].strip() if len(date[0].strip()) == 2 else "0"+date[0].strip()
            date = date[2].strip()  + "-" + date[1].strip() + "-" +  dia
            #reemplazar los nombres de los meses por numeros
            date = date.replace("January", "01")
            date = date.replace("February", "02")
            date = date.replace("March", "03")
            date = date.replace("April", "04")
            date = date.replace("May", "05")
            date = date.replace("June", "06")
            date = date.replace("July", "07")
            date = date.replace("August", "08")
            date = date.replace("September", "09")
            date = date.replace("October", "10")
            date = date.replace("November", "11")
            date = date.replace("December", "12")
        except:
            date = None
        return date



