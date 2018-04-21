"""
Script for splitting labels into train and test set by clip_id
"""
import glob
import os
import shutil
from random import shuffle

_LABEL_DIR = 'data/labels'
_TRAIN_DIR = os.path.join(_LABEL_DIR, 'training')
_TEST_DIR = os.path.join(_LABEL_DIR, 'test')


def __make_dirs__():
    if not os.path.exists(_TRAIN_DIR):
        os.makedirs(_TRAIN_DIR)
    if not os.path.exists(_TEST_DIR):
        os.makedirs(_TEST_DIR)


def split_manually():
    train_list = ['-3K26M-m_00-7.json', '-7awJE4cqBk-12.json', '0ASj-PXYdjs-482.json', '0DfG444DXr0-47.json', '0NgLxOGQPPM-172.json', '1w5UhvYB0xA-373.json', '26V9UzqSguo-422.json', '288q24DJO6k-421.json', '2bKXv_XviFc-425.json', '2gUnD1u8WX0-473.json', '2qihpJVmGbc-487.json', '4G8J79arVBw-480.json', '4WZImk31njQ-196.json', '7cUS5EmqJio-461.json', '7iqnoz3zGUM-291.json', '8EjTUYek_Hw-416.json', '8gSZYiL8F6Q-477.json', '8ZWaQmjCmfk-412.json', '9vayXvWExAY-465.json', 'AEEma1sKBWQ-471.json', 'Aqko6DwEqq4-352.json', 'bEpc1i-9P88-484.json', 'brufeKyiK4k-463.json', 'Cft2VDsPCp4-356.json', 'eurKfWDMzYA-476.json', 'eVT7EtQPzf0-459.json', 'FkbfzgRNx4I-457.json', 'FQnhIjvKIZE-452.json', 'fWZkkDYTLSI-422.json', 'Gr0HpDM8Ki8-413.json', 'GT4CKnmIvdQ-369.json', 'Gvp-cj3bmIY-491.json', 'hENjgSV3bcA-461.json', 'iJiiV3_Rnok-481.json', 'Ly-uIzZCdn0-383.json', 'MtjZvZ8IlBA-466.json', 'N5UD8FGzDek-447.json', 'nt3D26lrkho-413.json', 'NuOiKCBO1hU-424.json', 'qtH5rI9Q1no-451.json', 'RfikfB1PflA-407.json', 'RNjt7MkyZTY-469.json', 'SlWhMdqRRpo-488.json', 'TNSuTEJcxjA-456.json', 'Ub4x0R21R-M-414.json', 'uDU6c9eNvO8-475.json', 'ukMFR0IQ3Yc-200.json', 'UrsCy6qIGoo-490.json', 'VgZW62uxRGk-450.json', 'Vmef_8MY46w-446.json', 'VxTS1mJyhig-460.json', 'wuPXIr9yCdY-455.json', 'Xbw_9hrp2KY-420.json', 'Y6Asp_FtgRA-424.json', 'YKcRcia_DSc-454.json', 'ZY2U35eiP6s-483.json', '_7bYuV6C-P4-489.json', '_x8FdEXh_Tg-425.json']
    __make_dirs__()
    for p in train_list:
        shutil.move(os.path.join(_LABEL_DIR, p), os.path.join(_TRAIN_DIR, p))


def main():
    label_paths = glob.glob(os.path.join(_LABEL_DIR, '*.json'))

    assert len(label_paths) > 0

    shuffle(label_paths)

    split_idx = round(len(label_paths) * 0.8)

    train_paths = label_paths[:split_idx]
    test_paths = label_paths[split_idx:]

    __make_dirs__()

    for p in train_paths:
        file_name = os.path.basename(p)
        shutil.move(p, os.path.join(_TRAIN_DIR, file_name))

    for p in test_paths:
        file_name = os.path.basename(p)
        shutil.move(p, os.path.join(_TEST_DIR, file_name))


if __name__ == '__main__':
    # main()
    split_manually()
