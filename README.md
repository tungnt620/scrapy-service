# Note
* This is internal service, don't public
* Our's system run in background with upstart
* upstart config file at /etc/init/scrapyd.conf

```
init-checkconf /path/to/your.conf to check if your configuration is valid or not.
initctl start <service> to start the service
initctl stop <service> to stop the service
initctl restart <service> to restart the service
initctl status <service> to see the status your service, whether its stopped, running etc.
initctl reload-configuration is used after you created a new configuration to reload the configurations
initctl list to see the list of all registered services
initctl list | grep <service> to see if your service is registered or not
```
* log file at ```/var/log/upstart/service_name.log```

# Setup virtualenv
* pip3 install virtualenv
* virtualenv -p python3 virtualenv
* source virtualenv/bin/activate
* pip3 install Scrapy
    * Some dependency may need:
        * sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
        * sudo apt-get install python3 python3-dev
 * pip3 install -r requirements.txt


# Run
* ```scrapy crawl ttv_book -a redis_stream_name=abc -a book_url=https://truyen.tangthuvien.vn/doc-truyen/dai-y-lang-nhien -a id=1```
* ```scrapy crawl ttv_chapter -a redis_stream_name=abc -a book_url=https://truyen.tangthuvien.vn/doc-truyen/dai-y-lang-nhien -a book_id=2 -a chapter_num=2 -a old_chapter_id=1```
* ```scrapy crawl new_ttv_book -a redis_stream_name=abc2```

# Scrapy shell
* scrapy shell https://sadsa.com

# Website banned
* Use a like human user agent

## Setup
In order to run Scrapyd
````
$ cd scrapy_app
$ scrapyd
````

Scrapyd is running on: http://localhost:5000


At this point you will be able to send job request to Scrapyd. This project is setup with a demo spider from the oficial tutorial of scrapy. To run it you must send a http request to Scrapyd with the job info
````
curl http://localhost:5000/schedule.json -d project=default -d spider=toscrape-css
````

# Scrapyd-deploy
* Must upload file: ```/data/release/scrapy-service/google-cloud-key.json```
* list all target: ```scrapyd-deploy -l```
* target may use for scalable a system
* Config a target:
```[deploy:example]
url = http://scrapyd.example.com/api/scrapyd
username = scrapy
password = secret
```
* deploy to default target with default project
```
scrapyd-deploy
```

* deploy to all target
```
scrapyd-deploy -a -p <project>
```

* Schedule a spider
```
curl http://confession.vn:5000/schedule.json -d project=book -d spider=ttv_book -d book_url=https://truyen.tangthuvien.vn/doc-truyen/de-ba -d redis_stream_name=abc 
curl http://confession.vn:5000/schedule.json -d project=book -d spider=ttv_chapter -d book_url=https://truyen.tangthuvien.vn/doc-truyen/de-ba -d book_id=1 -d redis_stream_name=abc
```

* upload google-cloud-key.json file to server and set env
``` 
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/google-cloud-key.json"
```

## Deploy manual
```
git pull
pip3 install -r requirements.txt
reload scrapyd
```

# TODO
* Add is_full field to ttv_book
* Add basic authentication to config files
* Build logic notify when data crawl maybe incorrect