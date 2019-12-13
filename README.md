# Setup virtualenv
* pip3 install virtualenv
* virtualenv -p python3 virtualenv
* source virtualenv/bin/activate
* pip3 install Scrapy
    * Some dependency may need:
        * sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
        * sudo apt-get install python3 python3-dev
 * pip3 install -r requirements.txt
 

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


# TODO
* Add basic authentication to config files