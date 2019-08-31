FROM python:3

WORKDIR /

ADD app /
RUN python -m pip install -r requirements.txt
ENTRYPOINT ["/bin/bash"] 
