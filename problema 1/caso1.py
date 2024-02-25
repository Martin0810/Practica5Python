import pandas as pd

# Leer el archivo CSV
df_airbnb = pd.read_csv("./airbnb.csv")

# Filtrar según los criterios de Alicia
filtered_df = df_airbnb[(df_airbnb['accommodates'] >= 4) & 
                        (df_airbnb['bedrooms'] >= 2) & 
                        (df_airbnb['reviews'] > 10) & 
                        (df_airbnb['overall_satisfaction'] > 4)]

# Ordenar por puntuación y número de críticas
sorted_df = filtered_df.sort_values(by=['overall_satisfaction', 'reviews'], ascending=[False, False])

# Seleccionar las 3 mejores opciones
top_3_options = sorted_df.head(3)

# Mostrar las opciones a Alicia
print("Las 3 mejores opciones para Alicia son:")
print(top_3_options[['room_id', 'room_type', 'neighborhood', 'reviews', 'overall_satisfaction', 'accommodates', 'bedrooms', 'price']])