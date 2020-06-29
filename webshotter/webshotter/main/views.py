from typing import Dict

import json
import os
import shlex
import subprocess
import uuid

import aiohttp_jinja2
import markdown2
from aiohttp import web

from webshotter.constants import PROJECT_DIR
from webshotter.main.tables import screenshots_tbl
from webshotter.utils.db import select_screenshot_by_id, select_last_50_screenshots


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Dict[str, str]:
    with open(PROJECT_DIR / 'README.md') as f:
        text = markdown2.markdown(f.read())

    return {"text": text}


async def handle(request):
    """
    Отправка данных через POST:
        curl -X POST http://127.0.0.1:8080 -d '{"url_list": ["https://ya.ru"]}'
    Ответ:
        {"status": "success", "token": "d744a5ba-13cc-4faf-a35f-70a0cb03fd4e"}
    :param request:
    :return:
    """
    data = await request.json()
    # print(data)
    url_list = data['url_list']
    token = str(uuid.uuid4())
    output_directory = os.path.join("/tmp/webshotter/", token)
    os.makedirs(output_directory)
    app = request.app
    for url in url_list:
        screenshot_filename = str(uuid.uuid4()) + '.png'
        screenshot_path = os.path.join(output_directory, screenshot_filename)
        async with app['db'].acquire() as conn:
            await conn.execute(screenshots_tbl.insert().values(token=token, url=url, picture_name=screenshot_filename))

        command = f"phantomjs " \
                  f"--ignore-ssl-errors=true " \
                  f"--ssl-protocol=any " \
                  f"--ssl-ciphers=ALL " \
                  f"{ app['config']['WEBSCREENSHOTJS_PATH'] } " \
                  f"url_capture={url} " \
                  f"output_file={screenshot_path}"
        # print(command)
        p = subprocess.Popen(shlex.split(command, posix=True), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    response_obj = {'status': 'success', 'token': token}
    return web.Response(text=json.dumps(response_obj), status=200)



@aiohttp_jinja2.template('screenshots.html')
async def screenshots(request):
    """
    Получение скриншота через GET:
        curl -X GET http://127.0.0.1:8080/?screenshot_id=1 --output /tmp/1.png
    :param request:
    :return:
    """
    app = request.app
    if 'screenshot_id' in request.rel_url.query.keys():
        screenshot_id = request.rel_url.query['screenshot_id']
        async with app['db'].acquire() as conn:
            screenshot_obj = await select_screenshot_by_id(conn, screenshot_id)

        screenshot_path = output_directory = os.path.join("/tmp/webshotter/", screenshot_obj.token, screenshot_obj.picture_name)
        try:
            screenshot = open(screenshot_path, 'br')
            return web.Response(body=screenshot, content_type="image/png", headers={'Content-Disposition': ''})
        except:
            return web.Response(text='not found', status=404)
    else:
        async with app['db'].acquire() as conn:
            screenshots_list = await select_last_50_screenshots(conn)
        return {"screenshots_list": screenshots_list}
