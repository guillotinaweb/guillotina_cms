



async def test_tiles_endpoint_gives_us_registered_tiles(cms_requester):

  async with cms_requester as requester:
        # now test it...
        response, status = await requester('GET', '/db/guillotina/@tiles')
        assert status == 200
        assert len(response) >= 1
        assert '@tiles/' in response[0]['@id']

        response, status = await requester('GET', '/db/guillotina/@tiles/title')
        assert status == 200
        print(response)
        assert response["type"] == "object"
