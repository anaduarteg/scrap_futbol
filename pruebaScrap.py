import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL del equipo en Transfermarkt
url = 'https://www.transfermarkt.com/club-cerro-porteno/kader/verein/1214/saison_id/2023/plus/1'

# Encabezados para simular un navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

# Realizar la solicitud GET a la página web con el User-Agent modificado
try:
    r = requests.get(url, headers=headers)
    r.raise_for_status()  # Verificar si la solicitud fue exitosa
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

# Pausar para evitar ser bloqueado
time.sleep(2)

# Parsear el contenido HTML
html_soup = BeautifulSoup(r.text, 'html.parser')

# Encontrar la tabla correcta
tablas_jugadores = html_soup.find_all('table', class_="items")

# Definir las columnas del DataFrame
columnas = ['jugador', 'posicion', 'nacimiento', 'nacionalidad', 'estatura', 'pie', 'unido', 'firmado', 'contrato', 'valor']

# Crear el DataFrame vacío
df = pd.DataFrame(columns=columnas)

# Recorrer cada fila de la tabla
for table in tablas_jugadores:
    for row in table.find_all('tr')[1:]:
        jugador = row.find('a').text.strip() if row.find('a') else 'N/A'
        posicion = row.find('td').text.strip() if row.find('td') else 'N/A'
        nacimiento = row.find_all('td', class_='zentriert')[1].text.strip() if len(row.find_all('td', class_='zentriert')) > 1 else 'N/A'
        nacionalidad = row.find('img', class_='flaggenrahmen')['title'] if row.find('img', class_='flaggenrahmen') else 'N/A'
        estatura = row.find_all('td', class_='zentriert')[2].text.strip() if len(row.find_all('td', class_='zentriert')) > 2 else 'N/A'
        pie = row.find_all('td', class_='zentriert')[4].text.strip() if len(row.find_all('td', class_='zentriert')) > 4 else 'N/A'
        unido = row.find_all('td', class_='zentriert')[5].text.strip() if len(row.find_all('td', class_='zentriert')) > 5 else 'N/A'
        firmado = row.find_all('td', class_='zentriert')[4].text.strip() if len(row.find_all('td', class_='zentriert')) > 4 else 'N/A'
        contrato = row.find_all('td', class_='zentriert')[5].text.strip() if len(row.find_all('td', class_='zentriert')) > 5 else 'N/A'
        valor = row.find('td', class_='rechts').text.strip() if row.find('td', class_='rechts') else 'N/A'

        # Añadir los datos al DataFrame
        df = df._append({
            'jugador': jugador,
            'posicion': posicion,
            'nacimiento': nacimiento,
            'nacionalidad': nacionalidad,
            'estatura': estatura,
            'pie': pie,
            'unido': unido,
            'firmado': firmado,
            'contrato': contrato,
            'valor': valor
        }, ignore_index=True)

# Guardar los datos en un archivo Excel
df.to_excel('prueba_players.xlsx', index=False)

print("Datos guardados en 'prueba_players.xlsx'")
