# BookScraper

## Descripción

BookScraper es una aplicación desarrollada en Python que permite extraer información de libros del sitio web Books to Scrape.

El programa obtiene información como el título, precio, disponibilidad y valoración de los libros. Los datos se procesan y se presentan mediante una aplicación web desarrollada con Flask.

## Tecnologías utilizadas

- Python: lenguaje de programación.
- Requests: permite realizar solicitudes HTTP.
- BeautifulSoup: facilita la extracción de información del HTML.
- Flask: permite desarrollar la aplicación web.
- Pytest: permite ejecutar pruebas automatizadas.

## Instalación

1. Clonar o descargar el repositorio.
2. Abrir una terminal en la carpeta `BookScraper`.
3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Ejecutar el siguiente comando:

```bash
python app.py
```

Después, abrir en el navegador la dirección local que indique Flask, normalmente:

`http://127.0.0.1:5000/`

## Pruebas automatizadas

Desde la carpeta principal del proyecto, ejecutar:

```bash
python -m pytest -v
```

Las pruebas permiten verificar que la aplicación se encuentre creada y que la página principal responda correctamente.