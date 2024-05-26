from celery import shared_task
from cloudinary import uploader

from images.models import Image


@shared_task()
def upload_image(image_id, image):
    asset = uploader.upload(image)
    Image.objects.filter(pk=image_id).update(url=asset['secure_url'])

