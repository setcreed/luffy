from rest_framework import serializers

from . import models
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseCategory
        fields = ('name', 'id')


# 子序列化类
class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = (
            'name',
            'title',
            'signature',
            'image',
            'brief',
            'role_name',
        )

class CourseModelSerializer(serializers.ModelSerializer):
    teacher = TeacherModelSerializer()
    class Meta:
        model = models.Course
        fields = (
            'id',
            'name',
            'brief',
            'course_img',
            'level_name',
            'period',
            'price',
            'pub_sections',
            'students',
            'sections',
            'teacher',
            'section_list',
        )
        # fields = (
        #     'name',
        # )


# 子序列化
class CourseSectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = (
            'name',
            'duration',
            'free_trail',
            'orders',
        )

class CourseChapterModelSerializer(serializers.ModelSerializer):
    coursesections = CourseSectionModelSerializer(many=True)
    class Meta:
        model = models.CourseChapter
        fields = (
            'id',
            'name',
            'chapter',
            'coursesections',
        )
