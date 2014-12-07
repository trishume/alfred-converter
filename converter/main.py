import os
import sys
import constants
import functools
from xml.etree import cElementTree as ET


def create_item(parent, attrib={}, **kwargs):
    # Make sure all attributes are strings
    for k in list(attrib):
        attrib[k] = str(attrib[k])

    item = ET.SubElement(parent, 'item', attrib)
    for k, v in kwargs.items():
        elem = ET.SubElement(item, k)
        elem.text = str(v)

    return item


def item_creator(parent):
    def _item_creator(*args, **kwargs):
        return create_item(parent, *args, **kwargs)

    return _item_creator


def to_xml(f):
    @functools.wraps(f)
    def _to_xml(*args, **kwargs):
        try:
            # The repetition of the items, tree and write methods are needed
            # since the objects get changed in-place. This catches all errors.
            items = ET.Element('items')
            tree = ET.ElementTree(items)

            f(items, *args, **kwargs)

            assert items, 'No results for %r' % args
            tree.write(sys.__stdout__)

        except Exception, e:  # pragma: no cover
            items = ET.Element('items')
            tree = ET.ElementTree(items)
            item = ET.SubElement(items, 'item', valid='no')

            title = ET.SubElement(item, 'title')
            title.text = '%s: %s' % (e.__class__.__name__, str(e))

            import traceback
            subtitle = ET.SubElement(item, 'subtitle')
            subtitle.text = '%s: %s' % (
                traceback.format_exc().split('\n')[-4].strip(),
                traceback.format_exc().split('\n')[-3].strip(),
            )
            tree.write(sys.__stdout__)
            traceback.print_exc()

    return _to_xml


@to_xml
def scriptfilter(items, query):
    import convert
    import cPickle as pickle

    try:
        with open(constants.UNITS_PICKLE_FILE, 'rb') as fh:
            units = pickle.load(fh)
    except:  # pragma: no cover
        units = convert.Units()
        units.load(constants.UNITS_XML_FILE)

        with open(constants.UNITS_PICKLE_FILE, 'wb') as fh:
            pickle.dump(units, fh, -1)

        with open(constants.UNITS_PICKLE_FILE, 'rb') as fh:
            units = pickle.load(fh)

    list(convert.main(units, query, item_creator(items)))


if __name__ == '__main__':
    scriptfilter(' '.join(sys.argv[1:]))
else:
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')