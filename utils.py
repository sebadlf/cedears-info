def get_float(value):
    try:
        value = float(value.replace(",", ""))
    except:
        print("Error converting ", value)
        value = None

    return value