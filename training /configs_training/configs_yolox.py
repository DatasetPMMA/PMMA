_base_ = 'mmdetection/configs/yolox/yolox_x_8xb8-300e_coco.py'

# Custom classes
num_classes = 9
classes = ('Ped', 'PushWheel1', 'PushWheel2', 'PushWheel3', 'PushWheelEmpty',
           'WalkerRest', 'WalkerWalking', 'Wheelchair', 'Cane')

# Dataset root directory
data_root = './dataset/PMMA'

# Model settings
model = dict(
    bbox_head=dict(
        num_classes=num_classes
    )
)

# Training pipeline (without mosaic/mixup)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]

# Testing pipeline
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='PackDetInputs')
]

# Data loader settings
train_dataloader = dict(
    batch_size=2,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type='CocoDataset',
        data_root=data_root,
        ann_file='annotations_1/train_updated.json',
        data_prefix=dict(img='images/'),
        metainfo=dict(classes=classes),
        filter_cfg=dict(filter_empty_gt=True),
        pipeline=train_pipeline
    )
)

val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='CocoDataset',
        data_root=data_root,
        ann_file='annotations_1/val_updated.json',
        data_prefix=dict(img='images/'),
        metainfo=dict(classes=classes),
        pipeline=test_pipeline
    )
)

# Test dataloader is the same as validation
test_dataloader = val_dataloader

# Evaluation settings
val_evaluator = dict(
    type='CocoMetric',
    ann_file=f'{data_root}/annotations_1/val_updated.json',
    metric='bbox'
)
test_evaluator = val_evaluator

# Runtime settings
default_scope = 'mmdet'
work_dir = '/scratch2/liuqin/work_dirs/yolox'

# Pretrained model checkpoint
load_from = 'https://download.openmmlab.com/mmdetection/v2.0/yolox/yolox_x_8x8_300e_coco/yolox_x_8x8_300e_coco_20211126_140254-1ef88d67.pth'

# Training epochs and learning rate
train_cfg = dict(max_epochs=12)
optim_wrapper = dict(
    optimizer=dict(
        lr=0.02 / 8
    )
)

# Logging and checkpoint settings
default_hooks = dict(
    logger=dict(type='LoggerHook', interval=50),
    checkpoint=dict(type='CheckpointHook', interval=1, save_best='auto')
)

# NOTE: To be compatible with YOLOXModeSwitchHook (since we are using CocoDataset instead of MultiImageMixDataset),
# we need to monkey-patch the CocoDataset class with the following:
# ------------------------------------------------
# from mmdet.datasets import CocoDataset
# def update_skip_type_keys(self, skip_type_keys):
#     self.skip_type_keys = skip_type_keys
# CocoDataset.update_skip_type_keys = update_skip_type_keys
# ------------------------------------------------