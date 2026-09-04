from fastapi import Depends, FastAPI, HTTPException, status, Query
import uvicorn

import models
from typing import List,Optional,Literal
from database import Base, engine, get_db

from sqlalchemy.orm import Session

from schemas import (
    LotCreate,
    LotOut,
    LotWithSlips,
    SlipCreate,
    SlipTransfer,
    SlipOut,
)


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post("/lots",response_model=LotOut,status_code=201)
def create_lot(lot: LotCreate, db:Session = Depends(get_db)) -> LotOut:
    new_lot = models.Lot(
        name = lot.name,
        zone = lot.zone,
    )

    db.add(new_lot)
    db.commit()
    db.refresh(new_lot)

    return new_lot

@app.post("/lots/{lot_id}/slips",response_model=SlipOut,status_code=201)
def add_slip(lot_id:int, slip:SlipCreate, db: Session = Depends(get_db)) -> SlipOut:
    lot = (
        db.query(models.Lot).filter(models.Lot.id == lot_id).first()
    )

    if lot is None:
        raise HTTPException(
            status_code=404,
            detail=f"there is no lot_id equals {lot_id}"
        )
    new_slip = models.Slip(
        ticket_code=slip.ticket_code,
        vehicle_class=slip.vehicle_class,
        parked_minutes=slip.parked_minutes,
        lot_id=lot_id
    )

    db.add(new_slip)
    db.commit()
    db.refresh(new_slip)

    return new_slip


@app.get("/lots/{lot_id}",response_model=LotWithSlips,status_code=200)
def get_lot(lot_id: int, vehicle_class:Optional[str]=None,sort:Optional[Literal["ticket_code","parked_minutes"]]=Query(None),db:Session = Depends(get_db)) -> LotWithSlips:
    lot = (
        db.query(models.Lot).filter(models.Lot.id == lot_id).first()
    )

    if lot is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid lot id is provided {lot_id}"
        )
    entry = (db.query(models.Slip).filter(models.Slip.lot_id == lot_id))
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"invalid lot id {lot_id}"
        )

    if vehicle_class is not None:
        entry = entry.filter(models.Slip.vehicle_class == vehicle_class)
    if sort == "ticket_code":
        entry = entry.order_by(models.Slip.ticket_code.asc())
    if sort == "parked_minutes":
        entry = entry.order_by(models.Slip.parked_minutes.asc())

    entry = entry.all()

    return LotWithSlips(
        id=lot_id,
        name=lot.name,
        zone=lot.zone,
        slips=entry
    )


@app.post("/lots/{lot_id}/slips/transfer",response_model=LotWithSlips,status_code=200)
def transfer_slips(lot_id:int, transfer:SlipTransfer, db: Session = Depends(get_db)) -> LotWithSlips:
    lot = (
        db.query(models.Lot).filter(models.Lot.id == lot_id).first()
    )

    if lot is None:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid lot id is provided {lot_id}"
        )

   
    target_lot = (db.query(models.Lot).filter(models.Lot.id == transfer.target_lot_id).first())

    if target_lot is None:
        raise HTTPException(
            status_code=404,
            detail=f"invalid lot id {lot_id}"
        )
    
    entry = (db.query(models.Slip).filter(models.Slip.lot_id == lot_id).all())
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"invalid lot id {lot_id}"
        )

    for i in entry:
        i.lot_id = transfer.target_lot_id

    db.commit()

    target_slip = db.query(models.Slip).filter(models.Slip.lot_id == transfer.target_lot_id).all()

    return LotWithSlips(
        id=target_lot.id,
        name=target_lot.name,
        zone=target_lot.zone,
        slips=target_slip,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

