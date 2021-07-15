FROM python:3.7-buster

LABEL maintainer="fabio.beranizo@gmail.com"

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./url_downloader /app/url_downloader
COPY ./setup.py /app/setup.py

WORKDIR /app/

EXPOSE 8000

ENTRYPOINT ["uvicorn", "url_downloader.app:app"]
CMD ["--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
