
FROM python:3.6

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# code setup and package installation
RUN mkdir /code
WORKDIR /code
COPY . /code/
ENV CONFIG_PATH /code/config_dev
RUN apt-get update && apt-get install -y \
	zlib1g-dev \
	libjpeg-dev \
	python3-pythonmagick \
	inkscape \
	xvfb \
	poppler-utils \
	libfile-mimeinfo-perl \
	qpdf \
	libimage-exiftool-perl \
	ufraw-batch \
	ffmpeg

RUN pip3 install -r requirements.txt

