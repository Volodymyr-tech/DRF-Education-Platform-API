import re

from rest_framework.serializers import ValidationError


class LinkValidator:

    def __init__(self, link_field):
        self.link_field = link_field

    def __call__(self, values):
        pattern = r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w\-]{11}"
        link = dict(values).get(self.link_field, None)
        print(values)
        print(type(link))
        if not re.match(pattern, link):
            raise ValidationError(
                f"{self.link_field} field is required and must be a valid YouTube link."
            )
