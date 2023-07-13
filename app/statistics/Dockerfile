FROM python:3

WORKDIR /statistics
COPY ./app/statistics /statistics
RUN pip install -r requirements.txt

RUN chmod u+x main.py

EXPOSE 8003
EXPOSE 8083

ENTRYPOINT [ "python" ]
CMD ["main.py"]
