FROM python:3

WORKDIR /authentication
COPY ./app/authentication/ /authentication
RUN pip install -r requirements.txt

RUN chmod u+x main.py

EXPOSE 8001
EXPOSE 8081

ENTRYPOINT [ "python" ]
CMD ["main.py"]