
## Detectron

### Inference

https://github.com/Mastergalen/Detectron

```
python2 tools/infer_simple.py \
    --cfg configs/12_2017_baselines/e2e_mask_rcnn_X-101-32x8d-FPN_1x.yaml \
    --output-dir /tmp/detectron-visualizations \
    --image-ext jpg \
    --wts https://s3-us-west-2.amazonaws.com/detectron/36761843/12_2017_baselines/e2e_mask_rcnn_X-101-32x8d-FPN_1x.yaml.06_35_59.RZotkLKI/output/train/coco_2014_train%3Acoco_2014_valminusminival/generalized_rcnn/model_final.pkl \
    demo
```