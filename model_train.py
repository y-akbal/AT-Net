### Here we go!!!
import torch
import os
from torch import nn as nn
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch import functional as F
from tqdm import tqdm
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.nn as nn
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import Subset
import torch.multiprocessing as mp
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
### end of torch ### 
import hydra
from omegaconf import DictConfig, OmegaConf
### import model and train and validation data and trainer ###
from model import main_model
from dataset_generator import test_data, train_data
from train_tools import trainer as Trainer



def ddp_setup():
    init_process_group(backend="nccl")
    torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))

def train_val_data_loader(train_data, test_data, **kwargs):
    root_dir_train = kwargs["train_path"]["root_dir"]
    root_dir_val = kwargs["val_path"]["root_dir"]
    csv_file_val = kwargs["val_path"]["csv_file"]

    train_image_generator, dict_val = train_data(root_dir = root_dir_train)
    test_image_generator = test_data(root_dir = root_dir_val,
              csv_file = csv_file_val,
              classes_dict = dict_val
    )
    

    kwargs_train = kwargs["train_data_details"]
    kwargs_test = kwargs["val_data_details"]


    train_sampler = DistributedSampler(train_image_generator)
    val_sampler = DistributedSampler(test_image_generator)


    train_data = DataLoader(
        dataset= train_image_generator,
        sampler = train_sampler,
        **kwargs_train,
    )
    test_data = DataLoader(
        dataset= test_image_generator,
        sampler = val_sampler,
        **kwargs_test,
    )

    return train_data, test_data


@hydra.main(version_base=None, config_path=".", config_name="model_config")
def main(cfg : DictConfig):
    ddp_setup()
    ## model configuration ##
    model_config, optimizer_config, scheduler_config = cfg["model_config"], cfg["optimizer_config"], cfg["scheduler_config"]

    ## --- ### 

    ## model_config -- optimizer config -- scheduler config ##
    torch.manual_seed(0)
    model = main_model.from_dict(**model_config)
    optimizer = torch.optim.SGD(model.parameters(), **optimizer_config)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, **scheduler_config)
    ## batched train and validation data loader ## 
    train_images, test_images = train_val_data_loader(train_data, test_data, **cfg["data"])

    print(len(train_images), len(test_images))
    print(os.environ["LOCAL_RANK"])
    


    destroy_process_group()


if __name__ == '__main__':
    ## use here weights and biases!!!!
    ## use it properly dude!!!
    main()