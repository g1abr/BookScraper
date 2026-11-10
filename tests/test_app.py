
import pytest
from BookScraper import app as bookscraper


@pytest.fixture
def cliente():
    bookscraper.app.config["TESTING"] = True

    with bookscraper.app.test_client() as cliente:
        yield cliente


def test_aplicacion_creada():
    assert bookscraper.app is not None


def test_ruta_principal_responde(cliente, monkeypatch):

    datos_prueba = [
        {
            "titulo": "Libro de prueba",
            "precio": "£20.00",
            "precio_numero": 20.00,
            "disponibilidad": "In stock",
            "valoracion": 3,
            "imagen": "",
            "url": "https://books.toscrape.com/"
        }
    ]

    # Simular extracción de libros
    monkeypatch.setattr(
        bookscraper,
        "extraer_libros",
        lambda: datos_prueba
    )

    # Evitar crear archivos durante la prueba
    monkeypatch.setattr(
        bookscraper,
        "guardar_csv",
        lambda libros: None
    )

    monkeypatch.setattr(
        bookscraper,
        "guardar_pagina",
        lambda libros, analisis: None
    )

    # Consultar la página principal
    respuesta = cliente.get("/")

    assert respuesta.status_code == 200
    assert b"BookScraper" in respuesta.data
    assert b"Libro de prueba" in respuesta.data
    assert b"20.00" in respuesta.data
