import torch
from torch import nn
from torch.autograd import Variable
import numpy as np
import json

class linearRegression(nn.Module):
    def __init__(self):
        super(linearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        out = self.linear(x)
        return out

with open('input.json') as input_json:
    input = json.load(input_json)

def run():
    model = torch.load("model.pt")
    model.eval()
    
    output = model(torch.Tensor([input["x"]]))
    with open('output.json', 'w') as fp:
        json.dump({"result": output.detach().numpy().item()}, fp)

run()