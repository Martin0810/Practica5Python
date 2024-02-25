#pip install pyarrow

import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('./winemag-data-130k-v2.csv')

# Renombrar columnas
df.rename(columns={'Unnamed: 0': 'id', 'designation': 'vineyard', 'region_1': 'region', 'region_2': 'subregion'}, inplace=True)

# Crear nuevas columnas
df['points_category'] = pd.cut(df['points'], bins=[0, 85, 90, 95, 100], labels=['Bajo', 'Normal', 'Bueno', 'Excelente'])
df['price_category'] = pd.cut(df['price'], bins=[0, 20, 50, 100, float('inf')], labels=['Económico', 'Moderado', 'Caro', 'Muy caro'])
df['review_to_points_ratio'] = df['points'] / df['price']

# Reporte 1: Promedio de puntos por país
avg_points_by_country = df.groupby('country')['points'].mean().sort_values(ascending=False).reset_index()

# Reporte 2: Cantidad de vinos por variedad
wine_count_by_variety = df.groupby('variety').size().sort_values(ascending=False).reset_index(name='wine_count')

# Reporte 3: Promedio de precio por región
avg_price_by_region = df.groupby('region')['price'].mean().sort_values(ascending=False).reset_index()

# Reporte 4: Vinos más caros por país
most_expensive_wines_by_country = df.loc[df.groupby('country')['price'].idxmax()][['country', 'title', 'price']]

# Guardar el reporte 4 en un archivo CSV
most_expensive_wines_by_country.to_csv('most_expensive_wines_by_country.csv', index=False)

# Mostrar los reportes
print("Reporte 1: Promedio de puntos por país")
print(avg_points_by_country.head())

print("\nReporte 2: Cantidad de vinos por variedad")
print(wine_count_by_variety.head())

print("\nReporte 3: Promedio de precio por región")
print(avg_price_by_region.head())

print("\nReporte 4: Vinos más caros por país")
print(most_expensive_wines_by_country.head())