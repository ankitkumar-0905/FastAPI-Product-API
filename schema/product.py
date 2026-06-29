from pydantic import BaseModel,Field , AnyUrl,field_validator,model_validator,EmailStr ,computed_field
from typing import Annotated,Literal,Optional,List
from uuid import UUID
from datetime import datetime
#CREATE 
#this file will contain the schema for the product model
class Saller(BaseModel):
    saller_id: UUID
    
    saller_name: Annotated[
        str, Field(
            min_length=3,
            max_length=50,
            title="Saller_Name",
            description="Name of the saller"
        )
    ]
    email : EmailStr
    website : AnyUrl
    @field_validator("email",mode="after")
    @classmethod
    def validate_saller_email(cls,value:EmailStr):
        allowed_domain = [
            "mistore.in","hpworld.in","apple.in","dell.com"
            "samsung.in","sony.in","lg.in","asus.in","lenovo.in"]
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domain:
            raise ValueError(f"Saller email domain not allowed : {domain}")
        
        
        return value

#this class will contain the schema for the product model
class DimensionCM(BaseModel):
    length :Annotated[float,Field(
        gt=0,setattr =True,
        desription = "put the length in cm",
        example =2.5
    )]
    width:Annotated[float,Field(
        gt=0,setattr =True,
        desription = "put the width in cm ",
        example =6.5
        )]
    height:Annotated[float,Field(
        gt=0,setattr =True,
        desription = "put the heigth in cm ",
        example =44.6
        )]

#this class will contain the schema for the product model
class Product(BaseModel):
    id: UUID
    sku: Annotated[
        str, Field(
            description="Stock Keeping Unit",
            min_length=3,max_length=20,
            title="SKU",
            example="734-nhc-7348r7-334"
                )
                ]  
    name: Annotated[
        str, Field(
            min_length=3,
            max_length=50,
            title="Product Name",
            example="Wireless Mouse",
            description="Name of the product"
        )
    ]
    description: Annotated[
        str, Field(
            max_length=500,
            title="Product Description",
            example="A high-quality wireless mouse with ergonomic design.",
            description="Detailed description of the product"
        )
    ]
    category: Annotated[
        str, Field(
            min_length=3,
            max_length=30,
            title="Product Category",
            example="Electronics",
            description="Category to which the product belongs"
        )
    ]
    brand: Annotated[     
        str, Field(
            min_length=2,
            max_length=30,
            title="Brand Name",
            example="Logitech",
            description="Brand of the product"
        )
    ]
    price: Annotated[
        float, Field(
            gt=0,
            title="Product Price",
            example=29.99,
            description="Price of the product in IND currency"
        )
    ]
    currency: Literal["IND"] = "IND"
    discount: Optional[Annotated[
        float, Field(
            ge=0,
            le=100,
            title="Discount Percentage",
            example=10.0,
            description="Discount percentage on the product"
        )
    ]] = None
    stock: Annotated[
        int, Field(
            ge=0,
            title="Stock Quantity",
            example=100,
            description="Available stock quantity of the product"
        )
    ]
    is_active: bool = True
    rating: Optional[Annotated[
        float, Field(
            ge=0,
            le=5,
            title="Product Rating",
            example=4.5,
        )
    ]] = None

    tags: Optional[Annotated[
        List[str], Field(
            default = None,
            max_length=10,
            description="List of tags associated with the product",
        )
    ]] = None

    images_urls:Annotated[List[AnyUrl],Field(
            max_length =1 ,
            description="At list 1 ulr of product images"
    )]

    Dimension_cm : DimensionCM

    Seller : Saller

    created_at: datetime
    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku_format(cls,value:str):
        if "-" not in value:
            raise ValueError("SKU must have '-'")
        last = value.split("-")[-1]
        if not (len(last)==3 and last.isdigit()):
            raise ValueError("SKU must have 3-digit like -123")
        
        return value    
    
    @model_validator(mode = "after")
    @classmethod
    def validate_business_rules(cls,model:"Product"):
        if model.stock ==0 and model.is_active==True:
            raise ValueError("Product cannot be active if stock is zero")
        if model.discount  > 0 and model.rating == 0:
            raise ValueError("Product with discount cannot have zero rating")
        
        return model
    @computed_field
    @property
    def volume_cm3(self) -> float:
        d= self.Dimension_cm
        return round(d.length * d.width * d.height,2)


#UPDATE 
class SallerUpdate(BaseModel):
    
    saller_name: Optional[
        str]= Field(
            min_length=3,
            max_length=50,
            title="Saller_Name",
            description="Name of the saller"
        )
    
    email : Optional[EmailStr]
    website :Optional[AnyUrl]
    @field_validator("email",mode="after")
    @classmethod
    def validate_saller_email(cls,value:EmailStr):
        allowed_domain = [
            "mistore.in","hpworld.in","apple.in","dell.com"
            "samsung.in","sony.in","lg.in","asus.in","lenovo.in"]
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domain:
            raise ValueError(f"Saller email domain not allowed : {domain}")
        
        
        return value

class DimensionCMUpdate(BaseModel):
    length :Optional[float]= Field(
        gt=0,setattr =True,
        desription = "put the length in cm",
        example =2.5
    )
    width:Optional[float]= Field(
        gt=0,setattr =True,
        desription = "put the width in cm ",
        example =6.5
        )
    height:Optional[float]= Field(
        gt=0,setattr =True,
        desription = "put the heigth in cm ",
        example =44.6
        )

class ProductUpdate(BaseModel):  
    name: Optional[
        str]= Field(
            min_length=3,
            max_length=50,
            title="Product Name",
            example="Wireless Mouse",
            description="Name of the product"
        )
    
    description: Optional[
        str]= Field(
            max_length=500,
            title="Product Description",
            example="A high-quality wireless mouse with ergonomic design.",
            description="Detailed description of the product"
        )
    
    category: Optional[
        str]= Field(
            min_length=3,
            max_length=30,
            title="Product Category",
            example="Electronics",
            description="Category to which the product belongs"
        )

    brand: Optional[
        str]= Field(
            min_length=2,
            max_length=30,
            title="Brand Name",
            example="Logitech",
            description="Brand of the product"
        )
    
    price: Optional[
        float]= Field(
            gt=0,
            title="Product Price",
            example=29.99,
            description="Price of the product in IND currency"
        )
    
    currency:Optional[Literal["IND"]] = "IND"
    discount: Optional[Annotated[
        float, Field(
            ge=0,
            le=100,
            title="Discount Percentage",
            example=10.0,
            description="Discount percentage on the product"
        )
    ]] = None
    stock: Optional[
        int]= Field(
            ge=0,
            title="Stock Quantity",
            example=100,
            description="Available stock quantity of the product"
        )
    
    is_active: Optional[bool] 
    rating: Optional[Annotated[
        float, Field(
            ge=0,
            le=5,
            title="Product Rating",
            example=4.5,
        )
    ]] = None

    tags: Optional[Annotated[
        List[str], Field(
            default = None,
            max_length=10,
            description="List of tags associated with the product",
        )
    ]] = None

    images_urls:Optional[List[AnyUrl]]=Field(
            max_length =1 ,
            description="At list 1 ulr of product images"
    )

    Dimension_cm : Optional[DimensionCMUpdate]

    Seller : Optional[SallerUpdate]

    created_at:Optional[datetime]
        
    
    @model_validator(mode = "after")
    @classmethod
    def validate_business_rules(cls,model:"Product"):
        if model.stock ==0 and model.is_active==True:
            raise ValueError("Product cannot be active if stock is zero")
        if model.discount  > 0 and model.rating == 0:
            raise ValueError("Product with discount cannot have zero rating")
        
        return model
    @computed_field
    @property
    def volume_cm3(self) -> float:
        d= self.Dimension_cm
        return round(d.length * d.width * d.height,2)
