import datetime
import mysql.connector
from mysql.connector import errorcode
import config as cfg
import sys
import requests

traducciones = {
    'Monday': 'L',  
    'Tuesday': 'M',
    'Wednesday': 'I',
    'Thursday': 'J',
    'Friday': 'V',
    'Saturday': 'S',
    'Sunday': 'D',
}

def enviar_notificacion(codigo_usuario, nombre_programa):
    """Esta función se encargará de enviar la notificación al usuario"""

    url = "https://onesignal.com/api/v1/notifications"
    carga = {
	"app_id": "51c63cff-c83b-405e-927b-a9ce3234ec65",
	"include_player_ids": [codigo_usuario],
	"contents": {"en": f"The program {nombre_programa} will start in an hour", "es": f"El programa {nombre_programa} comenzará en una hora"},
	"headings": {"en": "Program Notification", "es": "Notificación de Programa"}
    }
    respuesta = requests.post(url, headers={"Content-Type": "application/json; charset=utf-8", "Authorization": "Basic YTQzM2RiOTQtYzUxYy00MTlmLWE3NTQtODhiYWJiYmFhYTBm"}, json=carga)
    if(respuesta.status_code != 200):
        print(f"Error al enviar notificación al usuario: {codigo_usuario}")

def consultar_notificaciones(fecha_actual, cnx):
    """Esta función checará si existe alguna notificación que se tiene que mandar"""
    
    comando = ("SELECT codigo_usuario, nombre_programa FROM radiocucei.notificaciones WHERE horario = %s AND dia = %s")
    cursor = cnx.cursor()
    dia = traducciones[fecha_actual.strftime("%A")]
    hora = (fecha_actual + datetime.timedelta(hours=1)).hour
    valores = (f"{'0' if hora < 10 else ''}{hora}:00", dia)
    cursor.execute(comando, valores)
    for (codigo, nombre_programa) in cursor:
        enviar_notificacion(codigo, nombre_programa)

def main():
    try:
        cnx = mysql.connector.connect(**cfg.mysql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            sys.exit(1)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            sys.exit(1)
        else:
            print(err)
            sys.exit(1)
    consultar_notificaciones(datetime.datetime.now(), cnx)
    cnx.close()
    sys.exit(0)

if __name__ == "__main__":
    main()