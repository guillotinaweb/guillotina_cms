.. contents::

GUILLOTINA_CMS
==============

WIP: This package is a work in progress to provide CMS on guillotina

Bundle of cms functionality for guillotina

Bootstrap dev
-------------

docker-compose create
git submodule init
git submodule update


Compile Pastanaga
-----------------

Using yarn::

    cd pastanaga-angular
    yarn install
    ng build --base-href /pastanage/
    cd ..



Compile Angular SDK
-------------------

Using yarn::

    cd plone-angular-demo
    yarn install
    ng build --base-href /ng/
    cd ..

Prepare Docker env
------------------

MacOS:

    screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
    sysctl -w vm.max_map_count=262144
    (to exit Ctrl + a + d)

Start Docker Background
-----------------------

    docker-compose create
    docker-compose start cockroachdb
    docker-compose start cockroachdb2
    docker-compose start elasticsearch
    docker exec -it guillotina_cms_cockroachdb_1 /cockroach/cockroach sql --insecure --execute="CREATE DATABASE guillotina;"

Run dev
-------

docker-compose run --service-ports guillotina


Add CMS container
-----------------

curl -X POST --user root:root http://localhost:8081/db -d '{"@type": "Container", "id": "web", "title": "Plone Site"}'

curl -X POST --user root:root http://localhost:8081/db/web/@addons -d '{"id": "cms"}'


Running Plone React
-------------------

Using yarn on a new terminal::

    cd plone-react
    yarn install
    npm run dev

    access http://localhost:4300