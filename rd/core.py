import datetime
import logging

JRD_TYPES = ('application/json', 'application/xrd+json', 'text/json')
XRD_TYPES = ('application/xrd+xml', 'text/xml')

logger = logging.getLogger("rd")


def _is_str(s):
    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)


def loads(content, content_type):

    from rd import jrd, xrd

    content_type = content_type.split(";")[0]

    if content_type in JRD_TYPES:
        logger.debug("loads() loading JRD")
        return jrd.loads(content)

    elif content_type in XRD_TYPES:
        logger.debug("loads() loading XRD")
        return xrd.loads(content)


#
# special XRD types
#

class Attribute(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def __eq__(self, other):
        return str(self) == other

    def __str__(self):
        return "%s=%s" % (self.name, self.value)


class Element(object):

    def __init__(self, name, value, attrs=None):
        self.name = name
        self.value = value
        self.attrs = attrs or {}


class Title(object):

    def __init__(self, value, lang=None):
        self.value = value
        self.lang = lang

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        if self.lang:
            return "%s:%s" % (self.lang, self.value)
        return self.value


class Property(object):

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def __eq__(self, other):
        return str(self) == other

    def __str__(self):
        if self.value:
            return "%s:%s" % (self.type, self.value)
        return self.type


#
# special list types
#

class ListLikeObject(list):

    def __setitem__(self, key, value):
        value = self.item(value)
        super(ListLikeObject, self).__setitem__(key, value)

    def append(self, value):
        value = self.item(value)
        super(ListLikeObject, self).append(value)

    def extend(self, values):
        values = (self.item(value) for value in values)
        super(ListLikeObject, self).extend(values)


class AttributeList(ListLikeObject):

    def __call__(self, name):
        for attr in self:
            if attr.name == name:
                yield attr

    def item(self, value):
        if isinstance(value, (list, tuple)):
            return Attribute(*value)
        elif not isinstance(value, Attribute):
            raise ValueError('value must be an instance of Attribute')
        return value


class ElementList(ListLikeObject):

    def item(self, value):
        if not isinstance(value, Element):
            raise ValueError('value must be an instance of Type')
        return value


class TitleList(ListLikeObject):

    def item(self, value):
        if _is_str(value):
            return Title(value)
        elif isinstance(value, (list, tuple)):
            return Title(*value)
        elif not isinstance(value, Title):
            raise ValueError('value must be an instance of Title')
        return value


class LinkList(ListLikeObject):

    def __call__(self, rel):
        for link in self:
            if link.rel == rel:
                yield link

    def item(self, value):
        if not isinstance(value, Link):
            raise ValueError('value must be an instance of Link')
        return value


class PropertyList(ListLikeObject):

    def __call__(self, type_):
        for prop in self:
            if prop.type == type_:
                yield prop

    def item(self, value):
        if _is_str(value):
            return Property(value)
        elif isinstance(value, (tuple, list)):
            return Property(*value)
        elif not isinstance(value, Property):
            raise ValueError('value must be an instance of Property')
        return value


#
# Link object
#

class Link(object):

    def __init__(self, rel=None, type=None, href=None, template=None):
        self.rel = rel
        self.type = type
        self.href = href
        self.template = template
        self._titles = TitleList()
        self._properties = PropertyList()

    def get_titles(self):
        return self._titles
    titles = property(get_titles)

    def get_properties(self):
        return self._properties
    properties = property(get_properties)


#
# main RD class
#

class RD(object):

    def __init__(self, xml_id=None, subject=None):

        self.xml_id = xml_id
        self.subject = subject
        self._expires = None
        self._aliases = []
        self._properties = PropertyList()
        self._links = LinkList()
        self._signatures = []

        self._attributes = AttributeList()
        self._elements = ElementList()

    # ser/deser methods

    def to_json(self):
        from rd import jrd
        return jrd.dumps(self)

    def to_xml(self):
        from rd import xrd
        return xrd.dumps(self)

    # helper methods

    def find_link(self, rels, attr=None):
        if not isinstance(rels, (list, tuple)):
            rels = (rels,)
        for link in self.links:
            if link.rel in rels:
                if attr:
                    return getattr(link, attr, None)
                return link

    # custom elements and attributes

    def get_elements(self):
        return self._elements
    elements = property(get_elements)

    @property
    def attributes(self):
        return self._attributes

    # defined elements and attributes

    def get_expires(self):
        return self._expires

    def set_expires(self, expires):
        if not isinstance(expires, datetime.datetime):
            raise ValueError('expires must be a datetime object')
        self._expires = expires
    expires = property(get_expires, set_expires)

    def get_aliases(self):
        return self._aliases
    aliases = property(get_aliases)

    def get_properties(self):
        return self._properties
    properties = property(get_properties)

    def get_links(self):
        return self._links
    links = property(get_links)

    def get_signatures(self):
        return self._signatures
    signatures = property(get_links)
