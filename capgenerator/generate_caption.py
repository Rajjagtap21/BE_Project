import argparse, json, os
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pyttsx3
import skimage
import skimage.transform
import torch
import torchvision.transforms as transforms
from math import ceil
from PIL import Image

from .decoder import Decoder
from .encoder import Encoder

data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def pil_loader(path):
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')
    
def getcap(path):
    word_dict = json.load(open('G:/BE project/ImageCapGen/model/word_dict.json', 'r'))
    vocabulary_size = len(word_dict)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    encoder = Encoder(network='vgg19').to(device)
    decoder = Decoder(vocabulary_size, encoder.dim).to(device)
    
    decoder.load_state_dict(torch.load('G:/BE project/ImageCapGen/model/model_10.pth', map_location=device))

    encoder.eval()
    decoder.eval()
    
    cps = generate_caption_visualization(encoder, decoder, path, word_dict, device)
    return cps
    
def generate_caption_visualization(encoder, decoder, img_path, word_dict, device, beam_size=3, smooth=True):
    img = pil_loader(img_path)
    img = data_transforms(img).unsqueeze(0).to(device)  # Add batch dimension and move to device

    img_features = encoder(img)
    img_features = img_features.expand(beam_size, img_features.size(1), img_features.size(2))
    sentence, alpha = decoder.caption(img_features, beam_size)

    token_dict = {idx: word for word, idx in word_dict.items()}
    sentence_tokens = []
    cp = []
    for word_idx in sentence:
        sentence_tokens.append(token_dict[word_idx])
        if word_idx == word_dict['<eos>']:
            cp = sentence_tokens.copy()
            cp.remove('<start>')
            cp.remove('<eos>')

    img = Image.open(img_path)
    w, h = img.size
    if w > h:
        w = w * 256 / h
        h = 256
    else:
        h = h * 256 / w
        w = 256
    left = (w - 224) / 2
    top = (h - 224) / 2
    resized_img = img.resize((int(w), int(h)), Image.BICUBIC).crop((left, top, left + 224, top + 224))
    img = np.array(resized_img.convert('RGB').getdata()).reshape(224, 224, 3)
    img = img.astype('float32') / 255

    num_words = len(sentence_tokens)
    w = np.round(np.sqrt(num_words))
    h = np.ceil(np.float32(num_words) / w)
    alpha = torch.tensor(alpha).to(device)

    plot_height = ceil((num_words + 3) / 4.0)
    ax1 = plt.subplot(4, plot_height, 1)
    plt.imshow(img)
    plt.axis('off')
    
    for idx in range(num_words):
        ax2 = plt.subplot(4, plot_height, idx + 2)
        label = sentence_tokens[idx]
        plt.text(0, 1, label, backgroundcolor='white', fontsize=13)
        plt.text(0, 1, label, color='black', fontsize=13)
        plt.imshow(img)

        if encoder.network == 'vgg19':
            shape_size = 14
        else:
            shape_size = 7

        if smooth:
            alpha_img = skimage.transform.pyramid_expand(alpha[idx, :].reshape(shape_size, shape_size), upscale=16, sigma=20)
        else:
            alpha_img = skimage.transform.resize(alpha[idx, :].reshape(shape_size, shape_size), [img.shape[0], img.shape[1]])

        plt.imshow(alpha_img, alpha=0.8)
        plt.set_cmap(cm.Greys_r)
        plt.axis('off')

    os.makedirs('./output', exist_ok=True)  # Ensure output directory exists
    plt.savefig('./output/1.png')
    plt.close()
    
    return cp
