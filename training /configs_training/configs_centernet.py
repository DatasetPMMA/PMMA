# CUDA_VISIBLE_DEVICES=0,1 PORT=29500 ./mmdetection/tools/dist_train.sh configs_centernet.py 2
_base_ = './mmdetection/configs/centernet/centernet-update_r50-caffe_fpn_ms-1x_coco.py'

load_from = 'https://download.openmmlab.com/mmdetection/v3.0/centernet/centernet-update_r50-caffe_fpn_ms-1x_coco/centernet-update_r50-caffe_fpn_ms-1x_coco_20230512_203845-8306baf2.pth'

method_name = 'centernet'
training_bs = 8

# Custom classes
classes = ('Ped', 'PushWheel1', 'PushWheel2', 'PushWheel3', 'PushWheelEmpty',
           'Walker_Rest', 'Walker_Walking', 'Wheelchair', 'Cane')

# Dataset config
data_root = './dataset/PMMA'

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs'),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='PackDetInputs'),
]

train_dataloader = dict(
    batch_size=training_bs,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type='CocoDataset',
        data_root=data_root,
        ann_file='annotations_1/train.json',
        data_prefix=dict(img='images/'),
        metainfo=dict(classes=classes),
        filter_cfg=dict(filter_empty_gt=True),
        pipeline=train_pipeline,
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
        pipeline=test_pipeline,
    )
)

test_dataloader = val_dataloader

val_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'annotations_1/val.json',
    metric='bbox'
)
test_evaluator = val_evaluator

# CenterNet model-specific config: just set num_classes here
model = dict(
    bbox_head=dict(num_classes=len(classes))
)

# Runtime
default_scope = 'mmdet'
work_dir = f'./PMMA_work_dirs/{method_name}'

# Training schedule
train_cfg = dict(max_epochs=140)  # CenterNet default is 140 epochs
optim_wrapper = dict(optimizer=dict(lr=0.02 / 8))

default_hooks = dict(
    logger=dict(interval=50),
    checkpoint=dict(interval=1, save_best='auto')
)