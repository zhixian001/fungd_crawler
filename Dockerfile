FROM python:3.8.0-alpine

WORKDIR /crawler

COPY . .

ENV OUTPUT_FILE_NAME=output.txt

VOLUME [ "/output" ]

RUN pip3 install -r requirements.txt && \
    chmod ug+x ./linux_launch.sh && \
    mv "./${OUTPUT_FILE_NAME}" "/output/${OUTPUT_FILE_NAME}"


ENTRYPOINT [ "./linux_launch.sh" ]

