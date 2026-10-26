import pandas as pd

class DatasetSummarizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generar_resumen(self, output_file: str = 'resumen.txt') -> None:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Resumen del DataFrame ===\n")
            f.write(f"Cantidad de filas: {self.df.shape[0]}\n")
            f.write(f"Cantidad de columnas: {self.df.shape[1]}\n\n")
            
            f.write("--- Columnas y Tipos de Datos ---\n")
            f.write(self.df.dtypes.to_string() + "\n\n")
            
            f.write("--- Conteo de Valores Nulos ---\n")
            f.write(self.df.isnull().sum().to_string() + "\n\n")
            
            f.write("--- Estadísticas Descriptivas ---\n")
            f.write(self.df.describe(include='all').to_string() + "\n")
            