Procedure for changes to example_typedef.json (please verify first)
```
python3 -m memory_map_manager.code_gen -cfgp example_typedef.json -ocfg example_typedef.json -ouc
```

Testing a package locally
```
sudo pip3 uninstall -y memory_map_manager
rm -rf sdist
python3 setup.py sdist
sudo pip3 install dist/memory_map_manager-x.x.x.tar.gz
```

Upload to pip
```
python3 setup.py sdist
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
