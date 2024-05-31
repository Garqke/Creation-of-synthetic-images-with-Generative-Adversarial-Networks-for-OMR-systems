import os
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

IMG_HEIGHT = 128
IMG_WIDTH = 128
IMG_SIZE = 128
NUM_CHANNEL = 1

# Definir los tokens y vocabulario
tokens = {
    'PAD_TOKEN': 0,
    'SOS_TOKEN': 1,
    'EOS_TOKEN': 2,
    'UNK_TOKEN': 3
}

class MusicSymbolDataset(Dataset):
    def __init__(self, data_dirs, transform=None):
        self.data_dirs = data_dirs
        self.transform = transform or transforms.Compose([
            transforms.Resize((IMG_HEIGHT, IMG_WIDTH)),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor()
        ])
        self.data = []
        self.classes = []
        for data_dir in data_dirs:
            print(f"Procesando directorio: {data_dir}")
            if not os.path.exists(data_dir):
                print(f"Directorio no existe: {data_dir}")
                continue
            for symbol in os.listdir(data_dir):
                symbol_dir = os.path.join(data_dir, symbol)
                if os.path.isdir(symbol_dir):
                    symbol_lower = symbol.lower()
                    if symbol_lower not in tokens:
                        tokens[symbol_lower] = len(tokens)
                    if symbol_lower not in self.classes:
                        self.classes.append(symbol_lower)
                    print(f"Existente: {symbol_dir}")
                    png_count = 0
                    for img_file in os.listdir(symbol_dir):
                        if img_file.lower().endswith('.png'):
                            png_count += 1
                            self.data.append((os.path.join(symbol_dir, img_file), tokens[symbol_lower]))
                            print(f"Añadido: {os.path.join(symbol_dir, img_file)}")
                    print(f"Archivos .png encontrados en {symbol_dir}: {png_count}")
                else:
                    print(f"Directorio no encontrado para símbolo: {symbol_dir}")
        print(f"Total de imágenes encontradas: {len(self.data)}")
        print(f"Clases encontradas: {self.classes}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path, label = self.data[idx]
        image = Image.open(img_path).convert('RGB')
        image = self.transform(image)
        return image, label

def loadData(oov, directories=None, batch_size=128, num_workers=0):
    if directories is None:
        directories = ['./dataset1/dataset1', './dataset2/dataset2', './data/open_omr_raw', './data/images', './data/muscima_pp_raw']

    train_dataset = MusicSymbolDataset(directories)
    test_dataset = MusicSymbolDataset(directories)

    if len(train_dataset) == 0:
        raise ValueError("El dataset de entrenamiento está vacío")

    if len(test_dataset) == 0:
        raise ValueError("El dataset de prueba está vacío")

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    return train_loader, test_loader

# Definir vocab_size basado en tokens
index2letter = {v: k for k, v in tokens.items()}
vocab_size = len(tokens)
num_tokens = 4

# Exportar variables
__all__ = ['vocab_size', 'IMG_WIDTH', 'IMG_HEIGHT', 'loadData']

# Ejemplo de uso
if __name__ == "__main__":
    train_loader, test_loader = loadData(oov=True)
