"""Clase para importar, modificar y guardar archivos CSV (csv.reader / csv.writer)."""
from __future__ import annotations

import csv
from pathlib import Path


class ManejadorCSV:
    """Importa un CSV local, permite modificar sus registros y guarda una copia nueva.

    Los datos se manejan como una lista de encabezados y una lista de filas
    (cada fila es una lista de cadenas), tal como las entrega ``csv.reader``.

    Args:
        ruta_entrada: Ruta relativa del CSV original.
        url_origen: URL de Hugging Face de donde se descargó el archivo.
    """

    def __init__(self, ruta_entrada: str | Path, url_origen: str = "") -> None:
        self.ruta_entrada = Path(ruta_entrada)
        self.url_origen = url_origen
        self.ruta_salida: Path | None = None
        self.encabezados: list[str] = []
        self.filas: list[list[str]] = []
        self.registros_importados = 0
        self.modificaciones: list[str] = []
        self.metodos_usados: list[str] = []

    # ------------------------------------------------------------------ lectura
    def importar(self) -> list[list[str]]:
        """Lee el CSV con ``csv.reader``; la primera fila se toma como encabezados."""
        with open(self.ruta_entrada, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo)
            self.encabezados = next(lector)
            self.filas = [fila for fila in lector if fila]
        self.registros_importados = len(self.filas)
        self._registrar_metodo("importar")
        return self.filas

    def vista_previa(self, n: int = 5) -> list[list[str]]:
        """Devuelve los encabezados y las primeras ``n`` filas."""
        return [self.encabezados, *self.filas[:n]]

    def buscar(self, columna: str, valor: str) -> list[list[str]]:
        """Devuelve las filas cuyo valor en ``columna`` coincide con ``valor``."""
        i = self._indice(columna)
        return [fila for fila in self.filas if fila[i] == valor]

    # ------------------------------------------------------------ modificación
    def actualizar_valor(
        self, columna_id: str, valor_id: str, columna: str, nuevo_valor: str
    ) -> int:
        """Cambia ``columna`` por ``nuevo_valor`` en las filas donde ``columna_id == valor_id``.

        Returns:
            Cantidad de filas actualizadas.
        """
        i_id, i_col = self._indice(columna_id), self._indice(columna)
        cambios = 0
        for fila in self.filas:
            if fila[i_id] == valor_id:
                anterior = fila[i_col]
                fila[i_col] = str(nuevo_valor)
                cambios += 1
                self.modificaciones.append(
                    f"Actualizar valor: {columna_id}={valor_id} -> "
                    f"{columna}: '{anterior}' => '{nuevo_valor}'"
                )
        self._registrar_metodo("actualizar_valor")
        return cambios

    def agregar_registro(self, registro: dict[str, str] | list[str]) -> None:
        """Agrega una fila al final. Acepta una lista ordenada o un dict por encabezado."""
        if isinstance(registro, dict):
            fila = [str(registro.get(col, "")) for col in self.encabezados]
        else:
            fila = [str(v) for v in registro]
        if len(fila) != len(self.encabezados):
            raise ValueError(
                f"El registro tiene {len(fila)} valores y se esperaban {len(self.encabezados)}."
            )
        self.filas.append(fila)
        resumen = " | ".join(v for v in fila if v)
        self.modificaciones.append(f"Agregar registro: {resumen[:150]}")
        self._registrar_metodo("agregar_registro")

    def eliminar_registros(self, columna: str, valor: str) -> int:
        """Elimina las filas cuyo valor en ``columna`` sea igual a ``valor``.

        Returns:
            Cantidad de filas eliminadas.
        """
        i = self._indice(columna)
        antes = len(self.filas)
        self.filas = [fila for fila in self.filas if fila[i] != valor]
        eliminadas = antes - len(self.filas)
        self.modificaciones.append(
            f"Eliminar registros: {columna}={valor} ({eliminadas} filas)"
        )
        self._registrar_metodo("eliminar_registros")
        return eliminadas

    # ------------------------------------------------------------- escritura
    def guardar(self, ruta_salida: str | Path) -> Path:
        """Guarda encabezados y filas en un CSV nuevo con ``csv.writer``."""
        self.ruta_salida = Path(ruta_salida)
        self.ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta_salida, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(self.encabezados)
            escritor.writerows(self.filas)
        self._registrar_metodo("guardar")
        return self.ruta_salida

    # ------------------------------------------------------------- resultados
    def resultados(self) -> dict:
        """Resume lo realizado para enviarlo a la clase que genera el .txt."""
        return {
            "formato": "CSV",
            "clase": type(self).__name__,
            "url_origen": self.url_origen,
            "archivo_importado": str(self.ruta_entrada),
            "archivo_guardado": str(self.ruta_salida) if self.ruta_salida else "",
            "registros_importados": self.registros_importados,
            "registros_finales": len(self.filas),
            "modificaciones": list(self.modificaciones),
            "metodos_usados": list(self.metodos_usados),
        }

    # ------------------------------------------------------------- auxiliares
    def _indice(self, columna: str) -> int:
        if columna not in self.encabezados:
            raise KeyError(f"La columna '{columna}' no existe. Columnas: {self.encabezados}")
        return self.encabezados.index(columna)

    def _registrar_metodo(self, nombre: str) -> None:
        if nombre not in self.metodos_usados:
            self.metodos_usados.append(nombre)
