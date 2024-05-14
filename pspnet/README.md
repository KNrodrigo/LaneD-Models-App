# Lane Detection Using PSPNet

## Overview
This project leverages the Pyramid Scene Parsing Network (PSPNet) architecture for the task of lane detection within image data. PSPNet is a deep learning model originally designed for the field of computer vision, specifically for the purpose of semantic segmentation. By adapting PSPNet to the lane detection problem, the project aims to achieve accurate identification and delineation of road lanes within images.


## Requirements

Python >= 3.7

## Installation
1. Clone the repository: `https://github.com/KNrodrigo/LaneD-Models-App.git`
2. Move the `pspnet` folder: `cd pspnet`
3. Create a virtual environment: `python3 -m venv pspnet`
4. Activate a virtual environment:
* Windows: `<env_name>\Scripts\activate`
* macOS/Linux: `source pspnet/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Download the VIL-100 dataset using this [Link](https://github.com/yujun0-0/MMA-Net)

## Train and get evaluation results

```python
python pspnet.py --root_dir "..\VIL100" --backbone "resnet34" --saved_model_pth "model.keras" --epochs 100
```

## Visualisations
Can be found on the `pspnet.ipynb`.

## Pretrained Models
All pre-trained models can found under `pspnet/trained_models` folder.

## Reference
* [https://github.com/yujun0-0/MMA-Net](https://github.com/yujun0-0/MMA-Net)
* [https://github.com/qubvel/segmentation_models](https://github.com/qubvel/segmentation_models)
