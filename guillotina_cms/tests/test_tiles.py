



async def test_tiles_endpoint_gives_us_registered_tiles(cms_requester):

  async with cms_requester as requester:
        # now test it...
        response, status = await requester('GET', '/db/guillotina/@tiles')
        assert status == 200


