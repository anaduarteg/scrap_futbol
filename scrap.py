import requests
from bs4 import BeautifulSoup
import pandas as pd 

url = 'https://www.transfermarkt.com/club-cerro-porteno/kader/verein/1214/saison_id/2023/plus/1'

r = requests.get(url)
html_contents = r.text

html_soup = BeautifulSoup(html_contents, 'html.parser')

tablas_jugadores = html_soup.find_all('table',
                                      class_="inline-table")

columnas = ['jugador','posicion','nacimiento','edad',
            'nacionalidad','estatura','pie','unido','firmado',
            'contrato','valor']

df = pd.DataFrame(columns=columnas)

for table in tablas_jugadores:
    for row in table.find_all('tr')[1:]:
        values = []
        for col in row.find_all(['th','td']):
            values.append(col.text)
        if len(values) == len (columnas):
            df.loc[len(df)] = values

# Guardar los datos en un archivo Excel
df.to_excel('players.xlsx', index=False)

print("Datos guardados en 'players.xlsx'")