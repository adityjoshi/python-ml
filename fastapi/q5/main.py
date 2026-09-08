from typing import Literal, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import uvicorn

import models
from database import Base, engine, get_db
from schemas import (
    BoutiqueCreate,
    BoutiqueOut,
    BoutiqueWithProducts,
    ProductCreate,
    ProductOut,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/boutiques", response_model=BoutiqueOut, status_code=201)
def create_boutique(
    boutique: BoutiqueCreate, db: Session = Depends(get_db)
) -> BoutiqueOut:
    new_boutique = models.Boutique(
        name=boutique.name,
        city=boutique.city,
    )
    db.add(new_boutique)
    db.commit()
    db.refresh(new_boutique)
    return new_boutique


@app.post(
    "/boutiques/{boutique_id}/products",
    response_model=ProductOut,
    status_code=201,
)
def add_product(
    boutique_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductOut:
    boutique = (
        db.query(models.Boutique)
        .filter(models.Boutique.id == boutique_id)
        .first()
    )
    if boutique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No boutique found with id {boutique_id}",
        )

    new_product = models.Product(
        name=product.name,
        category=product.category,
        price=product.price,
        highlighted=False,
        boutique_id=boutique_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get(
    "/boutiques/{boutique_id}",
    response_model=BoutiqueWithProducts,
    status_code=200,
)
def get_boutique(
    boutique_id: int,
    category: Optional[str] = None,
    sort: Optional[Literal["name", "price"]] = Query(None),
    db: Session = Depends(get_db),
) -> BoutiqueWithProducts:
    boutique = (
        db.query(models.Boutique)
        .filter(models.Boutique.id == boutique_id)
        .first()
    )
    if boutique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No boutique found with id {boutique_id}",
        )

    product_q = db.query(models.Product).filter(
        models.Product.boutique_id == boutique_id
    )
    if category is not None:
        product_q = product_q.filter(models.Product.category == category)
    if sort == "name":
        product_q = product_q.order_by(models.Product.name.asc())
    elif sort == "price":
        product_q = product_q.order_by(models.Product.price.asc())

    products = product_q.all()

    return BoutiqueWithProducts(
        id=boutique.id,
        name=boutique.name,
        city=boutique.city,
        products=products,
    )


@app.put(
    "/boutiques/{boutique_id}/products/{product_id}/highlight",
    response_model=ProductOut,
    status_code=200,
)
def highlight_product(
    boutique_id: int,
    product_id: int,
    db: Session = Depends(get_db),
) -> ProductOut:
    boutique = (
        db.query(models.Boutique)
        .filter(models.Boutique.id == boutique_id)
        .first()
    )
    if boutique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No boutique found with id {boutique_id}",
        )

    product = (
        db.query(models.Product)
        .filter(
            models.Product.id == product_id,
            models.Product.boutique_id == boutique_id,
        )
        .first()
    )
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"No product found with id {product_id} at boutique {boutique_id}",
        )

    all_products = (
        db.query(models.Product)
        .filter(models.Product.boutique_id == boutique_id)
        .all()
    )
    for item in all_products:
        item.highlighted = False

    product.highlighted = True

    db.commit()
    db.refresh(product)
    return product


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
