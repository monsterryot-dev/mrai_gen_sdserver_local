def validateRouter(validatorDict):
    requiredKey = ["router", "prefix"]
    for key in validatorDict:
        if key not in requiredKey:
            raise KeyError(f"Invalid key in router configuration: {key}")