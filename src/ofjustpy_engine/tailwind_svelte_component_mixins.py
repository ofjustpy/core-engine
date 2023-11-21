class CollapsibleMixin:
    vue_type = "Collapsible"
    html_tag = "div"
    def __init__(
        self,
        hide_banner_text="The content is hidden. Click the button to expand.",
        hide_banner_classes="bg-green-100",
        toggler_classes="ml-4 bg-blue-500 text-white rounded-full p-1",
        **kwargs,
    ):
        self.domDict.html_tag = "div"
        self.domDict.vue_type = "Collapsible"
        self.domDict.class_name = "Collapsible"
        self.domDict.hide_banner_text = hide_banner_text
        self.domDict.toggler_classes = toggler_classes
        self.domDict.hide_banner_classes = hide_banner_classes


# TODO: Svelte implementation of Switch is still not functional
#
class SwitchMixin:
    html_tag = "div"
    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "div"
        self.domDict.vue_type = "Switch"
        self.domDict.class_name = "Switch"
        pass
