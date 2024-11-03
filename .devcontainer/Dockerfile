FROM mcr.microsoft.com/devcontainers/python:1-3.12

COPY ./requirements.txt /

COPY ./.devcontainer/entrypoint.sh /entrypoint.sh

WORKDIR /workspace

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["sleep infinity"]