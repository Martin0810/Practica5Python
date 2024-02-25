import pandas as pd

# Leer el archivo CSV
df_airbnb = pd.read_csv("./airbnb.csv")

# Filtrar según los criterios de Diana
filtered_df = df_airbnb[(df_airbnb['accommodates'] >= 1) & 
                        (df_airbnb['price'] <= 50) & 
                        (df_airbnb['room_type'] == 'Shared room')]

# Ordenar por precio y puntuación
sorted_df = filtered_df.sort_values(by=['price', 'overall_satisfaction'], ascending=[True, False])

# Seleccionar las 10 opciones más baratas
top_10_options = sorted_df.head(10)

# Mostrar las opciones a Diana
print("Las 10 opciones más baratas para Diana son:")
print(top_10_options[['room_id', 'room_type', 'neighborhood', 'reviews', 'overall_satisfaction', 'accommodates', 'bedrooms', 'price']])