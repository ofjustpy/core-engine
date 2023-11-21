"""
A single API to generate various types of mutable Div: HCCMutable, HCCStatic, Mutable
"""
import json

from addict_tracking_changes import Dict
from addict_tracking_changes_fixed_attributes import EmptyDict, OneKeyDict
from . import HC_Div_type_mixins as TR
from .mutable_TF_impl import CoreChildMixin
from .mutable_TF_impl import DivMutable_JsonMixin
from .mutable_TF_impl import HCCMixin_MutableChilds
from .mutable_TF_impl import RenderHTML_HCCMutableChildsMixin
from .mutable_TF_impl import RenderHTML_HCCStaticChildsMixin
from .mutable_TF_impl import Prepare_HtmlRenderMixin
from .mutable_TF_impl import HCCMixin_StaticChilds
from .mutable_TF_impl import HCCMutable_JsonMixin
from .mutable_TF_impl import HCCStatic_JsonMixin
from .mutable_TF_impl import StaticCore_JsonMixin
from .mutable_TF_impl import StaticCoreSharer_BaseMixin
from .mutable_TF_impl import StaticCoreSharer_ClassesMixin
from .mutable_TF_impl import StaticCoreSharer_EventMixin
from .mutable_TF_impl import StaticCoreSharer_HCCStaticMixin
from .mutable_TF_impl import StaticCoreSharer_IdMixin


def classTypeGen(
    hc_tag="Div",
    hctag_mixin=TR.DivMixin,
    static_core_mixins=[],
    mutable_shell_mixins=[],
    is_childs_mutable=True,
    is_self_mutable=False,
):
    assert is_childs_mutable or is_self_mutable

    if is_self_mutable:
        core_mixins = [
            TR.KeyMixin,
            TR.IdMixin,
            TR.jpBaseComponentMixin,
            TR.EventMixin,
            StaticCore_JsonMixin,
            CoreChildMixin,
            hctag_mixin,
        ]
        shell_mixins = [
            TR.TwStyMixin,
            StaticCoreSharer_EventMixin,
        ]
        static_core_sharer = [
            StaticCoreSharer_BaseMixin,
            StaticCoreSharer_IdMixin, # Also has key sharer
        ]

    else:
        core_mixins = [
            TR.jpBaseComponentMixin,
            TR.TwStyMixin,
            TR.PassiveKeyIdMixin,
            StaticCore_JsonMixin,
            CoreChildMixin,
            hctag_mixin,
            Prepare_HtmlRenderMixin
        ]

        shell_mixins = []
        static_core_sharer = (StaticCoreSharer_BaseMixin, StaticCoreSharer_IdMixin, StaticCoreSharer_ClassesMixin)

    if is_childs_mutable:
        shell_mixins.append(HCCMixin_MutableChilds)
        shell_mixins.append(RenderHTML_HCCMutableChildsMixin)

    else:
        core_mixins.append(HCCMixin_StaticChilds)
        static_core_sharer.append(StaticCoreSharer_HCCStaticMixin)
        shell_mixins.append(RenderHTML_HCCStaticChildsMixin)

    match is_self_mutable, is_childs_mutable:
        case False, True:
            shell_mixins.append(HCCMutable_JsonMixin)
            pass
        case True, True:
            shell_mixins.append(DivMutable_JsonMixin)
        case True, False:
            shell_mixins.append(HCCStatic_JsonMixin)
        case _:
            assert False

    attr_tracked_keys = []
    domDict_tracked_keys = []

    for mixin in [*mutable_shell_mixins, *shell_mixins]:
        for _ in mixin.attr_tracked_keys:
            attr_tracked_keys.append(_)
        for _ in mixin.domDict_tracked_keys:
            domDict_tracked_keys.append(_)

    shell_mixins.append(TR.DOMEdgeMixin)

    class StaticCore(*core_mixins, *static_core_mixins):
        def __init__(self, *args, **kwargs):
            self.domDict = Dict()
            self.attrs = Dict()
            self.htmlRender_attr = []
            self.htmlRender_body = []
            for _ in core_mixins:
                _.__init__(self, *args, **kwargs)

            for _ in static_core_mixins:
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
        *static_core_sharer,
        *shell_mixins,
        *mutable_shell_mixins,
    ):
        def __init__(self, *args, **kwargs):
            if len(domDict_tracked_keys) == 0:
                self.domDict = EmptyDict()
            elif len(domDict_tracked_keys) == 1:
                self.domDict = OneKeyDict(domDict_tracked_keys[0])
            else:
                self.domDict = Dict(track_changes=True)

            self.attrs = Dict(track_changes=True)
            self.htmlRender_attr = []
            self.htmlRender_body = []
            for _ in static_core_sharer:
                _.__init__(self, *args, **kwargs)

            for _ in shell_mixins:
                _.__init__(self, *args, **kwargs)

            for _ in mutable_shell_mixins:
                _.__init__(self, *args, **kwargs)

        def prepare_htmlRender(self):
            """
            mutable shells do not prepare render chunks
            
            """
            pass


    return StaticCore, MutableShell
