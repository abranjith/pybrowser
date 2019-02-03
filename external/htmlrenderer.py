import os
import asyncio
from pyppeteer import launch
from ..log_adapter import get_logger
from ..common_utils import get_user_home_dir, add_to_osenv
from ..constants import CONSTANTS

def render_html(url=None, html=None, get_text=False, script=None, reload=False, wait_time=5, timeout=10):
    result, content = None, None
    _set_env()
    try:
        result, content = asyncio.get_event_loop().run_until_complete(_render(url, html, get_text, reload, wait_time, timeout))
    except IOError as e:
        get_logger().error(f"Error in render_html method - {str(e)}")
        #print({str(e)})
    return result, content

def _set_env():
    d = os.path.join(get_user_home_dir(), CONSTANTS.DIR_NAME, CONSTANTS.PYPPETEER_HOME)
    add_to_osenv('PYPPETEER_HOME', d)

async def _render(url=None, html=None, get_text=False, script=None, reload=False, wait_time=5, timeout=10):
    page = None
    result, content = None, None
    try:
        browser = await launch(ignoreHTTPSErrors=True, headless=True)
        page = await browser.newPage()
        await asyncio.sleep(wait_time)
        if reload and url:
            await page.goto(url, options={'timeout': int(timeout * 1000), 'waitUntil': ['domcontentloaded', 'load']})
        elif html:
            await page.goto(f'data:text/html,{html}', options={'timeout': int(timeout * 1000), 'waitUntil': ['domcontentloaded', 'load']})
        elif url:
            await page.goto(url, options={'timeout': int(timeout * 1000), 'waitUntil': ['domcontentloaded', 'load']})
        #await page.screenshot({'path': 'example.png'})
        if script:
            result = await page.evaluate(script)
        if get_text:
            content = await page.evaluate('document.body.textContent')
        else:
            #content = await page.evaluate('document.body.outerHTML')
            content = await page.content()
        if page:
            await page.close()
            page = None
    except Exception as e:
        if page:
            await page.close()
            page = None
    return result, content

if __name__ == "__main__":
    result, content = render_html("http://selenium-release.storage.googleapis.com/index.html?path=3.14/")
    print(content)
