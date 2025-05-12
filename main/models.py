from django.db import models

class CV(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    # Translations
    firstname_translated = models.CharField(max_length=100, blank=True)
    lastname_translated = models.CharField(max_length=100, blank=True)
    bio_translated = models.TextField(blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Contact(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="contacts")
    type = models.CharField(max_length=50, choices=[
        ("email", "Email"),
        ("phone", "Phone"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("website", "Website"),
    ])
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type}: {self.value}"


class Skill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=[
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ])

    # Translations
    name_translated = models.CharField(max_length=100, blank=True)
    level_translated = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.level})"


class Project(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True)

    # Translations
    title_translated = models.CharField(max_length=200, blank=True)
    description_translated = models.TextField(blank=True)

    def __str__(self):
        return self.title
