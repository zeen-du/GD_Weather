FROM python:3.7.10-slim

EXPOSE 8080

COPY ./ /weather

WORKDIR /weather

RUN /usr/local/bin/python -m pip install -i https://mirrors.cloud.tencent.com/pypi/simple --upgrade pip
RUN pip install -i https://mirrors.cloud.tencent.com/pypi/simple .

CMD ["python", "-m", "gd_weather"]