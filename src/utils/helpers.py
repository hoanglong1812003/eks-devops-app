import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def normalize_query(question: str) -> str:
    q = question.lower()

    NAME_MAP = {
        "anh hưng": "Nguyễn Gia Hưng",
        "sư phụ hưng": "Nguyễn Gia Hưng",
        "anh thiện": "Lữ Hoàn Thiện",
        "anh vĩ": "Trần Đại Vĩ",
        "anh long": "Huỳnh Hoàng Long",
        "anh quy": "Phạm Hoàng Quy",
        "anh việt": "Bùi Hoàng Việt",
        "chị thư": "Đặng Thị Minh Thư",
        "anh huy": "Lý Kiên Huy",
        "anh đạt": "Nguyễn Đỗ Thành Đạt",
    }

    for k, v in NAME_MAP.items():
        if k in q:
            q = q.replace(k, v)

    ENTITY_MAP = {
        "fcaj": "FCAJ",
        "fcj": "FCAJ",
        "first cloud journey": "FCAJ",
        "first cloud ai journey": "FCAJ",
    }
    for k, v in ENTITY_MAP.items():
        if k in q:
            q = q.replace(k, v)

    return q
