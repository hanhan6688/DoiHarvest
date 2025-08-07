# Sci-Hub域名池（自动轮询避免封禁）
SCI_HUB_DOMAINS = [
    "https://sci-hub.hkvisa.net/",  
    "https://sci-hub.ru/",
    "https://sci-hub.st/",
    "https://sci-hub.se/",
    "https://sci-hub.ren/",
    "https://sci-hub.tw/",
    "https://sci-hub.ee/",
    "https://sci-hub.shop/",
    "https://sci-hub.ru/",
    "https://sci-hub.la/"
]

# 下载参数
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
MAX_THREADS = 15          # 并发数
RETRY_COUNT = 5           # 重试次数
TIMEOUT = 30              # 超时时间
MIN_DELAY = 2             # 最小延迟
MAX_DELAY = 8             # 最大延迟