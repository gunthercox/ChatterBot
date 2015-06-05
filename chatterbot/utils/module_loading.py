import importlib


def import_module(dotted_path):
    """
    Imports the specified module based on the
    dot notated import path for the module.
    """

    module_parts = dotted_path.split(".")
    module_path = ".".join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])
