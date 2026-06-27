from app.schemas.employee_schema import EmployeeSchema
from app.extensions import db
from app.models import Employee, Department

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

class EmployeeService:

    @staticmethod
    def create(data):

        if Employee.query.filter_by(
            employee_code=data["employee_code"]
        ).first():
            return {
                "message": "Employee code already exists."
            }, 409

        if Employee.query.filter_by(
            email=data["email"]
        ).first():
            return {
                "message": "Email already exists."
            }, 409

        department = Department.query.get(data["department_id"])

        if not department:
            return {
                "message": "Department not found."
            }, 404

        employee = Employee(**data)

        db.session.add(employee)
        db.session.commit()

        return {
            "message": "Employee created successfully."
        }, 201

    @staticmethod
    def get_all():

        employees = Employee.query.all()

        return [
            employee.to_dict() for employee in employees
        ], 200

    @staticmethod
    def get_by_id(employee_id):

        employee = Employee.query.get(employee_id)

        if not employee:
            return {
                "message": "Employee not found."
            }, 404

        return employee.to_dict(), 200
    
    @staticmethod
    def get_all():

        employees = Employee.query.all()

        return employees_schema.dump(employees), 200

    @staticmethod
    def get_by_id(employee_id):

        employee = Employee.query.get(employee_id)

        if not employee:
            return {
                "message": "Employee not found."
            }, 404

        return employee_schema.dump(employee), 200