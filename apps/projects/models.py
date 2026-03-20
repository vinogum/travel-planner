from django.db import models


class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def check_completion(self):
        has_places = self.places.exists()
        all_visited = not self.places.filter(is_visited=False).exists()

        if has_places and all_visited:
            if not self.is_completed:
                self.is_completed = True
                self.save(update_fields=["is_completed"])
        else:
            if self.is_completed:
                self.is_completed = False
                self.save(update_fields=["is_completed"])

    def __str__(self):
        return self.name


class Place(models.Model):
    external_id = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)
    project = models.ForeignKey(
        TravelProject, on_delete=models.CASCADE, related_name="places"
    )

    class Meta:
        unique_together = ("external_id", "project")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.check_completion()

    def delete(self, *args, **kwargs):
        project = self.project
        super().delete(*args, **kwargs)
        project.check_completion()

    def __str__(self):
        return self.external_id
