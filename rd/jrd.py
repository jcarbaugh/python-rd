from __future__ import unicode_literals
import json
import isodate

from rd.core import RD, Attribute, Element, Link, Property, Title


def _clean_dict(d):
    for key in list(d.keys()):
        if not d[key]:
            del d[key]


def loads(content):

    def expires_handler(key, val, obj):
        obj.expires = isodate.parse_datetime(val)

    def subject_handler(key, val, obj):
        obj.subject = val

    def aliases_handler(key, val, obj):
        for alias in val:
            obj.aliases.append(alias)

    def properties_handler(key, val, obj):
        for prop in val:
            prop_type = list(prop.keys())[0]
            prop_value = list(prop.values())[0]
            obj.properties.append(Property(prop_type, prop_value))

    def titles_handler(key, val, obj):
        for title in val:
            title_lang = list(title.keys())[0]
            if title_lang == 'default':
                title_lang = None
            title_value = list(title.values())[0]
            obj.titles.append(Title(title_value, title_lang))

    def links_handler(key, val, obj):
        for link in val:
            l = Link()
            l.rel = link.get('rel', None)
            l.type = link.get('type', None)
            l.href = link.get('href', None)
            l.template = link.get('template', None)
            if 'titles' in link:
                titles_handler('title', link['titles'], l)
            if 'properties' in link:
                properties_handler('property', link['properties'], l)
            obj.links.append(l)

    def namespace_handler(key, val, obj):
        for namespace in val:
            ns = list(namespace.keys())[0]
            ns_uri = list(namespace.values())[0]
            obj.attributes.append(Attribute("xmlns:%s" % ns, ns_uri))

    handlers = {
        'expires': expires_handler,
        'subject': subject_handler,
        'aliases': aliases_handler,
        'properties': properties_handler,
        'links': links_handler,
        'titles': titles_handler,
        'namespace': namespace_handler,
    }

    def unknown_handler(key, val, obj):
        if ':' in key:
            (ns, name) = key.split(':')
            key = "%s:%s" % (ns, name.capitalize())
        obj.elements.append(Element(key, val))

    doc = json.loads(content)

    rd = RD()

    for key, value in doc.items():
        handler = handlers.get(key, unknown_handler)
        handler(key, value, rd)

    return rd


def dumps(xrd):

    doc = {
        "aliases": [],
        "links": [],
        "namespace": [],
        "properties": [],
        "titles": [],
    }

    #list_keys = doc.keys()

    for attr in xrd.attributes:
        if attr.name.startswith("xmlns:"):
            ns = attr.name.split(":")[1]
            doc['namespace'].append({ns: attr.value})

    if xrd.expires:
        doc['expires'] = xrd.expires.isoformat()

    if xrd.subject:
        doc['subject'] = xrd.subject

    for alias in xrd.aliases:
        doc['aliases'].append(alias)

    for prop in xrd.properties:
        doc['properties'].append({prop.type: prop.value})

    for link in xrd.links:

        link_doc = {
            'title': [],
            'property': [],
        }

        if link.rel:
            link_doc['rel'] = link.rel

        if link.type:
            link_doc['type'] = link.type

        if link.href:
            link_doc['href'] = link.href

        if link.template:
            link_doc['template'] = link.template

        for prop in link.properties:
            link_doc['properties'].append({prop.type: prop.value})

        for title in link.titles:
            lang = title.lang or "default"
            link_doc['titles'].append({lang: title.value})

        _clean_dict(link_doc)

        doc['links'].append(link_doc)

    for elem in xrd.elements:
        doc[elem.name.lower()] = elem.value

    _clean_dict(doc)

    return json.dumps(doc)