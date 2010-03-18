import xml.etree.ElementTree as ET

__all__ = ['xml_to_dict']

def xml_to_dict(xml):
    tree = ET.fromstring(xml)
    return _tree_to_dict(tree)

def _tree_to_dict(tree):
    ret = {}

    if len(tree.items()) > 0:
        ret.update(dict(tree.items()))

    for child in tree.getchildren():
        new_item = _tree_to_dict(child)
        if ret.has_key(child.tag):
            if isinstance(ret[child.tag], list):
                ret[child.tag].append(new_item)
            else:
                ret[child.tag] = [ret[child.tag], new_item]
        else:
            ret[child.tag] = new_item

    if tree.text is None:
        text = ''
    else:
        text = tree.text.strip()

    if len(ret) > 0:
        if len(text) > 0:
            ret['_text'] = text
    else:
        ret = text

    return ret
