import os
import json

class DataReader:
    def __

    def all_ids_in_clip(clip_id):
        """
        Reads all entity IDs in clip from JSON
        :return: Set of IDs in video
        """
        json_path = os.path.join(args.videos_dir, '{}.json'.format(clip_id))

        with open(json_path) as f:
            data = json.load(f)

        ids = set()
        for frame in data['annotations']:
            for annotation in frame:
                ids.add(annotation[0])