# SimplePluginFramework
SPF is a simple, low-code, dependency free plugin framework following the design principals laid out by Marty Alchin in his blog post [A Simple Plugin Framework](https://web.archive.org/web/20190415035530/http://martyalchin.com/2008/jan/10/simple-plugin-framework/)

# Install

`pip install spf`

# Usage

```python

from spf import PluginMount

class MyMountPoint(metaclass=PluginMount):
    entry_point = "my_mount_point"

class MyPlugin(MyMountPoint):
    pass

print(MyMountPoint.plugins)
```
