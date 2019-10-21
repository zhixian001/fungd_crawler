FROM python:3.8.0-alpine

WORKDIR /crawler

COPY . .

ENV OUTPUT_FILE_NAME=output.txt

RUN pip3 install -r requirements.txt && \
    chmod ug+x ./linux_launch.sh && \
    mkdir /output && \
    mv ./output.txt /output/output.txt

VOLUME [ "/output" ]

ENTRYPOINT [ "sh", "-c" ]
# entrypoint script's arg
CMD [ "./linux_launch.sh", "/output/${OUTPUT_FILE_NAME}"]
