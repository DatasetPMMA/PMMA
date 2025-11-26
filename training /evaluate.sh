#!/bin/bash
source /home/liuqin/miniconda3/etc/profile.d/conda.sh
conda activate /scratch2/liuqin/2025/venv/openmmlab
export CUDA_VISIBLE_DEVICES=0
cd /home/liuqin/Documents/PMMA_Processing

##########################################################################################
#### faster-rcnn test
python mmdetection/tools/test.py configs_faster_rcnn_test.py \
       --work-dir /scratch2/liuqin/z_PMMA_test_final/faster_rcnn \
       ./PMMA_results/m1_faster_rcnn/best_coco_bbox_mAP_epoch_8.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric \
       | tee test_faster_rcnn_log.txt


#### faster-rcnn val
python mmdetection/tools/test.py configs_faster_rcnn_val.py \
       --work-dir /scratch2/liuqin/z_PMMA_val_final/faster_rcnn \
       ./PMMA_results/m1_faster_rcnn/best_coco_bbox_mAP_epoch_8.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric \
       | tee val_faster_rcnn_log.txt

echo 'Faster-rcnn finished.'
##########################################################################################
#### centernet test
python mmdetection/tools/test.py configs_centernet_test.py \
       --work-dir /scratch2/liuqin/z_PMMA_test_final/centernet \
       PMMA_results/m2_centernet/best_coco_bbox_mAP_epoch_7.pth\
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric \
       | tee test_centernet_log.txt

#### centernet val
python mmdetection/tools/test.py configs_centernet_val.py \
       --work-dir /scratch2/liuqin/z_PMMA_val_final/centernet \
       PMMA_results/m2_centernet/best_coco_bbox_mAP_epoch_7.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric \
       | tee val_centernet_log.txt

echo 'Centernet finished.'
##########################################################################################
#### yolox test
python mmdetection/tools/test.py configs_yolox_test.py \
       --work-dir /scratch2/liuqin/z_PMMA_test_final/yolox \
       ./PMMA_results/m4_yolox/best_coco_bbox_mAP_epoch_20.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee test_yolox_log.txt

#### yolox val
python mmdetection/tools/test.py configs_yolox_val.py \
       --work-dir /scratch2/liuqin/z_PMMA_val_final/yolox \
       ./PMMA_results/m4_yolox/best_coco_bbox_mAP_epoch_20.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee val_yolox_log.txt

echo 'Yolox finished.'
##########################################################################################
#### detr test
python mmdetection/tools/test.py configs_detr_test.py \
       --work-dir /scratch2/liuqin/z_PMMA_test_final/detr \
       PMMA_results/m3_detr/best_coco_bbox_mAP_epoch_13.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee test_detr_log.txt

#### detr val
python mmdetection/tools/test.py configs_detr_val.py \
       --work-dir /scratch2/liuqin/z_PMMA_val_final/detr \
       PMMA_results/m3_detr/best_coco_bbox_mAP_epoch_13.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee val_detr_log.txt

echo 'Detr finished.'
##########################################################################################
#### deformable_detr test
python mmdetection/tools/test.py configs_deformable_detr_test.py \
       --work-dir /scratch2/liuqin/z_PMMA_test_final/deformable_detr \
       PMMA_results/m5_deformable_detr/deformable_detr/epoch_40.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee test_deformable_detr_log.txt

#### deformable_detr val
python mmdetection/tools/test.py configs_deformable_detr_val.py \
       --work-dir /scratch2/liuqin/z_PMMA_val_final/deformable_detr \
       PMMA_results/m5_deformable_detr/deformable_detr/epoch_40.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee val_deformable_detr_log.txt

echo 'Deformable-detr finished.'
##########################################################################################
#### dino test
python mmdetection/tools/test.py configs_dino_test.py \
       --work-dir /scratch2/liuqin/z_PMMA_test_final/dino \
       PMMA_results/m6_dino/dino/epoch_5.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee test_dino_log.txt

python mmdetection/tools/test.py configs_dino_val.py \
       --work-dir /scratch2/liuqin/z_PMMA_val_final/dino \
       PMMA_results/m6_dino/dino/epoch_5.pth \
       --cfg-options test_evaluator.classwise=True \
       test_evaluator.metric=bbox  \
       test_evaluator.type=CocoMetric\
       | tee val_dino_log.txt

echo 'Dino finished.'