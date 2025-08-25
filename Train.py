import shutil
from sklearn.model_selection import KFold
import os
from pathlib import Path
from ultralytics import YOLO
import torch
import yaml

def main():

    print(torch.cuda.is_available()) 
    print(torch.cuda.current_device())
    print(torch.cuda.get_device_name(0))

    # Pastas existentes
    train_images = Path("Dataset/train/images")
    val_images = Path("Dataset/val/images")
    train_labels = Path("Dataset/train/labels")
    val_labels = Path("Dataset/val/labels")

    # Pasta de destino unificada
    all_images = Path("dataset_all/images")
    all_labels = Path("dataset_all/labels")
    all_images.mkdir(parents=True, exist_ok=True)
    all_labels.mkdir(parents=True, exist_ok=True)

    # Copia tudo de train e val
    for img in list(train_images.glob("*")) + list(val_images.glob("*")):
        shutil.copy(img, all_images / img.name)

    for lbl in list(train_labels.glob("*")) + list(val_labels.glob("*")):
        shutil.copy(lbl, all_labels / lbl.name)

    images = sorted(os.listdir(all_images))
    labels = sorted(os.listdir(all_labels))
    assert len(images) == len(labels), "Número de imagens e labels não bate!"

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    folds = []
    for fold, (train_idx, val_idx) in enumerate(kf.split(images), start=1):
        train_files = [images[i] for i in train_idx]
        val_files = [images[i] for i in val_idx]
        folds.append((train_files, val_files))

    fold_results = []
    best_global_model = None
    best_global_map50 = 0.0

    for fold, (train_files, val_files) in enumerate(folds, start=1):
        print(f"\n=== Fold {fold} ===")

        # Criar estrutura temporária para YOLO
        fold_dir = Path(f"fold_{fold}")
        (fold_dir / "images/train").mkdir(parents=True, exist_ok=True)
        (fold_dir / "images/val").mkdir(parents=True, exist_ok=True)
        (fold_dir / "labels/train").mkdir(parents=True, exist_ok=True)
        (fold_dir / "labels/val").mkdir(parents=True, exist_ok=True)

        # Copia arquivos para cada split
        for img_name in train_files:
            shutil.copy(all_images / img_name, fold_dir / "images/train" / img_name)
            shutil.copy(all_labels / img_name.replace(".jpg", ".txt"), fold_dir / "labels/train" / img_name.replace(".jpg", ".txt"))

        for img_name in val_files:
            shutil.copy(all_images / img_name, fold_dir / "images/val" / img_name)
            shutil.copy(all_labels / img_name.replace(".jpg", ".txt"), fold_dir / "labels/val" / img_name.replace(".jpg", ".txt"))

        # Criar arquivo de configuração YAML
        yaml_content = f"""
        path: {fold_dir}
        train: images/train
        val: images/val
        nc: 1
        names: ['cisto']
        """
        with open(fold_dir / "data.yaml", "w") as f:
            f.write(yaml_content)

        # Treinar YOLO
        model = YOLO("yolo11m-seg.pt")  # ou yolov11, etc.
        results = model.train(data=str(fold_dir / "data.yaml"), epochs=50, imgsz=225, lr0=0.001,project=f"fold_{fold}")

        # Validar e obter métricas
        metrics = model.val()
        map50 = metrics.box.map50  # mAP50
        map = metrics.box.map      # mAP50-95
        precision = metrics.box.p.mean()
        recall = metrics.box.r.mean()

        # Armazenar resultados do fold
        fold_results.append({
            'fold': fold,
            'map50': map50,
            'map': map,
            'precision': precision,
            'recall': recall,
            'model_path': Path(model.trainer.save_dir) / 'weights' / 'best.pt'
        })

        # Atualizar melhor modelo global
        if map50 > best_global_map50:
            best_global_map50 = map50
            best_global_model = fold_results[-1]

    # Resultados finais
    print("\n=== RESUMO FINAL ===")
    for res in fold_results:
        print(f"Fold {res['fold']}: mAP50={res['map50']:.4f}, Precision={res['precision']:.4f}, Recall={res['recall']:.4f}")

    print("\n=== MELHOR MODELO ===")
    print(f"Fold {best_global_model['fold']}:")
    print(f"mAP50: {best_global_model['map50']:.4f}")
    print(f"Precision: {best_global_model['precision']:.4f}")
    print(f"Recall: {best_global_model['recall']:.4f}")
    print(f"Caminho: {best_global_model['model_path']}")

    # Salvar configuração do melhor modelo
    with open('best_model_info.yaml', 'w') as f:
        yaml.dump(best_global_model, f)

if __name__ == '__main__':
    main()