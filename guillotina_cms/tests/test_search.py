import pytest
import json
from guillotina_cms.tests.utils import add_content
from guillotina.tests.test_catalog import PG_CATALOG_SETTINGS, NOT_POSTGRES

pytestmark = pytest.mark.asyncio


@pytest.mark.app_settings(PG_CATALOG_SETTINGS)
@pytest.mark.skipif(NOT_POSTGRES, reason="Only PG")
async def test_search(cms_requester):
    async with cms_requester as requester:
        await add_content(requester)
        resp, status = await requester("GET", "/db/guillotina/@search")
        assert resp["items_total"] == 22

        resp, status = await requester(
            "GET", "/db/guillotina/@search?path__starts=cms-folder0&depth__gte=1"
        )
        # Folder included
        assert resp["items_total"] == 11

        resp, status = await requester(
            "GET", "/db/guillotina/@search?path__starts=cms-folder0&depth__gte=2"
        )
        assert resp["items_total"] == 10

        assert resp["items"][0]["is_folderish"]
        resp, status = await requester(
            "GET", "/db/guillotina/@search?text__in=needs&portal_type=Document&_size=30"
        )
        assert resp["items_total"] == 20

        resp, status = await requester(
            "GET", "/db/guillotina/cms-folder0/document-3/@navigation"
        )
        assert len(resp["items"]) == 2

        resp, status = await requester(
            "PATCH",
            "/db/guillotina/cms-folder0",
            data=json.dumps(
                {
                    "title": "Hidden doc",
                    "guillotina_cms.interfaces.base.ICMSBehavior": {
                        "hidden_navigation": True
                    },
                }
            ),
        )
        assert status == 204

        resp, status = await requester(
            "GET", "/db/guillotina/cms-folder0/document-3/@navigation"
        )
        assert len(resp["items"]) == 1
