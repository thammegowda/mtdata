# Release instructions

Using twine : https://twine.readthedocs.io/en/latest/

1. Update the `__version__` in `mtdata/__init__.py`
   Clear `rm -rf build dist *.egg-info`   if those dir exist.
2. Build :: `$ python setup.py sdist bdist_wheel`
   where `sdist` is source code; `bdist_wheel` is universal ie. for all platforms
3.  Make docs: `docs/make-docs.sh`
   You may need to install these tools: `sudo apt install ruby-full; gem install asciidoctor kramdown-asciidoc`
4. Upload to **testpypi** ::  `$ twine upload -r testpypi dist/*`
5. Upload to **pypi** ::  `$ twine upload -r pypi dist/*`


### The `.pypirc` file

The rc file `~/.pypirc` should have something like this 
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username = __token__
password = <TOKEN HERE>

[testpypi]
repository: https://test.pypi.org/legacy/
username = __token__
password = <TOKEN HERE>
```