from rest_framework import serializers

from . import models
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ['name', ]


# 子序列化类
class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = [
            'name',
            'title',
            'signature',
            'image',
            'brief',
            'role_name'
        ]


class CourseModelSerializer(serializers.ModelSerializer):
    teacher = TeacherModelSerializer()
    class Meta:
        model = models.Course
        fields = [
            'name',
            'course_img',
            'level_name',
            'period',
            'price',
            'students',
            'sections',
            'teacher',
            'section_list'
        ]
