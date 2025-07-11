from django.db import models


# username:user pass=1234
# Create your models here.
class Resume(models.Model):
    # resume = models.FieldFile(upload_to="resume")
    resume = models.FileField(upload_to="resume", blank=True, null=True)


class JobDescription(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()

    def __str__(self) -> str:
        return self.job_title
