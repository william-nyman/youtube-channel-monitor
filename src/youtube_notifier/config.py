import tomllib


def interval_minutes():
    with open("config.toml", "rb") as file:
        data = tomllib.load(file)
        interval = data["check_interval_minutes"]
    return interval
