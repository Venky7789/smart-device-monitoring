from flask import Blueprint, jsonify
from db import db
from models import Company, Device, DeviceReading
from sqlalchemy import func
from datetime import datetime, timezone, timedelta

bp = Blueprint("companies", __name__, url_prefix="/api")

@bp.route("/companies", methods=["GET"])
def get_companies():
    companies = Company.query.order_by(Company.name).all()
    data = [{"id": c.id, "name": c.name} for c in companies]
    return jsonify({"companies": data}), 200

@bp.route("/companies/<int:company_id>/devices", methods=["GET"])
def get_devices_for_company(company_id):
    # Subquery: latest reading per device
    subq = db.session.query(
        DeviceReading.device_id,
        func.max(DeviceReading.timestamp).label("last_ts")
    ).group_by(DeviceReading.device_id).subquery()

    q = db.session.query(
        Device.id,
        Device.name,
        subq.c.last_ts
    ).outerjoin(subq, Device.id == subq.c.device_id).filter(Device.company_id == company_id)

    devices = []
    now = datetime.now(timezone.utc)

    for d_id, d_name, last_ts in q.all():
        status = "offline"
        last_iso = None
        if last_ts:
            last_dt = last_ts
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            delta = now - last_dt
            if delta <= timedelta(minutes=2):  # change to 1 minute if you want
                status = "online"
            last_iso = last_dt.isoformat()
        devices.append({
            "id": d_id,
            "name": d_name,
            "last_reading": last_iso,
            "status": status
        })
    return jsonify({"devices": devices}), 200
