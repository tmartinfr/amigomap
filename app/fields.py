import re

from django.core.validators import RegexValidator
from django.db import models
from typing import Any


class ColorValidator(RegexValidator):
    """
    Validate color hex code.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        return super(ColorValidator, self).__init__(
            regex=re.compile("^[0-9a-f]{6}$"), message="Invalid color code"
        )


class ColorField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        return super(ColorField, self).__init__(
            max_length=6, default="000000", validators=[ColorValidator()]
        )
