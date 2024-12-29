FROM python:3.12-slim AS bigimage
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
      pip wheel --wheel-dir=/root/wheels -r /app/requirements.txt --timeout 120


FROM python:3.12-slim AS smallimage
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=bigimage /root/wheels /root/wheels
COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip && pip install \
      --no-index \
      --find-links=/root/wheels --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
