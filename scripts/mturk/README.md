This folder contains scripts used for interacting with the AMT API.

## Installation

* Setup the API keys in `../../.env`

```
pip install python-dotenv boto3
```

## Launch HITs

Edit the `videoIds` to be annotated to annotate in `launch.py`

```
python -m scripts.mturk.launch
```

## Import labels from AMT

```
python -m scripts.mturk.import
```
