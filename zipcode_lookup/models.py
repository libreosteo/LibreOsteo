from django.db import models
from django.core.validators import RegexValidator

validate_french_zipcode = RegexValidator(
    regex='\d{5}',
    message='Does not look like a french zipcode',
)

class ZipcodeMapping(models.Model):
    zipcode = models.CharField(
        max_length=5,
        validators=[validate_french_zipcode],
        db_index=True,
    )
    city = models.CharField(max_length=60, db_index=True)
