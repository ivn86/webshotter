FROM python:3.7

WORKDIR /app
ARG requirements=requirements/production.txt

ADD . /app
RUN cd /opt/ && wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && tar xvf phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN ln -s /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs


RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -r $requirements
