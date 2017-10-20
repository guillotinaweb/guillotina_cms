FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install aiohttp_autoreload
RUN pip install aiomonitor

COPY . .
# RUN pip install --no-cache-dir -r pastanaga/requirements.txt

RUN python setup.py develop

CMD [ "guillotina", "--monitor", "--profile", "--profile-output=/usr/src/app/kk.output" ]
