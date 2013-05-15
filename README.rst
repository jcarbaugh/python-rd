Resource Descriptors in Python
==============================

Supports serialization/deserialization of XRD (http://docs.oasis-open.org/xri/xrd/v1.0/xrd-1.0.html) and JRD (http://tools.ietf.org/html/rfc6415).

Outstanding issues:

- support ds:Signature
- support XRDS
- parsing of Expires date stamp from XML
- more tests are needed

Basic usage::

    from rd import RD, Link

    lnk = Link(rel='http://spec.example.net/photo/1.0',
               type='image/jpeg',
               href='http://photos.example.com/gpburdell.jpg')
    lnk.titles.append(('User Photo', 'en'))
    lnk.titles.append(('Benutzerfoto', 'de'))
    lnk.properties.append(('http://spec.example.net/created/1.0', '1970-01-01'))

    rd = RD(subject='http://example.com/gpburdell')
    rd.properties.append('http://spec.example.net/type/person')
    rd.links.append(lnk)

    rd.to_json()
    rd.to_xml()
