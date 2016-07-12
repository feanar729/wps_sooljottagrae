from django.db.models import Q

from rest_framework.filters import(
        SearchFilter,
        OrderingFilter,
)

from rest_framework.generics import (
        ListAPIView,
        CreateAPIView,
        RetrieveAPIView,
        UpdateAPIView,
        RetrieveUpdateAPIView,
        DestroyAPIView,
)

from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
        IsAdminUser,
        IsAuthenticatedOrReadOnly,
)

from posts.models import Post

from apis.serializers import (
        PostCreateUpdateSerializer,
        PostListSerializer,
        PostDetailSerializer,
)

from apis.permissions import IsOwnerOrReadOnly


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'user__username']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryst_list.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(user__username__icontains=query)
                    ).distinct()
        return queryset_list


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "pk"


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
