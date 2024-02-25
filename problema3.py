import pandas as pd
import requests
from bs4 import BeautifulSoup

def limpiar_columnas(df):
    df.columns = df.columns.str.lower().str.replace(' ', '').str.replace('[^\w\s]', '').str.normalize('NFKD').str.encode('ascii', 'ignore').str.decode('utf-8')

    df = df.loc[:, ~df.columns.duplicated()]

    if 'dispositivo_legal' in df.columns:

        df['dispositivo_legal'] = df['dispositivo_legal'].replace({',': ''}, regex=True)

    return df

def obtener_tipo_cambio():
    #https://api.apis.net.pe/v1/tipo-cambio-sunat
    url = 'https://api.apis.net.pe/v1/tipo-cambio-sunat'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Acceder a la clave 'compra' como valor del tipo de cambio
        tipo_cambio = data.get('compra', None)

        if tipo_cambio is not None:
            return tipo_cambio
        else:
            print("La clave 'compra' no está presente en el JSON.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el tipo de cambio: {e}")
        return None

def dolarizar_montos(df):
    # Obtener el tipo de cambio actual del dólar
    tipo_cambio = obtener_tipo_cambio()

    if tipo_cambio is not None:
        # Dolarizar los valores de las columnas 'monto_inversion' y 'monto_transferencia'
        df['monto_inversion_dolar'] = df['monto_inversion'] / tipo_cambio
        df['monto_transferencia_dolar'] = df['monto_transferencia'] / tipo_cambio

    return df

def transformar_estado(df):
    # Cambiar valores de la columna 'estado'
    df['estado'] = df['estado'].replace({'ActosPrevios': 1, 'Resuelto': 0, 'Ejecucion': 2, 'Concluido': 3})

    return df

def almacenar_ubigeos(df):
    # Crear una tabla de ubigeos sin duplicados
    ubigeos_df = df[['ubigeo', 'region', 'provincia', 'distrito']].drop_duplicates()

    # Almacenar en un archivo CSV
    ubigeos_df.to_csv('ubigeos.csv', index=False)

def generar_reportes_por_region(df):
    # Generar CSV con el top 5 de costo de inversión para cada región y tipo de obra

    # Suponga que la columna 'tipo_obra' indica el tipo de obra
    # y la columna 'estado' indica el estado (1, 2, 3)
    for region, region_data in df.groupby('region'):
        for tipo_obra, tipo_obra_data in region_data.groupby('tipo_obra'):
            for estado in [1, 2, 3]:
                # Cree un CSV con el top 5 de costo de inversión
                file_name = f'{region}_{tipo_obra}_estado_{estado}_top5.csv'
                tipo_obra_data[tipo_obra_data['estado'] == estado].nlargest(5, 'costo_inversion').to_csv(file_name, index=False)

def enviar_correo(asunto, cuerpo, archivos_adjuntos):
    # Implemente la lógica para enviar el correo con los reportes generados
    # Utilice solo las bibliotecas requests para enviar correo si es posible

    # Ejemplo de envío de correo a través de una API ficticia
    url = 'https://api.example.com/enviar_correo'
    data = {'asunto': asunto, 'cuerpo': cuerpo, 'archivos_adjuntos': archivos_adjuntos}
    response = requests.post(url, json=data)

    # Verifique la respuesta para confirmar que el correo se envió con éxito
    if response.status_code == 200:
        print("Correo enviado con éxito.")
    else:
        print(f"Error al enviar correo. Código de estado: {response.status_code}")

# Cargar el archivo reactiva.xlsx
df = pd.read_excel('./reactiva.xlsx')

# Llamar a las funciones en orden
df = limpiar_columnas(df)
df = dolarizar_montos(df)
df = transformar_estado(df)
almacenar_ubigeos(df)
generar_reportes_por_region(df)
enviar_correo()
