FROM python:3.8.5-alpine

# Prevent writeing pyc files to disk
ENV PYTHONUNBUFFERED 1
# Prevent python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1

# Install Required Packages
RUN apk update && apk add nano && pip install --upgrade pip
RUN apk add --no-cache build-base
RUN apk add --no-cache build-base libffi-dev

WORKDIR /usr/src/candidate_profiles

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "8000"]
