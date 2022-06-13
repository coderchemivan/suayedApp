# #Inicio proyecto 27/05/22
#
#
#
# from time import sleep
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# import mysql.connector
#
#
#
# class Feedback():
#     def __init__(self,materias,driver):
#         self.materias = materias
#         self.driver = driver
#
#
#         #Abriendo la página
#         self.driver.get("https://administracion.suayed.fca.unam.mx/login/index.php")
#
#
#
#         # Logeo en la página
#         user_input = self.driver.find_element(By.ID, "username")
#         password_input = self.driver.find_element(By.ID, "password")
#         sleep(2.0)
#         user_input.send_keys("421157110")
#         password_input.send_keys("16091997")
#         password_input.send_keys(Keys.ENTER)
#
#         try:
#             menu_btn = self.driver.find_element(By.XPATH, '//button[@aria-expanded="false"]').click()
#         except:
#             None
#
#     def extraccion_feedback(self):
#         for materia in self.materias:
#
#             try:
#                 menu_btn = self.driver.find_element(By.XPATH, '//button[@aria-expanded="false"]').click()
#             except:
#                 None
#
#             # Seleccionando la materia
#             conn = mysql.connector.connect(user="root", password="123456",
#                                            host="localhost",
#                                            database="fca_materias",
#                                            port='3306'
#                                            )
#
#             cur = conn.cursor()
#             select_subjet_activities= "SELECT Actividad FROM materias_actividades WHERE Clave = " + materia
#             cur.execute(select_subjet_activities)
#             actividades_materia = cur.fetchall()
#
#
#             actividades,= list(zip(*actividades_materia))
#
#             print({materia:actividades})
#             #subject = self.driver.find_element(By.XPATH, '//*[contains(text(),"' + materia + '")]').click()
#
#             subject = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"' + materia + '")]'))
#
#             )
#
#             subject = self.driver.find_element(By.XPATH, '//*[contains(text(),"' + materia + '")]').click()
#
#             for i in range(len(actividades)):
#
#
#                 subject_content = WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_element_located((By.ID, 'region-main'))
#
#                 )
#
#
#                 status_calificacion =  "SELECT Calificada FROM materias_actividades " \
#                                        "WHERE Clave ='"+materia+"' AND Actividad = '" + actividades[i] + "'"
#                 cur.execute(status_calificacion)
#                 status_calificacion = cur.fetchall()
#                 status_calificacion, = list(zip(*status_calificacion))
#                 status_calificacion = status_calificacion[0]
#
#                 if status_calificacion == 'Y':
#                     continue
#
#                 # Abriendo la actividad
#                 try:
#                     actividad = self.driver.find_element(By.XPATH,
#                                                          './/span[contains(text(),"' + actividades[i] + '")]').click()
#                 except:
#                     continue
#
#
#                 # Obteniendo calificación y fecha de calificación de la actividad
#                 try:
#                     feedback_content = self.driver.find_elements_by_xpath('.//td[@class="cell c1 lastcol"]')
#                     calificacion = feedback_content[4].text
#                     calificado_en = feedback_content[5].text
#
#
#                     update_fecha_calificacion = "UPDATE materias_actividades SET Calificado_en = '" + calificado_en + \
#                                                 "' WHERE Clave ='"+materia+"' AND Actividad = '" + actividades[i] + "'"
#
#                     update_calificacion = "UPDATE materias_actividades SET Calificación ='" + calificacion +  \
#                                           "' WHERE Clave ='"+materia+"' AND Actividad = '" + actividades[i] + "'"
#
#                     update_calificacion_status = "UPDATE materias_actividades SET Calificada ='Y' " \
#                                                  "WHERE Clave ='" + materia + "' AND Actividad = '" + actividades[i] + "'"
#
#                     conn.commit()
#
#
#                     cur.execute(update_fecha_calificacion)
#                     cur.execute(update_calificacion)
#                     cur.execute(update_calificacion_status)
#                     actividades_materia = cur.fetchall()
#                 except:
#                     None
#
#                 # Obteniendo comentarios de la actividad
#                 try:
#                     btn_show_more = self.driver.find_element(By.XPATH,
#                                                              '//*[contains(@class,"expandsummaryicon expand")]').click()  # btn_show_more = driver.find_element(By.XPATH,'//*[@class="expandsummaryicon expand_assignfeedback_comments_386697"]')
#                     comentarios = self.driver.find_elements_by_xpath(
#                         '//*[contains(@class,"box py-3 boxaligncenter full_assignfeedback_comments")]/p')
#
#                     feedback = ""
#                     for comentario in comentarios:
#                         feedback += ' ' + comentario.text
#                         # print(comentario.text)
#                     # print(feedback)
#                     update_comments = "UPDATE materias_actividades SET Comentario = '" + feedback + \
#                                       "' WHERE Clave ='" + materia + "' AND Actividad = '" + actividades[i] + "'"
#                     cur.execute(update_comments)
#                 except:
#                     None
#
#                 conn.commit()
#                 #print(calificacion, calificado_en, feedback)
#                 self.driver.back()
#             self.driver.back()
#         self.driver.quit()
#
#
#         conn.close()
#
# opts = Options()
# opts.add_argument(
#              "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
#
# driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver.exe', options=opts)
# prueba1 = Feedback(['1533'],driver)
# prueba1.extraccion_feedback()







