from django.db import models
from django.db.models import Min


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserModel(TimeStampedMixin):
    user_id = models.CharField(max_length=255, unique=True, verbose_name="ID пользователя")
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name="Username пользователя")
    chat_id = models.CharField(blank=True, null=True, verbose_name="Chat id пользователя")
    answer = models.CharField(blank=True, null=True, verbose_name="Переменная для хранения ответа пользователя")
    from_where = models.CharField(blank=True, null=True, verbose_name="Откуда пришел пользователь")
    last_viewed_job_id = models.IntegerField(default=0)


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.user_id}"


class CvModel(TimeStampedMixin):
    user_id = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    cv_name = models.TextField(verbose_name="Название резюме пользователя")
    cv_text = models.TextField(verbose_name="Текст резюме пользователя")

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return f"{self.cv_name}"


class ProjectModel(TimeStampedMixin):
    user_id = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    project_name = models.TextField(verbose_name="Название проекта пользователя")
    project_text = models.TextField(verbose_name="Текст проекта пользователя")

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return f"{self.project_name}"


class VacancyModel(TimeStampedMixin):
    project_name = models.ForeignKey('ProjectModel', on_delete=models.CASCADE)
    user_id = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    vacancy_name = models.TextField(verbose_name="Название вакансии проекта")
    vacancy_text = models.TextField(verbose_name="Текст вакансии проекта")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return f"{self.vacancy_name}"
