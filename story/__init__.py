import os

if os.environ.get('IS_DEV', False):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nguyentung/Downloads/google-cloud-key.json"
else:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/data/release/scrapy-service/google-cloud-key.json"
