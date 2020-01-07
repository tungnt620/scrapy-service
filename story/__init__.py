import os

if os.environ["IS_DEV"]:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nguyentung/Downloads/google-cloud-key.json"
else:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/data/release/scrapy-service/google-cloud-key.json"
