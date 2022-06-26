from django.db import models

class Video(models.Model):
    id = models.CharField("Id", primary_key=True, max_length=10)
    title = models.CharField("Video Title", max_length=255)
    description = models.TextField("Description")
    published_on = models.DateTimeField("publishing datetime")
    thumbnail_url = models.URLField("Thumbnail URL", max_length=255)
    video_link = models.URLField("Video Link", max_length=255)

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"
        ordering = ["-published_on"]    # newest first

    def __str__(self):
        return self.title