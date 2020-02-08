FROM python:3.5

WORKDIR /project
ENV HOME /project
EXPOSE 5000

COPY ./requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt -i https://pypi.doubanio.com/simple/

VOLUME /project
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod 775 /entrypoint.sh && chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]