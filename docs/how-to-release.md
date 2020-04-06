# Release instructions 

Using twine : https://twine.readthedocs.io/en/latest/ 

1. Update the `__version__` in `awkg/__init__.py`
2. Build :: `$ python setup.py sdist bdist_wheel`    
3. Upload to **testpypi** ::  `$ twine upload -r testpypi dist/*`
4. Upload to **pypi** ::  `$ twine upload -r pypi dist/*`


### The `.pypirc` file

The rc file `~/.pypirc` should have something like this 
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username:Thamme.Gowda
password:<password_here>


[testpypi]
repository: https://test.pypi.org/legacy/
username:Thamme.Gowda
password:<password_here>
```