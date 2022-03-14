import datetime
import mysql.connector
import config as cfg

traducciones = {
    'Monday': 'L',
    'Tuesday': 'M',
    'Wednesday': 'I',
    'Thursday': 'J',
    'Friday': 'V',
    'Saturday': 'S',
    'Sunday': 'D',
}

datos_prueba = {
    'L': {'5:00': [1,2],'4:00': [3,4], '8:00': [5,6]}
}

def consultar_usuarios(fecha_actual):
    """Esta función nos permitirá consultar la base de datos de usuarios"""
    dia = fecha_actual.strftime("%A")
    hora = fecha_actual.hour
    if traducciones[dia] in datos_prueba:
        print(datos_prueba[traducciones[dia]])
    else:
        print("Nada programado para hoy")
    pass

def main():
    cnx = mysql.connector.connect(**cfg.mysql)
    cnx.close()
    """Esta función checará si existe alguna notificación que se tiene que mandar"""
    consultar_usuarios(datetime.datetime.now())

if __name__ == "__main__":
    main()