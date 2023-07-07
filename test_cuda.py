# install python 3.8-3.11
# uninstall pytorch if already installed just in case.
# install pytorch from here: https://pytorch.org/get-started/locally/
## pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
## Note the version you install, as of july 2023, CUDA 11.8 was downloaded from pytorch
# install cuda from here: https://developer.nvidia.com/cuda-11-8-0-download-archive
## Note the version you install, as of july 2023, CUDA 11.8 was downloaded from nvidia
# Run this file, if it shows True, and a bunch of arrays looking like the following, you're good.
#       True
#       tensor([[0.5501, 0.9391, 0.8764],
#               [0.9291, 0.7754, 0.0546],
#               [0.9611, 0.9695, 0.2663],
#               [0.2534, 0.1226, 0.8644],
#               [0.4071, 0.6316, 0.3806]])

import torch

print(torch.cuda.is_available())
x = torch.rand(5, 3)
print(x)