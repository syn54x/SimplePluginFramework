from abc import ABCMeta
from typing import List, Any

import pkg_resources


class PluginMount(ABCMeta):
    REQUIRED_STATIC_PROPERTIES = ["entry_point"]

    def __init__(cls: Any, name: str, bases: List[Any], attrs: List[Any]) -> None: # sourcery skip: instance-method-first-arg-name
        

        if not hasattr(cls, "plugins"):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = {}
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins[cls.__name__] = cls
    @classmethod
    def _verify_attributes(cls):
        for base in set(cls.__mro__):
            if not_implemented := set(cls.REQUIRED_STATIC_PROPERTIES) - set(
                base.__dict__.keys()
            ):
                raise NotImplementedError(
                    f"Attribute(s) {not_implemented} not implemented by class {base.__name__}"
                )

    @classmethod
    def load(cls):
        cls._verify_attributes()
        for entry_point in pkg_resources.iter_entry_points(cls.entry_point):
            entry_point.load()
