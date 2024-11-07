FROM python:3.13-alpine
LABEL MAINTAINER="Stefan Eiermann <foss@ultraapp.de>"
ENV PS1="\[\e[0;33m\]|> tfutils <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir -r requirements.txt \
    && python setup.py install
WORKDIR /
ENTRYPOINT ["tfutils"]
