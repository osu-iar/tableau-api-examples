FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --disable-pip-version-check --root-user-action=ignore --upgrade pip

COPY python/* ./
RUN pip install --disable-pip-version-check --root-user-action=ignore --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "/app/tableau-to-csv.py"]
