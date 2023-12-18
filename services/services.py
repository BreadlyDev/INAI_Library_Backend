from rest_framework.response import Response


def base_view(request, function, *args, **kwargs):
    try:
        object_data = function(request, *args, **kwargs)
        return Response(object_data)
    except Exception as e:
        return Response({"Error happened": e})


def get_all_objects(model):
    return model.objects.all()


def get_objects_by_field(model, field: str, value: any):
    field_kw: dict = {field: value}
    return model.objects.filter(**field_kw)


def deserialize_data(request, serialized_class, raise_exception=True, model=None,
                     partial=False, return_model=False):
    serializer = serialized_class(data=request.data, model=model, partial=partial)
    serializer.is_valid(raise_exception=raise_exception)
    model_ = serializer.save()
    if return_model:
        return serializer.validated_data, model_
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
