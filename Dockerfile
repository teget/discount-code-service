FROM python:3.9
ADD . /discount-code-service
WORKDIR /discount-code-service
RUN pip install -r requirements.txt
EXPOSE 5000