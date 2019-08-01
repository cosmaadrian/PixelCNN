import torch

from pixelcnn import PixelCNN

import argparse
from utils import str2bool, save_samples


def main():
    parser = argparse.ArgumentParser(description='PixelCNN')

    parser.add_argument('--causal-ksize', type=int, default=7,
                        help='Kernel size of causal convolution')
    parser.add_argument('--hidden-ksize', type=int, default=3,
                        help='Kernel size of hidden layers convolutions')

    parser.add_argument('--data-channels', type=int, default=3,
                        help='Number of data channels')
    parser.add_argument('--color-levels', type=int, default=7,
                        help='Number of levels to quantisize value of each channel of each pixel into')

    parser.add_argument('--hidden-fmaps', type=int, default=128,
                        help='Number of feature maps in hidden layer')
    parser.add_argument('--out-hidden-fmaps', type=int, default=32,
                        help='Number of feature maps in outer hidden layer')
    parser.add_argument('--hidden-layers', type=int, default=10,
                        help='Number of layers of gated convolutions with mask of type "B"')

    parser.add_argument('--cuda', type=str2bool, default=True,
                        help='Flag indicating whether CUDA should be used')
    parser.add_argument('--model-path', '-m', default='',
                        help="Path to model's saved parameters")
    parser.add_argument('--output-fname', '-o', type=str, default='samples/samples.jpg',
                        help='Output filename')

    parser.add_argument('--count', '-c', type=int, default=10,
                        help='Number of images to generate \
                                  (is rounded to the nearest integer square)')
    parser.add_argument('--height', type=int, default=28, help='Output image height')
    parser.add_argument('--width', type=int, default=28, help='Output image width')

    cfg = parser.parse_args()

    model = PixelCNN(cfg=cfg)
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() and cfg.cuda else "cpu")
    model.to(device)

    model.load_state_dict(torch.load(cfg.model_path))

    samples = model.sample((cfg.data_channels, cfg.height, cfg.width), cfg.count)
    save_samples(samples, cfg.output_fname)


if __name__ == '__main__':
    main()
