def assertDictContainsKeyWithValue(obj, key, value):
    assert key in obj, f"{key} is not in dict: {obj}"
    assert obj[key] == value, f"{obj[key]} does not equal {value}"


def assertDictContainsKeyWithValueType(obj, key, value):
    assert key in obj, f"{key} is not in dict: {obj}"
    assert isinstance(obj[key], value)


def assertIsInstance(obja, objb):

    assert isinstance(obja, objb)


def assertEqual(obja, objb):

    assert obja == objb
