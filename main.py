# import packages
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel # parent class untuk buat schema di request body
import pandas as pd
from datetime import datetime # Untuk mendapatkan waktu terkini

# membuat objek FastAPI
app = FastAPI()

# variable password
password = "kopiluwakgabikinkenyang123"

# membuat endpoint -> ketentuan untuk endpoint adalah
# 1. harus diawali dengan /
# 2. harus ada fungsi yang mengembalikan response
# function (get, post, put, delete)

# ---------------------------------

# endppoint pertama/root untuk menampilkan pesan 'selamat datang'
@app.get("/")
def getWelcome(): # function untuk menghandle endpoint diatas
    return {
        "message": "Selamat datang di API FastAPI"
    }

# endpoitn untuk menampilakn data set

@app.get("/data")
def getData():
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    # mengembalikan response isi dataset
    # Kita menambahkan parameter orient="" untuk merubah format
    # output nya(dict,list,records = gunakan records untuk format JSON pada umumnya).
    return df.to_dict(orient="records")



# ---------------------------------

# routing/path parameter -> url dinamis -> menyesuaikan dengan data yang ada di server
# endpint untuk menampilkan data sesuai dengan lokasi
# data dari Rusia -> /data/russia
# data dari Rusia -> /data/zimbabwe

@app.get("/profile/{location}")
def getData(location: str):
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")

    #filter data berdasarkan parameter, lalu disimpan ke dataframe baru
    result = df[df.location == location]

    # validate apakah hasil ada
    if len(result) == 0:
        # menampilkan pesan error -> jika tidak ada datanya
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")

    # mengembalikan response isi dataset
    # Kita menambahkan parameter orient="" untuk merubah format
    # output nya(dict,list,records = gunakan records untuk format JSON pada umumnya).
    return result.to_dict(orient="records") # update dataframe yang digunakan


# ------------------------------------

# endpoint untuk menghapus data berdasrakan id
# {} <- path parameter
@app.delete("/data/{id}")
def deleteData(id: int, api_key: str = Header(None)):

    # proses verifikasi authentication
    if api_key == None or api_key != password:
        # kalau tidak ada kasih pesan error -> tidak ada akses.
        raise HTTPException(status_code=401, detail="You dont have access!")

    # kalau ada, lanjut ke proses delete
    # proses penambikan data
    df = pd.read_csv("dataset.csv")

    #cek apakah ada
    result = df[df.id == id]

    # validate apakah hasil ada
    if len(result) == 0:
        # menampilkan pesan error -> jika tidak ada datanya
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    
    # proses hapus data
    # condition
    result = df[df.id != id]

    #udpate csv/dataset nya
    result.to_csv("dataset.csv", index=False)

    # message after updating data
    return {
        "msg": "Data has been deleted!"
    }
    
# ------------------------------------

class Profile(BaseModel):
    
    id: int
    name: str
    age: int
    location: str

# endpoint untuk menambahkan data baru
# perlu ada request body -> kita perlu membuat schema/model

@app.post("/data/")
def createData(profile: Profile):

    df = pd.read_csv("dataset.csv")

    #proses menambah baris data
    newData = pd.DataFrame({
        "id": [profile.id],
        "name":[profile.name],
        "age":[profile.age],
        "location":[profile.location],
        "created_at":[datetime.now().date()],
    }) 

    #concat
    df = pd.concat([df, newData])

    # update csv
    df.to_csv("dataset.csv", index=False)

    return {
        "msg":"data has been created"
    }
  
# ------------------------------------

# Untuk matiin fast API ctrl + c
# Kalau mau jalanin fastapi dev judul file python nya main.py
# Kalau judulnya bukan main.py -> <nama file>.py dev