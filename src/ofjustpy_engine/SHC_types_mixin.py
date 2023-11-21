"""
Mixins to build static hc/div types. 
"""
import json

from addict import Dict
from py_tailwind_utils import dget

from . import HC_Div_type_mixins as TR




        
# ========================== all json mixins =========================


class StaticJsonMixin:
    """Mixin for static objects that have id/event handler attached to it."""

    def __init__(self, *args, **kwargs):
        self.obj_json = None
        pass

    def get_obj_props_json(self):
        return "[]"

    def build_json(self):
        domDict_json = json.dumps(self.domDict, default=str)[1:-1]
        attrs_json = json.dumps(self.attrs, default=str)[1:-1]
        object_props_json = self.get_obj_props_json()

        self.obj_json = f"""{{ {domDict_json},  "attrs":{{ {attrs_json} }}, "object_props":{object_props_json} }}"""

    def convert_object_to_json(self, parent_hidden=False):
         return self.obj_json

    def get_changed_diff_patch(self, parent_hidden=False):
        return
        yield

    def clear_changed_history(self):
        raise NotImplementedError("Static types don't mutate -- changed diff not applicable")

class PassiveJsonMixin(StaticJsonMixin):
    """
    passive items that do not have id/key
    """

    def __init__(self, *args, **kwargs):
        StaticJsonMixin.__init__(self, *args, **kwargs)

        pass
    
    # def get_changed_diff_patch(self, parent_hidden=False):
    #     yield
    #     return
    

    
class ActiveJsonMixin(StaticJsonMixin):
    """
    passive items that do not have id/key
    """

    def __init__(self, *args, **kwargs):
        StaticJsonMixin.__init__(self, *args, **kwargs)

    # def get_changed_diff_patch(self, parent_hidden=False):
        
    #     yield
    #     return 
    
class HCCPassiveJsonMixin(StaticJsonMixin):
    def __init__(self, *args, **kwargs):
        StaticJsonMixin.__init__(self, *args, **kwargs)

        pass

    def get_obj_props_json(self):
        return (
            "[" + ",".join([_.convert_object_to_json() for _ in self.components]) + "]"
        )


class HCCJsonMixin(StaticJsonMixin):
    def __init__(self, *args, **kwargs):
        self.obj_json = None
        StaticJsonMixin.__init__(self, *args, **kwargs)

        pass

    def build_json(self):
        # first build child json
        # then self json
        for c in self.components:
            c.build_json()

        super().build_json()

    def get_obj_props_json(self):
        return (
            "[" + ",".join([_.convert_object_to_json() for _ in self.components]) + "]"
        )


class HTTPRequestCallbackMixin:
    """
    after a connection is made -- starlette hands
    over request object. This request object is used
    to resolve route label to full url.
    When an object is instantiated, this call back would be invoked.
    """

    def __init__(self, *args, **kwargs):
        pass

    def request_callback(self, request):
        pass


# ================================ end ===============================


class DataValidators:
    def __init__(self, *args, **kwargs):
        if "data_validators" in kwargs:
            self.data_validators = kwargs.get("data_validators")



class StaticCore(
    TR.jpBaseComponentMixin,
    TR.TwStyMixin,
    TR.DOMEdgeMixin,
):
    """
    provides baseComponent (id, show, debounce, etc)
             divBase: (text, object_props)
             Label: label tag and label specific attributes
    """

    def __init__(self, *args, **kwargs):
        self.domDict = Dict()
        self.attrs = Dict()
        TR.jpBaseComponentMixin.__init__(
            self, domDict=self.domDict, attrs=self.attrs, **kwargs
        )
        TR.DOMEdgeMixin.__init__(
            self, *args, domDict=self.domDict, attrs=self.attrs, **kwargs
        )
        TR.TwStyMixin.__init__(
            self, *args, domDict=self.domDict, attrs=self.attrs, **kwargs
        )


class HCCStaticMixin:
    def __init__(self, **kwargs):
        # active childs are not added via stub-callable route
        # the target is directly added
        self.components = kwargs.get("childs")


# class HCCMixin:
#     def __init__(self, **kwargs):
#         self.components = kwargs.get("childs")

#     def add_register_childs(self):
#         for achild in self.components:
#             # call the child stubs -- so that
#             # active childs can be registered
#             # but ignore the stubs as the child
#             # is already added as part of components
#             stub = achild.stub()
#             # invoke __call_ of stub
#             # to assign id, build json
#             stub(self, attach_to_parent=False)

# TODO: rename/refactor to HCCStaticMixin
class HCCStaticMixin:
    """

    :param childs: A list of child components to be associated with the parent.
    :type childs: list

    :ivar components: The list of child components associated with the parent.
    """

    def __init__(self, *args, **kwargs):
        self.components = kwargs.get("childs")

        
    def add_register_childs(self):

        for achild in self.components:
            stub = achild.stub()
            # invoke __call_ of stub
            # to assign id, build json
            stub(self, attach_to_parent=False)

            
# build_renderHtml will be done in TF_impl
# after add_register_childs calls

class HCCPassiveMixin(HCCStaticMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)



        
class HCCActiveMixin(HCCStaticMixin):
    """
    Ideally we should have post_id_assign_callback here
    as well as with renderHTML.
    add_register_childs is called by renderHTML
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        

class PassiveHC_RenderHTMLMixin:
    def __init__(self, *args, **kwargs):

        self.htmlRender = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''
        pass

    def build_renderHtml(self):
        
        pass
    
    def prepare_htmlRender(self):
        # mutable shell's staticCore have
        # prepare_htmlRender which gets
        # updated after update to attrs

        self.htmlRender = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''

    def to_html(self):
        # The url_for curse of A tag
        #return self.htmlRender
        return f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''

    def to_html_iter(self):
        #yield self.htmlRender
        self.prepare_htmlRender()
        yield f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''
        



class ActiveDiv_RenderHTMLMixin:
    def __init__(self, *args, **kwargs):
        # attach all childrens htmls
        # this might get called after
        # prepare_htmlRender call from eventMixin may 
        # already populate so htmlRender_body
        self.htmlRender_body = []
        for achild in self.components:
            self.htmlRender_body.append(achild.to_html())
        pass

    def post_id_assign_callback(self):
        self.build_renderHtml()
        
        pass
    
    def build_renderHtml(self):
        self.htmlRender = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''
    def to_html(self):
        # because oj.AC.A href attribute is big problem
        # it is updated at runtime we will not
        # precompute htmlRender...instead generate it on the fly
        # return self.htmlRender
        return  f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''

    def prepare_htmlRender(self):
        # mutable shell's staticCore have
        # prepare_htmlRender which gets
        # updated after update to attrs
        # prepare_htmlRender is also called
        # by eventMixin following .on
        # event addition. 
        self.htmlRender_body = []

        for achild in self.components:
            self.htmlRender_body.append(achild.to_html())
        self.build_renderHtml()

        
    def to_html_iter(self):
        self.prepare_htmlRender()
        yield f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''


class ActiveHC_RenderHTMLMixin:
    # We cannot build_renderHtml at init
    # because id is assigned by assign_id
    # after the object has been initialized
    
    def __init__(self, *args, **kwargs):
        pass

    # Ideally call should be part of final class
    # and not belong to this mixin: keeping here
    # for less code
    def post_id_assign_callback(self):
        self.build_renderHtml()
        pass
    def build_renderHtml(self):
        self.htmlRender = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''

    def prepare_htmlRender(self):
        # mutable shell's staticCore have
        # prepare_htmlRender which gets
        # updated after update to attrs
        self.build_renderHtml()
    def to_html(self):
        #return self.htmlRender
        return f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''
    

    def to_html_iter(self):
        #yield self.htmlRender
        yield f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''



class PassiveDiv_RenderHTMLMixin:
    def __init__(self, *args, **kwargs):
        # collect the html of childrens
        for achild in self.components:
            self.htmlRender_body.append(achild.to_html())
        # build the final html
        self.build_renderHtml()
        pass

    def prepare_htmlRender(self):
        # mutable shell's staticCore have
        # prepare_htmlRender which gets
        # updated after update to attrs
        self.htmlRender_body = []
        for achild in self.components:
            self.htmlRender_body.append(achild.to_html())
            
        self.build_renderHtml()
        
    def build_renderHtml(self):
        
        self.htmlRender = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''

    def to_html(self):
        # see ActiveDiv.to_htmlRender
        #return self.htmlRender
        self.prepare_htmlRender()
        return f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''
        

    def to_html_iter(self):
        #yield self.htmlRender
        self.prepare_htmlRender()
        yield f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''
    


    
# class ActiveHC_RenderHTMLMixin:
#     def __init__(self, *args, **kwargs):
#         pass

#     def to_html(self):
#         event_handlers = ' '.join([f"""on{key}='eventHandlers.{key}'""" for key in map(lambda _: _.split("_")[1], self.event_handlers.keys())])
        
#         attrs_kv =" ".join([f'{key}="{value}"' for key, value in self.attrs.items()])
#         return f"""<{self.html_tag} {attrs_kv} class="{self.classes}" {event_handlers}>{self.text}</{self.html_tag}>"""
        
#         pass

    
def staticClassTypeGen(
    taglabel="Label",
    tagtype=TR.LabelMixin,
    hccMixinType=HCCPassiveMixin,
    jsonMixinType=PassiveJsonMixin,
    make_container=False,
    attach_event_handling=False,
    http_request_callback_mixin=HTTPRequestCallbackMixin,
    addon_mixins=[],
    **kwargs,
):
    if addon_mixins:
        raise ValueError("addon_mixins not implemented yet")

    def constructor(self, *args, **kwargs):
        self.htmlRender_attr = []
        self.htmlRender_body = []
        StaticCore.__init__(self, *args, **kwargs)
        tagtype.__init__(self, *args, **kwargs)
        TR.SvelteSafelistMixin.__init__(self, *args, **kwargs)

        

        if make_container:
            hccMixinType.__init__(self, *args, **kwargs)
        else:
            TR.HCTextMixin.__init__(
                self, domDict=self.domDict, attrs=self.attrs, **kwargs
            )

        if attach_event_handling:
            TR.KeyMixin.__init__(self, *args, **kwargs)
            TR.EventMixin.__init__(self, *args, **kwargs)
            TR.IdMixin.__init__(self, *args, **kwargs)
            DataValidators.__init__(self, *args, **kwargs)
            http_request_callback_mixin.__init__(self, *args, **kwargs)

        else:
            TR.PassiveKeyIdMixin.__init__(self, *args, **kwargs)
        # JsonMixin should come after HCCMixin
        jsonMixinType.__init__(self, *args, **kwargs)

        if make_container:
            if attach_event_handling:
                ActiveDiv_RenderHTMLMixin.__init__(self, *args, **kwargs)
                pass
            else:
                PassiveDiv_RenderHTMLMixin.__init__(self, *args, **kwargs)
                pass
        else:
            if attach_event_handling:
                ActiveHC_RenderHTMLMixin.__init__(self, *args, **kwargs)
            else:
                PassiveHC_RenderHTMLMixin.__init__(self, *args, **kwargs)
                pass

    base_types = (StaticCore, tagtype, TR.SvelteSafelistMixin)
    if make_container:
        if attach_event_handling:
            base_types = (
                StaticCore,
                jsonMixinType,
                tagtype,
                TR.SvelteSafelistMixin,
                hccMixinType,
                TR.EventMixin,
                TR.KeyMixin,
                TR.IdMixin,
                DataValidators,
                http_request_callback_mixin,
                ActiveDiv_RenderHTMLMixin
            )

        else:
            base_types = (StaticCore,
                          TR.SvelteSafelistMixin,
                          TR.PassiveKeyIdMixin,
                          jsonMixinType,
                          tagtype,
                          hccMixinType,
                          PassiveDiv_RenderHTMLMixin
                          )
    else:
        if attach_event_handling:
            base_types = (
                StaticCore,
                TR.SvelteSafelistMixin,
                jsonMixinType,
                tagtype,
                TR.EventMixin,
                TR.KeyMixin,
                TR.IdMixin,
                TR.HCTextMixin,
                DataValidators,
                http_request_callback_mixin,
                ActiveHC_RenderHTMLMixin
            )
        else:
            base_types = (StaticCore,
                          TR.SvelteSafelistMixin,
                          TR.PassiveKeyIdMixin,
                          jsonMixinType,
                          tagtype,
                          TR.HCTextMixin,
                          PassiveHC_RenderHTMLMixin
                          )

    return type(
        taglabel,
        base_types,
        {
            # constructor
            "__init__": constructor
        },
    )
