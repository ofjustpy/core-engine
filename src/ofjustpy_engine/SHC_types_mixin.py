"""
Mixins to build static hc/div types. 
"""
import json

from addict import Dict
from py_tailwind_utils import dget

from . import HC_Div_type_mixins as TR




        
# ========================== all json mixins =========================


class JsonMixin:
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


class PassiveJsonMixin(JsonMixin):
    """
    passive items that do not have id/key
    """

    def __init__(self, *args, **kwargs):
        JsonMixin.__init__(self, *args, **kwargs)
        # self.build_json()
        pass
    def get_changed_diff_patch(self, parent_hidden=False):

        return
        yield

class HCCPassiveJsonMixin(PassiveJsonMixin):
    def __init__(self, *args, **kwargs):
        PassiveJsonMixin.__init__(self, *args, **kwargs)

        pass

    def get_obj_props_json(self):
        return (
            "[" + ",".join([_.convert_object_to_json() for _ in self.components]) + "]"
        )


class HCCJsonMixin(JsonMixin):
    def __init__(self, *args, **kwargs):
        self.obj_json = None
        JsonMixin.__init__(self, *args, **kwargs)

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


class HCCMixin:
    def __init__(self, **kwargs):
        self.components = kwargs.get("childs")

    def add_register_childs(self):
        for achild in self.components:
            # call the child stubs -- so that
            # active childs can be registered
            # but ignore the stubs as the child
            # is already added as part of components
            stub = achild.stub()
            # invoke __call_ of stub
            # to assign id, build json
            stub(self, attach_to_parent=False)


class HCCPassiveMixin:
    """Initialize the HCCPassiveMixin object.

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


def staticClassTypeGen(
    taglabel="Label",
    tagtype=TR.LabelMixin,
    hccMixinType=HCCMixin,
    jsonMixinType=JsonMixin,
    make_container=False,
    attach_event_handling=False,
    http_request_callback_mixin=HTTPRequestCallbackMixin,
    addon_mixins=[],
    **kwargs,
):
    if addon_mixins:
        raise ValueError("addon_mixins not implemented yet")

    def constructor(self, *args, **kwargs):
        StaticCore.__init__(self, *args, **kwargs)
        tagtype.__init__(self, *args, **kwargs)

        if make_container:
            hccMixinType.__init__(self, *args, **kwargs)
        else:
            TR.HCTextMixin.__init__(
                self, domDict=self.domDict, attrs=self.attrs, **kwargs
            )
            pass

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

    base_types = (StaticCore, tagtype)
    if make_container:
        if attach_event_handling:
            base_types = (
                StaticCore,
                jsonMixinType,
                tagtype,
                hccMixinType,
                TR.EventMixin,
                TR.KeyMixin,
                TR.IdMixin,
                DataValidators,
                http_request_callback_mixin,
            )

        else:
            base_types = (StaticCore, TR.PassiveKeyIdMixin, jsonMixinType, tagtype, hccMixinType)
    else:
        if attach_event_handling:
            base_types = (
                StaticCore,
                jsonMixinType,
                tagtype,
                TR.EventMixin,
                TR.KeyMixin,
                TR.IdMixin,
                TR.HCTextMixin,
                DataValidators,
                http_request_callback_mixin,
            )
        else:
            base_types = (StaticCore, TR.PassiveKeyIdMixin, jsonMixinType, tagtype, TR.HCTextMixin)

    return type(
        taglabel,
        base_types,
        {
            # constructor
            "__init__": constructor
        },
    )
