from rest_framework import mixins, viewsets


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Базовый класс с возможностью !только! создания записей и получения списка.
    """
    pass
