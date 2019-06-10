from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Worker(models.Model):

    supervisor = models.ForeignKey(
        User,
        verbose_name="Supervisor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(
        "Name of Worker", 
        max_length=50,
    )
    surname = models.CharField(
        "Surname of Worker", 
        max_length=50,
    )
    pesel = models.CharField(
        "Pesel",
        max_length=11,
    )
    salary = models.IntegerField(
        "Salary of Worker",
    )
    position = models.ForeignKey(
        "Position",
        verbose_name="Position of Worker",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    employment_date = models.DateField(
        "Date when Worker was employed", 
        auto_now=False, 
        auto_now_add=False,
    )
    promotion_date = models.DateField(
        "Date when Worker got promoted",
        auto_now=False,
        auto_now_add=False,
    )
    can_be_subbed_by = models.ManyToManyField(
        "Worker", 
        verbose_name="Can Be Subbed By",
        blank=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_position_id = self.position.id

    def __str__(self):
        return "ID {}: {} {}".format(self.pk, self.name, self.surname)

    def save(self, *args, **kwargs):
        if self.old_position_id != self.position.id:
            import datetime
            self.promotion_date = datetime.date.today()
            self.old_position_id = self.position.id
        super().save(*args, **kwargs)

class Substitution(models.Model):

    substitute_begin = models.DateField(
        "Date defining start of Substitution",
        auto_now=False,
        auto_now_add=False,
    )
    substitute_end = models.DateField(
        "Date defining end of Substitution",
        auto_now=False,
        auto_now_add=False,
    )
    substituted_worker = models.OneToOneField(
        "Worker",
        verbose_name="Worker to be Substituted",
        related_name="subbed",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    substituting_worker = models.ForeignKey(
        "Worker",
        verbose_name="Worker Substituting other",
        related_name="subbing",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reason = models.ForeignKey(
        "SubstitutionReason",
        verbose_name="Reason for Substitution",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "{} substituted by {}: {:%Y-%m-%d} - {:%Y-%m-%d}".format(
            self.substituted_worker, self.substituting_worker,
            self.substitute_begin, self.substitute_end,
        )

    def clean(self, *args, **kwargs):

        if self.substituted_worker == self.substituting_worker:
            raise ValidationError({
                "substituted_worker": "Cannot substitute yourself",
                "substituting_worker": "Cannot substitute yourself",
            })

        substituted_set = Substitution.objects.filter(substituted_worker=self.substituting_worker)
        if substituted_set:
            raise ValidationError({
                "substituting_worker": "Someone currently substituted cannot be substituting"
            })

        substituting_set = Substitution.objects.filter(substituting_worker=self.substituted_worker)
        if substituting_set:
            raise ValidationError({
                "substituted_worker": "This Worker is currently substituting someone"
            })

        super(Substitution, self).clean(*args, **kwargs)

class Permission(models.Model):

    name = models.CharField(
        "Name of Permission",
        max_length=100,
    )

    def __str__(self):
        return self.name

class Position(models.Model):

    name = models.CharField(
        "Name of Position",
        max_length=100,
        unique=True,
    )
    permissions = models.ManyToManyField(
        "Permission", 
        verbose_name="Permissions of Position",
        blank=True,
    )

    def __str__(self):
        return self.name

class SubstitutionReason(models.Model):

    desc = models.TextField(
        "Reason of Substitution",
        unique=True,
    )

    def __str__(self):
        return self.desc

class LogEntry(models.Model):

    substitute_begin = models.DateField(
        "Date defining start of Substitution",
        auto_now=False,
        auto_now_add=False,
    )
    substitute_end = models.DateField(
        "Date defining end of Substitution",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    subbed = models.ForeignKey(
        "Worker",
        verbose_name="Worker to be Substituted",
        related_name="le_subbed",
        on_delete=models.CASCADE,
    )
    subbing = models.ForeignKey(
        "Worker",
        verbose_name="Worker Substituting other",
        related_name="le_subbing",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reason = models.ForeignKey(
        "PermissionChangeReason",
        verbose_name="Reason for Substitution",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    old_perms = models.ManyToManyField(
        "Permission",
        verbose_name="Old Permissions",
        related_name="oldperms",
        blank=True,
    )
    new_perms = models.ManyToManyField(
        "Permission",
        verbose_name="New Permissions",
        related_name="newperms",
        blank=True,
    )

    def __str__(self):
        return "{} by {}: {} - {} because {}".format(
            self.subbed, self.subbing,  
            self.substitute_begin, self.substitute_end, self.reason,
        )

class PermissionChangeReason(models.Model):
    
    desc = models.TextField(
        "Reason of Substitution",
        unique=True,
    )

    def __str__(self):
        return self.desc
