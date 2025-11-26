# CUDA_VISIBLE_DEVICES=0,1 PORT=29500 ./mmdetection/tools/dist_train.sh projects/DINO/configs/dino_r50_8xb2_50e_coco.py 2
# import torch
# torch.cuda.empty_cache()

method_name = 'dino'
training_bs = 1
max_epochs = 50
data_root = './dataset/PMMA'
##################

_base_ = './mmdetection/configs/dino/dino-5scale_swin-l_8xb2-36e_coco.py'
load_from = f'https://github.com/RistoranteRist/mmlab-weights/releases/download/dino-swinl/dino-5scale_swin-l_8xb2-36e_coco-5486e051.pth'



# Custom classes
classes = ('Ped', 'PushWheel1', 'PushWheel2', 'PushWheel3', 'PushWheelEmpty',
           'Walker_Rest', 'Walker_Walking', 'Wheelchair', 'Cane')



train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='PackDetInputs')
]

train_dataloader = dict(
    batch_size=training_bs,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type='CocoDataset',
        data_root=data_root,
        ann_file='annotations_1/train_10pct.json',
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
        ann_file='annotations_1/val.json',
        data_prefix=dict(img='images/'),
        metainfo=dict(classes=classes),
        pipeline=test_pipeline
    )
)

test_dataloader = val_dataloader

val_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'annotations_1/val.json',
    metric='bbox'
)
test_evaluator = val_evaluator

# Modify DINO’s model for your number of classes
model = dict(
    bbox_head=dict(num_classes=len(classes))
)

train_cfg = dict(max_epochs=max_epochs)

optim_wrapper = dict(
    optimizer=dict(
        lr=0.0001,  # Lower LR than Faster R-CNN
        weight_decay=0.0001
    )
)

default_scope = 'mmdet'
work_dir = f'/scratch2/liuqin/work_dirs/{method_name}'

default_hooks = dict(
    logger=dict(interval=50),
    checkpoint=dict(interval=4, save_best='auto')
)