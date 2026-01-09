# PMMA dataset processing and training document

# Data Link:
**PMMA Dataset (via DOI)**: [https://doi.org/10.5683/SP3/XJPQUG](https://doi.org/10.5683/SP3/XJPQUG)
# Data preparation
Download original videos from link and put it in 'data_processing/raw_data/original_videos'

1) Go to the data path 
    ```
    cd data_processing
    ```
2) Convert videos to images

    ```
    python step_1_video_2_images.py
    ```
3) Merge images for building training/validation/test sets
    ```
    python step_2_merge_images.py
    ```
4) Convert CVAT annotations to COCO format
    ```
    python step_3_convert_cvat_to_coco_full.py
    ```
5) Split the images into training/validation/test sets
    ```
    python step_4_splitting.py
    ```

## Training
MMDetection is used to train Faster R-CNN, DINO, CenterNet, YOLOX, DETR, and Deformable DETR. Please refer to the [MMdetection](https://mmdetection.readthedocs.io/en/latest/) documentation for environment setup and installation instructions. 

RT-DETR is used to train RT-DETR. Please refer to the [RT-DETR](https://github.com/lyuwenyu/RT-DETR) documentation for environment setup and installation instructions.

```
cd training
```
**MMdetection:**

Exmaple for training:
1) Go to the MMdetection path
    ```
    cd /path/to/MMdetection
    ```

2) Use Faster R-CNN as an example, train the model: 
    ```
    CUDA_VISIBLE_DEVICES=0,1,2,3 ./mmdetection/tools/dist_train.sh configs_training/configs_faster_rcnn.py 4
    ```
    where 0,1,2,3 are available GPU names, 4 is the number of GPUs


**RT-DETR:**


1) Copy the data yaml and model info to RT-DETR
    ```
    cp configs_training/coco_detection_PMMA.yml /path/to/RT-DETR/redetrv2-pytorch/configs/dataset

    ```
    ```
    cp configs_training/rtdetrv2_r50vd_6x_coco_run.yml /path/to/RT-DETR/redetrv2-pytorch/configs/redetrv2
    ```

2) Go to RT-DETR path:
    ```
    cd /path/to/RT-DETR/redetrv2-pytorch/
    ```

3) Train the model:
    ```
    python tools/train.py -c configs/rtdetrv2/rtdetrv2_r50vd_6x_coco_run.yml
    ```
## Layout
```
PMMA/
├── raw_annotations/
│   ├── video_1_annotations.xml
│   └── video_2_annotations.xml
│   └── video_3_annotations.xml
│
├── annotations/
│   ├── train.json
│   └── val.json
│   └── val.json
│
├── images/
│   └── video_2/
│         ├── video_2_1.zip
│         ├── video_2_2.zip
│         ├── video_2_3.zip
│         ├── video_2_4.zip
│         ├── video_2_5.zip
│         ├── video_2_6.zip
│
├── videos/
│   ├── video_1.mp4
│   ├── video_3_1.mp4
│   ├── video_3_1.mp4
└── README.md
```
Notes: The original video_2 is not provided as video_1 and video_3, as the video was involved with people who are volunteers. Instead, images are provided in "images/video_2".

