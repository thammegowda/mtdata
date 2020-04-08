# MT Data Crawler

This crawler craws the metadata of machine translation datasets. 

As of now these MT data indexes are supported 
- [Opus - the Open Parallel Corpus](http://opus.nlpl.eu/)

## Requirements
Scrapy 2.0+, python 3.7+


## How to run

### OPUS crawl

    # One entry per coprus. url is %s-%s to replace it with langs list. 
    scrapy crawl opus -o opus-min.jl   # Always use JSON Lines
    
    # One entry per item.
    scrapy crawl opus -o opus-flat.jl  -a flat=True

Minimal JSON example
```json
{"url": "http://opus.nlpl.eu/download.php?f=EUconst/v1/moses%s-%s.txt.zip",
"name": "EUconst_v1", 
"langs": [["cs", "da"], ["cs", "de"], ["da", "de"], ...]
}
```
Flat JSON example:
```json
{"url": "http://opus.nlpl.eu/download.php?f=JW300/v1/xml/ab-ach.xml.gz", 
"name": "JW300_v1_xml", "id": "JW300/v1/xml/ab-ach.xml.gz", 
"langs": ["ab", "ach"], 
"title": "sentence alignments for 'Acoli-Abkhazian' (180 aligned documents, 18.2k links, 0.6M tokens)"}
```



## Developers
-  [Thamme Gowda](https://twitter.com/thammegowda)




