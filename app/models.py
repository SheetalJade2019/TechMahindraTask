from django.db import models

# Create your models here.
class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    excel_file = models.FileField(upload_to='upload', blank=True)
    
    def save(self, *args, **kwargs):
        try :
            #                  binary mode ↓
            with open('excel_file.xlsx', 'rb') as myFile:
                name = 'new_test.xlsx'
                self.excel_file.save(name, File(myFile), save=False)
            super().save(*args, **kwargs)

        except Exception as e:
            print(e)
    
