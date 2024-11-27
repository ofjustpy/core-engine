import asyncio
import inspect
import json
import logging
import os
import sys
import typing
import contextlib
import databases


from .jpcore import jpconfig as jpconfig
from .jpcore import AppDB
from .jpcore.justpy_app import cookie_signer
from .jpcore.justpy_app import handle_event
from .jpcore.justpy_app import JustpyAjaxEndpoint
from .jpcore.justpy_app import JustpyApp
from .jpcore.justpy_app import template_options
from .jpcore.utilities import create_delayed_task
from .jpcore.utilities import run_task
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.responses import HTMLResponse
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from .session_middleware import  SessionMiddleware
#from starlette.middleware.sessions import SessionMiddleware
from oj_signing_middleware import SerializedSignedCookieMiddleware

from starlette.middleware.base import BaseHTTPMiddleware



    
#
# globals
#
current_module = sys.modules[__name__]
current_dir = os.path.dirname(current_module.__file__)
if jpconfig.VERBOSE:
    print(current_dir.replace("\\", "/"))
    print(f"Module directory: {current_dir}, Application directory: {os.getcwd()}")

    

    # create a middleware


            
def cookie_cfg(cookie_name,
               state_attr_name = None,
               max_age = 14 * 24 * 60 * 60,  # 14 days, in seconds
               path="/",
               domain=None,
               secure = False,
               httponly = False,
               samesite= "lax"
               ):

    if not state_attr_name:
        state_attr_name = cookie_name
    return {
            "state_attr_name": state_attr_name,
            "cookie_name": cookie_name,
            "max_age": cookie_ttl,
            "properties": {
                "path": "/",
                "domain": None,
                "secure": False,
                "https_only": False,
                "samesite": samesite,
            },
        }
        

    
def build_app(
    middlewares=None,
    APPCLASS=JustpyApp,
    startup_func=None,
        shutdown_func = None, 
    cookie_signer_secret_keys=[],
    cookie_cfg_iter=[
    ],
        
        middlewares_suffix = None,
        lifespans = [],
        **kwargs
):
    """
    middlewares_suffix: Put cors middleware here. It is required that CORS is the last middleware, otherwise won't work. See https://github.com/fastapi/fastapi/issues/1663
    """
    if not middlewares:
        middlewares = []
    # middlewares.append(Middleware(GZipMiddleware))
    if jpconfig.SSL_KEYFILE and jpconfig.SSL_CERTFILE:
        middlewares.append(Middleware(HTTPSRedirectMiddleware))

    # JustpyApp instance will maintain the list of cookie state attribute names.
    # This is passed on to WebPage_TF:CookieMixin to initialize request.state.
    cookie_state_attr_names = []

    if jpconfig.USE_COOKIE_MIDDLEWARE:
        for secret_key, cookie_cfg in zip(cookie_signer_secret_keys, cookie_cfg_iter):
            middlewares.append(
                Middleware(
                    SerializedSignedCookieMiddleware,
                    secret=secret_key,
                    state_attribute_name=cookie_cfg["state_attr_name"],
                    cookie_name=cookie_cfg["cookie_name"],
                    max_age=cookie_cfg["max_age"],
                    path = cookie_cfg["properties"]["path"], 
                    same_site = cookie_cfg["properties"]["samesite"],
                    https_only = cookie_cfg["properties"]["https_only"],
                    domain = cookie_cfg["properties"]["domain"]
                )
            )
            cookie_state_attr_names.append(cookie_cfg["state_attr_name"])
    # @TODO
    # implement https://github.com/justpy-org/justpy/issues/535

    if jpconfig.SESSIONS:
        middlewares.append(Middleware(SessionMiddleware, session_cookie = jpconfig.SESSION_COOKIE_NAME,
                                      secret_key=jpconfig.SECRET_KEY))



    if middlewares_suffix:
        middlewares.extend(middlewares_suffix)


    @contextlib.asynccontextmanager
    async def lifespan(app):
        AppDB.loop = asyncio.get_event_loop()
        # invoke other lifespances
        for alifespan in lifespans:
            await alifespan.__anext__()
            
        yield

        for alifespan in lifespans:
            try:
                await alifespan.__anext__()
            except StopAsyncIteration:
                pass  # This is expected after the first yield

                
            

    app = APPCLASS(
        middleware=middlewares,
        debug=jpconfig.DEBUG,
        cookie_state_attr_names=cookie_state_attr_names,
        lifespan=lifespan,
        **kwargs
    )
    assert app is not None
    app.mount(
        jpconfig.STATIC_ROUTE,
        StaticFiles(directory=jpconfig.STATIC_DIRECTORY),
        name=jpconfig.STATIC_NAME,
    )

    app.mount(
        "/templates",
        StaticFiles(directory=current_dir + "/templates"),
        name="templates",
    )


    @app.route("/zzz_justpy_ajax")
    class AjaxEndpoint(JustpyAjaxEndpoint):
        """
        Justpy ajax handler
        """

    @app.websocket_route("/")
    class JustpyEvents(WebSocketEndpoint):
        socket_id = 0

        async def on_connect(self, websocket):
            await websocket.accept()
            websocket.id = JustpyEvents.socket_id
            websocket.open = True
            logging.debug(f"Websocket {JustpyEvents.socket_id} connected")
            JustpyEvents.socket_id += 1
            # Send back socket_id to page
            # await websocket.send_json({'type': 'websocket_update', 'data': websocket.id})
            # WebPage.loop.create_task(
            #     websocket.send_json({"type": "websocket_update", "data": websocket.id})
            # )
            AppDB.loop.create_task(
                websocket.send_json({"type": "websocket_update", "data": websocket.id})
            )

        async def on_receive(self, websocket, data):
            """
            Method to accept and act on data received from websocket
            """
            logging.debug("%s %s", f"Socket {websocket.id} data received:", data)
            
            data_dict = json.loads(data)
            msg_type = data_dict["type"]
            # data_dict['event_data']['type'] = msg_type
            if msg_type == "connect":
                # Initial message sent from browser after connection is established
                # WebPage.sockets is a dictionary of dictionaries
                # First dictionary key is page id
                # Second dictionary key is socket id
                page_key = data_dict["page_id"]
                websocket.page_id = page_key
                # The BigInternal Surgery
                # if page_key in WebPage.sockets:
                #     WebPage.sockets[page_key][websocket.id] = websocket
                # else:
                #     WebPage.sockets[page_key] = {websocket.id: websocket}
                if page_key in AppDB.pageId_to_websockets:
                    AppDB.pageId_to_websockets[page_key][websocket.id] = websocket
                else:
                    AppDB.pageId_to_websockets[page_key] = {websocket.id: websocket}

                return

            if msg_type == "event" or msg_type == "page_event":
                # Message sent when an event occurs in the browser
                session_cookie = websocket.cookies.get(jpconfig.SESSION_COOKIE_NAME)
                if jpconfig.SESSIONS and session_cookie:
                    session_id = websocket.session["session_id"] 
                    data_dict["event_data"]["session_id"] = session_id
                # await self._event(data_dict)
                data_dict["event_data"]["msg_type"] = msg_type
                page_event = True if msg_type == "page_event" else False
                # ====================================================
                # The BigInternal Surgery
                AppDB.loop.create_task(
                    handle_event(data_dict, com_type=0, page_event=page_event)
                )
                # WebPage.loop.create_task(
                #     handle_event(data_dict, com_type=0, page_event=page_event)
                # )
                # ======================== end =======================
                return
            if msg_type == "zzz_page_event":
                # Message sent when an event occurs in the browser
                session_cookie = websocket.cookies.get(jpconfig.SESSION_COOKIE_NAME)
                if jpconfig.SESSIONS and session_cookie:
                    session_id = websocket.session["session_id"] 
                    data_dict["event_data"]["session_id"] = session_id
                data_dict["event_data"]["msg_type"] = msg_type
                # ====================================================
                # The BigInternal Surgery
                AppDB.loop.create_task(
                    handle_event(data_dict, com_type=0, page_event=True)
                )
                # WebPage.loop.create_task(
                #     handle_event(data_dict, com_type=0, page_event=True)
                # )
                return

        async def on_disconnect(self, websocket, close_code):
            print("websocket disconnect called")
            try:
                pid = websocket.page_id
            except:
                return
            websocket.open = False
            AppDB.pageId_to_websockets[pid].pop(websocket.id)
            if not AppDB.pageId_to_websockets[pid]:
                AppDB.pageId_to_websockets.pop(pid)
            await AppDB.pageId_to_webpageInstance[pid].on_disconnect(
                websocket
            )  # Run the specific page disconnect function
            if jpconfig.MEMORY_DEBUG:
                print("************************")
                print(
                    "Elements: ",
                    len(AppDB.pageId_to_webpageInstance),
                    AppDB.pageId_to_webpageInstance,
                )
                print(
                    "WebPages: ",
                    len(AppDB.pageId_to_webpageInstance),
                    AppDB.pageId_to_webpageInstance,
                )
                print(
                    "Sockets: ",
                    len(AppDB.pageId_to_webpageInstance),
                    AppDB.pageId_to_webpageInstance,
                )
                import psutil

                process = psutil.Process(os.getpid())
                print(f"Memory used: {process.memory_info().rss:,}")
                print("************************")

    return app


def report_memory_usage():
    print("************************")
    print(
        "Elements: ",
        len(AppDB.pageId_to_webpageInstance),
    )
    print(
        "WebPages: ",
        len(AppDB.pageId_to_webpageInstance),
    )
    print(
        "Sockets: ",
        len(AppDB.pageId_to_webpageInstance),
    )
    import psutil

    process = psutil.Process(os.getpid())
    print(f"Memory used: {process.memory_info().rss:,}")
    print("************************")
