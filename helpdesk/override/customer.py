import frappe
from erpnext.selling.doctype.customer.customer import Customer

class CustomCustomer(Customer):
    # Hàm default_list_data phục vụ cho việc lấy dữ liệu những trường cần lấy trong doctype Customer khi làm form list view
    @staticmethod
    def default_list_data():
        columns = [
            {
                "label": "Name",
                "type": "Text",
                "key": "name",
                "width": "25rem",
            },
            {
                "label": "Email",
                "type": "Read Only",
                "key": "email_id",
                "width": "25rem",
            },
            {
                "label": "Phone",
                "type": "Read Only",
                "key": "mobile_no",
                "width": "25rem",
            },
            {
                "label": "Primary Contact Email",
                "type": "Read Only",
                "key": "email_id",
                "width": "25rem",
            },
        ]
        rows = [
            "name",
            "email_id",
            "mobile_no",
            "email_id",
        ]
        return {"columns": columns, "rows": rows}

