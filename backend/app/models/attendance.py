from datetime import datetime

from app.extensions import db


class Attendance(db.Model):
    __table_args__ = (
        db.UniqueConstraint(
            "employee_id",
            "attendance_date",
            name="unique_employee_attendance"
        ),
    )
    
    __tablename__ = "attendances"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    attendance_date = db.Column(
        db.Date,
        nullable=False
    )

    check_in = db.Column(
        db.DateTime,
        nullable=True
    )

    check_out = db.Column(
        db.DateTime,
        nullable=True
    )

    working_hours = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Absent"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    employee = db.relationship(
        "Employee",
        backref="attendances",
        lazy=True
    )

    def __repr__(self):
        return f"<Attendance {self.employee_id} - {self.attendance_date}>"