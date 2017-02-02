FROM python:3
ADD dev-requirements.txt /tmp
ADD test-requirements.txt /tmp
ADD requirements.txt /tmp
RUN pip install -r /tmp/dev-requirements.txt
RUN pip install -r /tmp/test-requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /app
