import torch
import torch.nn as nn
from torch.utils import data
from torchvision import transforms
import torch.optim as optim
import numpy as np
import os
import argparse
import time
import torchvision
from model import MyDataset, autoencoder
from train import training,validation


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(dest='arg1', type=int, help="Number of Epochs")
    parser.add_argument(dest='arg2', type=int, default=16, help="Batch Size")

    args = parser.parse_args()
    num_epochs = args.arg1
    batch_size = args.arg2

    print(num_epochs, batch_size)

    if not os.path.exists("../output"):
        os.mkdir("../output")

    if not os.path.exists("../weights"):
        os.mkdir("../weights")


    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    u_velocityCylinder = np.load('../data/cylinder_u.npy')
    print('Data loaded')

    img_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
    ])

    # batch_size = 16
    train_dataset = MyDataset(u_velocityCylinder, transform=img_transform)
    train_loader_args = dict(batch_size=batch_size, shuffle=True, num_workers=4)
    train_loader = data.DataLoader(train_dataset, **train_loader_args)
    
    validation_dataset=MyDataset(u_velocityCylinder, transform=img_transform)
    val_loader_args = dict(batch_size=1, shuffle=False, num_workers=4)
    val_loader = data.DataLoader(validation_dataset, **val_loader_args)

    model= autoencoder()
    model=model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion=nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', 
                    factor=0.1, patience=3, verbose=False, 
                    threshold=0.01, threshold_mode='rel', 
                        cooldown=2, min_lr=0.000001, eps=1e-08)

    for epoch in range(num_epochs):
        start_time=time.time()
        print('Epoch no: ',epoch)
        training(model,train_loader,criterion,optimizer)
        if epoch%20==0:
            output=validation(model,val_loader,criterion)
            name='../output/'+str(epoch) +'.npy'        
            np.save(name,output)
            path='../weights/'+ str(epoch) +'.pth'
            torch.save(model.state_dict(),path)

        print("Time : ",time.time()-start_time)
        print('='*50)