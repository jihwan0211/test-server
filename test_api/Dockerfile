FROM python:3.6

RUN apt-get update
#RUN apt-get install -y uwsgi redis-server

#RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
#	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
#	&& apt-get update \
#	&& apt-get install -y ca-certificates nginx gettext-base \
#	&& rm -rf /var/lib/apt/lists/*
#RUN ln -sf /dev/stdout /var/log/nginx/access.log \
#	&& ln -sf /dev/stderr /var/log/nginx/error.log

#RUN rm /etc/nginx/nginx.conf
#COPY nginx.conf /etc/nginx/
#RUN echo "daemon off;" >> /etc/nginx/nginx.conf
#COPY uwsgi.ini /etc/uwsgi/

#RUN apt-get update && apt-get install -y supervisor \
#&& rm -rf /var/lib/apt/lists/*

#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p /test_api
WORKDIR /test_api

COPY ./api /test_api
RUN pip install --no-cache-dir -r requirements.txt

#CMD ["supervisord", "-n"]
#EXPOSE 80

ENTRYPOINT ["python"]
CMD ["application.py"]
EXPOSE 5000
