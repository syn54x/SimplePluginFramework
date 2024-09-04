from abc import ABCMeta
from typing import List, Any
from functools import wraps

from singleton_decorator import singleton

try:
    from importlib.metadata import entry_points

    USE_LEGACY = False

except ImportError:
    import pkg_resources

    USE_LEGACY = True


@singleton
class MountPointRegistry:
    mount_points: dict = {}

    def register(self, mount_point: Any) -> None:
        self.mount_points[mount_point.__name__] = mount_point


def plugin_mount(cls):
    if not hasattr(cls, "entry_point"):
        raise AttributeError(f"`{cls.__name__}` does not have the required property `entry_point`")
    if getattr(cls, "entry_point") is None:
        raise AttributeError("`entry_point` cannot be None")

    MountPointRegistry().register(cls)

    @wraps(cls)
    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)

    return wrapper


class PluginMount(ABCMeta):
    """
    Metaclass for defining plugin mount points.

    Explanation
    -----------
    This metaclass is used to define plugin mount points, which are used as
    base classes for plugin implementations.  It provides functionality for
    registering and verifying plugin implementations.

    Parameters
    ----------
    name : str
        The name of the class.
    bases : List[Any]
        The base classes of the class.
    attrs : List[Any]
        The attributes of the class.

    Attributes
    ----------
    REQUIRED_STATIC_PROPERTIES : List[str]
        The list of required static properties that plugin implementations must implement.

    Methods
    -------
    __init__(cls, name, bases, attrs)
        Initializes the plugin mount point or registers a plugin implementation.
    verify(cls)
        Verifies that the required static properties are implemented by the class.
    load(cls)
        Loads all plugins registered under the specified entry point.
    """

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
            cls.verify()
            cls.plugins[cls.__name__] = cls

    def verify(cls):  # sourcery skip: instance-method-first-arg-name
        """Verifies that the required static properties are implemented by the class.

        Raises
        ------
        NotImplementedError
            If any of the required static properties are not implemented.

        Examples
        --------

        >>> MyMountPoint.verify()
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

        Examples
        --------

        >>> MyMountPoint.load()
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
