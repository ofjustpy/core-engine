"""
Mixins to express all types of html components: Span, label, Ul, etc.
"""


class LabelMixin:
    """
    The Label class represents the HTML <label> element, which is used to associate a label with a form control, such as
    an <input> or <textarea> element. The attributes 'for' and 'form' are used to configure the label's behavior and
    association with form elements.
    """

    html_tag = "label"

    def __init__(self, **kwargs):
        # self.domDict  = kwargs.get('domDict') #Dict(track_changes=False)
        # self.attrs = kwargs.get("attrs")
        self.domDict.html_tag = "label"
        self.domDict.class_name = "Label"
        for attr in ["for", "form"]:
            if attr in kwargs:
                self.attrs[attr] = kwargs[attr]
                self.htmlRender_attr.append(f'''{attr}="{kwargs.get(attr)}"''')

    @property
    def for_(self):
        """
        The 'for' attribute of the <label> element specifies the id of the form control with which the label is
        associated. The value is the id of a form control element.
        """
        return self.attrs.get("for", None)

    @for_.setter
    def for_(self, value):
        if value is not None:
            self.attrs["for"] = value
        elif "for" in self.attrs:
            del self.attrs["for"]

    @property
    def form(self):
        """
        The 'form' attribute of the <label> element specifies the id of the form to which the label belongs.
        The value is the id of a <form> element.
        """
        return self.attrs.get("form", None)

    @form.setter
    def form(self, value):
        if value is not None:
            self.attrs["form"] = value
        elif "form" in self.attrs:
            del self.attrs["form"]


class SpanMixin:
    html_tag = "span"

    def __init__(self, **kwargs):
        self.domDict.html_tag = SpanMixin.html_tag


class PMixin:
    html_tag = "p"

    def __init__(self, **kwargs):
        self.domDict.html_tag = PMixin.html_tag


class ButtonMixin:
    """
    Represents an HTML <button> element, which is used to create a clickable button.
    """

    html_tag = "button"

    def __init__(self, **kwargs):
        self.domDict.html_tag = ButtonMixin.html_tag
        for key in [
            "autofocus",
            "disabled",
            "form",
            "formaction",
            "formenctype",
            "formmethod",
            "formnovalidate",
            "formtarget",
            "name",
            "type",
        ]:
            if key in kwargs:
                self.attrs[key] = kwargs.get(key)
                self.htmlRender_attr.append(f'''{key}="{kwargs.get(key)}"''')
        if "value" in kwargs:
            self.domDict["value"] = kwargs.get("value")
            self.htmlRender_attr.append(f'''value="{kwargs.get("value")}"''')
            
    @property
    def value(self):
        """
        The 'value' attribute of the <data> element specifies the machine-readable value associated with the element.
        """
        return self.domDict.get("value", None)

    # @value.setter
    # def value(self, value):
    #     if value is not None:
    #         self.domDict["value"] = value
    #     elif "value" in self.domDict:
    #         del self.domDict["value"]

    @property
    def autofocus(self):
        """
        The 'autofocus' attribute of the <button> element specifies whether the button should automatically get focus when the page loads.
        Possible values: True or False.
        """
        return self.attrs.get("autofocus", None)

    @autofocus.setter
    def autofocus(self, value):
        if value is not None:
            self.attrs["autofocus"] = value
        elif "autofocus" in self.attrs:
            del self.attrs["autofocus"]

    @property
    def disabled(self):
        """
        The 'disabled' attribute of the <button> element specifies whether the button should be disabled or not.
        Possible values: True or False.
        """
        return self.attrs.get("disabled", None)

    @disabled.setter
    def disabled(self, value):
        if value is not None:
            self.attrs["disabled"] = value
        elif "disabled" in self.attrs:
            del self.attrs["disabled"]

    @property
    def form(self):
        """
        The 'form' attribute of the <button> element specifies the form the button belongs to.
        """
        return self.attrs.get("form", None)

    @form.setter
    def form(self, value):
        if value is not None:
            self.attrs["form"] = value
        elif "form" in self.attrs:
            del self.attrs["form"]

    @property
    def formaction(self):
        """
        The 'formaction' attribute of the <button> element specifies the URL of the file that will process the input control when the form is submitted.
        """
        return self.attrs.get("formaction", None)

    @formaction.setter
    def formaction(self, value):
        if value is not None:
            self.attrs["formaction"] = value
        elif "formaction" in self.attrs:
            del self.attrs["formaction"]

    @property
    def formenctype(self):
        """
        The 'formenctype' attribute of the <button> element specifies how the form-data should be encoded when submitting it to the server.
        Possible values: "application/x-www-form-urlencoded", "multipart/form-data", or "text/plain".
        """
        return self.attrs.get("formenctype", None)

    @formenctype.setter
    def formenctype(self, value):
        if value is not None:
            self.attrs["formenctype"] = value
        elif "formenctype" in self.attrs:
            del self.attrs["formenctype"]

    @property
    def formmethod(self):
        """
        The 'formmethod' attribute of the <button> element specifies the HTTP method to use when sending form-data.
        Possible values: "GET" or "POST".
        """
        return self.attrs.get("formmethod", None)

    @formmethod.setter
    def formmethod(self, value):
        if value is not None:
            self.attrs["formmethod"] = value
        elif "formmethod" in self.attrs:
            del self.attrs["formmethod"]

    @property
    def formnovalidate(self):
        """
        The 'formnovalidate' attribute of the <button> element specifies that the form-data should not be validated on submission.
        Possible values: True or False.
        """
        return self.attrs.get("formnovalidate", None)

    @formnovalidate.setter
    def formnovalidate(self, value):
        if value is not None:
            self.attrs["formnovalidate"] = value
        elif "formnovalidate" in self.attrs:
            del self.attrs["formnovalidate"]

    @property
    def formtarget(self):
        """
        The 'formtarget' attribute of the <button> element specifies a name or a keyword that indicates where to display the response that is received after submitting the form.
        Possible values: "_blank", "_self", "_parent", "_top", or a custom target name.
        """
        return self.attrs.get("formtarget", None)

    @formtarget.setter
    def formtarget(self, value):
        if value is not None:
            self.attrs["formtarget"]


class InputMixin:
    """
    All attribute specific to Input html tag except
    value feature. In most usual case, this should be
    part of staticCore.
    Input should always be accompanied with even handler
    Notes:     #skipping before_event_handler which is suppose to set
    #self.value to the value coming from browser
    #apps retrieve value by msg.value from event handler.
    """
    html_tag = "input"
    def __init__(self, *args, **kwargs):
        for k in ["name", "autofocus", "disabled", "readonly", "required", "form"]:
            if k in kwargs:
                self.attrs[k] = kwargs.get(k)

        self.domDict.debounce = kwargs.get("debounce", 200)
        self.domDict.html_tag = "input"

    @property
    def name(self):
        return self.attrs["name"]

    @name.setter
    def name(self, value):
        self.attrs["name"] = value

    @property
    def autofocus(self):
        return self.attrs["autofocus"]

    @autofocus.setter
    def autofocus(self, value):
        self.attrs["autofocus"] = value

    @property
    def disabled(self):
        return self.attrs["disabled"]

    @disabled.setter
    def disabled(self, value):
        self.attrs["disabled"] = value


class TextInputMixin(InputMixin):
    def __init__(self, *args, **kwargs):
        InputMixin.__init__(self, *args, **kwargs)
        self.attrs["type"] = "text"
        for attr in [
            "autocomplete",
            "maxlength",
            "minlength",
            "pattern",
            "placeholder",
            "size",
        ]:
            if attr in kwargs:
                self.attrs[attr] = kwargs[attr]
                self.htmlRender_attr.append(f'''{attr}="{kwargs.get(attr)}"''')

    @property
    def autocomplete(self):
        return self.attrs["autocomplete"]

    @autocomplete.setter
    def autocomplete(self, value):
        self.attrs["autocomplete"] = value

    @property
    def maxlength(self):
        return self.attrs["maxlength"]

    @maxlength.setter
    def maxlength(self, value):
        self.attrs["maxlength"] = value

    @property
    def minlength(self):
        return self.attrs["minlength"]

    @minlength.setter
    def minlength(self, value):
        self.attrs["minlength"] = value

    @property
    def pattern(self):
        return self.attrs["pattern"]

    @pattern.setter
    def pattern(self, value):
        self.attrs["pattern"] = value

    @property
    def placeholder(self):
        return self.attrs["placeholder"]

    @placeholder.setter
    def placeholder(self, value):
        self.attrs["placeholder"] = value

    @property
    def size(self):
        return self.attrs["size"]

    @size.setter
    def size(self, value):
        self.attrs["size"] = value


class CheckboxInputMixin(InputMixin):
    """
    The CheckboxInput class represents the HTML <input> element with the type "checkbox", which is used to create a
    checkbox input field in a web form for user input. This class is derived from the Input class and includes
    initialization and property setters specific to the checkbox input type.
    """

    def __init__(self, **kwargs):
        InputMixin.__init__(self, **kwargs)
        self.attrs["type"] = "checkbox"

        if "checked" in kwargs:
            self.attrs["checked"] = kwargs.get("checked", False)

        # def default_input(self, msg):
        #     return self.before_event_handler(msg)

        # if not self.no_events:
        #     self.on("before", default_input)

    # # event hook to toggle checkbox input
    # def before_event_handler(self, msg):
    #     if msg.event_type not in ["input", "change", "select"]:
    #         return

    #     self.domDict.attrs.checked = msg.checked

    @property
    def checked(self):
        """
        The 'checked' attribute of the <input> element with type "checkbox" specifies whether the checkbox is initially
        checked (True) or unchecked (False). The value is a boolean.
        """
        return self.attrs.get("checked", None)

    @checked.setter
    def checked(self, value):
        if value is not None:
            self.attrs["checked"] = value
        elif "checked" in self.attrs:
            del self.attrs["checked"]


class TextareaMixin(InputMixin):
    """
    The Textarea class represents the HTML <textarea> element, which is used to create a multiline text input field
    in a web form for user input. This class is derived from the TextInput class and includes initialization and property
    setters specific to the textarea element.
    """

    html_tag = "textarea"

    def __init__(self, **kwargs):
        InputMixin.__init__(self, **kwargs)
        self.domDict.html_tag = "textarea"
        for attr in ["cols", "rows", "wrap", "placeholder"]:
            if attr in kwargs:
                self.attrs[attr] = kwargs[attr]
                self.htmlRender_attr.append(f'''{attr}="{kwargs.get(attr)}"''')

    @property
    def cols(self):
        """
        The 'cols' attribute of the <textarea> element specifies the visible width of the textarea in average character
        widths. The value is a positive integer.
        """
        return self.attrs.get("cols", None)

    @cols.setter
    def cols(self, value):
        if value is not None:
            self.attrs["cols"] = value
        elif "cols" in self.attrs:
            del self.attrs["cols"]

    @property
    def rows(self):
        """
        The 'rows' attribute of the <textarea> element specifies the visible number of lines in the textarea.
        The value is a positive integer.
        """
        return self.attrs.get("rows", None)

    @rows.setter
    def rows(self, value):
        if value is not None:
            self.attrs["rows"] = value
        elif "rows" in self.attrs:
            del self.attrs["rows"]

    @property
    def wrap(self):
        """
        The 'wrap' attribute of the <textarea> element specifies how the text in the textarea is to be wrapped when
        submitted in a form. Possible values are:
        - 'soft': Default. Text is wrapped for appearance only. The text will be submitted with line breaks as entered.
        - 'hard': Text is wrapped for appearance and the submitted text will have line breaks at wrap points.
        """
        return self.attrs.get("wrap", None)

    @wrap.setter
    def wrap(self, value):
        if value is not None:
            self.attrs["wrap"] = value
        elif "wrap" in self.attrs:
            del self.attrs["wrap"]

    @property
    def placeholder(self):
        """ """
        return self.attrs.get("placeholder", None)

    @wrap.setter
    def wrap(self, value):
        if value is not None:
            self.attrs["placeholder"] = value
        elif "wrap" in self.attrs:
            del self.attrs["placeholder"]


class OptionMixin:
    """
    The Option class represents the HTML <option> element, which is used to define the individual options within a
    <select> element dropdown list. The attributes 'disabled', 'label', 'selected', 'value' are used to configure
    the option's behavior and appearance.
    """

    html_tag = "option"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "option"

        for attr in ["disabled", "label", "selected", "value"]:
            if attr in kwargs:
                self.attrs[attr] = kwargs[attr]
                self.htmlRender_attr.append(f'''{attr}="{kwargs.get(attr)}"''')

    @property
    def disabled(self):
        """
        The 'disabled' attribute of the <option> element specifies that the option should be disabled and not
        selectable. If present, the attribute does not need a value.
        """
        return "disabled" in self.attrs

    @disabled.setter
    def disabled(self, value):
        if value:
            self.attrs["disabled"] = None
        elif "disabled" in self.attrs:
            del self.attrs["disabled"]

    @property
    def label(self):
        """
        The 'label' attribute of the <option> element specifies a label for the option. If not present, the value of
        the 'value' attribute will be used as the label. The value is a string.
        """
        return self.attrs.get("label", None)

    @label.setter
    def label(self, value):
        if value is not None:
            self.attrs["label"] = value
        elif "label" in self.attrs:
            del self.attrs["label"]

    @property
    def selected(self):
        """
        The 'selected' attribute of the <option> element specifies that the option should be pre-selected when the
        page loads. If present, the attribute does not need a value.
        """
        return self.attrs["selected"]

    @selected.setter
    def selected(self, value):
        if value is not None:
            self.attrs["selected"] = value
        elif "selected" in self.attrs:
            del self.attrs["selected"]

    @property
    def value(self):
        """
        The 'value' attribute of the <option> element specifies the value to be sent to the server when the form is
        submitted. The value is a string.
        """
        return self.attrs.get("value", None)

    @value.setter
    def value(self, value):
        if value is not None:
            self.attrs["value"] = value
        elif "value" in self.attrs:
            del self.attrs["value"]


class SelectInputMixin(InputMixin):
    """
    The Select class represents the HTML <select> element, which is used to create a dropdown list for user input.
    This class is derived from the Input class and includes initialization and property setters specific to the
    select element.
    """

    html_tag = "select"

    def __init__(self, **kwargs):
        InputMixin.__init__(self, **kwargs)
        self.domDict.html_tag = "select"

        for attr in [
            "autofocus",
            "default",
            "disabled",
            "form",
            "multiple",
            "name",
            "required",
            "size",
        ]:
            if attr in kwargs:
                self.attrs[attr] = kwargs[attr]
                self.htmlRender_attr.append(f'''{attr}="{kwargs.get(attr)}"''')
                
    @property
    def multiple(self):
        """
        The 'multiple' attribute of the <select> element specifies that multiple options can be selected at once.
        If present, the attribute does not need a value.
        """
        return "multiple" in self.attrs

    @multiple.setter
    def multiple(self, value):
        if value:
            self.attrs["multiple"] = value
        elif "multiple" in self.attrs:
            del self.attrs["multiple"]

    @property
    def size(self):
        """
        The 'size' attribute of the <select> element specifies the number of visible options in the dropdown list.
        The value is a positive integer.
        """
        return self.attrs.get("size", None)

    @size.setter
    def size(self, value):
        if value is not None:
            self.attrs["size"] = value
        elif "size" in self.attrs:
            del self.attrs["size"]


class HrMixin:
    """
    The `Hr` class corresponds to the HTML `<hr>` element. The HTML `<hr>` element represents a thematic break between paragraph-level elements. For example, a shift of topic in a section of a text, or a transition to a different set of design elements.

    In terms of semantics, it can be thought of as a separator that splits the content into different sections. It's often used in documents, slides, books and such to denote a change of sections or chapters.

    The `<hr>` element does not have any special attributes, but it can use all the global HTML attributes like `class`, `id`, `style`, etc.

    Note: The `<hr>` element is a void element, it does not have a closing tag.
    """

    html_tag = "hr"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "hr"


class CodeMixin:
    """
    The `Code` class represents the HTML <code> element. This tag is used to define a piece of
    computer code. The content inside is displayed in the browser's default monospace font.

    It is typically used when displaying code snippets in HTML or documenting HTML itself. Note
    that it does not perform syntax highlighting or other transformations on the contained code.
    """

    html_tag = "code"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "code"


class PreMixin:
    """
    The `Pre` class represents the HTML <pre> element. This tag represents preformatted text
    which is to be presented exactly as written in the HTML file. The text is typically rendered
    in a non-proportional ("monospace") font exactly as it is laid out in the file. Whitespace
    inside this element is displayed as typed.

    """

    html_tag = "pre"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "pre"


class AMixin:
    """
    The A class represents the HTML <a> element, which is used to create a hyperlink.
    """

    html_tag = "a"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "a"
        for key in [
            "href",
            "title",
            "rel",
            "download",
            "target",
            "scroll",
            "scroll_option",
            "block_option",
            "inline_option",
        ]:
            if key in kwargs:
                self.attrs[key] = kwargs[key]
                self.htmlRender_attr.append(f'''{key}="{kwargs.get(key)}"''')
        if kwargs.get("bookmark", None) is not None:
            # bookmark = kwargs["bookmark"]
            # self.attrs["href"] = "#" + str(bookmark.id)
            # self.attrs["scroll_to"] = str(bookmark.id)
            #TODO: needs to be implemented yet
            pass
            
    # Add getters and setters for the new attributes

    # @property
    # def bookmark(self):
    #     """
    #     The 'bookmark' attribute represents a reference to another element on the page.
    #     When clicked, the hyperlink will scroll to the specified element.
    #     """
    #     return self.attrs.get("bookmark", None)

    # @bookmark.setter
    # def bookmark(self, value):
    #     if value is not None:
    #         self.attrs["bookmark"] = value
    #         self.attrs["href"] = "#" + str(value.id)
    #         self.attrs["scroll_to"] = str(value.id)
    #     elif "bookmark" in self.attrs:
    #         del self.attrs["bookmark"]

    # @property
    # def scroll(self):
    #     """
    #     The 'scroll' attribute represents whether scrolling is enabled when the hyperlink is clicked.
    #     If set to True, the browser will scroll to the specified element smoothly.
    #     """
    #     return self.attrs.get("scroll", False)

    # @scroll.setter
    # def scroll(self, value):
    #     self.attrs["scroll"] = value

    # @property
    # def scroll_option(self):
    #     """
    #     The 'scroll_option' attribute specifies the type of scrolling when the hyperlink is clicked.
    #     Possible values are "auto" or "smooth".
    #     """
    #     return self.attrs.get("scroll_option", "smooth")

    # @scroll_option.setter
    # def scroll_option(self, value):
    #     self.attrs["scroll_option"] = value

    # @property
    # def block_option(self):
    #     """
    #     The 'block_option' attribute specifies the vertical alignment of the target element when scrolling.
    #     Possible values are "start", "center", "end", or "nearest". Defaults to "start".
    #     """
    #     return self.attrs.get("block_option", "start")

    # @block_option.setter
    # def block_option(self, value):
    #     self.attrs["block_option"] = value

    # @property
    # def inline_option(self):
    #     """
    #     The 'inline_option' attribute specifies the horizontal alignment of the target element when scrolling.
    #     Possible values are "start", "center", "end", or "nearest". Defaults to "nearest".
    #     """
    #     return self.attrs.get("inline_option", "nearest")

    # @inline_option.setter
    # def inline_option(self, value):
    #     self.attrs["inline_option"] = value

    @property
    def href(self):
        """ """
        return self.attrs.get("href")

    @href.setter
    def href(self, value):
        if f'''href="{self.attrs["href"]}"''' in self.htmlRender_attr:
            self.htmlRender_attr.remove(f'''href="{self.attrs["href"]}"''')
        self.attrs["href"] = value
        self.htmlRender_attr.append(f'''href="{value}"''')
        self.prepare_htmlRender()


class SourceMixin:
    """
    The `Source` class corresponds to the HTML `<source>` element. This element specifies multiple media resources for media elements (`<picture>`, `<audio>` and `<video>`).
    """

    html_tag = "source"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "source"


class StyleMixin:
    """
    The `Style` class corresponds to the HTML `<style>` element. This element is used to embed CSS styles in an HTML document.
    """

    def __init__(self, **kwargs):
        self.domDict.html_tag = "style"


class TdMixin:
    """
    The `Td` class corresponds to the HTML `<td>` element. This element defines a cell of a table that contains data.
    """

    html_tag = "td"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "td"


class ThMixin:
    """
    The `Th` class corresponds to the HTML `<th>` element. This element defines a header cell in a table.
    """

    def __init__(self, **kwargs):
        self.domDict.html_tag = "td"


class TimeMixin:
    """
    The `Time` class corresponds to the HTML `<time>` element. This element represents a specific period in time.
    """

    def __init__(self, **kwargs):
        self.domDict.html_tag = "time"


class TrackMixin:
    """
    The `Track` class corresponds to the HTML `<track>` element. This element is used as a child of the media elements, `<audio>` and `<video>`. It lets you specify timed text tracks (or time-based data), for example to automatically handle subtitles.
    """

    def __init__(self, **kwargs):
        self.domDict.html_tag = "track"


class VideoMixin:
    """
    The `Video` class corresponds to the HTML `<video>` element. This element is used to embed video content in an HTML document.
    """

    def __init__(self, **kwargs):
        self.domDict.html_tag = "video"


class UlMixin:
    """
    The `Ul` class corresponds to the HTML `<ul>` element. The `<ul>` element represents an unordered list of items, typically rendered as a bulleted list.

    This element is typically used to represent a list of items where the order does not explicitly matter, like a list of bullet points. It can be nested, so lists can contain sublists, both unordered (`<ul>`) and ordered (`<ol>`).

    Each item in the list is marked up using a `<li>` (list item) element.
    """

    html_tag = "ul"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "ul"


class LiMixin:
    """
    The `Li` class corresponds to the HTML `<li>` element. This element is used to represent an item in a list. It must be contained within a parent element, like an ordered list (`<ol>`) or an unordered list (`<ul>`).
    """

    html_tag = "li"

    def __init__(self, **kwargs):
        self.domDict.html_tag = "li"


# ============================ end ChartJSMixin ===========================


class ImgMixin:
    """
    The `Img` class corresponds to the HTML `<img>` element. The `<img>` element represents an image in an HTML document.

    """

    html_tag = "img"

    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "img"
        for key in ["alt", "crossorigin", "height", "ismap", "longdesc", "sizes", "src", "srcset", "usemap", "width"]:
            if key in kwargs:
                self.attrs[key] = kwargs[key]
                self.htmlRender_attr.append(f'''{key}="{kwargs.get(key)}"''')

    @property
    def alt(self):
        """
        alt: A text description of the image, providing a textual alternative for users who cannot see the image.
        """
        return self.attrs.get("alt", None)

    @alt.setter
    def alt(self, value):
        if value is None:
            self.attrs.pop("alt", None)
        else:
            self.htmlRender_attr.remove(f'''alt="{self.attrs["alt"]}"''')
            self.attrs["alt"] = value
            self.htmlRender_attr.append(f'''alt="{self.attrs["alt"]}"''')
            
    @property
    def crossorigin(self):
        """
        crossorigin: A CORS settings attribute that indicates how the element handles crossorigin requests.
        Possible values: 'anonymous', 'use-credentials'
        """
        return self.attrs.get("crossorigin", None)

    @crossorigin.setter
    def crossorigin(self, value):
        if value is None:
            self.attrs.pop("crossorigin", None)
        else:
            self.htmlRender_attr.remove(f'''crossorigin="{self.attrs["crossorigin"]}"''')
            self.attrs["crossorigin"] = value
            self.htmlRender_attr.append(f'''crossorigin="{self.attrs["crossorigin"]}"''')

    @property
    def height(self):
        """
        height: The intrinsic height of the image, in pixels. Must be a positive integer.
        """
        return self.attrs.get("height", None)

    @height.setter
    def height(self, value):
        if value is None:
            self.attrs.pop("height", None)
        else:
            self.htmlRender_attr.remove(f'''height="{self.attrs["height"]}"''')
            self.attrs["height"] = value
            self.htmlRender_attr.append(f'''height="{self.attrs["height"]}"''')
    #TODO: fix for htmlRender_attr

    @property
    def ismap(self):
        """
        ismap: Indicates that the image is part of a server-side image map.
        Value should be a boolean: True or False.
        """
        return self.attrs.get("ismap", None)

    @ismap.setter
    def ismap(self, value):
        if value is None:
            self.attrs.pop("ismap", None)
        else:
            self.attrs["ismap"] = value

    @property
    def longdesc(self):
        """
        longdesc: A URL to a more detailed description of the image.
        """
        return self.attrs.get("longdesc", None)

    @longdesc.setter
    def longdesc(self, value):
        if value is None:
            self.attrs.pop("longdesc", None)
        else:
            self.attrs["longdesc"] = value


class H1Mixin:
    """
    The `H1` class corresponds to the HTML `<h1>` element. It represents the top level heading in HTML.

    The `<h1>` tag is used to indicate the most important (or highest-level) heading on the page. It's typically reserved for the title or main heading of the page.
    """

    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "h1"


class H2Mixin:
    """
    The `H2` class corresponds to the HTML `<h2>` element. It is used to denote a second level heading.
    It's typically used for subheadings of the top-level heading (H1).
    """

    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "h2"
        super().__init__(*args, **kwargs)


class H3Mixin:
    """
    The `H3` class corresponds to the HTML `<h3>` element. It represents a third level heading.
    It's typically used for subheadings of the second-level heading (H2).
    """
    html_tag = "h3"
    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "h3"
        super().__init__(*args, **kwargs)


class H4Mixin:
    """
    The `H4` class corresponds to the HTML `<h4>` element. It represents a fourth level heading.
    It's typically used for subheadings of the third-level heading (H3).
    """
    html_tag = "h4"
    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "h4"
        super().__init__(*args, **kwargs)


class H5Mixin:
    """
    The `H5` class corresponds to the HTML `<h5>` element. It represents a fifth level heading.
    It's typically used for subheadings of the fourth-level heading (H4).
    """
    html_tag = "h5"
    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "h5"
        super().__init__(*args, **kwargs)


class H6Mixin:
    """
    The `H6` class corresponds to the HTML `<h6>` element. It represents the sixth and lowest level heading.
    It's typically used for subheadings of the fifth-level heading (H5).
    """
    html_tag = "h6"
    def __init__(self, *args, **kwargs):
        self.domDict.html_tag = "h6"
        super().__init__(*args, **kwargs)


class FormMixin:
    """
    The Form class represents the HTML <form> element, which is used to create a web form for user input.
    The attributes 'accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate',
    and 'target' are used to configure the form's behavior and submission settings.
    """
    html_tag = "form"
    def __init__(self, **kwargs):
        self.domDict.html_tag = "form"
        for attr in [
            "accept-charset",
            "action",
            "autocomplete",
            "enctype",
            "method",
            "name",
            "novalidate",
            "target",
        ]:
            if attr in kwargs:
                self.attrs[attr] = kwargs[attr]
                self.htmlRender_attr.append(f'''{attr}="{kwargs.get(attr)}"''')

    # Add getters and setters for "accept-charset", "action", "autocomplete", "enctype", "method", "name", "novalidate", and "target"

    @property
    def accept_charset(self):
        """
        The 'accept-charset' attribute of the <form> element specifies the character encodings that are
        to be used for the form submission. The value is a space-separated list of character encoding names.
        Example: "UTF-8 ISO-8859-1"
        """
        return self.attrs.get("accept-charset", None)

    @accept_charset.setter
    def accept_charset(self, value):
        if value is not None:
            self.attrs["accept-charset"] = value
        elif "accept-charset" in self.attrs:
            del self.attrs["accept-charset"]

    @property
    def action(self):
        """
        The 'action' attribute of the <form> element specifies the URL where the form data should be
        submitted when the form is submitted. The value is an absolute or relative URL.
        """
        return self.attrs.get("action", None)

    @action.setter
    def action(self, value):
        if value is not None:
            self.attrs["action"] = value
        elif "action" in self.attrs:
            del self.attrs["action"]

    @property
    def autocomplete(self):
        """
        The 'autocomplete' attribute of the <form> element specifies whether the browser should enable
        autocomplete for the entire form. The value is either 'on' or 'off'.
        """
        return self.attrs.get("autocomplete", None)

    @autocomplete.setter
    def autocomplete(self, value):
        if value is not None:
            self.attrs["autocomplete"] = value
        elif "autocomplete" in self.attrs:
            del self.attrs["autocomplete"]

    @property
    def enctype(self):
        """
        The 'enctype' attribute of the <form> element specifies how the form data should be encoded when
        submitted to the server. Possible values are:
        - 'application/x-www-form-urlencoded': Default encoding for forms with no file upload.
        - 'multipart/form-data': Required when uploading files.
        - 'text/plain': No encoding, spaces are converted to "+" symbols.
        """
        return self.attrs.get("enctype", None)

    @enctype.setter
    def enctype(self, value):
        if value is not None:
            self.attrs["enctype"] = value
        elif "enctype" in self.attrs:
            del self.attrs["enctype"]

    @property
    def method(self):
        """
        The 'method' attribute of the <form> element specifies the HTTP method to use when submitting the
        form data. Possible values are 'get' and 'post'. The default value is 'get'.
        """
        return self.attrs.get("method", None)

    @method.setter
    def method(self, value):
        if value is not None:
            self.attrs["method"] = value
        elif "method" in self.attrs:
            del self.attrs["method"]

    @property
    def name(self):
        """
        The 'name' attribute of the <form> element specifies a name for the form. This can be used for
        scripting purposes, such as referencing the form from JavaScript.
        """
        return self.attrs.get("name", None)

    @name.setter
    def name(self, value):
        if value is not None:
            self.attrs["name"] = value
        elif "name" in self.attrs:
            del self.attrs["name"]

    @property
    def novalidate(self):
        """
        The 'novalidate' attribute of the <form> element is a boolean attribute. When present, it specifies
        that the form should not be validated when submitted.
        """
        return self.attrs.get("novalidate", None)

    @novalidate.setter
    def novalidate(self, value):
        if value is not None:
            self.attrs["novalidate"] = value
        elif "novalidate" in self.attrs:
            del self.attrs["novalidate"]

    @property
    def target(self):
        """
        The 'target' attribute of the <form> element specifies where the response received after submitting
        the form should be displayed. Possible values are:
        - '_blank': The response opens in a new window or tab.
        - '_self': The response opens in the same frame (default value).
        - '_parent': The response opens in the parent frame.
        - '_top': The response opens in the full body of the window.
        - 'framename': The response opens in a named frame.
        """
        return self.attrs.get("target", None)

    @target.setter
    def target(self, value):
        if value is not None:
            self.attrs["target"] = value
        elif "target" in self.attrs:
            del self.attrs["target"]


class NavMixin:
    """ """
    html_tag = "nav"
    def __init__(self, **kwargs):
        self.domDict.html_tag = "nav"


class FooterMixin:
    """ """
    html_tag = "footer"
    def __init__(self, **kwargs):
        self.domDict.html_tag = "footer"
