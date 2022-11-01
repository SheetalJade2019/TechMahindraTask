from django.shortcuts import render
from .forms import *
from .models import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from project.settings import BASE_DIR
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        # get input data from request & store it to media folder
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(f"{myfile.name}", myfile)
        uploaded_file_url = fs.url(filename)
        uploaded_file_url = f"{BASE_DIR}\media\{myfile}"
        print("uploaded_file_url ",uploaded_file_url)

        # read csv and create dataframe
        df = pd.read_excel(f"{BASE_DIR}\media\{myfile}", engine="openpyxl")
        print("\n 3 rows of input file \n",df.head(3))

        # database connection
        my_path=f"{BASE_DIR}\db.sqlite3" # update path
        my_conn = sqlite3.connect(my_path)
        print("Connected to database successfully")
        my_conn = create_engine("sqlite:///"+ my_path) # connection object

        try:
            column_ls = df.columns
            # create SQLite db table Input.
            df.to_sql(con=my_conn,name='Input',if_exists='append') 
            # print("Worked")
            # query to collect record
            query="SELECT * FROM Input"  
            df = pd.read_sql(query,my_conn,columns= column_ls) # create DataFrame
            df = df.sort_values(by=['Category'])
            # df = df.drop(['index'], axis=1)
            print("\n------  top 3 rows of dataframe  -------\n",df.head(3)) # Print top 5 rows as sample
            unique_val = df["Category"].unique()
            df = [x for _, x in df.groupby(df['Category'])]
            print("len(df) : ",len(df))
            df = pd.DataFrame(df)
            print(df.head(2))
            # df = df.T
            # print(df.head(2))
            # df_temp = pd.DataFrame(columns = column_ls)
            # global df1
            # for r in df.iterrows():
            #     for i in unique_val[:-1]:
            #         df1 = pd.DataFrame(columns = column_ls)
            # #     print(r[0] , r[1])
            #         print(r[0])
            #         if r[1].any() == unique_val[0]:
            #             df_temp = pd.DataFrame(r,columns = column_ls)
            #             df_temp.loc[len(df_temp.index)] = df_temp[column_ls].sum()
            #             global new_df
            #             new_df = pd.concat([df1, df_temp], axis=0)
            #             print("\n new df\n" ,new_df.head())
            #     # temp_df.to_excel("temp_df.xlsx", index=True)

            # save result to excel
            df.to_excel(f"{BASE_DIR}\media\output\{myfile}_result.xlsx", index=True)
        except SQLAlchemyError as e:
            print(e)
            error = str(e.__dict__['orig'])
            print(error)
        else: 
            pass

        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html',{'uploaded_file_url': None})