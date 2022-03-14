import datetime
import mysql.connector
from mysql.connector import errorcode
import config as cfg
import sys

traducciones = {
    'Monday': 'L',  
    'Tuesday': 'M',
    'Wednesday': 'I',
    'Thursday': 'J',
    'Friday': 'V',
    'Saturday': 'S',
    'Sunday': 'D',
}

def consultar_notificaciones(fecha_actual, cnx):
    """Esta función checará si existe alguna notificación que se tiene que mandar"""
    
    comando = ("SELECT codigo_usuario, nombre_programa FROM radiocucei.notificaciones WHERE horario = %s AND dia = %s")
    cursor = cnx.cursor()
    dia = traducciones[fecha_actual.strftime("%A")]
    hora = fecha_actual.hour
    valores = (hora, dia)
    cursor.execute(comando, valores)
    for (codigo, nombre_programa) in cursor:
        print(f'Mandar el programa {nombre_programa} al usuario {codigo}')

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