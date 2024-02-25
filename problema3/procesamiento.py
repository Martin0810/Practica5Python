import pandas as pd
import requests

def limpiar_columnas(df):
    # Renombrar columnas eliminando espacios, tildes y convirtiendo a minúsculas
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    
    # Eliminar columna ID y TipoMoneda duplicadas
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Eliminar comas de la columna "DISPOSITIVO LEGAL"
    df['dispositivo_legal'] = df['dispositivo_legal'].replace({',': ''}, regex=True)
    
    return df

def dolarizar_valores(df):
    # Obtener valor actual del dólar desde la API de sunat en la pc4
    # Supongamos que la API de sunat devuelve el valor en la variable 'valor_dolar'
    valor_dolar = requests.get('https://api.sunat.com/dolar').json()['valor']

    # Dolarizar montos de inversión y transferencia en nuevas columnas
    df['monto_inversion_usd'] = df['monto_inversion'] / valor_dolar
    df['monto_transferencia_usd'] = df['monto_transferencia'] / valor_dolar
    
    return df

def transformar_estado(df):
    # Cambiar valores de la columna "Estado"
    df['estado'] = df['estado'].replace({
        'ActosPrevios': 1,
        'Resuelto': 0,
        'Ejecucion': 2,
        'Concluido': 3
    })
    
    return df

def generar_reporte_ubigeos(df):
    # Crear tabla de ubigeos sin duplicados
    ubigeos_df = df[['ubigeo', 'region', 'provincia', 'distrito']].drop_duplicates()
    
    # Almacenar en una base de datos
    # Puedes usar SQLAlchemy u otra biblioteca para esto
    
    return ubigeos_df

def generar_reporte_region(df):
    # Generar reportes por región
    regiones = df['region'].unique()
    
    for region in regiones:
        region_df = df[df['region'] == region]
        
        # Filtrar por tipo Urbano y estado 1, 2, 3
        urbano_df = region_df[(region_df['tipo'] == 'Urbano') & (region_df['estado'].isin([1, 2, 3]))]
        
        # Obtener top 5 de costo inversión
        top5_inversion = urbano_df.nlargest(5, 'monto_inversion')
        
        # Generar Excel para cada región
        top5_inversion.to_excel(f'Top5_{region}_Urbano.xlsx', index=False)



if __name__ == "__main__":
    # Leer el archivo reactiva.xlsx
    df_reactiva = pd.read_excel('reactiva.xlsx')
   
    # Aplicar funciones de procesamiento
    df_reactiva = limpiar_columnas(df_reactiva)
    df_reactiva = dolarizar_valores(df_reactiva)
    df_reactiva = transformar_estado(df_reactiva)

    generar_reporte_ubigeos(df_reactiva)
    generar_reporte_region(df_reactiva)