# PMMA dataset processing and training document

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