import torch
from utils.helpers import *
import warnings
from PIL import Image
from torchvision import transforms
#from torchsummary import summary
from collections import OrderedDict
def image_transform(image):
    test_transforms = transforms.Compose([transforms.Resize(255),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])
    # image = Image.open(imagepath)
    imagetensor = test_transforms(image)
    return imagetensor


def predict(imagepath, verbose=False):
    if not verbose:
        warnings.filterwarnings('ignore')
    model_path = './models/catvdog.pth'
    try:
        checks_if_model_is_loaded = type(model)
    except:
        model = load_model(model_path)
    model.eval()
    #summary(model, input_size=(3,244,244))
    if verbose:
        print("Model Loaded..")
    image = image_transform(imagepath)
    image1 = image[None,:,:,:]
    out = model(image1)

    ps=torch.exp(out)
    p = ps.topk(2,dim=1)

    val = p.values
    inds = p.indices
    val = val.detach().numpy()
    topconf, topclass = ps.topk(1, dim=1)


    classes = {0:"cat",1:"dog"}

    res =  {classes[int(inds[0][1] )]:float(val[0][1]), classes[int(inds[0][0] )]:float(val[0][0])}

    dict1 = OrderedDict(sorted(res.items()))
    return dict1