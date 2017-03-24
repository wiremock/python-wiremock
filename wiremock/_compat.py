from __future__ import unicode_literals
import six

PY2 = six.PY2
PY3 = six.PY3

# conversions
unichr = six.unichr
if PY3:
    long_ = int
else:
    long_ = long
text_type = six.text_type
string_types = six.string_types
integer_types = six.integer_types
bool_types = (bool, )
binary_types = (six.binary_type, )
float_types = (float, )
array_types = (tuple, list)
int_to_byte = six.int2byte

# iterator functions
iterkeys = six.iterkeys
itervalues = six.itervalues
iteritems = six.iteritems
iterlists = six.iterlists
iterbytes = six.iterbytes
reraise = six.reraise

with_metaclass = six.with_metaclass
add_metaclass = six.add_metaclass
print_ = six.print_
urllib = six.moves.urllib

get_method_self = six.get_method_self