Testing a package locally
```
pip uninstall memory_map_generator
python3 setup.py sdist
pip install dist/memory_map_generator-x.x.x.tar.gz
```

Upload to pip
```
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

Basic test
```
python3 setup.py test
```

Reset regression test
```
python3 setup.py test --addopts --regtest-reset
```

View regression output
```
python3 setup.py test --addopts --regtest-tee
```
