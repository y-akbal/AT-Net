### Here we go!!!
import torch
from torch import nn as nn
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch import functional as F
from tqdm import tqdm

### --- ###
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.nn as nn
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
### --- ###

import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import Subset
### --- ###
import hydra
from omegaconf import DictConfig, OmegaConf

### import model and train and validation data ###
from model import main_model
from dataset_generator import test_data, train_data
## --- ###
from train_tools import trainer as Trainer



def train_val_data_loader(**kwargs):
    return None


@hydra.main(version_base=None, config_path=".", config_name="model_config")
def main(cfg : DictConfig):
    ## model configuration ##
    model_config, optimizer_config, scheduler_config = cfg["model_config"], cfg["optimizer_config"], cfg["scheduler_config"]
    snapshot_path = cfg["snapshot_path"]
    save_every = cfg["save_every"]

    ## model_config -- optimizer config -- scheduler config ##
    torch.manual_seed(0)
    model = main_model.from_dict(**model_config)
    ### Optimizer ###
    optimizer = torch.optim.SGD(model.parameters(), **optimizer_config)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, **scheduler_config)
    ##  train and validation data loader ## 
    
    
    ### Training Stuff Here it comes ###
    
    trainer = Trainer(model = model, 
            train_data= train_dataloader,
            val_data = val_dataloader,
            optimizer = optimizer, 
            scheduler = scheduler,
            save_every = save_every,
            snapshot_path=snapshot_path,
            compile_model=cfg["compile_model"],
            
    )
    
    trainer.train(max_epochs = 2)
    trainer.validate()


"""






if __name__ == '__main__':
    ## use here weights and biases!!!!
    ## use it properly dude!!!
    main()