
import random
import numpy as np
from tqdm import tqdm
import torch 
from torch import optim
import torch.nn as nn
from utils import get_network

def train_clf(X, y, representation_dim, num_classes, device, reg_weight=1e-3, iter=500):
    print('\nL2 Regularization weight: %g' % reg_weight)

    criterion = nn.CrossEntropyLoss()
    n_lbfgs_steps = iter

    # Should be reset after each epoch for a completely independent evaluation
    clf = nn.Linear(representation_dim, num_classes).to(device)
    clf_optimizer = optim.LBFGS(clf.parameters())
    clf.train()

    t = tqdm(range(n_lbfgs_steps), desc='Loss: **** | Train Acc: ****% ', bar_format='{desc}{bar}{r_bar}')
    for _ in t:
        def closure():
            clf_optimizer.zero_grad()
            raw_scores = clf(X)
            loss = criterion(raw_scores, y)
            loss += reg_weight * clf.weight.pow(2).sum()
            loss.backward()

            _, predicted = raw_scores.max(1)
            correct = predicted.eq(y).sum().item()

            t.set_description('Loss: %.3f | Train Acc: %.3f%% ' % (loss, 100. * correct / y.shape[0]))

            return loss

        clf_optimizer.step(closure)

    return clf


def test_clf(testloader, device, net, clf, feature=False):
    criterion = nn.CrossEntropyLoss()
    net.eval()
    clf.eval()
    test_clf_loss = 0
    correct = 0
    total = 0
    acc_per_point = []
    with torch.no_grad():
        t = tqdm(enumerate(testloader), total=len(testloader), desc='Loss: **** | Test Acc: ****% ',
                 bar_format='{desc}{bar}{r_bar}')
        for batch_idx, (inputs, targets) in t:
            inputs, targets = inputs.to(device), targets.to(device)
            representation = None
            if feature:
                representation = net.features(inputs).view(len(inputs), -1)
            else:
                representation = net(inputs)
            raw_scores = clf(representation)
            clf_loss = criterion(raw_scores, targets)
            test_clf_loss += clf_loss.item()
            _, predicted = raw_scores.max(1)
            total += targets.size(0)
            acc_per_point.append(predicted.eq(targets))
            correct += acc_per_point[-1].sum().item()
            t.set_description('Loss: %.3f | Test Acc: %.3f%% ' % (test_clf_loss / (batch_idx + 1), 100. * correct / total))
            
    acc = 100. * correct / total
    return acc, torch.cat(acc_per_point, dim=0).cpu().numpy()

def top5accuracy(output, target, topk=(5,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        print(correct)
        for k in topk:
            correct_k = correct[:k].contiguous().view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size).item())
        return res


def le_run(
    train_model, 
    channel,
    num_classes,
    img_size,
    device, 
    init_model, 
    dl_tr, 
    dl_te,
    le_iters=20,
    seed=0,
):  

    # set seed first 

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    # model
    model = get_network(train_model, channel, num_classes, img_size, fix_net=True).to(device)
    if hasattr(init_model, "classifier"):
        del init_model.classifier
    model.load_state_dict(init_model.state_dict(), strict=False)
    model.classifier = nn.Identity()

    # -------------------------------------------------------------------------------------------------------------------------------------------------------#
    """FEATURES"""
    Z = []
    Y = []
    with torch.no_grad():
        for X, y in tqdm(dl_tr, desc="encoding"):
            Z.append(model.features(X.to(device)).view(len(X), -1))
            Y.append(y.to(device))
    
    Z = torch.cat(Z, dim=0)
    Y = torch.cat(Y, dim=0)
    print(Z.shape)
    print(Y.shape)
    # -------------------------------------------------------------------------------------------------------------------------------------------------------#
    """LINEAR EVALUATION"""
    clf = train_clf(Z, Y, Z.shape[1], num_classes, device, iter=le_iters)
    acc, acc_per_point = test_clf(dl_te, device, model, clf, feature=True)

    return acc