import frappe
from frappe import _

@frappe.whitelist()
def get_information_contact(name):
    infor_user = frappe.get_value("Customer", name, ["image", "customer_name","email_id","mobile_no", "customer_details","website","customer_primary_address"])
    
    if infor_user :
        address_user = frappe.get_value("Address", infor_user[6], ["address_line1"])
    return {
        "image": infor_user[0] if infor_user[0] else infor_user[1][0],
        "name": infor_user[1],
        "email" : infor_user[2],
        "phone" : infor_user[3],
        "website":infor_user[5],
        "address": address_user[0],
        "description": infor_user[4],
        "primary_contact" : infor_user[2],
    }

@frappe.whitelist()
def get_data_number_of_ticket_by_channel(name):
    infor_user = frappe.get_value("Customer", name, ["email_id"])
    result = frappe.db.sql("""
        SELECT 
            COUNT(*) as total_tickets,
            SUM(CASE WHEN via_customer_portal = 1 THEN 1 ELSE 0 END) as total_portal,
            SUM(CASE WHEN via_customer_portal = 0 THEN 1 ELSE 0 END) as total_email
        FROM `tabHD Ticket`
        WHERE owner = %s
    """,infor_user, as_dict=True)
    # Lấy giá trị từ kết quả
    data = result[0]
    total_tickets = data['total_tickets'] or 0
    total_portal = data['total_portal'] or 0
    total_email = data['total_email'] or 0

    if total_tickets == 0:
        percent_total_portal  = 0
        percent_total_email = 0
    else:
        percent_total_portal = (total_portal / total_tickets) * 100
        percent_total_email = (total_email / total_tickets) * 100

    res = [
        {
        "total_tickets": total_tickets or 0,
        },
        [
            { "value": total_portal , "name": "Portal","percent" : percent_total_portal},
            { "value": total_email, "name": "Email","percent" : percent_total_email }
        ],
        [
            { "value": total_portal , "name": "Portal" },
            { "value": total_email, "name": "Email" }
        ]
    ]
    return res

@frappe.whitelist()
def get_data_number_of_ticket_by_status(name):
    infor_user = frappe.get_value("Customer", name, ["email_id"])
    result = frappe.db.sql("""
        SELECT 
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as total_open,
            SUM(CASE WHEN status = 'Replied' THEN 1 ELSE 0 END) as total_replied,
            SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as total_resolved,
            SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) as total_closed
        FROM `tabHD Ticket`
        WHERE owner = %s
    """,infor_user, as_dict=True)
    data = result[0] if result[0] else []
    return [
        { "value": data.get("total_open"), "name": "Open" },
        { "value": data.get("total_replied"), "name": "Replied" },
        { "value": data.get("total_resolved"), "name": "Resolved" },
        { "value": data.get("total_closed"), "name": "Closed" },
    ]

@frappe.whitelist()
def get_data_pending_tickets(name):
    infor_user = frappe.get_value("Customer", name, ["email_id"])
    result = frappe.db.sql("""
        SELECT 
            name AS id,
            name AS name,
            subject AS title,
            DATE_FORMAT(creation, '%%M %%e, %%Y') AS created,
            priority AS priority,
            _assign AS assign
        FROM `tabHD Ticket`
        WHERE 1 = 1 
            AND status = 'Open'
            AND agreement_status = 'First Response Due' 
            AND owner = %s
    """,infor_user, as_dict=True)

    data = result if result else []
    return data

@frappe.whitelist()
def get_data_all_tickets(name):
    infor_user = frappe.get_value("Customer", name, ["email_id"])
    result = frappe.db.sql("""
        SELECT 
            name AS id,
            name AS name,
            subject AS title,
            DATE_FORMAT(creation, '%%M %%e, %%Y') AS created,
            status AS status,
            priority AS priority,
            _assign AS assign
        FROM `tabHD Ticket`
        WHERE owner = %s
    """,infor_user, as_dict=True)

    data = result if result else []
    return data

@frappe.whitelist()
def get_data_tickets_time(name):
    # Lấy email_id của khách hàng
    email_id = frappe.get_value("Customer", name, "email_id")
    
    # Truy vấn tất cả dữ liệu cần thiết trong một lần
    tickets = frappe.db.sql("""
        SELECT 
            DATE(creation) AS created,
            name AS id,
            name AS name,
            %s AS creator,
            subject AS title,
            status AS status
        FROM `tabHD Ticket`
        WHERE owner = %s
    """, (name, email_id), as_dict=True)
    
    # Tạo cấu trúc dữ liệu kết quả
    result = []
    tickets_by_date = {}
    
    # Sắp xếp dữ liệu theo ngày
    for ticket in tickets:
        created_date = ticket.get('created')
        if created_date not in tickets_by_date:
            tickets_by_date[created_date] = []
        tickets_by_date[created_date].append({
            "id": ticket.get('id'),
            "name": ticket.get('name'),
            "creator": ticket.get('creator'),
            "title": ticket.get('title'),
            "status": ticket.get('status'),
        })
    
    # Tạo cấu trúc kết quả
    for date, items in tickets_by_date.items():
        result.append({
            "group": date,
            "collapsed": 'true',
            "rows": items,
        })
    
    return result

@frappe.whitelist()
def get_data_average_ratings(name):
    infor_user = frappe.get_value("Customer", name, ["email_id"])
    get_average_rating = frappe.db.sql("""
        SELECT 
            COUNT(*) as total_tickets,
            SUM(
                CASE 
                    WHEN feedback_rating = 0.2 THEN '1'
                    WHEN feedback_rating = 0.4 THEN '2'
                    WHEN feedback_rating = 0.6 THEN '3'
                    WHEN feedback_rating = 0.8 THEN '4'
                    WHEN feedback_rating = 1.0 THEN '5'
                    ELSE 0 
                END) AS rating_value
        FROM `tabHD Ticket`
        WHERE 
            owner = %s 
            AND feedback_rating > 0
    """,infor_user, as_dict=True)
    data = get_average_rating[0]
    if len(get_average_rating) > 0 :
        return {
            "total_tickets" : data.get("total_tickets"),
            "average_rating" : round((int(data.get("rating_value")) / int(data.get("total_tickets"))),1) if data.get("total_tickets") > 0 else 0
        }
    else :
        return []  

@frappe.whitelist()
def get_data_all_ratings(name):
    infor_user = frappe.get_value("Customer", name, ["email_id"])
    get_average_rating = frappe.db.sql("""
        SELECT 
            feedback_rating as point_rating,
            COUNT(feedback_rating) as total_tickets
        FROM `tabHD Ticket`
        WHERE
            owner = %s  
            AND feedback_rating > 0
        GROUP BY feedback_rating
        ORDER BY feedback_rating DESC
    """,infor_user, as_dict=True)
    if len(get_average_rating) > 0 :
        return get_average_rating
    else :
        return []  

@frappe.whitelist()
def get_data_detail_list_ticket(name):
    infor_user = frappe.get_value("Customer", name, ["email_id"])
    result = frappe.db.sql("""
        SELECT 
            name AS id,
            feedback_rating AS feedback_rating,
            DATE_FORMAT(creation, '%%M %%d, %%Y %%h:%%i %%p') AS created,
            feedback AS feedback,
            feedback_extra AS feedback_extra,
            _assign AS assign
        FROM `tabHD Ticket`
        WHERE  owner = %s
               AND feedback_rating > 0
    """,infor_user, as_dict=True)

    data = result if result else []
    return data

@frappe.whitelist()
def get_data_list_knowledge_base():
    result = frappe.db.sql("""
        SELECT 
            hdac.parent_category AS category_level_one,
            hda.category AS category_level_two,
            hda.name AS category_level_three,
            CONCAT(hdac.category_name, ' / ', hda.title) AS category_beadcrum
        FROM `tabHD Article` as hda
        LEFT JOIN `tabHD Article Category` as hdac on hda.category = hdac.name
        WHERE 1 = 1 AND hda.status = 'Published'  AND hdac.status = 'Published'
    """,as_dict=True)
    return result


@frappe.whitelist()
# Hàm kiểm tra tài khoản đăng nhập xem có quyền là agent không
def get_check_role_agent_user_login():
    user = frappe.get_doc("User", frappe.session.user)
    is_agent = any(role.role == "Agent" for role in user.roles)
    return {"is_agent": is_agent}