FROM python:3.9-slim AS bigimage
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install git build-essential software-properties-common ninja-build -y && python -m pip install --upgrade pip && \
      pip wheel --wheel-dir=/root/wheels -r /app/requirements.txt --timeout 120 && \
      pip wheel --wheel-dir=/root/wheels 'git+https://github.com/facebookresearch/fvcore' --timeout 120 && \
      pip install --no-index --find-links=/root/wheels torch torchvision fvcore --timeout 120 && \
      pip wheel --wheel-dir=/root/wheels 'git+https://github.com/facebookresearch/detectron2' --timeout 120


FROM python:3.9-slim AS smallimage
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY --from=bigimage /root/wheels /root/wheels
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install git ffmpeg libsm6 libxext6 x265 libx265-dev wget -y && python -m pip install --upgrade pip && pip install \
      --no-index \
      --find-links=/root/wheels --no-cache-dir -r /app/requirements.txt && \
      pip install --no-index --find-links=/root/wheels --no-cache-dir fvcore detectron2

# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
