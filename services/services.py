from rest_framework.response import Response


def get_all_objects(model):
    return model.objects.all()


def get_objects_by_field(model, field: str, value: any):
    field_kw: dict = {field: value}
    return model.objects.filter(**field_kw)


def get_request_field_values(data: dict, fields: list[str]) -> list | dict:
    values: list = []
    for field in fields:
        if not data.get(field):
            continue
        values.append(data.get(field))
    return values


def serialize_data(model, serializer, many=False):
    result = serializer.__init__(model, many=many)
    return result.data


def deserialize_data(request, serializer, raise_exception=True, return_model=False):
    result = serializer.__init__(serializer, instance=None, data=request.data)
    result.is_valid(raise_exception=raise_exception)
    model = result.save()
    if return_model:
        return result, model
    return result


def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    return wrapper
