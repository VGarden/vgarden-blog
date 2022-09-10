# vgarden-blog

link: https://vgarden.github.io/vgarden-blog/

# For authors

## How-to regenerate the Table of Content

The Table of Content (navigation.json) is an auto-generated file that should not be updated manually.

In order to auto-generate it from a Python script, please proceed to the following procedure:

```py
cd autogen
python main.py "the_absolute_path_to_root_project"
```

This script will generate for you the `navigation.json` file in the root project.
The configuration file should be found in `autogen/config` file, relatively to the root folder.

No dependencies required. Python 3.9 is fine, but other versions should be good too.

**Note**: If you do not provide the path to the folder,
the script will try to find it from the environment variable `VGARDEN_CONFIG`.
This might be of interest for githooks.
