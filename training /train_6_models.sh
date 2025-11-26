
CUDA_VISIBLE_DEVICES=0,1 ./mmdetection/tools/dist_train.sh configs_training/configs_faster_rcnn.py 2

CUDA_VISIBLE_DEVICES=0,1 PORT=29500 ./mmdetection/tools/dist_train.sh m1_configs_faster_rcnn_updated.py 2


CUDA_VISIBLE_DEVICES=0,1 PORT=29500 ./mmdetection/tools/dist_train.sh m1.py 2




CUDA_VISIBLE_DEVICES=2 PORT=29503 ./mmdetection/tools/dist_train.sh m3_configs_detr.py 1 # copied from narval