### git-share:


#### Description

A Full-featured forum software built with Flask and MongoDB for share interesting project，Now has been deploy on[git-share](http://www.git-share.com)


### Installation

* add settings.py in app

```python

import os

SECRET_KEY = "secret-key"

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

MODE = 'DEV' # 'DEV' or 'CORE'

ERRORLOG_ENABLE = True
ERRORLOG_FILE = 'logs/error.log'

MONGODB_SETTINGS = 'mongodb://zy:123456@127.0.0.1:27017/zy?authSource=admin' # logs

# Geetest 
GEETEST_ID = ""
GEETEST_KEY = ""

# login
COOKIE_NAME = "YOUR_KEY"
COOKIE_MAX_AGE = 10000 

SENDER = {"email": "", "password": ""}

GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""

GITHUB_CALLBACK = ""
SENTRY_DSN = ''


```

* install requirements

```python

pip3 install -r requirements.txt

```


### Deployment

* run server[dev]

```bash

python3 manager.py

```

* Docker[core]

```bash

cd ~/git-share
docker build -t gs/git-share:v1 .
docker run  -d -p 127.0.0.1:3000:80 --name git-share-v1 -v /var/logs/gunicorn/logs:/logs \
                                                        -v /srv/git-share/logs:/srv/git-share/logs \
                                                        -v /srv/git-share/settings.py:/tmp/git-share.py \
                                                        -e "GIT_SHARE_ENV=/tmp/git-share.py" gs/git-share:v1

```



