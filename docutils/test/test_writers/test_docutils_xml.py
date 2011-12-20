#!/usr/bin/env python

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for docutils XML writer.
"""

from __init__ import DocutilsTestSupport

import sys
import docutils
import docutils.core

# sample strings:

source = u"""\
Test

----------

Test. \xe4\xf6\xfc\u20ac"""

xmldecl = u"""<?xml version="1.0" encoding="iso-8859-1"?>
"""

doctypedecl = u"""\
<!DOCTYPE document PUBLIC "+//IDN docutils.sourceforge.net\
//DTD Docutils Generic//EN//XML"\
 "http://docutils.sourceforge.net/docs/ref/docutils.dtd">
"""

generatedby = u'<!-- Generated by Docutils %s -->\n' % docutils.__version__

bodynormal = u"""\
<document source="&lt;string&gt;"><paragraph>Test</paragraph>\
<transition/><paragraph>Test. \xe4\xf6\xfc&#8364;</paragraph>\
</document>"""

bodynewlines = u"""\
<document source="&lt;string&gt;">
<paragraph>Test</paragraph>
<transition/>
<paragraph>Test. \xe4\xf6\xfc&#8364;</paragraph>
</document>
"""

bodynewlines_old = u"""\
<document source="&lt;string&gt;">
<paragraph>
Test
</paragraph>
<transition/>
<paragraph>
Test. \xe4\xf6\xfc&#8364;
</paragraph>
</document>
"""

bodyindents = u"""\
<document source="&lt;string&gt;">
    <paragraph>Test</paragraph>
    <transition/>
    <paragraph>Test. \xe4\xf6\xfc&#8364;</paragraph>
</document>
"""

bodyindents_old = u"""\
<document source="&lt;string&gt;">
    <paragraph>
        Test
    </paragraph>
    <transition/>
    <paragraph>
        Test. \xe4\xf6\xfc&#8364;
    </paragraph>
</document>
"""

# New formatting introduced in versions 2.7.3 and 3.2.3 on 2011-11-18
# to fix http://bugs.python.org/issue4147
# (Some distributions ship also earlier versions with this patch.)
if (sys.version_info < (2, 7, 3) or
    sys.version_info[0] == 3 and sys.version_info < (3, 2, 3)):
    whitespace_fix = False
else:
    whitespace_fix = True

def publish_xml(settings):
    return docutils.core.publish_string(source=source.encode('utf8'),
                                        reader_name='standalone',
                                        writer_name='docutils_xml',
                                        settings_overrides=settings)


class DocutilsXMLTestCase(DocutilsTestSupport.StandardTestCase):

    settings = {'input_encoding': 'utf8',
                'output_encoding': 'iso-8859-1',
                '_disable_config': 1}

    def test_publish(self):
        for self.settings['xml_declaration'] in True, False:
            for self.settings['doctype_declaration'] in True, False:
                expected = u''
                if self.settings['xml_declaration']:
                    expected += xmldecl
                if self.settings['doctype_declaration']:
                    expected += doctypedecl
                expected += generatedby
                expected += bodynormal
                result = publish_xml(self.settings)
                self.assertEqual(result, expected.encode('latin1'))

    def test_publish_indents(self):
        self.settings['indents'] = True
        self.settings['newlines'] = False
        self.settings['xml_declaration'] = False
        self.settings['doctype_declaration'] = False
        result = publish_xml(self.settings)

        # New formatting introduced in versions 2.7.3 and 3.2.3
        if whitespace_fix:
            expected = (generatedby + bodyindents).encode('latin1')
        else:
            expected = (generatedby + bodyindents_old).encode('latin1')
        # Some distributions patch also earlier versions:
        if (result != expected and not whitespace_fix):
            expected = (generatedby + bodyindents).encode('latin1')

        self.assertEqual(result, expected)

    def test_publish_newlines(self):
        self.settings['newlines'] = True
        self.settings['indents'] = False
        self.settings['xml_declaration'] = False
        self.settings['doctype_declaration'] = False
        result = publish_xml(self.settings)

        # New formatting introduced in versions 2.7.3 and 3.2.3
        if whitespace_fix:
            expected = (generatedby + bodynewlines).encode('latin1')
        else:
            expected = (generatedby + bodynewlines_old).encode('latin1')
        # Some distributions patch also earlier versions:
        if (result != expected and not whitespace_fix):
            expected = (generatedby + bodynewlines).encode('latin1')

        self.assertEqual(result, expected)


if __name__ == '__main__':
    import unittest
    unittest.main()
