from fastapi import Request

from services.valueset import ValueSetIndex

def get_value_set_index(request: Request) -> ValueSetIndex:
    return request.app.state.value_set_index