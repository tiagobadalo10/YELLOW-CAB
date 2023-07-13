FROM python:3

WORKDIR /zones
COPY ./app/zones /zones
RUN pip install -r requirements.txt

RUN chmod u+x main.py

EXPOSE 8051
EXPOSE 50051

ENTRYPOINT [ "python" ]
CMD ["main.py"]