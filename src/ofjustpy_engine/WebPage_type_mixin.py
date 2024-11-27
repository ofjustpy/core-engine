"""
The WebPage class implments most of the engine code that drives
the request-update-response cycle, i.e. recieving msg from frontend, lookup and invoke handler
This file represents the building block for mixins for webPage class. 
"""
import asyncio

from .jpcore import AppDB
from enum import Enum
from .jpcore import jpconfig
class WebPageType(Enum):
    PASSIVE_STATIC = 'PassiveStatic'
    RESPONSIVE_STATIC = 'ResponsiveStatic'
    OTHER = 'OTHER'

    

class WebPageMixin:
    # has no domDict or attrs attribute
    use_websockets = True

    template_file = "svelte.html"

    def __init__(self, *args, **kwargs):
        # These attributes can move to static core
        self.title = kwargs.pop("title", "ofjustpy")
        self.favicon = None
        self.debug = False

        # TODO: probably not required; revisit page caching
        self.use_cache = False  # Determines whether the page uses the cache or not
        if jpconfig.SESSIONS:
            self.session_manager = kwargs.get("session_manager")
            self.page_id = (
                self.session_manager.session_id + ":" + self.staticCore.id
            )
        else:
            # SESSIONS is not enabled; session_id is not set; 
            self.session_manager = None
            self.page_id = ("None:" + 
                            self.staticCore.id
                            )
            
        self.display_url = ''
        self.redirect = ''
        self.open = None

        # non-http cookies ; accessible via javascript on the page
        self.css = ""
        self.head_html = kwargs.get("head_html", "")

        self.body_html = kwargs.get("body_html", "")
        self.html = ""
        self.body_style = kwargs.get("body_style", "")
        self.body_classes = kwargs.get("body_classes", "")
        self.reload_interval = None
        # rendering will depend on the webpage_type
        #
        self.skeleton_data_theme = kwargs.get("skeleton_data_theme", "skeleton")
        
        self.webpage_type = WebPageType.RESPONSIVE_STATIC
        AppDB.pageId_to_webpageInstance[self.page_id] = self
        self.is_active = 1
        self.is_cached = False
        if 'template_file' in kwargs:
            self.template_file = kwargs.get('template_file')
            
        pass

    def build_json(self):
        return (
            "["
            + ",".join(
                [obj.convert_object_to_json() for i, obj in enumerate(self.components)]
            )
            + "]"
        )

    def get_changed_diff_patch(self):

        for obj in self.components:
            yield from obj.get_changed_diff_patch()

    def add_component(self, child, position=None):
        if position is None:
            self.components.append(child)
        else:
            self.components.insert(position, child)
        return self

    def build_list(self):
        object_list = []
        self.react()
        for i, obj in enumerate(self.components):
            # TODO: This react is important...enable it. and document
            # obj.react(self.data)
            d = obj.convert_object_to_dict()
            object_list.append(d)

        return object_list

    async def flush_cookies(self):
        try:
            websocket_dict = AppDB.pageId_to_websockets[self.page_id]
        except:
            return self
        json_to_send = self.get_cookie_json()
        websockets = list(websocket_dict.values())
        _results = await asyncio.gather(
            *[websocket.send_text(json_to_send) for websocket in websockets],
            return_exceptions=True,
        )

    async def redirect_to_url(self, redirect_url,
                              ):
        """
        send message to websocket to update the page. Currently only supports
        page redirect
        """
        dict_to_send = {
            "type": "page_update",
            "page_options": {
                "redirect": redirect_url,
            },
        }

        try:
            websocket_dict = AppDB.pageId_to_websockets[self.page_id]
        except:
            
            return self
        websockets = list(websocket_dict.values())
        _results = await asyncio.gather(
            *[websocket.send_json(dict_to_send) for websocket in websockets],
            return_exceptions=True,
        )
        pass
    async def update(self, websocket=None):
        """
        update the Webpage

        Args:
            websocket(): The websocket to use (if any)
        """

        try:
            websocket_dict = AppDB.pageId_to_websockets[self.page_id]
        except:
            
            return self

        if self.to_json_optimized:
            # ================== Use optimized json ==================
            json_to_send = f"""{{ "type": "diff_patch_update",  "data" : {{ {",".join(self.get_changed_diff_patch())} }}    }}"""
            
            if websocket:
                AppDB.loop.create_task(websocket.send_text(json_to_send))
            else:
                websockets = list(websocket_dict.values())
                # https://stackoverflow.com/questions/54987361/python-asyncio-handling-exceptions-in-gather-documentation-unclear
                _results = await asyncio.gather(
                    *[websocket.send_text(json_to_send) for websocket in websockets],
                    return_exceptions=True,
                )

            # ========================================================
        else:
            # ============== build the dict and the json =============
            # no longer support sending entire dict and
            # rerendering the all the components 
            assert False
            # dict_to_send = {
            #     "type": "page_update",
            #     "data": self.build_list(),
            #     "page_options": {
            #         "display_url": self.display_url,
            #         "title": self.title,
            #         "redirect": self.redirect,
            #         "open": self.open,
            #         "favicon": self.favicon,
            #     },
            # }

            # if websocket:
            #     AppDB.loop.create_task(websocket.send_json(dict_to_send))
            # else:
            #     websockets = list(websocket_dict.values())
            #     _results = await asyncio.gather(
            #         *[websocket.send_json(dict_to_send) for websocket in websockets],
            #         return_exceptions=True,
            #     )
            #     # ======================== end =======================
            #     pass

        return self

    async def run_javascript(self, javascript_string:str, *, request_id=None, send=True):
        """
        run the given JavaScript code remotely
        
        Args:
            javascript_string(str): the javascript code to run remotely
        """
        try:
            websocket_dict = AppDB.pageId_to_websockets[self.page_id]
            # TODO: log failure points carefully
        except:
            return self
        dict_to_send = {
            "type": "run_javascript",
            "data": javascript_string,
            "request_id": request_id,
            "send": send,
        }
                    
        websockets = list(websocket_dict.values())
        await asyncio.gather(
            *[
                websocket.send_json(dict_to_send)
                for websocket in list(websocket_dict.values())
            ],
            return_exceptions=True,
        )
        return self

    async def trigger_toast(self, msg):
        """
        TODO: this function should be part of skeleton_mixing
        """

        await self.run_javascript(f"""
        skeleton_utilities.triggerToast("{msg}");
        """)
    async def on_disconnect(self, websocket=None):
        # don't do anything if caching is not enabled
        if not jpconfig.CACHE_WEBPAGES:
            return
        
        self.is_active -= 1
        if self.is_active == 0:
            if self.is_cached == False:
                if jpconfig.SESSIONS:
                    self.session_manager.schedule_page_removal(self)
                else:
                    # Purge the nosession/passive page
                    self.purge_page()
                    pass

        pass

    def purge_page(self):
        del AppDB.pageId_to_webpageInstance[self.page_id]
        pass
