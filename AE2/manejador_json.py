"""Clase para importar, modificar y guardar archivos JSON (json.load / json.dump)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ManejadorJSON:
    """Importa un JSON local, modifica sus registros y guarda una copia nueva.

    El JSON puede ser una lista de objetos o un objeto que contiene la lista
    de registros dentro de una clave (por ejemplo ``{"cities": [...]}``).
    En el segundo caso se indica ``clave_registros`` y, al guardar, se
    conserva el resto del objeto original.

    Args:
        ruta_entrada: Ruta relativa del JSON original.
        url_origen: URL de Hugging Face de donde se descargó el archivo.
        clave_registros: Clave del objeto JSON donde está la lista de registros.
    """

    def __init__(
        self, ruta_entrada: str | Path, url_origen: str = "", clave_registros: str | None = None
    ) -> None:
        self.ruta_entrada = Path(ruta_entrada)
        self.url_origen = url_origen
        self.clave_registros = clave_registros
        self.ruta_salida: Path | None = None
        self.contenido: Any = None
        self.datos: list[dict[str, Any]] = []
        self.registros_importados = 0
        self.modificaciones: list[str] = []
        self.metodos_usados: list[str] = []

    # ------------------------------------------------------------------ lectura
    def importar(self) -> list[dict[str, Any]]:
        """Lee el archivo con ``json.load`` y ubica la lista de registros."""
        with open(self.ruta_entrada, "r", encoding="utf-8") as archivo:
            self.contenido = json.load(archivo)
        registros = (
            self.contenido[self.clave_registros] if self.clave_registros else self.contenido
        )
        if not isinstance(registros, list):
            raise TypeError(
                "No se encontró una lista de registros. "
                "Si el JSON es un objeto, indica clave_registros."
            )
        self.datos = registros
        self.registros_importados = len(self.datos)
        self._registrar_metodo("importar")
        return self.datos

    def vista_previa(self, n: int = 3) -> list[dict[str, Any]]:
        """Devuelve los primeros ``n`` registros."""
        return self.datos[:n]

    def buscar(self, campo: str, valor: Any) -> list[dict[str, Any]]:
        """Devuelve los registros cuyo ``campo`` es igual a ``valor``."""
        return [r for r in self.datos if r.get(campo) == valor]

    # ------------------------------------------------------------ modificación
    def actualizar_valor(self, campo_id: str, valor_id: Any, campo: str, nuevo_valor: Any) -> int:
        """Cambia ``campo`` por ``nuevo_valor`` en los registros donde ``campo_id == valor_id``.

        Returns:
            Cantidad de registros actualizados.
        """
        cambios = 0
        for registro in self.datos:
            if registro.get(campo_id) == valor_id:
                anterior = registro.get(campo)
                registro[campo] = nuevo_valor
                cambios += 1
                self.modificaciones.append(
                    f"Actualizar valor: {campo_id}={valor_id} -> "
                    f"{campo}: {anterior!r} => {nuevo_valor!r}"
                )
        self._registrar_metodo("actualizar_valor")
        return cambios

    def agregar_registro(self, registro: dict[str, Any]) -> None:
        """Agrega un registro (diccionario) al final de la lista."""
        if not isinstance(registro, dict):
            raise TypeError("El registro debe ser un diccionario.")
        self.datos.append(registro)
        self.modificaciones.append(f"Agregar registro: {registro}")
        self._registrar_metodo("agregar_registro")

    def eliminar_registro(self, campo: str, valor: Any) -> int:
        """Elimina los registros cuyo ``campo`` es igual a ``valor``.

        Returns:
            Cantidad de registros eliminados.
        """
        antes = len(self.datos)
        self.datos = [r for r in self.datos if r.get(campo) != valor]
        eliminados = antes - len(self.datos)
        self.modificaciones.append(
            f"Eliminar registro: {campo}={valor!r} ({eliminados} registros)"
        )
        self._registrar_metodo("eliminar_registro")
        return eliminados

    # ------------------------------------------------------------- escritura
    def guardar(self, ruta_salida: str | Path) -> Path:
        """Guarda los datos en un JSON nuevo con ``json.dump``."""
        self.ruta_salida = Path(ruta_salida)
        self.ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        if self.clave_registros:
            self.contenido[self.clave_registros] = self.datos
            salida = self.contenido
        else:
            salida = self.datos
        with open(self.ruta_salida, "w", encoding="utf-8") as archivo:
            json.dump(salida, archivo, ensure_ascii=False, indent=2)
        self._registrar_metodo("guardar")
        return self.ruta_salida

    # ------------------------------------------------------------- resultados
    def resultados(self) -> dict:
        """Resume lo realizado para enviarlo a la clase que genera el .txt."""
        return {
            "formato": "JSON",
            "clase": type(self).__name__,
            "url_origen": self.url_origen,
            "archivo_importado": str(self.ruta_entrada)
            + (f" (clave '{self.clave_registros}')" if self.clave_registros else ""),
            "archivo_guardado": str(self.ruta_salida) if self.ruta_salida else "",
            "registros_importados": self.registros_importados,
            "registros_finales": len(self.datos),
            "modificaciones": list(self.modificaciones),
            "metodos_usados": list(self.metodos_usados),
        }

    def _registrar_metodo(self, nombre: str) -> None:
        if nombre not in self.metodos_usados:
            self.metodos_usados.append(nombre)
