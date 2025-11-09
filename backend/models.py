from datetime import datetime
from db import db

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    devices = db.relationship("Device", backref="company", lazy=True)

class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    readings = db.relationship("DeviceReading", backref="device", lazy=True)

class DeviceReading(db.Model):
    __tablename__ = "device_readings"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
