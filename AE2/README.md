# AE2 - Manejo de archivos CSV, JSON y TXT

Evidencia de Aprendizaje 2 - Unidad 1.

## Objetivo

Importar, modificar y guardar archivos CSV y JSON mediante clases de Python, coordinadas desde un notebook de Jupyter, y generar un resumen `.txt` con una tercera clase.

## Estructura

```
AE2/
|-- README.md
|-- manejador_csv.py             # Clase ManejadorCSV (csv.reader / csv.writer)
|-- manejador_json.py            # Clase ManejadorJSON (json.load / json.dump)
|-- generador_resumen_txt.py     # Clase GeneradorResumenTXT (genera resumen.txt)
|-- ae2_manejo_archivos.ipynb    # Notebook que coordina todo
|-- datos/
|   |-- originales/              # Archivos de Hugging Face sin modificar
|   |   |-- catalogue.csv
|   |   `-- road-tax.json
|   `-- modificados/             # Archivos generados con nombres nuevos
|       |-- catalogo_carros_modificado.csv
|       `-- impuestos_ciudades_modificado.json
`-- salidas/
    `-- resumen.txt              # Resumen generado por codigo
```

## Fuentes de datos

Dataset: [variantwise/indian-cars-variants](https://huggingface.co/datasets/variantwise/indian-cars-variants) - Datos: VariantWise (variantwise.com), licencia CC BY 4.0.

| Formato | Contenido | Registros | URL de origen |
|---------|-----------|-----------|---------------|
| CSV     | Catalogo de versiones de carros nuevos en India (marca, modelo, motor, combustible, transmision, precio) | 1.281 | https://huggingface.co/datasets/variantwise/indian-cars-variants/blob/main/data/catalogue.csv |
| JSON    | Impuestos de rodamiento y matricula; se trabaja la lista `cities` | 95 ciudades | https://huggingface.co/datasets/variantwise/indian-cars-variants/blob/main/data/road-tax.json |

## Clases y metodos

| Clase | Metodos |
|-------|---------|
| `ManejadorCSV` | `importar`, `vista_previa`, `buscar`, `actualizar_valor`, `agregar_registro`, `eliminar_registros`, `guardar`, `resultados` |
| `ManejadorJSON` | `importar`, `vista_previa`, `buscar`, `actualizar_valor`, `agregar_registro`, `eliminar_registro`, `guardar`, `resultados` (admite `clave_registros` para JSON con objetos anidados) |
| `GeneradorResumenTXT` | `agregar_resultado`, `generar_texto`, `guardar`, `leer` |

## Modificaciones realizadas

- **CSV**: se actualiza el precio de la version `sport-mt` (Jeep Compass) a 18.49 lakh, se agrega una version de prueba (`Grupo 2 Demo EV`) y se eliminan las versiones de la marca `Tesla`.
- **JSON** (`cities`): la ciudad `nagpur` pasa a `tier` 1, se agrega la ciudad `nellore` y se elimina la ciudad `leh`.

## Pasos de ejecucion

1. Clonar el repositorio o abrirlo en GitHub Codespaces.
2. Verificar que los archivos originales esten en `AE2/datos/originales/`. Se descargaron manualmente (sin token) desde los enlaces de la tabla "Fuentes de datos" (boton *download* de cada archivo en Hugging Face).
3. Instalar Jupyter si no esta disponible: `pip install notebook ipykernel`. Las clases solo usan la libreria estandar (`csv`, `json`, `pathlib`).
4. Abrir `AE2/ae2_manejo_archivos.ipynb` y ejecutar todas las celdas en orden (usa rutas relativas a la carpeta `AE2`). Tambien se puede ejecutar desde la terminal:
   ```bash
   cd AE2
   jupyter nbconvert --to notebook --execute --inplace ae2_manejo_archivos.ipynb
   ```
5. Revisar los archivos generados en `AE2/datos/modificados/` y el resumen en `AE2/salidas/resumen.txt`.
