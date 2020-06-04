FROM python:3
MAINTAINER Your Name "pangestu@alterra.id"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirement.txt
WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
