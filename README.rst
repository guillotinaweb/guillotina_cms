.. contents::

GUILLOTINA_CMS
==============

WIP: This package is a work in progress to provide CMS on guillotina

Bundle of cms functionality for guillotina

Bootstrap dev
-------------

docker-compose create
git submodule init pastanaga
git submodule init plone-react
git submodule update pastanaga
git submodule update plone-react
docker-compose start postgres

Compile Pastanaga
-----------------

Using yarn::

    cd pastanaga
    yarn install
    npm run build
    cd ..

Compile Plone React
-------------------

Using yarn::

    cd plone-react
    yarn install
    npm run build
    cd ..


Run dev
-------

docker-compose run --service-ports guillotina
