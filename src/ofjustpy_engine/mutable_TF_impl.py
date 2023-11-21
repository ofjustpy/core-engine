"""
mixins to build various mutable HC and Div types: HCCMutable, and HCCStatic.
mixins for Core, CoreSharer, HCC, and JSon.
"""
import json

from addict_tracking_changes import Dict
from py_tailwind_utils import dget

class StaticCore_HCRenderHTMLTemplateMixin:
    def __init__(self, *args, **kwargs):
        attrs_kv =" ".join([f'{key}="{value}"' for key, value in self.attrs.items()])
        event_handlers = ' '.join([f"""on{key}='eventHandlers.{key}'""" for key in map(lambda _: _.split("_")[1], self.event_handlers.keys())])
        
        self.html_render_template = f"""<{self.html_tag} {attrs_kv} {{}}" {event_handlers}>{self.text}</{self.html_tag}>"""
        pass
    
class StaticCore_JsonMixin:
    def __init__(self, *args, **kwargs):
        self.json_domDict = None
        self.json_attrs = None

    def get_domDict_json(self):
        # json_domDict is jsonified after tracker has assigned a ID
        if not self.json_domDict:
            self.json_domDict = json.dumps(self.domDict, default=str)[1:-1]
        return self.json_domDict

    def get_attrs_json(self):
        if not self.json_attrs:
            self.json_attrs = json.dumps(self.attrs, default=str)[1:-1]
        return self.json_attrs


class JsonMixin_Base:
    def __init__(self, *args, **kwargs):
        pass

    def get_obj_props_json(self, parent_hidden=False):
        return "[]"

    def build_json(self, parent_hidden=False):
        self.core_attrs_json = self.staticCore.get_attrs_json()
        self.core_domDict_json = self.staticCore.get_domDict_json()

        # get local json
        if not self.domDict:
            self.local_domDict_json = ""
        else:
            self.local_domDict_json = json.dumps(self.domDict, default=str)[1:-1]

        if not self.attrs:
            self.local_attrs_json = ""
        else:
            self.local_attrs_json = json.dumps(self.attrs, default=str)[1:-1]

        attrs_sep = ""
        if self.local_attrs_json != "" and self.core_attrs_json != "":
            attrs_sep = ","

        local_sep = ""
        if self.core_domDict_json != "" and self.local_domDict_json != "":
            local_sep = ","

        is_hidden = False  # shipping hidden as awell  "hidden" in self.classes

        if parent_hidden:
            object_props_json = "[]" #no need to ship json of childs if parent is hidden
        else:
            object_props_json = self.get_obj_props_json(parent_hidden=is_hidden)

        self.obj_json = f"""{{ {self.core_domDict_json}{local_sep}{self.local_domDict_json}, "attrs":{{ {self.core_attrs_json} {attrs_sep} {self.local_attrs_json}   }}, "object_props": {object_props_json} }}"""
        self.domDict.clear_changed_history()
        self.attrs.clear_changed_history()

    def get_obj_props_changed_diff_patch(self):
        return
        yield

    def get_mutable_shell_diff_patch(self):
        return
        yield

    def get_changed_diff_patch(self, parent_hidden=False):
        yield from self.get_mutable_shell_diff_patch()
        self.clear_changed_history()
        yield from self.get_obj_props_changed_diff_patch()

    def convert_object_to_json(self, parent_hidden=False):
        return

    def clear_changed_history(self):
        self.attrs.clear_changed_history()
        self.domDict.clear_changed_history()


class MutableShell_JsonMixin:
    def __init__(self, *args, **kwargs):
        pass

    def get_mutable_shell_diff_patch(self):
        if (
            not self.attrs.has_changed_history()
            and not self.domDict.has_changed_history()
        ):
            yield from self.get_obj_props_changed_diff_patch()

            return

        attrs_patch_kv = ""
        if self.attrs.has_changed_history():
            attrs_patch_kv = ",".join(
                [
                    f""" "{k}": "{self.attrs[k[1:]]}" """
                    for k in self.attrs.get_changed_history()
                ]
            )
        if attrs_patch_kv != "":
            attrs_patch_kv = f""" "attrs": {{ {attrs_patch_kv} }} """

        domDict_patch_kv = ""
        if self.domDict.has_changed_history():
            domDict_patch_kv = ",".join(
                [
                    f""" "{k}":  {json.dumps(dget(self.domDict, k))} """
                    for k in self.domDict.get_changed_history()
                ]
            )

        if domDict_patch_kv != "":
            domDict_patch_kv = f""" "domDict": {{ {domDict_patch_kv} }}"""

        sep = ""
        if attrs_patch_kv != "" and domDict_patch_kv != "":
            sep = ","

        yield f""" "{self.id}" : {{ {attrs_patch_kv} {sep} {domDict_patch_kv} }} """


class HCMutable_JsonMixin(MutableShell_JsonMixin, JsonMixin_Base):
    def convert_object_to_json(self, parent_hidden=False):
        if (
            not self.attrs.has_changed_history()
            and not self.domDict.has_changed_history()
        ):
            return self.obj_json

        if self.attrs.has_changed_history():
            self.local_attrs_json = json.dumps(self.attrs, default=str)[1:-1]
        if self.domDict.has_changed_history():
            self.local_domDict_json = json.dumps(self.domDict, default=str)[1:-1]

        sep = ""
        if self.core_attrs_json != "" and self.local_attrs_json != "":
            sep = ","

        object_props_json = "[]"
        self.obj_json = f"""{{ {self.core_domDict_json}, {self.local_domDict_json}, "attrs":{{ {self.local_attrs_json} {sep} {self.core_attrs_json}   }}, "object_props": {object_props_json} }}"""
        return self.obj_json


class HCCStatic_JsonMixin(MutableShell_JsonMixin, JsonMixin_Base):
    attr_tracked_keys = []
    domDict_tracked_keys = []

    def get_obj_props_json(self, parent_hidden=False):
        object_props_json = (
            "["
            + ",".join(
                [
                    _.convert_object_to_json(parent_hidden=parent_hidden)
                    for _ in self.components
                ]
            )
            + "]"
        )

        return object_props_json

    def convert_object_to_json(self, parent_hidden=False):
        is_hidden = False  # "hidden" in self.classes
        if self.attrs.has_changed_history():
            self.local_attrs_json = json.dumps(self.attrs, default=str)[1:-1]
            # self.attrs.clear_changed_history()

        if self.domDict.has_changed_history():
            self.local_domDict_json = json.dumps(self.domDict, default=str)[1:-1]
            # self.domDict.clear_changed_history()

        sep = ""
        if self.core_attrs_json != "" and self.local_attrs_json != "":
            sep = ","
        # TODO: if child are static (SHC_types) then we can store the object_props_json
        if parent_hidden:
            object_props_json = "[]"
        else:
            object_props_json = self.get_obj_props_json(parent_hidden=is_hidden)
        self.obj_json = f"""{{ {self.core_domDict_json}, {self.local_domDict_json}, "attrs":{{ {self.local_attrs_json} {sep} {self.core_attrs_json}   }}, "object_props": {object_props_json} }}"""
        return self.obj_json


class HCCMutable_JsonMixin(JsonMixin_Base):
    attr_tracked_keys = []
    domDict_tracked_keys = []

    def get_obj_props_json(self, parent_hidden=False):
        object_props_json = (
            "["
            + ",".join(
                [
                    _.convert_object_to_json(parent_hidden=parent_hidden)
                    for _ in self.components
                ]
            )
            + "]"
        )

        return object_props_json

    def convert_object_to_json(self, parent_hidden=False):
        is_hidden = False  # "hidden" in self.classes
        attrs_sep = ""

        if self.core_attrs_json != "" and self.local_attrs_json != "":
            attrs_sep = ","

        local_sep = ""
        if self.core_domDict_json != "" and self.local_domDict_json != "":
            local_sep = ","

        # TODO: if child are static (SHC_types) then we can store the object_props_json
        if parent_hidden:
            object_props_json = "[]"
        else:
            object_props_json = self.get_obj_props_json(parent_hidden=is_hidden)
        self.obj_json = f"""{{ {self.core_domDict_json}{local_sep}{self.local_domDict_json}, "attrs":{{ {self.local_attrs_json} {attrs_sep} {self.core_attrs_json}   }}, "object_props": {object_props_json} }}"""
        assert ", ," not in self.obj_json
        return self.obj_json

    def get_obj_props_changed_diff_patch(self, parent_hidden=False):
        is_hidden = False  # "hidden" in self.classes
        if not parent_hidden:
            for obj in self.components:
                # no need to render hidden objects
                # save on comm and frontend rendering
                # if not "hidden" in self.classes:
                yield from obj.get_changed_diff_patch(parent_hidden=is_hidden)
        else:
            return


class DivMutable_JsonMixin(MutableShell_JsonMixin, JsonMixin_Base):
    attr_tracked_keys = []
    domDict_tracked_keys = []

    def get_obj_props_json(self, parent_hidden=False):
        object_props_json = (
            "["
            + ",".join(
                [
                    _.convert_object_to_json(parent_hidden=parent_hidden)
                    for _ in self.components
                ]
            )
            + "]"
        )

        return object_props_json

    def convert_object_to_json(self, parent_hidden=False):
        is_hidden = False  # "hidden" in self.classes
        if self.attrs.has_changed_history():
            self.local_attrs_json = json.dumps(self.attrs, default=str)[1:-1]

        if self.domDict.has_changed_history():
            self.local_domDict_json = json.dumps(self.domDict, default=str)[1:-1]

        sep = ""
        if self.core_attrs_json != "" and self.local_attrs_json != "":
            sep = ","

        if parent_hidden:
            object_props_json = "[]"
        else:
            object_props_json = self.get_obj_props_json(parent_hidden=is_hidden)
        self.obj_json = f"""{{ {self.core_domDict_json}, {self.local_domDict_json}, "attrs":{{ {self.local_attrs_json} {sep} {self.core_attrs_json}   }}, "object_props": {object_props_json} }}"""
        return self.obj_json

    def get_obj_props_changed_diff_patch(self, parent_hidden=False):
        is_hidden = False  # "hidden" in self.classes
        if not parent_hidden:
            for obj in self.components:
                # no need to render hidden objects
                # save on comm and frontend rendering
                # if not "hidden" in self.classes:
                yield from obj.get_changed_diff_patch(parent_hidden=is_hidden)
        else:
            return


class CoreChildMixin:
    def __init__(self, *args, **kwargs):
        self.childs = kwargs.get("childs", [])

    pass


class HCCMixin_MutableChilds:
    attr_tracked_keys = []
    domDict_tracked_keys = []

    def __init__(self, **kwargs):
        self.components = []
        self.spathMap = Dict(track_changes=True)
        for c in self.staticCore.childs:
            # register the child (only active/mutable child will get registered)
            c_ = c.stub()
            # attach the child as part of self.components
            c_(self)
            if not c_.is_static():
                self.spathMap[c_.id] = c_.target
                
    def add_component(self, child, position=None, slot=None):
        """
        add a component

        Args:
            child: the component to add
            position: the position to add to (append if None)
            slot: if given set the slot of the child
        """
        if slot:
            child.slot = slot
        if position is None:
            self.components.append(child)
        else:
            self.components.insert(position, child)

        return self

class Prepare_HtmlRenderMixin:
    attr_tracked_keys = []
    domDict_tracked_keys = []
    def __init__(self, *args, **kwargs):
        # Since there is no assign id phase for HCCMutable
        # prepare_htmlRender can be called during init itself
        self.prepare_htmlRender()
        pass
    
    
class RenderHTML_HCCMutableChildsMixin:
    attr_tracked_keys = []
    domDict_tracked_keys = []
    def __init__(self, *args, **kwargs):
        # Since there is no assign id phase for HCCMutable
        # prepare_htmlRender can be called during init itself
        pass

    def to_html_iter(self):
        yield f'''{self.staticCore.htmlRender_chunk1}'''
        yield f''' {" ".join(self.htmlRender_attr)}{self.staticCore.htmlRender_chunk2}{"".join(self.htmlRender_body)}'''
        
        for c in self.components:
             yield from c.to_html_iter()
        yield f'''{self.staticCore.htmlRender_chunk3}'''


class RenderHTML_HCCStaticChildsMixin:
    """
    for now just copying the HCCMutable log
    
    """
    attr_tracked_keys = []
    domDict_tracked_keys = []
    def __init__(self, *args, **kwargs):
        pass

    def to_html_iter(self):
        """
        childs html are included by the staticCore
        """
        yield f'''{self.staticCore.htmlRender_chunk1}'''
        yield f''' {" ".join(self.htmlRender_attr)}{self.staticCore.htmlRender_chunk2}{"".join(self.htmlRender_body)}'''
        for c in self.components:
            yield from c.to_html_iter()
        
        yield f'''{self.staticCore.htmlRender_chunk3}'''        
            

class HCCMixin_StaticChilds:
    def __init__(self, **kwargs):
        self.components = kwargs.get("childs")
        # do not register static childs here (as in part of the init of staticCore)
        # active componenent require session manager to be registered
        # register childs as part of stub().__call__
        # we also cannot prepare the html if the childs have not been registered
        # register and prepare happens as part of StaticCoreSharer

    def add_register_childs(self):
        # TODO: still need to call child.stub with attach to parents false

        # Since the childs are static components
        # we need to call the stub to build json
        # but not attach to parents

        for c in self.components:
            c_ = c.stub()
            c_(self, attach_to_parent=False)
            # The A href update curse: we cannot precompute
            # childrens because of A.href is update upon request
            #self.htmlRender_body.append(c.to_html())
            
# ================================ end ===============================





            

# ========================= staticCore sharer ========================
class StaticCoreSharer_BaseMixin:
    def __init__(self, *args, **kwargs):
        self.staticCore = kwargs.get("staticCore")

    def get_domDict_json(self):
        return self.staticCore.get_domDict_json()

    def get_attrs_json(self):
        return self.staticCore.get_attrs_json()


class StaticCoreSharer_EventMixin:
    attr_tracked_keys = []
    domDict_tracked_keys = []

    def __init__(self, *args, **kwargs):
        pass

    def get_event_handler(self, event_type):
        return self.staticCore.event_handlers[event_type]


class StaticCoreSharer_ClassesMixin:
    def __init__(self, *args, **kwargs):
        pass

    @property
    def classes(self):
        return self.staticCore.classes


class StaticCoreSharer_IdMixin:
    def __init__(self, *args, **kwargs):
        pass

    @property
    def id(self):
        #assert self.staticCore.domDict.id is not None
        #return self.staticCore.domDict.get("id", None)
        return self.staticCore.id
    @property
    def key(self):
        return self.staticCore.key

    @property
    def html_tag(self):
        return self.staticCore.html_tag
    
        

class StaticCoreSharer_ValueMixin:
    def __init__(self, *args, **kwargs):
        pass

    # only applies for Button HC for now
    @property
    def value(self):
        assert "value" in self.staticCore.domDict
        return self.staticCore.domDict.get("value", None)


class StaticCoreSharer_HCCStaticMixin:
    def __init__(self, *args, **kwargs):
        self.staticCore.add_register_childs()
        self.staticCore.prepare_htmlRender()
        pass

    def get_obj_prop_json(self):
        return self.staticCore.get_obj_prop_json()

    def add_register_childs(self):
        return self.staticCore.add_register_childs()

    @property
    def components(self):
        return self.staticCore.components


# ================================ end ===============================
