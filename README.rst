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


Running Plone React
-------------------

Using yarn on a new terminal::

    cd plone-react
    yarn install
    npm run dev

    access http://localhost:4300