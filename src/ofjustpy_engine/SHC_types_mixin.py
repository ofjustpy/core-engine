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

    def get_obj_props_jsondict(self):
        return []

    def build_json(self):
        domDict_json = json.dumps(self.domDict, default=str)[1:-1]
        attrs_json = json.dumps(self.attrs, default=str)[1:-1]
        object_props_json = self.get_obj_props_json()

        self.obj_json = f"""{{ {domDict_json},  "attrs":{{ {attrs_json} }}, "object_props":{object_props_json} }}"""


        
    def convert_object_to_jsondict(self, parent_hidden=False):
        """
        jsondict is a dict representation that would converted to json.
        Currently used for skeleton's slot components
        """
        z = {**self.domDict, "attrs": self.attrs, "object_props": self.get_obj_props_jsondict()}
        return z
    
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

    
class ActiveJsonMixin(StaticJsonMixin):
    """
    passive items that do not have id/key
    """

    def __init__(self, *args, **kwargs):
        StaticJsonMixin.__init__(self, *args, **kwargs)


class HCCPassiveJsonMixin(StaticJsonMixin):
    def __init__(self, *args, **kwargs):
        StaticJsonMixin.__init__(self, *args, **kwargs)

        pass

    def get_obj_props_json(self):
        return (
            "[" + ",".join([_.convert_object_to_json() for _ in self.components]) + "]"
        )
    def get_obj_props_jsondict(self):
        return (
            [_.convert_object_to_jsondict() for _ in self.components]
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

    def get_obj_props_jsondict(self):
        return (
            [_.convert_object_to_jsondict() for _ in self.components]
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



class StaticCore:
    """
    provides baseComponent (id, show, debounce, etc)
             divBase: (text, object_props)
             Label: label tag and label specific attributes
    """

    def __init__(self, *args, **kwargs):
        self.domDict = Dict()
        self.attrs = Dict()
        
    @property
    def html_tag(self):
        return self.domDict.html_tag

    @html_tag.setter
    def html_tag(self, value):
        self.domDict.html_tag = value
        

class HCCStaticMixin:
    """

    :param childs: A list of child components to be associated with the parent.
    :type childs: list

    :ivar components: The list of child components associated with the parent.
    """

    def __init__(self, *args, **kwargs):
        self.components = kwargs.get("childs", [])
        # child_item_order is used by javascript render to render the childs in the
        # said order
        self.domDict["child_item_order"] = ["inner_html", "text", "childs"]
        
    def add_register_childs(self):

        for achild in self.components:
            stub = achild.stub()
            stub(self, attach_to_parent=False)

            
class HCCPassiveMixin(HCCStaticMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class HCCActiveMixin(HCCStaticMixin):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        

class PassiveHC_RenderHTMLMixin:
    def __init__(self, *args, **kwargs):
        self.prepare_htmlRender()
        pass

    def build_renderHtml(self):
        pass
    
    def prepare_htmlRender(self):
        # mutable shell's staticCore have
        # prepare_htmlRender which gets
        # updated after update to attrs
        self.htmlRender = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>{"".join(self.htmlRender_body)}</{self.html_tag}>'''

    def to_html_iter(self):
        yield self.htmlRender

class ActiveHC_RenderHTMLMixin:
    # We cannot build_renderHtml at init.
    # because id is assigned by assign_id which is called
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

    
    def to_html_iter(self):
        yield self.htmlRender

        

class ActiveDiv_RenderHTMLMixin:
    def __init__(self, *args, **kwargs):
        # can prepare htmlrender now as id is not assigned yet.
        # wait for assign_id callback to be done
        pass

    def post_id_assign_callback(self):
        self.prepare_htmlRender()
        pass
    
    def build_renderHtml(self):
        self.htmlRender_open_tag = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>'''
        self.htmlRender_close_tag =  f'''</{self.html_tag}>'''
        

    def prepare_htmlRender(self):
        # mutable shell's staticCore have
        # prepare_htmlRender which gets
        # updated after update to attrs
        # prepare_htmlRender is also called
        # by eventMixin following .on
        # event addition. 
        self.build_renderHtml()
    def to_html_iter(self):
        yield self.htmlRender_open_tag
        yield from self.htmlRender_body
        for achild in self.components:
            yield from achild.to_html_iter()
        yield self.htmlRender_close_tag





class PassiveDiv_RenderHTMLMixin:
    def __init__(self, *args, **kwargs):
        self.build_renderHtml()
        pass

    def prepare_htmlRender(self):
        # mutable shell's staticCore have
        # prepare_htmlRender which gets
        # updated after update to attrs
        self.build_renderHtml()
        
    def build_renderHtml(self):
        self.htmlRender_open_tag = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}>'''
        self.htmlRender_close_tag = f'''</{self.html_tag}>'''
        


    def to_html_iter(self):
        yield self.htmlRender_open_tag
        yield from self.htmlRender_body
        for achild in self.components:
            yield from achild.to_html_iter()
        yield self.htmlRender_close_tag
    

def staticClassTypeGen(
    taglabel="Label",
    tagtype=TR.LabelMixin,
    hccMixinType=HCCPassiveMixin,
    jsonMixinType=PassiveJsonMixin,
    baseComponentMixinType = TR.jpBaseComponentMixin,
    make_container=False,
    attach_event_handling=False,
    http_request_callback_mixin=HTTPRequestCallbackMixin,
    addon_mixins=[],
    html_tag = None,
    **rwargs,
):
    """
    baseMixinType: by default use jpBaseComponentMixin which will set vue_type to html_component.
    if using fontawesome_component then use special baseMixinType,
    html_tag: In some scenarios we pass two mixins where both have tags. 
    """
    # TODO: make_container_local is not necessary -- used for debug
    

    def constructor(self, *args,  make_container_local=make_container, **kwargs):
        self.htmlRender_attr = []
        self.htmlRender_body = []

        #. its important  that baseComponentMixinType is invoked first
        #. see .icons.py
        StaticCore.__init__(self, *args, **kwargs)
        baseComponentMixinType.__init__(self, *args, **kwargs)
        TR.TwStyMixin.__init__(
            self, *args, **kwargs
        )
        TR.DOMEdgeMixin.__init__(self, *args, **kwargs)
        tagtype.__init__(self, *args, **kwargs)
        TR.SvelteSafelistMixin.__init__(self, *args, **kwargs)
        

        if make_container_local:
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
            TR.PassiveKeyMixin.__init__(self, *args, **kwargs)
        # JsonMixin should come after HCCMixin
        jsonMixinType.__init__(self, *args, **kwargs)

        if make_container_local:
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

        for _ in addon_mixins:
            _.__init__(self, *args, **kwargs)

        # explicitly fix the html_tag
        if html_tag:
            self.domDict.html_tag = html_tag
    base_types = (StaticCore, baseComponentMixinType, tagtype, TR.SvelteSafelistMixin)
    if make_container:
        if attach_event_handling:
            base_types = (
                StaticCore,
                TR.TwStyMixin,
                TR.DOMEdgeMixin,
                baseComponentMixinType,
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
                          TR.TwStyMixin,
                          TR.DOMEdgeMixin,
                          baseComponentMixinType,
                          TR.SvelteSafelistMixin,
                          TR.PassiveKeyMixin,
                          jsonMixinType,
                          tagtype,
                          hccMixinType,
                          PassiveDiv_RenderHTMLMixin
                          )
    else:
        if attach_event_handling:
            base_types = (
                StaticCore,
                TR.TwStyMixin,
                TR.DOMEdgeMixin,
                baseComponentMixinType,
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
                          TR.TwStyMixin,
                          TR.DOMEdgeMixin,
                          baseComponentMixinType,
                          TR.SvelteSafelistMixin,
                          TR.PassiveKeyMixin,
                          jsonMixinType,
                          tagtype,
                          TR.HCTextMixin,
                          PassiveHC_RenderHTMLMixin
                          )

    return type(
        taglabel,
        (*base_types, *addon_mixins),
        {
            # constructor
            "__init__": constructor
        },
    )
