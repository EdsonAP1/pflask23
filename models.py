from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

db = SQLAlchemy()

class FormaPago(db.Model):
    __tablename__ = "formapago"

    idformapago = db.Column(db.Integer, primary_key=True)
    desformapago = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    # Relación con Egreso
    egresos = db.relationship(
        "Egreso", backref="forma_pago", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "idformapago": self.idformapago,
            "desformapago": self.desformapago,
            "estado": self.estado,
        }

class Egreso(db.Model):
    __tablename__ = "egreso"
    # __table_args__ = (db.Index('idx_gestion_mes', 'gestions', 'mes'),)
    idegreso = db.Column(db.Integer, primary_key=True)
    detalle = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.Date, nullable=False, server_default=func.current_date())
    fecha_add = db.Column(db.DateTime, default=datetime.now)
    fecha_upd = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    idformapago = db.Column(
        db.Integer, db.ForeignKey("formapago.idformapago"), nullable=False
    )

    def to_dict(self):
        return {
            "idegreso": self.idegreso,
            "detalle": self.detalle,
            "monto": float(self.monto),
            "fecha": self.fecha.isoformat(),
            "fecha_add": self.fecha_add.strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_upd": self.fecha_upd.strftime("%Y-%m-%d %H:%M:%S"),
            "idformapago": self.idformapago,
            "formapago": self.forma_pago.desformapago if self.forma_pago else None,
        }