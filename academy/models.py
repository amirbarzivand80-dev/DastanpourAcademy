from django.db import models

class Course(models.Model):

    COURSE_TYPES = [
        ("online", "آنلاین"),
        ("offline", "حضوری"),
        ("free", "رایگان"),
    ]

    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    course_type = models.CharField(
        max_length=20,
        choices=COURSE_TYPES
    )

    description = models.TextField()

    price = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True
    )
    teacher = models.CharField(
    max_length=100,
    default="",
    blank=True
    )

    start_date = models.CharField(
    max_length=50,
    default="",
    blank=True
    )

    start_time = models.CharField(
    max_length=20,
    default="",
    blank=True
    )

    end_time = models.CharField(
    max_length=20,
    default="",
    blank=True
    )

    capacity = models.PositiveIntegerField(
    default=10
    )

    location = models.CharField(
    max_length=200,
    default="",
    blank=True
    )

    duration = models.CharField(
    max_length=100,
    default="",
    blank=True
    )

    level = models.CharField(
    max_length=50,
    default="",
    blank=True
)

    prerequisite = models.TextField(
    default="",
    blank=True
    )

    intro_video = models.URLField(
    blank=True,
    default=""
)

    intro_pdf = models.FileField(
    upload_to="course_pdf/",
    blank=True,
    null=True
)

    status = models.CharField(
    max_length=20,
    choices=[
        ("open", "باز"),
        ("closed", "تکمیل ظرفیت"),
    ],
    default="open"
)
    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
class CourseSession(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to="course_videos/",
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to="course_pdfs/",
        blank=True,
        null=True
    )

    attachment = models.FileField(
        upload_to="course_files/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
class CourseStudent(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="students"
    )

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_paid = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            "course",
            "user",
        )

    def __str__(self):
        return f"{self.user.full_name} - {self.course.title}"
    
class CourseTopic(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="topics"
    )

    title = models.CharField(
        max_length=200
    )

    order = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return self.title
    

    
class CourseImage(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="course_gallery/"
    )


class CourseFeature(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="features"
    )

    icon = models.CharField(
    max_length=100,
    default="fa-solid fa-star"
    )

    title = models.CharField(
    max_length=200,
    default=""
    )


    description = models.CharField(
    max_length=300,
    default="",
    blank=True
    )
    def __str__(self):
        return self.title
    
class SessionProgress(models.Model):

    student = models.ForeignKey(
        CourseStudent,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    session = models.ForeignKey(
        CourseSession,
        on_delete=models.CASCADE
    )

    is_completed = models.BooleanField(
        default=False
    )

    watched_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.user.full_name} - {self.session.title}"
    
from django.conf import settings


class CourseFavorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_favorites"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="favorite_courses"
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("user", "course")


    def __str__(self):
        return f"{self.user.full_name} - {self.course.title}"