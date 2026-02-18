"""
Django models for the Flask application database.
These models map to existing MySQL tables.
"""

from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Category model for gallery items"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'myapp'
        db_table = 'categories'
        managed = False  # Don't let Django manage this table

    def __str__(self):
        return self.name


class Role(models.Model):
    """Role model for user permissions"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'myapp'
        db_table = 'roles'
        managed = False  # Don't let Django manage this table

    def __str__(self):
        return self.name


class Gallery(models.Model):
    """Gallery model for uploaded images and OCR results"""
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column='category_id',
        default=1
    )

    class Meta:
        app_label = 'myapp'
        db_table = 'gallery'
        managed = False  # Don't let Django manage this table
        ordering = ['-id']

    def __str__(self):
        return f"Gallery #{self.id} - {self.filename}"


class User(models.Model):
    """User model for application users"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        db_column='role_id',
        null=True,
        blank=True,
        default=2  # Default to 'user' role
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        app_label = 'myapp'
        db_table = 'users'
        managed = False  # Don't let Django manage this table
        ordering = ['-id']

    def __str__(self):
        return self.name


class Student(models.Model):
    """Student model for student management"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    course = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        app_label = 'myapp'
        db_table = 'students'
        managed = False  # Don't let Django manage this table
        ordering = ['-id']

    def __str__(self):
        return self.name


class WordData(models.Model):
    """Model to store extracted Word document text"""
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    text_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'myapp'
        db_table = 'word_data'
        managed = False
        ordering = ['-id']

    def __str__(self):
        return f"WordData #{self.id} - {self.filename}"


class WordImage(models.Model):
    """Model to store paths to extracted images from Word documents"""
    id = models.AutoField(primary_key=True)
    word_data = models.ForeignKey(
        WordData,
        on_delete=models.CASCADE,
        db_column='word_data_id',
        related_name='images'
    )
    image_path = models.CharField(max_length=255)
    label = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    round_number = models.IntegerField(default=0)
    audio_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'myapp'
        db_table = 'word_images'
        managed = False

    def __str__(self):
        return f"WordImage #{self.id} - {self.image_path}"
