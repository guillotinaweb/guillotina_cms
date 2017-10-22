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
docker-compose start postgres

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


Run dev
-------

docker-compose run --service-ports guillotina


Add CMS container
-----------------

curl -X POST --user root:root http://localhost:8080/db -d '{"@type": "Container", "id": "web", "title": "Plone Site"}'

curl -X POST --user root:root http://localhost:8080/db/web/@addons -d '{"id": "cms"}'


Running Plone React
-------------------

Using yarn on a new terminal::

    cd plone-react
    yarn install
    npm run dev

    access http://localhost:4300