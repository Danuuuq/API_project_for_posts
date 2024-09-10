from rest_framework import exceptions, mixins


class CommentPostBaseMixin(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                f"Вы не можете редактировать чужие {self.object_viewset}!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                f"Вы не можете удалять чужие {self.object_viewset}!")
        super().perform_destroy(instance)
