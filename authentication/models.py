from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import sys
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        # """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if 'createsuperuser' in sys.argv:
            first_name = input('Enter first name: ')
            extra_fields.setdefault('first_name', first_name)

            last_name = input('Enter last name: ')
            extra_fields.setdefault('last_name', last_name)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=40,
        help_text="Required. 40 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True)

    def file_size_validator(photo):
        """
        Function that checks whether file size not exceed the limit
        :param image: django.db.models.ImageField, user's image
        :return: None, ValidationError if image size exceeds the limit
        """
        file_size = photo.file.size
        megabyte_limit = 2.5
        if file_size > megabyte_limit * 1024 * 1024:
            raise ValidationError(f"File size should be {megabyte_limit} Mb")

    photo = models.ImageField(upload_to='avatars', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        file_size_validator])
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Magic method is redefined to show all information about User.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user password, user updated_at, user created_at,
                 user role, user is_active
        """
        return f"'id': {self.id}, 'email': '{self.email}'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of User object.
        :return: class, id
        """
        return f"{User.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        custom_user = User.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        custom_user = User.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        user_to_delete = User.objects.filter(id=user_id).first()
        if user_to_delete:
            User.objects.filter(id=user_id).delete()
            return True
        return False

    @staticmethod
    def create(email, password1, password2, username):
        """
        :param username: username of a user
        :type username: str
        :param email: email of a user
        :type email: str
        :param password1: password of a user
        :type password1: str
        :param password2: confirm password of a user
        :type password2: str
        :return: a new user object which is also written into the DB
        """
        if len(username) <= 40 and \
                len(email) <= 100 and \
                password1 == password2 and \
                len(email.split('@')) == 2 and \
                len(User.objects.filter(email=email)) == 0:
            custom_user = User(email=email, username=username, password=password1)
            custom_user.save()
            return custom_user
        return None

    def update(self,
               password=None,
               username=None,
               bio=None):
        """
        Updates user profile in the database with the specified parameters.\n
        :param password: password of a user
        :type password: str
        :param username: username of a user
        :type username: str
        :param bio: username of a user
        :type bio: str
        :return: None
        """
        user_to_update = User.objects.filter(email=self.email).first()

        if password is not None:
            user_to_update.set_password(password)
        if username is not None:
            user_to_update.username = username
        if bio is not None:
            user_to_update.bio = bio
        user_to_update.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        return User.objects.all()
