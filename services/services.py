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


def serialize_data(model, serialized_class, many=False):
    serializer = serialized_class(instance=model, many=many)
    return serializer.data


def deserialize_data(request, serialized_class, raise_exception=True, model=None,
                     partial=False, return_model=False):
    serializer = serialized_class(data=request.data, model=model, partial=partial)
    serializer.is_valid(raise_exception=raise_exception)
    model = serializer.save()
    if return_model:
        return serializer.validated_data, model
    return serializer.validated_data


def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    return wrapper
