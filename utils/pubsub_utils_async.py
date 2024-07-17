import logging
import sys
import cv2
import numpy as np
import torch

def get_module_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    return logger


async def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.resize(image, (28, 28))
    image = image.astype(np.float32) / 255.0
    return torch.tensor(image).unsqueeze(0).unsqueeze(0)

def load_model(model):
    model.load_state_dict(torch.load("model/model.pth", map_location=torch.device("cpu")))
    model.eval()

    return model

async def model_prediction(image_processed, model_load):
    output = model_load(image_processed)
    _, predicted = torch.max(output.data, 1)
    
    return predicted.item()
