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
columnas = ['jugador', 'posicion', 'nacimiento', 'nacionalidad', 'estatura', 'pie', 'fecha_union', 'club_anterior', 'contrato']

# Crear el DataFrame vacío
df = pd.DataFrame(columns=columnas)

# Recorrer cada fila de la tabla
for table in tablas_jugadores:
    rows = table.find_all('tr')[1:]  # Omitir el encabezado
    for row in rows:
        # Nombre del jugador
        nombre_element = row.find('a')
        jugador = nombre_element.text.strip() if nombre_element else 'N/A'

        # Verificar si el jugador ya está en el DataFrame
        if df['jugador'].str.contains(jugador).any():
            continue  # Saltar a la siguiente iteración si el jugador ya existe

        # Tabla anidada para la posición
        nested_table = row.find('table', class_='inline-table')
        if nested_table:
            nested_rows = nested_table.find_all('tr')
            posicion = nested_rows[1].find('td').text.strip() if len(nested_rows) > 1 and nested_rows[1].find('td') else 'N/A'
        else:
            posicion = 'N/A'

        # Nacimiento
        nacimiento = row.find_all('td', class_='zentriert')[1].text.strip() if len(row.find_all('td', class_='zentriert')) > 1 else 'N/A'

        # Nacionalidad
        img = row.find('img', class_='flaggenrahmen')
        nacionalidad = img['title'] if img else 'N/A'

        # Datos adicionales en la fila principal
        cols = row.find_all('td', class_='zentriert')
        estatura = cols[3].text.strip() if len(cols) > 3 else 'N/A'
        pie = cols[4].text.strip() if len(cols) > 4 else 'N/A'
        fecha_union = cols[5].text.strip() if len(cols) > 5 else 'N/A'
        #club_anterior = cols[6].text.strip() if len(cols) > 6 else 'N/A'
        contrato = cols[7].text.strip() if len(cols) > 7 else 'N/A'

        # Club anterior
        img = row.find('img', class_='')
        club_anterior = img['title'] if img else 'N/A'

        # Añadir los datos al DataFrame
        df = df._append({
            'jugador': jugador,
            'posicion': posicion,
            'nacimiento': nacimiento,
            'nacionalidad': nacionalidad,
            'estatura': estatura,
            'pie': pie,
            'fecha_union': fecha_union,
            'club_anterior': club_anterior,
            'contrato': contrato,
        }, ignore_index=True)

# Guardar los datos en un archivo Excel
df.to_excel('players.xlsx', index=False)

print("Datos guardados en 'players.xlsx'")
