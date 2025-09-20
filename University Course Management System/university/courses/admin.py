from django.contrib import admin
from .models import Student, Instructor, Course, Enrollment

# Inline to assign students inside Course admin
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'enrollment_date')
    search_fields = ('name',)
    list_filter = ('department',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'hire_date', 'course_count')

    def course_count(self, obj):
        return obj.course_set.count()
    course_count.short_description = "Courses Taught"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'title', 'credits', 'instructor', 'enrolled_students')
    inlines = [EnrollmentInline]

    def enrolled_students(self, obj):
        return obj.enrollment_set.count()
    enrolled_students.short_description = "Enrolled Students"

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'grade')
