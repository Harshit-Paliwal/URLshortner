from fastapi import FastAPI,Header,Depends,HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse,FileResponse
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from database import urls
from pymongo import MongoClient
from qrcode import qr_code

connection_string = "mongodb+srv://Harshitpaliwal:HkEa48DKKVF1Uu0S@infinix.kmedsqy.mongodb.net/"
mongo_db = MongoClient(connection_string)
database = mongo_db.UrlShortner
collection = database.urls

qr_obj = qr_code()
base_url = "https://hpurlshortner.onrender.com/"
url_obj = urls(collection)
class addURL(BaseModel):
  special_key : str
  url : str


app = FastAPI()

@app.get("/")
def hello():
  return "hello fast api world"   #http://127.0.0.1:8000

@app.get("/{specialKey}")#http://127.0.0.1:8000/hello
async def new(specialKey:str):
  url = url_obj.fetch_url(specialKey)
  return RedirectResponse(url,status_code=302)
  
    

# http://127.0.0.1:8000/speacial_key


@app.post("/addURL")
async def addurl(json:addURL):
  insert = url_obj.insert_url(json.special_key,json.url)
  if insert:
    return{"shortened URL": base_url+json.special_key}
  return{"Shortening the URL":insert}

@app.get("/count/{specialkey}")
async def count_clicks(specialkey:str):
    return url_obj.count(specialkey)

@app.get("/qrcode/{specialkey}")
async def make_qr(specialkey:str):
  qr_obj.make_qr(base_url+specialkey,specialkey)
  return  FileResponse(specialkey+".png")
