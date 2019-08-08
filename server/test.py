import falcon, torch
import torchvision.models as models

resnet18 = models.resnet18()
falcon.deploy(model=resnet18, code="falcon-run.py", name="resnet18-jtguibas", input="image.3x64x64", output="image.3x64x64")

