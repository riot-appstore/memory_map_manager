Testing a package locally
```
sudo pip3 uninstall memory_map_manager
python3 setup.py sdist
sudo pip3 install dist/memory_map_manager-x.x.x.tar.gz
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
