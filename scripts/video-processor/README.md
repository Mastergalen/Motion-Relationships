These scripts perform all the preprocessing needed before videos are ready for annotation.

It uses Mask-CNN for object detection, retrieves the bounding boxes, and then applies the Hungarian algorithm for tracking.

## Installation

Install all the dependencies and clone our fork of Detectron.

```
cd ~
pip3 install -r requirements.txt
sudo apt-get install ffmpeg python3-tk
git clone git@github.com:Mastergalen/Detectron.git my-detectron
```

## Download YouTube Videos

Run this script to download all 5s clips specified in `videos_to_annotate.csv` into the `./downloads` folder.

```
python3 download_youtube.py
```

## Run Detectron

This will run the object detection network on all frames and apply the tracker.

```
python3 bounding_box_generator.py
```

### Manual Inference

```
python2 tools/infer_simple.py \
    --cfg configs/12_2017_baselines/e2e_mask_rcnn_X-101-32x8d-FPN_1x.yaml \
    --output-dir /tmp/detectron-visualizations \
    --image-ext jpg \
    --wts https://s3-us-west-2.amazonaws.com/detectron/36761843/12_2017_baselines/e2e_mask_rcnn_X-101-32x8d-FPN_1x.yaml.06_35_59.RZotkLKI/output/train/coco_2014_train%3Acoco_2014_valminusminival/generalized_rcnn/model_final.pkl \
    videoframes
```

## Correcting ID mismatches

Run the utility script for manually correcting ID mismatches.

```
python fix_tracking.py 
```
