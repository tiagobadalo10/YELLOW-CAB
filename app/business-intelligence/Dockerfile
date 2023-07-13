FROM python:3

WORKDIR /business-intelligence
COPY ./app/business-intelligence /business-intelligence
RUN pip install -r requirements.txt

RUN chmod u+x main.py

EXPOSE 8002
EXPOSE 8082

ENTRYPOINT [ "python" ]
CMD ["main.py"]