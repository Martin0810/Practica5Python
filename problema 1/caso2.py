# se necesitara ejecutar pip install openpyxl

import pandas as pd

# Leer el archivo CSV
df_airbnb = pd.read_csv("./airbnb.csv")

# Filtrar propiedades de Roberto y Clara
roberto_clara_df = df_airbnb[df_airbnb['room_id'].isin([97503, 90387])]

# Guardar el dataframe en un archivo Excel
roberto_clara_df.to_excel("roberto.xlsx", index=False)

# Mostrar el dataframe resultante
print("Dataframe con propiedades de Roberto y Clara:")
print(roberto_clara_df[['room_id', 'host_id', 'room_type', 'neighborhood', 'reviews', 'overall_satisfaction', 'accommodates', 'bedrooms', 'price']])