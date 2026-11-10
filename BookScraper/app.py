
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from flask import Flask, render_template_string

app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN
# ==========================================

URL_CATALOGO = "https://books.toscrape.com/"
CARPETA = Path(__file__).resolve().parent
ARCHIVO_HTML = CARPETA / "pagina_libros.html"
ARCHIVO_CSV = CARPETA / "libros.csv"

HEADERS = {"User-Agent": "Mozilla/5.0"}
CANTIDAD_LIBROS = 10



# EXTRACCIÓN DE LOS 10 LIBROS


def extraer_libros():
    respuesta = requests.get(
        URL_CATALOGO,
        headers=HEADERS,
        timeout=30
    )
    respuesta.raise_for_status()

    soup = BeautifulSoup(respuesta.text, "html.parser")
    tarjetas = soup.select("article.product_pod")

    libros = []

    for tarjeta in tarjetas[:CANTIDAD_LIBROS]:
        enlace = tarjeta.select_one("h3 a")
        precio = tarjeta.select_one(".price_color")
        disponibilidad = tarjeta.select_one(".availability")
        valoracion = tarjeta.select_one(".star-rating")
        imagen = tarjeta.select_one("img")

        if not enlace or not precio:
            continue

        titulo = enlace.get("title") or enlace.get_text(strip=True)
        url_libro = urljoin(URL_CATALOGO, enlace.get("href", ""))
        precio_texto = precio.get_text(strip=True).replace("Â£", "£")

        # Convertir el precio a número para hacer comparaciones
        precio_limpio = (
            precio_texto.replace("£", "")
            .replace("Â", "")
            .strip()
        )
        precio_numero = float(precio_limpio)

        clases = (
            valoracion.get("class", [])
            if valoracion else []
        )
        estrellas = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        calificacion = (
            estrellas.get(clases[-1], 0)
            if len(clases) > 1 else 0
        )

        libros.append({
            "titulo": titulo,
            "precio": precio_texto,
            "precio_numero": precio_numero,
            "disponibilidad": (
                disponibilidad.get_text(" ", strip=True)
                if disponibilidad else "No disponible"
            ),
            "valoracion": calificacion,
            "imagen": (
                urljoin(URL_CATALOGO, imagen.get("src"))
                if imagen and imagen.get("src") else ""
            ),
            "url": url_libro
        })

    if not libros:
        raise ValueError(
            "No se encontraron libros en el catálogo."
        )

    return libros


# ==========================================
# ANÁLISIS COMPARATIVO
# ==========================================

def analizar_libros(libros):
    precios = [libro["precio_numero"] for libro in libros]

    return {
        "cantidad": len(libros),
        "promedio": sum(precios) / len(precios),
        "minimo": min(libros, key=lambda libro: libro["precio_numero"]),
        "maximo": max(libros, key=lambda libro: libro["precio_numero"]),
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }


# ==========================================
# GUARDAR CSV
# ==========================================

def guardar_csv(libros):
    columnas = [
        "titulo",
        "precio",
        "precio_numero",
        "disponibilidad",
        "valoracion",
        "imagen",
        "url"
    ]

    with open(
        ARCHIVO_CSV,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas
        )
        escritor.writeheader()
        escritor.writerows(libros)

    print(f"CSV guardado: {ARCHIVO_CSV}")


# ==========================================
# DISEÑO DE LA PÁGINA WEB
# ==========================================

PLANTILLA = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BookScraper - Comparación de libros</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 28px 18px;
    background: #f2f4f8;
    color: #202943;
    font-family: Arial, sans-serif;
}

.contenedor { max-width: 1200px; margin: auto; }

header {
    background: #202c65;
    color: white;
    padding: 28px;
    border-radius: 15px;
    margin-bottom: 22px;
}

header h1 { margin-top: 0; }
header p { color: #dce3ff; }

.resumen {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 16px;
    margin-bottom: 25px;
}

.indicador {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px #17255410;
}

.indicador h3 {
    font-size: 14px;
    color: #626b80;
    margin-top: 0;
}

.indicador p {
    font-size: 23px;
    font-weight: bold;
    color: #202c65;
    margin-bottom: 0;
    overflow-wrap: anywhere;
}

h2 { color: #202c65; }

.libros {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 18px;
}

.tarjeta {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 15px #17255410;
    display: flex;
    flex-direction: column;
}

.portada {
    height: 190px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 15px;
}

.portada img {
    max-height: 185px;
    max-width: 100%;
    object-fit: contain;
}

.tarjeta h3 {
    font-size: 16px;
    line-height: 1.5;
}

.precio {
    font-size: 23px;
    font-weight: bold;
    color: #16794b;
}

.detalle {
    font-size: 14px;
    line-height: 1.6;
    color: #4b5568;
}

a { color: #3347a8; }

.boton {
    display: inline-block;
    margin-top: auto;
    padding: 10px;
    background: #202c65;
    color: white;
    text-align: center;
    text-decoration: none;
    border-radius: 7px;
}

.tabla-contenedor {
    overflow-x: auto;
    background: white;
    border-radius: 12px;
    margin-top: 18px;
    padding: 12px;
}

table {
    border-collapse: collapse;
    width: 100%;
    min-width: 650px;
}

th, td {
    padding: 13px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}

th { background: #202c65; color: white; }
tr:nth-child(even) { background: #f7f8fc; }

footer {
    margin-top: 25px;
    color: #626b80;
    font-size: 13px;
    line-height: 1.7;
    overflow-wrap: anywhere;
}

@media (max-width: 600px) {
    body { padding: 14px 9px; }
    header { padding: 20px; }
}
</style>
</head>

<body>
<div class="contenedor">

<header>
    <h1>BookScraper</h1>
    <p>Análisis y comparación de productos mediante web scraping</p>
    <p>Datos extraídos: {{ analisis.fecha }}</p>
</header>

<section class="resumen">
    <div class="indicador">
        <h3>Libros analizados</h3>
        <p>{{ analisis.cantidad }}</p>
    </div>

    <div class="indicador">
        <h3>Precio promedio</h3>
        <p>£{{ "%.2f"|format(analisis.promedio) }}</p>
    </div>

    <div class="indicador">
        <h3>Libro más económico</h3>
        <p>£{{ "%.2f"|format(analisis.minimo.precio_numero) }}</p>
        <small>{{ analisis.minimo.titulo }}</small>
    </div>

    <div class="indicador">
        <h3>Libro más costoso</h3>
        <p>£{{ "%.2f"|format(analisis.maximo.precio_numero) }}</p>
        <small>{{ analisis.maximo.titulo }}</small>
    </div>
</section>

<h2>Catálogo de libros</h2>

<section class="libros">
{% for libro in libros %}
    <article class="tarjeta">
        <div class="portada">
            {% if libro.imagen %}
            <img src="{{ libro.imagen }}" alt="Portada del libro">
            {% else %}
            <p>Imagen no disponible</p>
            {% endif %}
        </div>

        <h3>{{ libro.titulo }}</h3>
        <p class="precio">{{ libro.precio }}</p>

        <p class="detalle">
            <strong>Valoración:</strong>
            {{ libro.valoracion }} de 5 estrellas
        </p>

        <p class="detalle">
            <strong>Disponibilidad:</strong>
            {{ libro.disponibilidad }}
        </p>

        <a class="boton" href="{{ libro.url }}" target="_blank"
           rel="noopener noreferrer">Ver libro original</a>
    </article>
{% endfor %}
</section>

<h2>Tabla comparativa</h2>

<div class="tabla-contenedor">
<table>
    <thead>
        <tr>
            <th>#</th>
            <th>Libro</th>
            <th>Precio</th>
            <th>Valoración</th>
            <th>Disponibilidad</th>
        </tr>
    </thead>

    <tbody>
    {% for libro in libros %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ libro.titulo }}</td>
            <td>{{ libro.precio }}</td>
            <td>{{ libro.valoracion }}/5</td>
            <td>{{ libro.disponibilidad }}</td>
        </tr>
    {% endfor %}
    </tbody>
</table>
</div>

<footer>
    <p><strong>Fuente:</strong>
    <a href="{{ url_catalogo }}">{{ url_catalogo }}</a></p>

    <p>Proyecto académico realizado con Python, Requests,
    BeautifulSoup y Flask. Books to Scrape es un sitio de
    práctica para proyectos de web scraping.</p>
</footer>

</div>
</body>
</html>
"""


# ==========================================
# GENERAR ARCHIVO HTML
# ==========================================
def guardar_pagina(libros, analisis):
    with app.app_context():
        html = render_template_string(
            PLANTILLA,
            libros=libros,
            analisis=analisis,
            url_catalogo=URL_CATALOGO
        )

    ARCHIVO_HTML.write_text(html, encoding="utf-8")
    print(f"Página web guardada: {ARCHIVO_HTML}")

# ==========================================
# RUTA WEB
# ==========================================

@app.route("/")
def inicio():
    try:
        libros = extraer_libros()
        analisis = analizar_libros(libros)

        guardar_csv(libros)
        guardar_pagina(libros, analisis)

        return render_template_string(
            PLANTILLA,
            libros=libros,
            analisis=analisis,
            url_catalogo=URL_CATALOGO
        )

    except Exception as error:
        return f"""
        <h1>No se pudo cargar el catálogo</h1>
        <p>Detalle: {error}</p>
        <p>Comprueba tu conexión a Internet e inténtalo nuevamente.</p>
        """, 500


# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    print("=" * 50)
    print("BOOKSCRAPER - COMPARACIÓN DE 10 LIBROS")
    print("=" * 50)

    try:
        libros = extraer_libros()
        analisis = analizar_libros(libros)

        guardar_csv(libros)
        guardar_pagina(libros, analisis)

        print(f"Libros extraídos: {len(libros)}")
        print(f"Precio promedio: £{analisis['promedio']:.2f}")
        print(f"Más barato: {analisis['minimo']['titulo']}")
        print(f"Más caro: {analisis['maximo']['titulo']}")

    except Exception as error:
        print(f"Error durante la extracción inicial: {error}")
        print("Puedes intentar acceder a la página desde Flask.")

    print("\nAbre en Chrome: http://127.0.0.1:5000")
    app.run(debug=False)
