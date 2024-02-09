# SimplePluginFramework
SPF is a simple, low-code, dependency free plugin framework following the design principals laid out by Marty Alchin in his blog post [A Simple Plugin Framework](https://web.archive.org/web/20190415035530/http://martyalchin.com/2008/jan/10/simple-plugin-framework/)


If you like, you can visit our [Docs pages](https://iviyg0t.github.io/SimplePluginFramework/).


# Install

`pip install simple-plugin-framework`


# Fundamentals Of A Plugin Framework

SPF is a dead simple, low code, pure python plugin framework.  There are three primary requirements for a plugin system:

## Declaration

> The framework needs to provide a mechanism for declaring a mount point for plugins

**How**

Declare a mount point by inheriting from `spf.PluginMount` metaclass.

```python
from spf import PluginMount

class MyMountPoint(metaclass=PluginMount):
    entry_point = "my_mount_point"
```

## Registration

> The framework needs to be able to register a plugin to a declared mount point.

**How**

Register a mount point by inheriting from your defined `MountPoint` class.

```python
class MyPlugin(MyMountPoint):
    pass
```

## Discovery

> The framework needs to be able to discover what plugins are available.

**How**

Discovery can happen in two ways...

1. If the plugin is imported, then the MountPoint discovers it:

```python

from my_pkg import MyMountPoint
from my_plugin import MyPlugin

print(MyMountPoint.plugins)

> {'MyPlugin': <class "__main__.MyPlugin">}
```
2. You can call the `MyMountPoint.load()` method to load plugins via `entry_points`.

Plugins can be provided to the mount points via python `entry_points`.  Entry points can be provided by various build tools like [setuptools](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#entry-points-for-plugins) or [poetry](https://python-poetry.org/docs/plugins#plugin-package)

```python

from my_pkg import MyMountPoint

MyMountPoint.load()
print(MyMountPoint.plugins)

> {'MyPlugin': <class "__main__.MyPlugin">}
```


