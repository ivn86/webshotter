from aiopg.sa import SAConnection as SAConn

from webshotter.main.tables import screenshots_tbl


async def select_screenshot_by_id(conn: SAConn, pk: int):
    cursor = await conn.execute(
        screenshots_tbl.select().where(screenshots_tbl.c.id == pk)
    )
    item = await cursor.fetchone()
    return item


async def select_last_50_screenshots(conn: SAConn):
    cursor = await conn.execute(
        screenshots_tbl.select().order_by(screenshots_tbl.c.id.desc()).limit(50)
    )
    items = await cursor.fetchall()
    return items
