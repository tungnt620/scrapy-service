# Note
* This is internal service, don't public
* Our's system run in background with upstart
* upstart config file at /etc/init/scrapy.conf
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
*  export GOOGLE_APPLICATION_CREDENTIALS="/Users/nguyentung/Downloads/google-cloud-key.json"
* ```scrapy crawl tangthuvien -a story_url=https://truyen.tangthuvien.vn/doc-truyen/quy-bi-chi-chu -a chapter_number=1```

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
curl http://confession.vn:5000/schedule.json -d project=default -d spider=tangthuvien -a story_url=https://tangthuvien.vn/lablalslaldlsalds -a chapter=2
```

* upload google-cloud-key.json file to server and set env
``` 
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/google-cloud-key.json"
```

# TODO
* Add basic authentication to config files