import os
import json


class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.clips_dir = os.path.join(data_dir, 'clips')

    def all_ids_in_clip(self, clip_id):
        """
        Reads all entity IDs in clip from JSON
        :return: Set of IDs in video
        """
        json_path = os.path.join(self.clips_dir, '{}.json'.format(clip_id))

        with open(json_path) as f:
            data = json.load(f)

        ids = set()
        for frame in data['annotations']:
            for annotation in frame:
                ids.add(annotation[0])

        return list(ids)

    def write(self, folder, filename, data):
        write_dir = os.path.join(self.data_dir, folder)
        write_path = os.path.join(write_dir, filename)

        if not os.path.exists(write_dir):
            os.makedirs(write_dir)

        with open(write_path, 'w') as fp:
            json.dump(data, fp)
