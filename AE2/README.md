# AE2 - Manejo de archivos CSV, JSON y TXT

Evidencia de Aprendizaje 2 - Unidad 1.

## Objetivo

Importar, modificar y guardar archivos CSV y JSON mediante clases de Python, coordinadas desde un notebook de Jupyter, y generar un resumen `.txt` con una tercera clase.

## Estructura

```
AE2/
|-- README.md
|-- manejador_csv.py             # Clase CSV (csv.reader / csv.writer)
|-- manejador_json.py            # Clase JSON (json.load / json.dump)
|-- generador_resumen_txt.py     # Clase que genera el resumen .txt
|-- ae2_manejo_archivos.ipynb    # Notebook que coordina todo
|-- datos/
|   |-- originales/              # CSV y JSON descargados de Hugging Face (sin modificar)
|   `-- modificados/             # Archivos generados con nombres nuevos
`-- salidas/
    `-- resumen.txt              # Resumen generado por codigo
```

## Fuentes de datos

| Formato | Dataset | URL de origen |
|---------|---------|---------------|
| CSV     | _pendiente_ | _pendiente_ |
| JSON    | _pendiente_ | _pendiente_ |

## Pasos de ejecucion

1. Clonar el repositorio o abrirlo en GitHub Codespaces.
2. Instalar dependencias: `pip install -r requirements.txt` (y `pip install notebook ipykernel` si no tienes Jupyter).
3. Verificar que los archivos originales esten en `AE2/datos/originales/`.
4. Abrir `AE2/ae2_manejo_archivos.ipynb` y ejecutar todas las celdas en orden. El notebook usa rutas relativas a la carpeta `AE2`.
5. Revisar los archivos generados en `AE2/datos/modificados/` y el resumen en `AE2/salidas/resumen.txt`.
