import json
import asyncio

async def add_content(requester, num_folders=10, num_items=10, base_id='cms-'):
    path = '/db/guillotina/'
    created = 0
    for fidx in range(num_folders):
        folder_id = f'{base_id}folder{str(fidx)}'
        resp, status = await requester(
            'POST',
            path,
            data=json.dumps({
                '@type': 'Folder',
                'title': 'Folder' + str(fidx),
                'id': folder_id
            })
        )
        created += 1
        assert status == 201
        path += '/' + folder_id
        for idx in range(num_items):
            resp, status = await requester(
                'POST',
                path,
                data=json.dumps({
                    '@type': 'Document',
                    'title': 'Document' + str(idx)
                })
            )
            created += 1
            assert status == 201
    await asyncio.sleep(1)  # make sure async index tasks finish
    return created