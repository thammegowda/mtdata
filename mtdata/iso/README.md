# ISO 639_3 Code Lookup

## CLI 
```bash
$ ✗ python -m mtdata.iso kn te ta en de nl xyz English Kannada French fr eng fra err ERR Error error
Input   ISO639_3        Name
kn      kan     Kannada
te      tel     Telugu
ta      tam     Tamil
en      eng     English
de      deu     German
nl      nld     Dutch
xyz     -none-  -none-
English eng     English
Kannada kan     Kannada
French  fra     French
fr      fra     French
eng     eng     English
fra     fra     French
err     err     Erre
ERR     err     Erre
Error   -none-  -none-
error   -none-  -none-
```

## Python API
```python

from mtdata.iso import iso3_code

def test_iso3_code():
    assert iso3_code("kn") == 'kan'
    assert iso3_code("KN") == 'kan'
    assert iso3_code("Kannada") == 'kan'
    assert iso3_code("kannada") == 'kan'
    assert iso3_code("kan") == 'kan'
    assert iso3_code("KANNADA") == 'kan'
    assert iso3_code("KaNnAdA") == 'kan'
    assert iso3_code("KAN") == 'kan'

    assert iso3_code("xyz") == None
    assert iso3_code("xyz", default="Error") == "Error"
    try:
        iso3_code("xyz", fail_error=True)
        assert False, 'Expected an exception'
    except:
        assert True
```

