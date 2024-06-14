from django.contrib.auth.models import User
from unfold.admin import ModelAdmin


class OwnerAdminBase(ModelAdmin):
    def save_model(self, request, obj, form, change):
        # 检查 obj 是否有 owner 字段，并且该字段的类型是 User
        if hasattr(obj, "owner") and obj._meta.get_field("owner").remote_field.model == User:
            # 把当前请求的用户设置为 owner
            obj.owner = request.user
        obj.save()
        # ModelAdmin 本身的逻辑
        for action in self.get_actions_submit_line(request):
            if action.action_name not in request.POST:
                continue

            action.method(request, obj)
