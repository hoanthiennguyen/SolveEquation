
def peek(list_based_stack: list):
    if len(list_based_stack) == 0:
        return None
    return list_based_stack[len(list_based_stack) - 1]


def check_is_an_integer(token):
    try:
        int(token)
        return True
    except TypeError:
        return False
    except ValueError:
        return False


def check_is_a_number(token):
    try:
        float(token)
        return True
    except TypeError:
        return False
    except ValueError:
        return False
