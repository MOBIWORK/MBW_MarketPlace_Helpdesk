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

    def before_save(self):
        if frappe.db.exists("User", {"email": self.email_id}):
            # Nếu email đã tồn tại, hiển thị thông báo và không tạo mới
            frappe.msgprint(f"Email {self.email_id} đã tồn tại trong User, không thể thêm mới User.")
        # Kiểm tra nếu trường email_id rỗng
        if not self.email_id:
            # Hiển thị thông báo cho người dùng về việc thiếu email
            frappe.throw("Không thể lưu khách hàng mới vì chưa có email. Vui lòng nhập địa chỉ email để tạo tài khoản đăng nhập cho khách hàng.")
            
    def after_insert(self) :
        # Mục địch của việc viết vào hàm after_insert là để  khi người dùng tạo mới một bản ghi trong doctype Customer khi lưu sẽ sinh ra một bản ghi mới trong doctype User 
        super(CustomCustomer, self).after_insert()
        new_user = frappe.get_doc({
            "doctype": "User",
            "email": self.email_id or " ",
            "enabled" : 0,
            "first_name": self.customer_name or "Unknown"  # Giả sử có trường first_name
        })
        new_user.insert()