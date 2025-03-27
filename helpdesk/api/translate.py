import os
import json
import csv
import frappe

@frappe.whitelist()
def export_labels(app_name, lang, output_file):
    """
    Quét tất cả label từ các Doctype trong thư mục crm/fcrm/doctype/ và xuất ra file CSV.

    Args:
        app_name (str): Tên ứng dụng (ví dụ: 'CRM')
        lang (str): Ngôn ngữ cần dịch (ví dụ: 'vi')
        output_file (str): Tên file CSV xuất ra (ví dụ: 'untranslated_crm.csv')
    """
    labels = set()  # Dùng set để tránh trùng lặp label

    # Xác định đường dẫn thư mục Doctype trong app
    app_path = frappe.get_app_path(app_name)  # Ví dụ: /home/frappe/frappe-bench/apps/crm
    doctype_path = os.path.join(app_path, "helpdesk", "doctype")  # Đường dẫn tới crm/fcrm/doctype/

    # Kiểm tra thư mục tồn tại không
    if not os.path.exists(doctype_path):
        print(f"❌ Không tìm thấy thư mục: {doctype_path}")
        return

    # Duyệt tất cả thư mục con trong crm/fcrm/doctype/
    for doctype in os.listdir(doctype_path):
        json_file = os.path.join(doctype_path, doctype, f"{doctype}.json")  # Đường dẫn file JSON

        if os.path.exists(json_file):  # Kiểm tra nếu file JSON tồn tại
            with open(json_file, "r", encoding="utf-8") as f:
                doctype_data = json.load(f)

                # Lấy label từ các field
                if "fields" in doctype_data:
                    for field in doctype_data["fields"]:
                        if "label" in field and field["label"]:
                            labels.add(field["label"])

                # Lấy trạng thái workflow (nếu có)
                if "states" in doctype_data:
                    for state in doctype_data["states"]:
                        if "state" in state and state["state"]:
                            labels.add(state["state"])

    # Ghi dữ liệu vào file CSV
    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source Text", "Translated Text", "Context", "Lang"])
        
        for label in sorted(labels):
            writer.writerow([label, "", "", lang])

    print(f"✅ Đã xuất file: {output_file}")

# Chạy hàm (có thể chạy bằng bench execute)
export_labels("helpdesk", "vi", "untranslated_helpdesk.csv")