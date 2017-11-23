import getpass
import os
from typing import Callable
from . import coordinator


def extra(name: str, desc: str) -> Callable:
    """
    Decorator for slave channel's "extra functions" interface.
    
    Args:
        name (str): A human readable name for the function.
        desc (str): A short description and usage of it. Use 
            ``{function_name}`` in place of the function name
            in the description.

    Returns:
        The decorated method.
    """

    def attr_dec(f):
        f.__setattr__("extra_fn", True)
        f.__setattr__("name", name)
        f.__setattr__("desc", desc)
        return f

    return attr_dec


def get_base_path() -> str:
    """
    Get the base data path for EFB. This is defined by the environment
    variable ``EFB_DATA_PATH``.
    
    When ``EFB_DATA_PATH`` is defined, the path is constructed by
    ``$EFB_DATA_PATH/$USERNAME``. By default, this gives
    ``~/.ehforwarderbot``.
    
    This method creates the queried path if not existing.
    
    Returns:
        str: The base path.
    """
    base_path = os.environ.get("EFB_DATA_PATH", None)
    if base_path:
        base_path = os.path.join(base_path, getpass.getuser(), "")
    else:
        base_path = os.path.expanduser("~/.ehforwarderbot/")
    os.makedirs(base_path, exist_ok=True)
    return base_path


def get_data_path(channel_id: str):
    """
    Get the path for channel data.
    
    This method creates the queried path if not existing.
    
    Args:
        channel_id (str): Channel ID

    Returns:
        str: The data path of selected channel.
    """
    profile = coordinator.profile
    base_path = get_base_path()
    data_path = os.path.join(base_path, 'profiles', profile, channel_id, "")
    os.makedirs(data_path, exist_ok=True)
    return data_path


def get_config_path(channel_id: str=None, ext: str='yaml') -> str:
    """
    Get path for configuration file. Defaulted to
    ``~/.ehforwarderbot/profiles/profile_name/channel_id/config.yaml``.
    
    This method creates the queried path if not existing. The config file will 
    not be created, however.
    
    Args:
        channel_id (str): Channel ID.
        ext (Optional[Str]): Extension name of the config file.
            Defaulted to ``"yaml"``.

    Returns:
        str: The path to the configuration file.
    """
    base_path = get_base_path()
    profile = coordinator.profile
    if channel_id:
        config_path = get_data_path(channel_id)
    else:
        config_path = os.path.join(base_path, 'profiles', profile)
    os.makedirs(config_path, exist_ok=True)
    return os.path.join(config_path, "config.%s" % ext)


def get_custom_channel_path() -> str:
    """
    Get the path for custom channels

    Returns:
        str: The path.
    """
    channel_path = os.path.join(get_base_path(), "channels")
    os.makedirs(channel_path, exist_ok=True)
    return channel_path