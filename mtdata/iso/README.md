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


# BCP 47

```bash
$ python -m mtdata.iso.bcp47 en English en_US en_GB en-Latn_US \
    kn kn-in kn-IN kn-Knda Kannada-Knda kannada-Deva-In kn-Knda-IN
INPUT   STANDARDIZED    LANG    SCRIPT  COUNTRY
en      eng     eng     None    None
English eng     eng     None    None
en_US   eng-US  eng     None    US
en_GB   eng-GB  eng     None    GB
en-Latn_US      eng-US  eng     None    US
kn      kan     kan     None    None
kn-in   kan-IN  kan     None    IN
kn-IN   kan-IN  kan     None    IN
kn-Knda kan     kan     None    None
Kannada-Knda    kan     kan     None    None
kannada-Deva-In kan-Deva-IN     kan     Deva    IN
kn-Knda-IN      kan-IN  kan     None    IN

```

RFC: https://www.rfc-editor.org/info/bcp47

* Country codes: (they did not give a download link; I scraped it)
  - https://www.iso.org/iso-3166-country-codes.html
* Script codes:
   - https://www.unicode.org/iso15924/codelists.html
   - Here is a nice download link: https://www.unicode.org/iso15924/iso15924.txt
* Lang code ISO 639:

* IANA Registry: it has
  * http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry 

## BCP 47 Convention

https://datatracker.ietf.org/doc/html/rfc5646#section-2.1.1

These conventions include:

* [ISO639-1] recommends that language codes be written in lowercase ('mn' Mongolian).
* [ISO15924] recommends that script codes use lowercase with the initial letter capitalized ('Cyrl' Cyrillic).
* [ISO3166-1] recommends that country codes be capitalized ('MN' Mongolia).

## Divergence from BCP 47

BCP 47 uses mixture of 2-letter and 3-letter ISO 639 codes. Here we use 3-letter codes (i.e. English is `eng` not `en`)


