import re
import unicodedata
from urllib.parse import urlparse

def remove_vietnamese_diacritics(text: str) -> str:
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return re.sub(r'\s+', '', text).lower()



# bỏ http/https và www, đưa về dạng domain/path?query
def strip_scheme_www(url: str) -> str:
    parsed = urlparse(url if url.startswith("http") else "http://" + url)
    domain = parsed.netloc.replace("www.", "")
    path   = parsed.path or ""
    query  = f"?{parsed.query}" if parsed.query else ""
    return (domain + path + query).rstrip("/").lower()

# Thêm scheme 
def normalize_url(url: str) -> str:
    return url if url.startswith(("http://", "https://")) else "http://" + url

# Lấy domain từ URL (không kèm scheme/path/query)
def extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        return parsed.netloc.lower()
    except:
        return ""

# Các từ khoá nghi ngờ phổ biến


RAW_KEYWORDS = [
    'login', 'secure', 'update', 'verify', 'account', 'bank', 'signin', 'submit',
    'paypal', 'ebay', 'confirm', 'wp', 'mail', 'admin', '88', '365', 'bet', '68', '86',
    'xoso', 'casino', 'bong88', 'banca', '1xbet', 'sex', 'jav', 'xxx', 'phim', 'phim18',
    'phimmoi', '18+', 'hdsex', 'livechat', 'gai goi', 'xo so', 'tructiepbongda',
    'lo de', 'da ga', 'keo bong', 'phim cap 3', 'phim sex', 'phim jav', 'phimlau',
    'vay tien', 'giai ngan', '789', 'vay', 'tien', 'co bac', 'sicbo', 'baccarat',
    'blackjack', 'sanh game', 'no hu', 'tai xiu', 'xoc dia', 'game bai', 'porn',
    'phimmoiz', 'phimhd', 'phimbo', 'vietsub', 'tra gop', 'lo to', 'rut tien',
    'hentai', 'lon', 'dit', 'xx', 'trung thuong', 'trung iphone', 'quay so',
    'qua tang', 'nhan thuong', 'khuyen mai', 'nude', 'free sex', "vay nhanh", "vay online", "vay tín chấp", "vay sinh viên", "hỗ trợ tài chính",
    "vay gấp", "vay không cần thế chấp", "vay nóng", "lãi suất thấp", "vay vốn", "clip nóng", "gái gọi", "gái xinh", "lộ hàng", "ảnh nude", "phim người lớn"
    , "dâm đãng", "dâm", "tặng quà", "quà miễn phí", "mã ưu đãi", "trúng xe", "nhận quà",
    "sự kiện hot", "quà tặng hấp dẫn"
]

# Loại bỏ trùng và chuẩn hóa chữ thường + loại khoảng trắng thừa
SUSPICIOUS_KEYWORDS = sorted(set(k.strip().lower() for k in RAW_KEYWORDS))


SUSPICIOUS_KEYWORDS = [remove_vietnamese_diacritics(w).replace(" ", "") for w in RAW_KEYWORDS]
