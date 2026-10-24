"""Clase que recibe los resultados de las clases CSV y JSON y genera salidas/resumen.txt."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path


class GeneradorResumenTXT:
    """Construye y guarda un resumen en texto plano con los resultados reales de la ejecución.

    Cada resultado es el diccionario que devuelve ``resultados()`` de
    ``ManejadorCSV`` o ``ManejadorJSON``.

    Args:
        ruta_salida: Ruta relativa del archivo .txt que se generará.
    """

    def __init__(self, ruta_salida: str | Path = "salidas/resumen.txt") -> None:
        self.ruta_salida = Path(ruta_salida)
        self.resultados: list[dict] = []

    def agregar_resultado(self, resultado: dict) -> None:
        """Agrega el resultado de una de las clases manejadoras."""
        self.resultados.append(resultado)

    def generar_texto(self) -> str:
        """Arma el contenido del resumen."""
        if not self.resultados:
            raise ValueError("No hay resultados. Usa agregar_resultado() primero.")

        lineas = [
            "RESUMEN AE2 - MANEJO DE ARCHIVOS CSV, JSON Y TXT",
            "=" * 60,
            f"Fecha de generación: {datetime.now():%Y-%m-%d %H:%M:%S}",
            "",
            "1. URL de origen",
            "-" * 60,
        ]
        lineas += [f"- {r['formato']}: {r['url_origen']}" for r in self.resultados]

        lineas += ["", "2. Archivos importados", "-" * 60]
        lineas += [
            f"- {r['formato']}: {r['archivo_importado']} ({r['registros_importados']} registros)"
            for r in self.resultados
        ]

        lineas += ["", "3. Modificaciones realizadas", "-" * 60]
        for r in self.resultados:
            lineas.append(f"{r['formato']}:")
            lineas += [f"  - {m}" for m in r["modificaciones"]] or ["  - (ninguna)"]

        lineas += ["", "4. Nuevos archivos guardados", "-" * 60]
        lineas += [
            f"- {r['formato']}: {r['archivo_guardado']} ({r['registros_finales']} registros)"
            for r in self.resultados
        ]

        lineas += ["", "5. Clases y métodos utilizados", "-" * 60]
        lineas += [
            f"- {r['clase']}: {', '.join(r['metodos_usados'])}" for r in self.resultados
        ]
        lineas.append(f"- {type(self).__name__}: agregar_resultado, generar_texto, guardar")

        total_importados = sum(r["registros_importados"] for r in self.resultados)
        total_finales = sum(r["registros_finales"] for r in self.resultados)
        lineas += [
            "",
            "6. Registros procesados",
            "-" * 60,
            *[
                f"- {r['formato']}: {r['registros_importados']} importados -> "
                f"{r['registros_finales']} guardados"
                for r in self.resultados
            ],
            f"- Total: {total_importados} importados -> {total_finales} guardados",
        ]
        return "\n".join(lineas) + "\n"

    def guardar(self) -> Path:
        """Escribe el resumen en ``ruta_salida`` y devuelve la ruta."""
        self.ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta_salida, "w", encoding="utf-8") as archivo:
            archivo.write(self.generar_texto())
        return self.ruta_salida

    def leer(self) -> str:
        """Lee el resumen guardado para mostrarlo en el notebook."""
        with open(self.ruta_salida, "r", encoding="utf-8") as archivo:
            return archivo.read()
