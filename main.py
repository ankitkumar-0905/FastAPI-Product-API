import uuid

from fastapi import FastAPI, HTTPException,Path
from service.products import change_product, get_all_products ,add_product,remove_product
from schema.product import Product ,ProductUpdate
from uuid import uuid4,UUID
from datetime import datetime

app = FastAPI()


# satctic
@app.get("/")
async def root():
    return {"message": "Hello World"}

'''
#Deinamic 

@app.get('/products/{id}')
def get_products(id:int):
    products =["brush",'laptop','mouse','moniter']
    return products[id]
    '''
#this endpoint will return all the products from the json file
@app.get("/products")
def get_products():
    return get_all_products()

#this endpoint will create a new product and add it to the json file
@app.post("/products",status_code=201)
def create_product(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] =str(uuid4())
    product_dict["created_at"] =datetime.utcnow().isoformat() + "Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))    

    return product.model_dump(mode="json")


#this endpoint will delete a product from the json file based on the product id
@app.delete("/products/{product_id}")
def delete_product(product_id:UUID = Path (..., description ="product UUID")):
    try:
        res=remove_product(str(product_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    


@app.put("/products/{product_id}")
def update_product(product_id:UUID = Path (..., description ="product UUID"), payload:ProductUpdate = None):
    try:
        updated_product = change_product(str(product_id),payload.model_dump(mode ="json",exclude_unset=True))
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
