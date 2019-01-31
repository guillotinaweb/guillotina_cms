from guillotina import configure
from guillotina.interfaces import IDatabaseInitializedEvent
from guillotina.db.interfaces import IPostgresStorage


statements = [
    """CREATE INDEX IF NOT EXISTS objects_pos_in_parent
ON {} (((json->>'position_in_parent')::int) DESC)""",
    """CREATE INDEX IF NOT EXISTS objects_pos_in_parent_asc
ON {} (((json->>'position_in_parent')::int) ASC)"""
]


@configure.subscriber(for_=IDatabaseInitializedEvent)
async def db_initialized(event):
    '''
    Initialize additional pg indexes
    '''
    storage = event.database.storage
    if not IPostgresStorage.providedBy(storage):
        return

    # create json data indexes
    async with storage.lock:
        for statement in statements:
            await storage.read_conn.execute(
                statement.format(storage._objects_table_name))
