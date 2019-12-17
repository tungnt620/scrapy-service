# -*- coding: utf-8 -*-

import uuid
import json
import os

from constants import STORY_RAW_DATA_BUCKET_NAME
from helpers import upload_file_to_google_storage


class StoryPipeline(object):
    def process_item(self, item, spider):
        file_name = uuid.uuid4().hex + '.json'
        with open(file_name, "w") as text_file:
            json_string = json.dumps(item)
            text_file.write(json_string)

        upload_file_to_google_storage(STORY_RAW_DATA_BUCKET_NAME, file_name, file_name)
        os.remove(file_name)

        return item
