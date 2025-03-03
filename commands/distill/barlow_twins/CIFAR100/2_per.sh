#!/bin/bash

CUDA_VISIBLE_DEVICES=1 python distill.py \
  --dataset CIFAR100 \
  --model ConvNet \
  --iters 5000 \
  --train_labels_path /home/jennyni/MKDT/target_rep/barlow_twins/CIFAR100_target_rep_train.pt \
  --expert_epochs 2 \
  --lr_img 1000 \
  --syn_steps 40 \
  --image_init_idx_path /home/jennyni/MKDT/init/cifar100/CIFAR100_barlow_twins_2_high_loss_indices.pkl \
  --max_start_epoch 2 \
  --expert_dir /home/jennyni/MKDT/buffers_barlow_twins/CIFAR100/ConvNet