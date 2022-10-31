from django.shortcuts import render
from .forms import *
from .models import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from project.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt
import pandas as pd



# Create your views here.
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        
        filename = fs.save(f"{myfile.name}", myfile)
        uploaded_file_url = fs.url(filename)
        print("uploaded_file_url ",uploaded_file_url)
        df = pd.read_excel(f"{BASE_DIR}\media\{myfile}", engine="openpyxl")
        # print(df.head())

        column_names = list(df.columns)
        print("column_names : ",column_names)
        unique_val = df["Category"].unique()
        print("unique_val ",unique_val)
        new_df = pd.read_excel("D:\SHEETAL\LEARN\INTERVIEWS\TechMahindra\project\media\Input.xlsx", engine="openpyxl", index_col="Category")
        new_col = new_df.columns
        for cv in unique_val:
            print(cv)
            temp_df = new_df.loc[cv]
            df_temp = pd.DataFrame(temp_df,columns=new_col)
            df_temp.loc[len(df_temp.index)] = df_temp[new_col].sum()
            df_temp.to_excel ('export_dataframe.xlsx', index = False, header=True)
            print(df_temp)

        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html')