from django.db import models
from django.utils.text import slugify
# Create your models here.

class Module(models.Model):
    module_id=models.AutoField(primary_key=True)
    module_code=models.SlugField(max_length=100, unique=True, blank=True)
    module_name=models.CharField(max_length=200)
    parent_module =models.ManyToManyField('self',symmetrical=False, related_name="child_module", blank=True)

    def save(self, *args, **kwargs):
        if not self.module_code:
            self.module_code=slugify(self.module_name)
            super().save(*args,**kwargs)

    def __str__(self):
        return self.module_name
class CompanyModule(models.Model):
    cm_id=models.AutoField(primary_key=True)
    company = models.ForeignKey('authapp.CompanyProfile', on_delete=models.CASCADE)
    module= models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.company.company_id} - {self.module.module_code}"
    
