from fastapi import FastAPI
app=FastAPI()

@app.get('/')        #slash means base url localhost 8000
def index():
    return {"data":{"name":"aryan"}}

@app.get('/about')
def about():
    return {"data " :{"aryan":"27"}}
