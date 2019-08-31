FROM python:3

WORKDIR /

ADD app /app
RUN python -m pip install -r /app/requirements.txt
ENTRYPOINT ["/bin/bash"] 
