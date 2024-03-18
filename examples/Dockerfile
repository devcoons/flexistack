FROM python:3.11.7-slim-bookworm AS base-slim 
RUN apt-get update --fix-missing
RUN apt-get upgrade -y
RUN apt-get install -y libgcrypt20 zlib1g nano 

FROM base-slim AS base-full
RUN apt-get install -y build-essential gcc g++ cmake make libgcrypt20-dev zlib1g-dev libssl-dev libffi-dev python3-dev cargo pkg-config
RUN apt-get update --fix-missing

FROM base-full AS compile-image 
RUN python -m venv /opt/venv --system-site-packages 
ENV PATH="/opt/venv/bin:$PATH" 
WORKDIR /tmp 
COPY "application/." /tmp/app 
WORKDIR "/tmp/app" 
RUN pip install flexistack

RUN python __main__.py -v

FROM base-slim 
COPY --from=compile-image /opt/venv /opt/venv 
WORKDIR "/opt"  
COPY "application/." ./app   
WORKDIR "/opt/app"   
ENV PATH="/opt/venv/bin:$PATH"   
RUN echo 'python /opt/app/__main__.py "$@"' >> /usr/bin/dummy-app  
RUN chmod +x /usr/bin/dummy-app   
ENTRYPOINT ["tail", "-f", "/dev/null"]   
