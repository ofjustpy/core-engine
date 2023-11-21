"""
Building block mixins for mutable HC types: 
"""
import json

from addict_tracking_changes import Dict
from addict_tracking_changes_fixed_attributes import EmptyDict, OneKeyDict
from . import HC_Div_type_mixins as TR
from .mutable_TF_impl import HCMutable_JsonMixin
from .mutable_TF_impl import StaticCore_JsonMixin
from .mutable_TF_impl import StaticCoreSharer_BaseMixin
from .mutable_TF_impl import StaticCoreSharer_ClassesMixin
from .mutable_TF_impl import StaticCoreSharer_EventMixin
from .mutable_TF_impl import StaticCoreSharer_IdMixin
from .mutable_TF_impl import StaticCoreSharer_ValueMixin

import sys
import traceback


class HCTextSharerMixin:
    def __init__(self, *args, **kwargs):
        pass

    @property
    def text(self):
        return self.staticCore.domDict.text


class TwStySharerMixin:
    def __init__(self, *args, **kwargs):
        pass

    @property
    def twsty_tags(self):
        return self.staticCore.twsty_tags


class HCTextPropertyMixin:
    @property
    def text(self):
        return self.domDict.text

    @text.setter
    def text(self, value):
        if value is not None:
            self.domDict["text"] = value


class RenderHTMLMixin:
    def __init__(self, *args, **kwargs):
        pass

    def build_renderHtml(self):
        assert False
        
    def to_html(self):
        self.htmlRender = f'''{self.staticCore.htmlRender_chunk1} {" ".join(self.htmlRender_attr)}{self.staticCore.htmlRender_chunk2}{"".join(self.htmlRender_body)}{self.staticCore.htmlRender_chunk3}'''
        
        return self.htmlRender

    def to_html_iter(self):
        self.htmlRender = f'''{self.staticCore.htmlRender_chunk1} {" ".join(self.htmlRender_attr)}{self.staticCore.htmlRender_chunk2}{"".join(self.htmlRender_body)}{self.staticCore.htmlRender_chunk3}'''
        yield self.htmlRender

    def prepare_htmlRender(self):
        """
        mutable shells do not prepare render chunks
        
        """
        pass
    pass

def classTypeGen(
    hc_tag,
    hctag_mixin,
    staticCoreMixins=[TR.HCTextMixin],
    mutableShellMixins=[TR.TwStyMixin],
    staticCore_addonMixins=[],
    mutableShell_addonMixins=[],
):
    core_mixins = [
        TR.IdMixin,
        TR.jpBaseComponentMixin,
        TR.EventMixin,
        StaticCore_JsonMixin,
        *staticCore_addonMixins,
        hctag_mixin,
    ]

    sharerMixins = [
        StaticCoreSharer_BaseMixin,
        StaticCoreSharer_IdMixin,
        StaticCoreSharer_EventMixin,
    ]

    for mixin in staticCoreMixins:
        match mixin:
            case TR.HCTextMixin:
                sharerMixins.append(HCTextSharerMixin)
            case TR.TwStyMixin:
                sharerMixins.append(TwStySharerMixin)
                sharerMixins.append(StaticCoreSharer_ClassesMixin)

    # mixins that will part of  mutableShell
    # collect the mutable keys for tracking
    attr_tracked_keys = []
    domDict_tracked_keys = []

    mutableShell_auxMixins = []
    for mixin in mutableShellMixins:
        for _ in mixin.attr_tracked_keys:
            attr_tracked_keys.append(_)
        for _ in mixin.domDict_tracked_keys:
            domDict_tracked_keys.append(_)

        match mixin:
            case TR.HCTextMixin:
                mutableShell_auxMixins.append(HCTextPropertyMixin)

            case TR.TwStyMixin:
                pass

    class StaticCore(*core_mixins, *staticCoreMixins):
        def __init__(self, *args, **kwargs):
            self.domDict = Dict()
            self.attrs = Dict()
            self.htmlRender_attr = []
            self.htmlRender_body = []
            self.key = kwargs.get("key", None)
            for _ in core_mixins:
                _.__init__(self, *args, **kwargs)

            for _ in staticCoreMixins:
                _.__init__(self, *args, **kwargs)

            for _ in staticCore_addonMixins:
                _.__init__(self, *args, **kwargs)

        def post_id_assign_callback(self):
            self.prepare_htmlRender()
            pass
        def prepare_htmlRender(self):
            
            self.htmlRender_chunk1 = f'''<{self.html_tag} {" ".join(self.htmlRender_attr)}'''
            self.htmlRender_chunk2 = f'''>{"".join(self.htmlRender_body)}'''
            self.htmlRender_chunk3 = f'''</{self.html_tag}>'''
            
            pass
    class MutableShell(
        TR.DOMEdgeMixin,
        HCMutable_JsonMixin,
        *sharerMixins,
        *mutableShellMixins,
        *mutableShell_addonMixins,
        *mutableShell_auxMixins,
            RenderHTMLMixin
    ):
        def __init__(self, *args, **kwargs):
            if len(domDict_tracked_keys) == 0:
                self.domDict = EmptyDict()
            elif len(domDict_tracked_keys) == 1:
                self.domDict = OneKeyDict(domDict_tracked_keys[0])
            else:
                self.domDict = Dict(track_changes=True)

            if len(attr_tracked_keys) == 0:
                self.attrs = EmptyDict()
            elif len(attr_tracked_keys) == 1:
                self.attrs = OneKeyDict(attr_tracked_keys[0])
            else:
                self.attrs = Dict(track_changes=True)

            self.htmlRender_attr = []
            self.htmlRender_body = []
            
            TR.DOMEdgeMixin.__init__(self, *args, **kwargs)
            HCMutable_JsonMixin.__init__(self, *args, **kwargs)
            for _ in sharerMixins:
                _.__init__(self, *args, **kwargs)

            for _ in mutableShellMixins:
                _.__init__(self, *args, **kwargs)

            for _ in mutableShell_addonMixins:
                _.__init__(self, *args, **kwargs)

            RenderHTMLMixin.__init__(self, *args, **kwargs)
            pass

    return StaticCore, MutableShell
