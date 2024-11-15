FROM python:3.13-alpine

LABEL org.opencontainers.image.description="Image with TfUtility. Build for amd64 Architecture based on Alpine."
LABEL org.opencontainers.image.licenses=AGPLv3
LABEL org.opencontainers.image.source=https://github.com/eieste/tfutility


LABEL MAINTAINER="Stefan Eiermann <foss@ultraapp.de>"
ENV PS1="\[\e[0;33m\]|> tfutility <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir -r requirements.txt \
    && python setup.py install
WORKDIR /
ENTRYPOINT ["tfutility"]
