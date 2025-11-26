max_epochs = 50
batch_size = 8
work_dir = '/scratch2/liuqin/work_dirs/deformable_detr_video_full'
###################
#_base_ = '../deformable_detr/deformable-detr_r50_16xb2-50e_coco.py'
_base_ = f'./mmdetection/configs/deformable_detr/deformable-detr-refine-twostage_r50_16xb2-50e_coco.py'
# Dataset settings
dataset_type = 'CocoDataset'
data_root = './dataset/PMMA'

metainfo = dict(
    classes=('Ped', 'PushWheel1', 'PushWheel2', 'PushWheel3', 'PushWheelEmpty',
             'Walker_Rest', 'Walker_Walking', 'Wheelchair', 'Cane')
)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    dict(type='PackDetInputs')
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='PackDetInputs')
]

train_dataloader = dict(
    batch_size=batch_size,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='annotations_1/train_10pct.json',
        data_prefix=dict(img='images/'),
        metainfo=metainfo,
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
        type=dataset_type,
        data_root=data_root,
        ann_file='annotations_1/val.json',
        data_prefix=dict(img='images/'),
        metainfo=metainfo,
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

# Model settings
model = dict(
    bbox_head=dict(num_classes=len(metainfo['classes']))
)

# Runtime settings
default_scope = 'mmdet'

load_from = 'https://download.openmmlab.com/mmdetection/v3.0/deformable_detr/deformable-detr-refine-twostage_r50_16xb2-50e_coco/deformable-detr-refine-twostage_r50_16xb2-50e_coco_20221021_184714-acc8a5ff.pth'

# Training schedule
train_cfg = dict(max_epochs=max_epochs)
optim_wrapper = dict(
    optimizer=dict(lr=0.0002)
)

# Hooks
default_hooks = dict(
    logger=dict(interval=50),
    checkpoint=dict(interval=1, save_best='auto')
)
