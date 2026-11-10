
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def analizar_libro():
   
    print("WEB SCRAPING CON BEAUTIFULSOUP")
    print("Fecha:", datetime.now().isoformat(timespec="seconds"))
    print("URL:", URL)

    try:
        respuesta = requests.get(
            URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )

        print("\nCódigo HTTP:", respuesta.status_code)
        respuesta.raise_for_status()

        soup = BeautifulSoup(respuesta.text, "html.parser")

        titulo = soup.select_one("div.product_main h1")
        precio = soup.select_one("p.price_color")
        disponibilidad = soup.select_one("p.instock")
        descripcion = soup.select_one("#product_description + p")
        valoracion = soup.select_one("div.product_main p.star-rating")
        imagen = soup.select_one("div.item.active img")

        nombre = titulo.get_text(strip=True) if titulo else "No encontrado"
        precio_texto = precio.get_text(strip=True) if precio else "No encontrado"
        stock = (
            disponibilidad.get_text(" ", strip=True)
            if disponibilidad else "No encontrado"
        )
        descripcion_texto = (
            descripcion.get_text(" ", strip=True)
            if descripcion else "No encontrada"
        )
        estrellas = (
            valoracion.get("class", [])[-1]
            if valoracion and len(valoracion.get("class", [])) > 1
            else "No encontrada"
        )
        url_imagen = (
            urljoin(URL, imagen.get("src"))
            if imagen and imagen.get("src")
            else "No encontrada"
        )

        print("\n Resultados")
        print("Título:", nombre)
        print("Precio:", precio_texto.replace("Â£", "£"))
        print("Disponibilidad:", stock)
        print("Valoración:", estrellas)
        print("Descripción:", descripcion_texto[:500])
        print("Imagen:", url_imagen)
        print("\nLongitud del HTML:", len(respuesta.text), "caracteres")
        print("Estado de la prueba: completada")

    except requests.RequestException as error:
        print("Error de conexión:", error)
    except Exception as error:
        print("Error inesperado:", error)

if __name__ == "__main__":
    analizar_libro()
