from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    def __str__(self):
        return self.get_full_name() + " ".join(" | " + str(_) for _ in self.company_set.all())
        # return self.get_full_name()
