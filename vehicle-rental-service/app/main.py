import logging
from itertools import count
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("vehicle-rental")

app = FastAPI(
    title="Vehicle Rental System API",
    description="REST API for vehicles, customers and rental bookings with Prometheus observability.",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app)

vehicles: Dict[int, dict] = {}
customers: Dict[int, dict] = {}
bookings: Dict[int, dict] = {}
vehicle_ids = count(1)
customer_ids = count(1)
booking_ids = count(1)


class Vehicle(BaseModel):
    registration_no: str = Field(min_length=2)
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    vehicle_type: str = Field(min_length=1)
    daily_rate: float = Field(gt=0)
    available: bool = True


class Customer(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(min_length=5)
    phone: str = Field(min_length=5)


class Booking(BaseModel):
    vehicle_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    start_date: str = Field(min_length=1)
    end_date: str = Field(min_length=1)
    total_amount: float = Field(gt=0)
    status: str = "confirmed"


@app.get("/", tags=["System"])
def root():
    return {"message": "Vehicle Rental API is running", "version": "v1.0.0"}


@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy"}


@app.get("/vehicles", tags=["Vehicles"])
def get_vehicles() -> List[dict]:
    return list(vehicles.values())


@app.post("/vehicles", tags=["Vehicles"], status_code=201)
def create_vehicle(vehicle: Vehicle):
    vehicle_id = next(vehicle_ids)
    data = {"id": vehicle_id, **vehicle.model_dump()}
    vehicles[vehicle_id] = data
    logger.info("Vehicle created id=%s registration=%s", vehicle_id, vehicle.registration_no)
    return data


@app.get("/vehicles/{vehicle_id}", tags=["Vehicles"])
def get_vehicle(vehicle_id: int):
    if vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicles[vehicle_id]


@app.put("/vehicles/{vehicle_id}", tags=["Vehicles"])
def update_vehicle(vehicle_id: int, vehicle: Vehicle):
    if vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    vehicles[vehicle_id] = {"id": vehicle_id, **vehicle.model_dump()}
    logger.info("Vehicle updated id=%s", vehicle_id)
    return vehicles[vehicle_id]


@app.delete("/vehicles/{vehicle_id}", tags=["Vehicles"])
def delete_vehicle(vehicle_id: int):
    if vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    del vehicles[vehicle_id]
    logger.info("Vehicle deleted id=%s", vehicle_id)
    return {"message": "Vehicle deleted", "id": vehicle_id}


@app.get("/customers", tags=["Customers"])
def get_customers() -> List[dict]:
    return list(customers.values())


@app.post("/customers", tags=["Customers"], status_code=201)
def create_customer(customer: Customer):
    customer_id = next(customer_ids)
    data = {"id": customer_id, **customer.model_dump()}
    customers[customer_id] = data
    logger.info("Customer created id=%s", customer_id)
    return data


@app.get("/customers/{customer_id}", tags=["Customers"])
def get_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customers[customer_id]


@app.put("/customers/{customer_id}", tags=["Customers"])
def update_customer(customer_id: int, customer: Customer):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    customers[customer_id] = {"id": customer_id, **customer.model_dump()}
    logger.info("Customer updated id=%s", customer_id)
    return customers[customer_id]


@app.delete("/customers/{customer_id}", tags=["Customers"])
def delete_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    del customers[customer_id]
    logger.info("Customer deleted id=%s", customer_id)
    return {"message": "Customer deleted", "id": customer_id}


@app.get("/bookings", tags=["Bookings"])
def get_bookings() -> List[dict]:
    return list(bookings.values())


@app.post("/bookings", tags=["Bookings"], status_code=201)
def create_booking(booking: Booking):
    if booking.vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if booking.customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")
    booking_id = next(booking_ids)
    data = {"id": booking_id, **booking.model_dump()}
    bookings[booking_id] = data
    vehicles[booking.vehicle_id]["available"] = False
    logger.info("Booking created id=%s vehicle=%s customer=%s", booking_id, booking.vehicle_id, booking.customer_id)
    return data


@app.get("/bookings/{booking_id}", tags=["Bookings"])
def get_booking(booking_id: int):
    if booking_id not in bookings:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bookings[booking_id]


@app.put("/bookings/{booking_id}", tags=["Bookings"])
def update_booking(booking_id: int, booking: Booking):
    if booking_id not in bookings:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.vehicle_id not in vehicles or booking.customer_id not in customers:
        raise HTTPException(status_code=404, detail="Vehicle or customer not found")
    bookings[booking_id] = {"id": booking_id, **booking.model_dump()}
    logger.info("Booking updated id=%s", booking_id)
    return bookings[booking_id]


@app.delete("/bookings/{booking_id}", tags=["Bookings"])
def delete_booking(booking_id: int):
    if booking_id not in bookings:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking = bookings.pop(booking_id)
    if booking["vehicle_id"] in vehicles:
        vehicles[booking["vehicle_id"]]["available"] = True
    logger.info("Booking deleted id=%s", booking_id)
    return {"message": "Booking deleted", "id": booking_id}
