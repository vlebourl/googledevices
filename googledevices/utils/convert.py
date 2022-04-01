"""Convert/restructure data sets."""


def get_device_type(device_type=0):
    """Return the device type from a device_type list."""
    device_types = {
        0: "Unknown",
        1: "Classic - BR/EDR devices",
        2: "Low Energy - LE-only",
        3: "Dual Mode - BR/EDR/LE",
    }
    return (
        device_types[device_type]
        if device_type in [1, 2, 3]
        else device_types[0]
    )


def format_json(source):
    """Structure json."""
    from json import dumps

    return dumps(source, indent=4, sort_keys=True)
