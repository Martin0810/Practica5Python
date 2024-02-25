from procesamiento import limpiar_columnas, dolarizar_valores, transformar_estado, generar_reporte_ubigeos, generar_reporte_region
from envio_correo import enviar_correo
import pandas as pd

if __name__ == "__main__":
    # Leer el archivo reactiva.xlsx
    df_reactiva = pd.read_excel('reactiva.xlsx')
    
    # Aplicar funciones de procesamiento
    df_reactiva = limpiar_columnas(df_reactiva)
    df_reactiva = dolarizar_valores(df_reactiva)
    df_reactiva = transformar_estado(df_reactiva)
    
    # Generar reportes
    ubigeos_df = generar_reporte_ubigeos(df_reactiva)
    generar_reporte_region(df_reactiva)
    
    # Enviar correo con un reporte adjunto
    enviar_correo('Reporte Reactiva', 'Adjunto encontrarás los reportes', 'destinatario@example.com', 'Top5_Lima_Urbano.xlsx')