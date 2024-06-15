from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, get_objects_for_user
from unfold.admin import ModelAdmin


class GuardedAdminBase(ModelAdmin, GuardedModelAdmin):

    # app是否在主页面中显示的话由该函数决定
    def has_module_permission(self, request):
        if request.user.is_superuser and request.user.is_active:
            return True
        return request.user.has_perm("view_%s" % self.opts.model_name)

    def get_model_perms(self, request):
        return {
            "add": True,
            "change": True,
            "delete": True,
        }

    # 内部用来获取某个用户有权限访问的数据行
    def get_model_objs(self, request, action=None, klass=None):
        if request.user.is_superuser and request.user.is_active:
            return super().get_queryset(request)

        opts = self.opts
        actions = ["view", "add", "change", "delete"]
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(
            user=request.user,
            perms=[f"{perm}_{model_name}" for perm in actions],
            klass=klass,
            any_perm=True,
        )

    # 在显示数据列表的时候，哪些数据显示，哪些不显示，由该函数控制
    def get_queryset(self, request):
        if request.user.is_superuser and request.user.is_active:
            return super().get_queryset(request)
        data = self.get_model_objs(request)

        # 用户只允许看到自己的数据
        if request.user.is_authenticated:
            data = data.filter(owner=request.user)
        return data

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change:
            for related_object in form.instance._meta.related_objects:
                related_set = getattr(form.instance, related_object.get_accessor_name())
                for obj in related_set.all():
                    if not obj.owner_id:
                        obj.owner_id = request.user.id
                        obj.save()

    # 用来判断某个用户是否有某个数据行的权限
    def has_perm(self, request, obj, action):
        if request.user.is_superuser:
            return True
        opts = self.opts
        codename = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{codename}", obj)
        else:
            return request.user.has_perm(f"{opts.app_label}.{codename}")

    # 是否有查看某个数据行的权限
    def has_view_permission(self, request, obj=None):
        return self.has_perm(request, obj, "view")

    # 是否有修改某个数据行的权限
    def has_change_permission(self, request, obj=None):
        return self.has_perm(request, obj, "change")

    # 是否有删除某个数据行的权限
    def has_delete_permission(self, request, obj=None):
        return self.has_perm(request, obj, "delete")

    # 用户应该拥有他新增的数据行的所有权限
    def save_model(self, request, obj, form, change):
        if not getattr(obj, "owner", None):
            obj.owner = request.user
        result = super().save_model(request, obj, form, change)
        if not request.user.is_superuser and not change:
            opts = self.opts
            actions = ["view", "add", "change", "delete"]
            [assign_perm(f"{opts.app_label}.{action}_{opts.model_name}", request.user, obj) for action in actions]
        return result

    def owner_name(self, obj):
        if obj.owner:
            return obj.owner.username
        return '-'

    owner_name.short_description = '所属用户'
