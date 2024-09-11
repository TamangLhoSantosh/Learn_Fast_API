from fastapi import FastAPI
# from typing import Optional

app = FastAPI()

@app.get('/blog')
def index(limit=10, published:bool = True):
        #    sort = Optional[str] = None):
    # Only get 10 published blogs
    if published:
        return {'data':f'{limit} published blogs from the db'}
    else:
        return {'data':f'{limit} blogs from the db'}
    
@app.get('/blog/unpublished')
def unpublished():
    return {'data' : {'all unpublished blogs'}}

@app.get('/blog/{id}')
def show ( id:int):
    return {'data':id}

@app.get('/blog/{id}/comments')
def comments(id,limit = 10):
    # Fetch comments of blog with id = id
    return {'data':{'1','2'}}
