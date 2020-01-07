# -*- coding: utf-8 -*-

import uuid
import json
import os

from constants import BOOK_RAW_DATA_BUCKET_NAME, CHAPTER_RAW_DATA_BUCKET_NAME
from helpers import upload_file_to_google_storage


class BasePipeline(object):

    def __init__(self):
        self.bucket_name = ''
        super().__init__()

    def process_item(self, item, spider):
        file_name = uuid.uuid4().hex + '.json'
        with open(file_name, "w") as text_file:
            json_string = json.dumps(item)
            text_file.write(json_string)

        upload_file_to_google_storage(self.bucket_name, file_name, file_name)
        os.remove(file_name)

        return item


class TTVBookPipeline(BasePipeline):

    def __init__(self):
        super().__init__()
        self.bucket_name = BOOK_RAW_DATA_BUCKET_NAME


class TTVChapterPipeline(BasePipeline):

    def __init__(self):
        super().__init__()
        self.bucket_name = CHAPTER_RAW_DATA_BUCKET_NAME
