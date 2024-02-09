from pathlib import Path
import pickle

import torch

from components.pointnet2.models.pointnet2_cls_ssg import get_model
from components.pointnet2.models.pointnet2_utils import inplace_relu


def infer():
    classifier = get_model(2, normal_channel=False)
    classifier.apply(inplace_relu)

    # Load weights
    checkpoint = torch.load(
        './components/pointnet2/checkpoints/best_model.pth',
        map_location=torch.device('cpu')
    )
    classifier.load_state_dict(checkpoint['model_state_dict'])
    # classifier = classifier.cuda()
    classifier = classifier.eval()

    # Read data
    pcd_dir = Path('./data/input/pcd')

    out_data = {}

    for file in pcd_dir.glob('*.pcd'):

        with open(file, 'rb') as pcd:
            pcd = pickle.load(pcd)
            pcd = torch.Tensor(pcd).view(1, -1, 3)
            pcd = pcd.transpose(2, 1).float()

        with torch.no_grad():
            pred, _ = classifier(pcd)
            pred_choice = pred.data.max(1)[1][0].item()

        out_data[file.stem] = pred_choice

    return out_data