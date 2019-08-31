FROM python:3

WORKDIR /app

ADD app /app
RUN python -m pip install -r requirements.txt
ENTRYPOINT ["/bin/bash"] 
