from django.db import models
from django.contrib.auth.models import User



def user_directory_path(instance, filename):
    # Файл буде завантажено в media/user/user_<id>/<filename>
    return f'users/user_id_{instance.user.id}/{filename}'         # дана функція буде створювати наступний шлях для кожного користувача при додаванні фото

def default_image_user():
    return f'users/default.png'         # Повертає фото default

class Profile(models.Model):            #  Окрема таблиця яка посилається на Django User + міститиме додаткову інформацію
    user = models.OneToOneField(User, on_delete=models.CASCADE , verbose_name='Користувач')     # Саме посилання на модель User
    # Використовуємо функцію замість рядка з дужками
    photo = models.ImageField(upload_to=user_directory_path, default=default_image_user, verbose_name="Фото користувача") # Для додавання фото використовуємо функцію вище


    def __str__(self):
        return f"Профайл користувача {self.user.username}"

    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural  = 'Профайли'