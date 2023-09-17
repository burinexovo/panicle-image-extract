import os
from skimage import io, transform
import torch
import torchvision
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms  # , utils
# import torch.optim as optim

import numpy as np
from PIL import Image
import glob
from pathlib import Path
import cv2 as cv
from tqdm import trange

from A00_data_loader import RescaleT
from A00_data_loader import ToTensor
from A00_data_loader import ToTensorLab
from A00_data_loader import SalObjDataset

from model import U2NET  # full size version 173.6 MB
from model import U2NETP  # small version u2net 4.7 MB

# normalize the predicted SOD probability map


def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d-mi)/(ma-mi)

    return dn


def save_output(image_name, pred, d_dir, image_dir):

    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray(predict_np*255).convert('RGB')
    img_name = image_name.split(os.sep)[-1]
    image = io.imread(image_name)
    imo = im.resize((image.shape[1], image.shape[0]), resample=Image.BILINEAR)

    pb_np = np.array(imo)

    aaa = img_name.split(".")
    bbb = aaa[0:-1]
    imidx = bbb[0]
    for i in range(1, len(bbb)):
        imidx = imidx + "." + bbb[i]
    # print(f'd_dir={d_dir}')
    # print(f'imidx={imidx}')
    # print('{d_dir}/{imidx}.png=', f'{d_dir}/{imidx}.png')
    # print('{image_dir}{image_name}.jpg', f'{image_dir}{image_name}.jpg')
    print(f'{ image_name }處理完成')
    image_path = f'{d_dir}/{imidx}.png'
    imo.save(image_path)
    image_name = Path(image_path).stem
    origin_image_path = glob.glob(f'{image_dir}/{image_name}.jpg')[0]
    mask_img = cv.imread(image_path)
    gray = cv.cvtColor(mask_img, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    binary[binary[:, :] == 255] = 1
    mask = np.dstack((binary, binary, binary))
    origin_img = cv.imread(origin_image_path)
    new_image = origin_img * mask

    new_image[new_image[:, :, 0] > new_image[:, :, 1]] = 0
    new_image[new_image[:, :, 0] > new_image[:, :, 2]] = 0
    cv.imwrite(f'{d_dir}/{image_name}.png', new_image)


def exec(inputFileDir, outFileDir):

    # --------- 1. get image path and name ---------
    # --------- 1. 取得圖片路徑與名稱(在這裡應該先把要去背的圖片單獨拉出來一個資料夾) ---------
    model_name = 'u2net'
    # os.path.join(os.getcwd(), 'datasets','images'+ os.sep)
    image_dir = inputFileDir
    # os.path.join(os.getcwd(), 'datasets','mask' + os.sep)
    prediction_dir = outFileDir
    # model的路徑
    # model_dir = os.path.join(os.getcwd(), 'models', 'u2net_rice_panicle_image_extract.pth')
    model_dir = os.path.join('./models', 'u2net_rice_panicle_image_extract.pth')
    print(f'./input/{image_dir}/*')
    img_name_list = glob.glob(f'{image_dir}/*')
    print(f'測試圖片資料集：{ img_name_list }')
    # --------- 2. dataloader ---------
    # 1. dataloader
    test_salobj_dataset = SalObjDataset(img_name_list=img_name_list,
                                        lbl_name_list=[],
                                        transform=transforms.Compose([RescaleT(256),
                                                                      ToTensorLab(flag=0)])
                                        )

    test_salobj_dataloader = DataLoader(test_salobj_dataset,
                                        batch_size=1,
                                        shuffle=False,
                                        num_workers=1)

    # --------- 3. model define ---------
    net = U2NET(3, 1)

    if torch.cuda.is_available():
        net.load_state_dict(torch.load(model_dir))
        net.cuda()
    else:
        net.load_state_dict(torch.load(model_dir, map_location='cpu'))
    net.eval()

    # --------- 4. inference for each image ---------
    print('稻穗去背中...')
    for i_test, data_test in enumerate(test_salobj_dataloader):
        print("稻穗影像去背處理中:", img_name_list[i_test].split(
            os.sep)[-1], f'{i_test + 1} / {len(test_salobj_dataloader)}')

        if os.path.isfile(prediction_dir + img_name_list[i_test].split(os.sep)[-1]) == True:
            continue

        inputs_test = data_test['image']
        inputs_test = inputs_test.type(torch.FloatTensor)

        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)

        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

        # normalization
        pred = d1[:, 0, :, :]
        pred = normPRED(pred)

        # save results to test_results folder
        if not os.path.exists(prediction_dir):
            os.makedirs(prediction_dir, exist_ok=True)
        save_output(img_name_list[i_test], pred, prediction_dir, image_dir)

        del d1, d2, d3, d4, d5, d6, d7
