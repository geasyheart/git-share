FROM python

MAINTAINER zy

RUN mkdir -pv /srv/git-share

WORKDIR /srv/git-share

RUN mkdir /logs
RUN mkdir logs

COPY app ./app
COPY manager.py ./manager.py
COPY requirements.txt ./requirements.txt
COPY gun_conf.py ./gun_conf.py


RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["gunicorn","-c","gun_conf.py", "manager:app"]

# docker run  -d -p 127.0.0.1:3000:80 --name git-share -v /var/logs/gunicorn/logs:/logs -v /srv/git-share/logs:/srv/git-share/logs -v /srv/git-share/settings.py:/tmp/git-share.py -e "GIT_SHARE_ENV=/tmp/git-share.py" zy/git-share:v1
