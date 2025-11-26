# CUDA_VISIBLE_DEVICES=2 

import os
import torch
from mmengine.config import Config
from mmengine.runner import Runner
from mmdet.utils import register_all_modules, setup_cache_size_limit_of_dynamo

# ========== Step 1: Setup ==========
method_name = f'faster_rcnn'

config_file = f'./m1_configs_faster_rcnn.py'
checkpoint_file = './PMMA_analysis/best_models/m1_faster_rcnn_epoch_7.pth'  # <<< change this

cfg = Config.fromfile(config_file)
cfg.load_from = checkpoint_file
cfg.device = 'cuda'  # Force CPU for Mac

# Ensure best performance on CPU
torch.set_num_threads(4)
setup_cache_size_limit_of_dynamo()
register_all_modules()

# ========== Step 2: Enable classwise COCO evaluation ==========
cfg.val_evaluator.classwise = True  # <<< This line gives you per-category AP
cfg.work_dir = f'./PMMA_analysis/eval_log_{method_name}'
# ========== Step 3: Run evaluation ==========
runner = Runner.from_cfg(cfg)
results = runner.test()

from pprint import pprint
pprint(results)
