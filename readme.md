# MKDT
Code for [Dataset Distillation via Knowledge Distillation: Towards Efficient Self-Supervised Pre-training of Deep Networks](https://arxiv.org/abs/2410.02116)

## Overview

## Installation

```
git clone git@github.com:jiayini1119/MKDT.git
conda activate mkdt
pip install -r requirements.txt
```


## Commands to Run the Experiments

### 1. Train the Teacher Model Using SSL and Getting Target Representation.
#### For Barlow Twins:
We obtained the teacher model trained with [Barlow Twins](https://arxiv.org/abs/2103.03230) using the checkpoint provided in the [KRRST](https://github.com/db-Lee/selfsup_dd). Download and save the checkpoints under the repository `/krrst_teacher_ckpt`.

#### For SimCLR:
We obtained the teacher model trained with [SimCLR](https://arxiv.org/abs/2002.05709) using the checkpoint provided in the [SAS](https://github.com/BigML-CS-UCLA/sas-data-efficient-contrastive-learning).

To get the target representation:

```
python get_target_rep.py --dataset {CIFAR10/CIFAR100/Tiny} --model {model: ConvNetD4 for TinyImageNet and ConvNet for other datasets} --ssl_algorithm {barlow_twins/simclr} --data_path {dataset path} --result_dir {directory to store the target representations} --device {device}
```

By default, the target representations will be saved in `/{result_dir}_{ssl_algorithm}/{dataset}_target_rep_train.pt`.


### 2. Get Expert Trajectories Using Knowledge Distillation.
Run the following sripts to get expert trajectories: 

CIFAR 10: `commands/buffer/{ssl_algorithm}/c10_get_trajectory.sh`

CIFAR 100: `commands/buffer/{ssl_algorithm}/c10_get_trajectory.sh`

Tiny ImageNet: `commands/buffer/{ssl_algorithm}/tiny_get_trajectory.sh`

The buffers will be saved in the directory `buffer/{ssl_algorithm}/{dataset}/{model}`.

### 3. Get the High Loss Subset.
To obtain the high loss subset for distilled dataset initialization: 
```
python get_target_rep.py --dataset {CIFAR10/CIFAR100/Tiny} --data_path {dataset path} --model {model} --num_buffers {number of buffers} --ssl_algo {Algorithm to train the ssl} --train_labels_path {path to the target representation of the dataset} --batch_train {batch size of the train dataset} --device {device}
```

For example, 

```
python get_target_rep.py --dataset CIFAR100 --data_path /home/data --model ConvNet --num_buffers 100 --ssl_algo barlow_twins --train_labels_path /home/jennyni/MKDT/target_rep/barlow_twins/CIFAR100_target_rep_train.pt
```

### 4. Run Distillation.

Run the following sripts to distill the dataset (SSL algorithm using barlow twins):

**CIFAR 10** 

2 percent: `commands/distill/barlow_twins/CIFAR10/2_per.sh`

5 percent: `commands/distill/barlow_twins/CIFAR10/5_per.sh`

**CIFAR 100**

2 percent: `commands/distill/barlow_twins/CIFAR100/2_per.sh`

5 percent: `commands/distill/barlow_twins/CIFAR100/5_per.sh`

**Tiny ImageNet**

2 percent: `commands/distill/barlow_twins/Tiny/2_per.sh`

5 percent: `commands/distill/barlow_twins/Tiny/5_per.sh`


### 5. Evaluation.

The following scripts contains the commands to run the evaluation for different subsets (e.g., MKDT, random, KRRST).

Append `--subset_frac {0.01/0.05/0.1/0.5}` to the command to evaluate the datasets using different evaluation subset fractions

**CIFAR 10** 

2 percent: `commands/eval/c10_2per.sh --subset_frac {0.01/0.05/0.1/0.5}`

5 percent: `commands/eval/c10_5per.sh --subset_frac {0.01/0.05/0.1/0.5}`

**CIFAR 100**

2 percent: `commands/eval/c100_2per.sh --subset_frac {0.01/0.05/0.1/0.5}`

5 percent: `commands/eval/c100_5per.sh --subset_frac {0.01/0.05/0.1/0.5}`

**Tiny ImageNet**

2 percent: `commands/eval/tiny_2per.sh --subset_frac {0.01/0.05/0.1/0.5}`

5 percent: `commands/eval/tiny_5per.sh --subset_frac {0.01/0.05/0.1/0.5}`

You can visualize the tables comparing different subset results for a dataset using `commands/exp_plotting.ipynb`.


## Acknowledgement
The code is based on the following repositories. 

https://github.com/GeorgeCazenavette/mtt-distillation

https://github.com/db-Lee/selfsup_dd

## BibTeX
```
@misc{joshi2024datasetdistillationknowledgedistillation,
      title={Dataset Distillation via Knowledge Distillation: Towards Efficient Self-Supervised Pre-Training of Deep Networks}, 
      author={Siddharth Joshi and Jiayi Ni and Baharan Mirzasoleiman},
      year={2024},
      eprint={2410.02116},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2410.02116}, 
}
```
