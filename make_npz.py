import torch
import torch.distributed as dist
from models import DiT_models
from download import find_model
from diffusion import create_diffusion
from diffusers.models import AutoencoderKL
from tqdm import tqdm
import os
from PIL import Image
import numpy as np
import math
import argparse
from global_path import *

def create_npz_from_sample_folder(sample_dir):
    """
    Builds a single .npz file from a folder of .png samples.
    """
    samples = []
    samples_image = os.listdir(sample_dir)
    num = len(samples_image)
    for i in tqdm(range(num), desc="Building .npz file from samples"):
        sample_pil = Image.open(f"{sample_dir}/{samples_image[i]}")
        sample_np = np.asarray(sample_pil).astype(np.uint8)
        samples.append(sample_np)
    samples = np.stack(samples)
    assert samples.shape == (num, samples.shape[1], samples.shape[2], 3)
    npz_path = f"{sample_dir}.npz"
    np.savez(npz_path, arr_0=samples)
    print(f"Saved .npz file to {npz_path} [shape={samples.shape}].")
    return npz_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_dir")
    args = parser.parse_args()
    create_npz_from_sample_folder(args.sample_dir)