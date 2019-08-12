from PIL import Image
import torch
from torchvision import transforms, utils

model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub', 'DCGAN', pretrained=False, useGPU=False)
model = torch.load('model.pt')


noise, _ = model.buildNoiseData(1)

def run(model, input):
    with torch.no_grad():
        result = model.test(input)
        utils.save_image(result, "result.png") 

run(model, noise)