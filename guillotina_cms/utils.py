import json

from guillotina.db.interfaces import IPostgresStorage
from guillotina.transactions import get_transaction


async def get_last_child_position(folder):
    txn = get_transaction()
    if not IPostgresStorage.providedBy(txn.storage):
        return await folder.async_len()
    conn = await txn.get_connection()
    results = await conn.fetch('''select json from {}
WHERE parent_id = $1 AND of IS NULL
ORDER BY (json->>'position_in_parent')::int DESC
limit 1'''.format(txn.storage._objects_table_name), folder._p_oid)
    if len(results) > 0:
        item = json.loads(results[0]['json'])
        return item.get('position_in_parent', 0)
    return -1