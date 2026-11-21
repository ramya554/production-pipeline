from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict

# Initialize the microservice
app = FastAPI(
    title="Product Inventory Microservice",
    version="1.0.0",
    description="A standalone microservice managing product catalog items."
)

# Data validation schema
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Wireless Mouse")
    price: float = Field(..., gt=0, example=29.99)
    stock: int = Field(..., ge=0, example=50)

class Product(ProductCreate):
    id: int

# In-memory database (replace with PostgreSQL/MongoDB in production)
fake_db: Dict[int, Product] = {}
current_id = 1

# Health check endpoint (essential for Kubernetes/Docker/Load Balancers)
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "product-service"}

# Create a new product
@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    global current_id
    new_product = Product(id=current_id, **product.model_dump())
    fake_db[current_id] = new_product
    current_id += 1
    return new_product

# Retrieve all products
@app.get("/products", response_model=list[Product])
async def list_products():
    return list(fake_db.values())

# Retrieve a single product by ID
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    if product_id not in fake_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_db[product_id]
