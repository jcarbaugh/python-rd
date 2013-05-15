from __future__ import unicode_literals
import datetime
import json
import os
import unittest

import pytz
from rd import RD, Link, Property, Title, jrd, xrd

PWD = os.path.abspath(os.path.dirname(__file__))


class TestXRDProperty(unittest.TestCase):

    def testassignment(self):

        # test RD object

        rd = RD()
        rd.properties.append('http://example.com/lang')
        rd.properties.append(('http://example.com/lang', 'en-US'))
        rd.properties.append(Property('http://example.com/lang'))
        rd.properties.append(Property('http://example.com/lang', 'en-US'))

        prop = rd.properties[0]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertIsNone(prop.value)

        prop = rd.properties[1]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertEqual(prop.value, "en-US")

        prop = rd.properties[2]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertIsNone(prop.value)

        prop = rd.properties[3]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertEqual(prop.value, "en-US")

        expected = [None, u'en-US', None, u'en-US']
        actual = [p.value for p in rd.properties("http://example.com/lang")]
        self.assertEqual(expected, actual)

        # test Link object

        link = Link()
        link.properties.append('http://example.com/lang')
        link.properties.append(('http://example.com/lang', 'en-US'))
        link.properties.append(Property('http://example.com/lang'))
        link.properties.append(Property('http://example.com/lang', 'en-US'))

        prop = link.properties[0]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertIsNone(prop.value)

        prop = link.properties[1]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertEqual(prop.value, "en-US")

        prop = link.properties[2]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertIsNone(prop.value)

        prop = link.properties[3]
        self.assertEqual(prop.type, "http://example.com/lang")
        self.assertEqual(prop.value, "en-US")

        expected = [None, u'en-US', None, u'en-US']
        actual = [p.value for p in rd.properties("http://example.com/lang")]
        self.assertEqual(expected, actual)

    def testequals(self):

        # same type and value
        p1 = Property('http://example.com/p1', '1234')
        p2 = Property('http://example.com/p1', '1234')
        self.assertTrue(p1 == p2)

        # same type, no value
        p1 = Property('http://example.com/p1')
        p2 = Property('http://example.com/p1')
        self.assertTrue(p1 == p2)

    def testnotequals(self):

        # same value, different type
        p1 = Property('http://example.com/p1', '1234')
        p2 = Property('http://example.com/p2', '1234')
        self.assertFalse(p1 == p2)

        # same type, different value
        p1 = Property('http://example.com/p1', '1234')
        p2 = Property('http://example.com/p1', '9876')
        self.assertFalse(p1 == p2)

        # same type, one value missing
        p1 = Property('http://example.com/p1')
        p2 = Property('http://example.com/p1', '12345')
        self.assertFalse(p1 == p2)

        # different type, no value
        p1 = Property('http://example.com/p1')
        p2 = Property('http://example.com/p2')
        self.assertFalse(p1 == p2)


class TestXRDTitle(unittest.TestCase):

    def testassignment(self):

        link = Link()
        link.titles.append('myfeed')
        link.titles.append(('myfeed', 'en-US'))
        link.titles.append(Title('myfeed'))
        link.titles.append(Title('myfeed', 'en-US'))

        title = link.titles[0]
        self.assertEqual(title.value, "myfeed")
        self.assertIsNone(title.lang)

        title = link.titles[1]
        self.assertEqual(title.value, "myfeed")
        self.assertEqual(title.lang, "en-US")

        title = link.titles[2]
        self.assertEqual(title.value, "myfeed")
        self.assertIsNone(title.lang)

        title = link.titles[3]
        self.assertEqual(title.value, "myfeed")
        self.assertEqual(title.lang, "en-US")

    def testequals(self):

        # same title and lang
        t1 = Title('myfeed', lang='en-US')
        t2 = Title('myfeed', lang='en-US')
        self.assertTrue(t1 == t2)

        # same title, no lang
        t1 = Title('myfeed')
        t2 = Title('myfeed')
        self.assertTrue(t1 == t2)

    def testnotequals(self):

        # same title, different lang
        t1 = Title('myfeed', 'en-US')
        t2 = Title('myfeed', 'en-GB')
        self.assertTrue(t1 != t2)

        # same lang, different title
        t1 = Title('myfeed', 'en-US')
        t2 = Title('yourfeed', 'en-US')
        self.assertTrue(t1 != t2)

        # same title, one missing lang
        t1 = Title('myfeed')
        t2 = Title('myfeed', 'en-GB')
        self.assertTrue(t1 != t2)

        # different title, no lang
        t1 = Title('myfeed')
        t2 = Title('yourfeed')
        self.assertTrue(t1 != t2)


class TestJRDDeserialization(unittest.TestCase):

    def setUp(self):
        self.rd = jrd.loads("""{
            "links": [
                {
                    "template": "http://google.com/{uri}",
                    "titles": {
                        "en_us": "this is my rel",
                        "default": "the real rel"
                    }
                }
            ],
            "properties": {
                "mimetype": "text/plain"
            }
        }""")

    def testproperty(self):
        prop = self.rd.properties[0]
        self.assertEqual(prop.type, "mimetype")
        self.assertEqual(prop.value, "text/plain")

    def testlink(self):
        link = self.rd.links[0]
        self.assertEqual(link.template, "http://google.com/{uri}")

        for title in link.titles:
            if title.lang == "en_us":
                self.assertEqual(title.value, "this is my rel")
            elif title.lang == "none":
                self.assertEqual(title.value, "the real rel")


class TestXRDDeserialization(unittest.TestCase):

    def setUp(self):
        self.rd = xrd.loads("""<?xml version="1.0" ?>
            <XRD xml:id="1234" xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">
                <Property type="mimetype">text/plain</Property>
                <Property type="none"></Property>
                <Link template="http://google.com/{uri}">
                    <Title xml:lang="en_us">this is my rel</Title>
                </Link>
            </XRD>
            """)

    def testxmlid(self):
        self.assertEqual(self.rd.xml_id, "1234")

    def testproperty(self):
        prop = self.rd.properties[0]
        self.assertEqual(prop.type, "mimetype")
        self.assertEqual(prop.value, "text/plain")

    def testnilproperty(self):
        prop = self.rd.properties[1]
        self.assertEqual(prop.type, "none")
        self.assertTrue(prop.value is None)

    def testlink(self):
        link = self.rd.links[0]
        self.assertEqual(link.template, "http://google.com/{uri}")


class TestJRDSerialization(unittest.TestCase):

    def setUp(self):
        self.rd = RD()
        self.rd.properties.append(('mimetype', 'text/plain'))
        self.rd.links.append(Link(template="http://google.com/{uri}"))
        self.doc = json.loads(self.rd.to_json())

    def testproperty(self):
        props = self.doc['properties']
        self.assertTrue('mimetype' in props)
        self.assertEqual(props['mimetype'], 'text/plain')

    def testlink(self):
        link = self.doc['links'][0]
        self.assertEqual(link['template'], "http://google.com/{uri}")


class TestXRDSerialization(unittest.TestCase):

    def setUp(self):
        self.rd = RD('9876')
        self.rd.properties.append(('mimetype', 'text/plain'))
        self.rd.properties.append('none')
        self.rd.links.append(Link(template="http://google.com/{uri}"))
        self.doc = self.rd.to_xml().documentElement

    def testxmlid(self):
        self.assertEqual(self.doc.getAttribute('xml:id'), '9876')

    def testproperty(self):
        prop = self.doc.getElementsByTagName('Property')[0]
        self.assertEqual(prop.getAttribute('type'), 'mimetype')
        self.assertEqual(xrd._get_text(prop), 'text/plain')

    def testnilproperty(self):
        prop = self.doc.getElementsByTagName('Property')[1]
        self.assertEqual(prop.getAttribute('type'), 'none')
        self.assertEqual(prop.getAttribute('xsi:nil'), 'true')
        self.assertTrue(xrd._get_text(prop) is None)

    def testlink(self):
        link = self.doc.getElementsByTagName('Link')[0]
        self.assertEqual(link.getAttribute('template'), "http://google.com/{uri}")


class ExamplesTestCase(unittest.TestCase):

    def load_example(self, filename):
        path = os.path.join(PWD, 'examples', filename)
        with open(path) as infile:
            data = infile.read()
        return data


class TextConversionExamples(ExamplesTestCase):

    def testrfc6415a(self):

        data = self.load_example("xrd-rfc6415-A.xml")
        x = xrd.loads(data)

        data = self.load_example("jrd-rfc6415-A.json")
        j = jrd.loads(data)

        self.assertEqual(x.subject, j.subject)
        self.assertEqual(x.expires, j.expires)
        self.assertEqual(x.aliases[0], j.aliases[0])
        self.assertEqual(x.aliases[1], j.aliases[1])

        xprops = [str(p) for p in x.properties]
        jprops = [str(p) for p in j.properties]
        self.assertItemsEqual(xprops, jprops)

        xlink = list(x.links("copyright"))[0]
        jlink = list(j.links("copyright"))[0]
        self.assertEqual(xlink.template, jlink.template)

        xauthors = list(x.links("author"))
        jauthors = list(j.links("author"))

        self.assertEqual(len(xauthors), len(jauthors))

        # first authors link

        xlink = xauthors[0]
        jlink = jauthors[0]

        self.assertEqual(xlink.type, jlink.type)
        self.assertEqual(xlink.href, jlink.href)
        self.assertEqual(sorted(xlink.properties), sorted(jlink.properties))
        self.assertEqual(sorted(xlink.titles), sorted(jlink.titles))

        # second authors link

        xlink = xauthors[1]
        jlink = jauthors[1]

        self.assertEqual(xlink.href, jlink.href)
        self.assertEqual(sorted(xlink.titles), sorted(jlink.titles))


class TestXRDExamples(ExamplesTestCase):

    def test10b1(self):

        data = self.load_example("xrd-1.0-b1.xml")
        rd = xrd.loads(data)

        self.assertEqual(rd.expires, datetime.datetime(1970, 1, 1, tzinfo=pytz.utc))
        self.assertEqual(rd.subject, "http://example.com/gpburdell")

        prop = rd.properties[0]
        self.assertEqual(prop.type, "http://spec.example.net/type/person")
        self.assertIsNone(prop.value)

        link = rd.links[0]
        self.assertEqual(link.rel, "http://spec.example.net/auth/1.0")
        self.assertEqual(link.href, "http://services.example.com/auth")

        # this is a big, multipart link

        link = rd.links[1]
        self.assertEqual(link.rel, "http://spec.example.net/photo/1.0")
        self.assertEqual(link.href, "http://photos.example.com/gpburdell.jpg")
        self.assertEqual(link.type, "image/jpeg")

        title = link.titles[0]
        self.assertEqual(title.value, "User Photo")
        self.assertEqual(title.lang, "en")

        title = link.titles[1]
        self.assertEqual(title.value, "Benutzerfoto")
        self.assertEqual(title.lang, "de")

        prop = link.properties[0]
        self.assertEqual(prop.type, "http://spec.example.net/created/1.0")
        self.assertEqual(prop.value, "1970-01-01")

    # signature stuff is not yet supported
    # def test10b2(self):
    #     data = self.load_example("xrd-1.0-b2.xml")
    #     xrd.loads(data)


class TestJRDExamples(ExamplesTestCase):

    def test41hostmeta(self):

        data = self.load_example("jrd-wf02-4.1-hostmeta.json")
        rd = jrd.loads(data)
        link = rd.find_link('lrdd')

        self.assertEqual(link.type, "application/json")
        self.assertEqual(link.template, "https://example.com/lrdd/?f=json&uri={uri}")

    def test41lrdd(self):

        data = self.load_example("jrd-wf02-4.1-lrdd.json")
        rd = jrd.loads(data)

        self.assertEqual(rd.subject, "acct:bob@example.com")
        self.assertEqual(rd.expires, datetime.datetime(2012, 10, 12, 20, 56, 11, tzinfo=pytz.utc))
        self.assertEqual(rd.aliases[0], "http://www.example.com/~bob/")

        links = {
            "http://webfinger.net/rel/avatar": "http://www.example.com/~bob/bob.jpg",
            "http://webfinger.net/rel/profile-page": "http://www.example.com/~bob/",
            "http://packetizer.com/rel/blog": "http://blogs.example.com/bob/",
            "vcard": "http://www.example.com/~bob/bob.vcf",
        }

        for rel, href in links.items():
            link = rd.find_link(rel)
            self.assertEqual(link.href, href)

    def test42hostmeta(self):

        data = self.load_example("jrd-wf02-4.2-hostmeta.json")
        rd = jrd.loads(data)

        self.assertEqual(rd.subject, "acct:carol@example.com")

        links = {
            "http://webfinger.net/rel/avatar": "http://example.com/~alice/alice.jpg",
            "http://specs.openid.net/auth/2.0/provider": "https://openid.example.com/carol",
        }

        for rel, href in links.items():
            link = rd.find_link(rel)
            self.assertEqual(link.href, href)


if __name__ == '__main__':
    unittest.main()
