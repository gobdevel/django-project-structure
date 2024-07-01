FROM python:3.10.9-slim

COPY . /project
WORKDIR /project

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements/production.txt && \
    chmod +x scripts/entrypoint.sh

CMD ["/project/scripts/entrypoint.sh"]