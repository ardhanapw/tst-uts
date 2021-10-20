import json
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import uvicorn


with open("menu.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()

@app.get('/')
def root():
    return {'Menu':'Item'}

#get all menu
@app.get('/menu')
async def read_all():
    return data

#get 1 menu from id
@app.get('/menu/{item_id}')
async def read(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

#add item (parameter id and name): add 1 item on the back of the list/array, id = +1 from last items id
@app.post('/menu')
async def add(name:str):
    id = 1
    if (len(data['menu'])>0):
        id = data['menu'][len(data['menu'])-1]['id']+1
    new_data = {'id':id,'name':name}
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data, write_file, indent = 4)
    write_file.close()
    return (new_data)

    raise HTTPException(
        status_code=500, detail=f'Internal Server Error'
    )

#update item (parameter id): search matching id -> rewrite the item name -> update list/array
@app.put('/menu/{item_id}')
async def update(item_id:int, name:str):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name'] = name
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent = 4)
            write_file.close()
            return {"message":"Data updated successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )   

#delete item (parameter id): search matching id with inputted int (id wants to be deleted) 
#                            -> delete whole item (id and name) -> update list
@app.delete('/menu/{item_id}')
async def delete(item_id:int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data['menu'].remove(menu_item)
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent = 4)
            write_file.close()
            return {"message":"Data deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )   

#delete all item from list/array
@app.delete('/menu')
async def delete_all():
    data['menu'].clear()
    return ("All data has been successfully deleted")

uvicorn.run(app, host = "127.0.0.1", port=8000)