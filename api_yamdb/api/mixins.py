from rest_framework import mixins, viewsets


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """
    A viewset that provides `create` action.
    """
    pass


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset that provides `create`, 'delete' and `retrieve list obj` actions.
    """
    pass
