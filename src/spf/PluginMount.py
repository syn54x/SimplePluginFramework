from abc import ABCMeta
from typing import List, Any

try:
    from importlib.metadata import entry_points

    USE_LEGACY = False

except ImportError:
    import pkg_resources

    USE_LEGACY = True


class PluginMount(ABCMeta):
    REQUIRED_STATIC_PROPERTIES = ["entry_point"]

    def __init__(
        cls: Any, name: str, bases: List[Any], attrs: List[Any]
    ) -> None:  # sourcery skip: instance-method-first-arg-name
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
            cls._verify()
            cls.plugins[cls.__name__] = cls

    def _verify(cls):  # sourcery skip: instance-method-first-arg-name
        """Verifies that the required static properties are implemented by the class.

        Raises
        ------
        NotImplementedError
            If any of the required static properties are not implemented.

        Examples
        --------

        >>> _verify(MyClass)
        """
        base = cls.__mro__[-2]
        if not_implemented := set(cls.REQUIRED_STATIC_PROPERTIES) - set(base.__dict__.keys()):
            raise NotImplementedError(
                f"Attribute(s) {not_implemented} not implemented by class {base.__name__}"
            )

    def load(cls) -> None:  # sourcery skip: instance-method-first-arg-name
        """Loads all plugins registered under the specified entry point.

        Returns
        -------
        None

        Example
        -------

        >>> load(PluginMount)
        """
        if cls == PluginMount:
            return None

        eps = (
            pkg_resources.iter_entry_points(cls.entry_point)
            if USE_LEGACY
            else entry_points().select(group=cls.entry_point)
        )

        for ep in eps:
            ep.load()
