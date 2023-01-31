FROM python AS runtime
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN apt update
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .