import pandas as pd
from datasets import load_dataset

class HFDatasetLoader:
    def __init__(self, dataset_id: str, split: str = 'train', max_rows: int = 1000):
        self.dataset_id = dataset_id
        self.split = split
        self.max_rows = max_rows

    def get_dataframe(self) -> pd.DataFrame:
        # streaming=True evita descargar 1.5 GB y evita saturar la memoria RAM del Codespace
        dataset = load_dataset(self.dataset_id, split=self.split, streaming=True)
        filas = list(dataset.take(self.max_rows))
        return pd.DataFrame(filas)