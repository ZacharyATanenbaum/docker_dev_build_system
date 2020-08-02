
## Contributing

### Overview

Feel free to fork this repo and send a pull request!


### Uploading to Pypi

Run the following commands from the base directory of this repo.
I.e. This directory with the `CONTRIBUTING.md` file.

```
# Build Package
python setup.py sdist bdist_wheel

# Send off to Twin
python -m twine upload dist/*
```
