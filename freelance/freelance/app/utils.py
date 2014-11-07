from datetime import datetime, date


def format_json(x):
    """Use as 'default' attribute in json.dumps to allow datetime."""
    if isinstance(x, (datetime, date)):
        return x.isoformat()
