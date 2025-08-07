import requests
from bs4 import BeautifulSoup
import os
import threading
import pandas as pd
import re,os
import random
import time
from queue import Queue
from config import *
from tqdm import tqdm
import glob
from urllib.parse import quote

# 清理非法文件名字符
def clean_filename(title):
    illegal_chars = r'[\\/:*?"<>|]'
    return re.sub(illegal_chars, '', title)[:120]  # 限制文件名长度

# 文献下载核心函数
def download_worker(queue, success_log, error_log, failed_dois):
    while not queue.empty():
        doi, title = queue.get()
        try:
            doi_link = f'https://doi.org/{doi}' if doi else 'No DOI'
            # 修改：无论下载是否成功，只要有DOI就记录到success_log中
            if doi:  # 只有当DOI存在时才记录
                success_log.append((title, doi_link))  # 存储标题和DOI链接
            file_name = f"{clean_filename(title)}.pdf"
            file_path = os.path.join("output", file_name)
            
            # 跳过已下载文件
            if os.path.exists(file_path):
                success_log.append(f"[SKIPPED] {doi} | {file_name}\n")
                queue.task_done()
                continue
            # 随机延迟防封禁
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            
            for retry in range(RETRY_COUNT):  # 默认重试5次
                domain = random.choice(SCI_HUB_DOMAINS)  # 随机选择一个域名
                try:
                    if not doi:
                        # 使用正确的搜索路径
                        search_url = f"{domain}?s={quote(title)}"
                        resp = requests.get(search_url, headers=HEADERS, timeout=TIMEOUT)
                    else:
                        resp = requests.get(f"{domain}{doi}", headers=HEADERS, timeout=TIMEOUT)
                    # 尝试从当前域名下载
                    soup = BeautifulSoup(resp.content, 'html.parser')
                    iframe = soup.find('iframe') or soup.find('embed')
                    pdf_url = iframe['src'] if iframe else None
                    
                    if not pdf_url or not pdf_url.startswith('http'):
                        continue
                    
                    # 下载PDF内容
                    pdf_resp = requests.get(pdf_url, headers=HEADERS, stream=True, timeout=TIMEOUT)
                    with open(file_path, 'wb') as f:
                        for chunk in pdf_resp.iter_content(chunk_size=1024):
                            if chunk: f.write(chunk)
                    
                    success_log.append(f"[SUCCESS] {doi} | {file_name}\n")
                    break  # 下载成功则跳出重试循环
                    
                except Exception as e:
                    # 如果当前域名失败，会继续下一次循环尝试其他域名
                    error_msg = f"{doi} | 错误: {str(e)[:50]} | 域名: {domain}"
                    if retry == RETRY_COUNT - 1:  # 最后一次重试也失败
                        failed_dois.append((doi, title))
                        error_log.append(f"[FAILED] {error_msg}\n")
        except Exception as e:
            error_msg = f"下载失败: {doi} | 错误: {str(e)} | 域名: {domain}"
            error_log.append(f"[ERROR] {error_msg}\n")
            print(f"尝试下载：{title} | 使用域名：{domain}")  # 实时显示下载尝试
            print(error_msg)  # 实时显示错误信息
            
            if retry == RETRY_COUNT - 1:
                failed_dois.append((doi, title))
        queue.task_done()
def validate_doi(doi):
    """验证DOI格式是否正确"""
    doi = doi.strip()
    if not doi:
        return False
    # 移除可能的DOI前缀
    doi = doi.replace("doi:", "").replace("DOI:", "").strip()
    # 检查基本格式
    # 当前验证正则表达式
    return re.match(r'^10\.\d+\/.+$', doi) is not None  # 允许路径中的特殊字符
# 主控流程
def main():
    os.makedirs("output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Initialize these at the beginning
    success_log = []
    error_log = []
    failed_dois = []
    
    excel_files = glob.glob("data/*.xls") + glob.glob("data/*.xlsx")
    doi_queue = Queue()
    skipped_count = 0
    
    # 第一次遍历：读取Excel文件并将文献添加到下载队列
    for excel_file in excel_files:
        print(f"正在读取文件: {excel_file}")
        try:
            df = pd.read_excel(excel_file)
            # 确保有DOI Link列
            if 'DOI Link' not in df.columns:
                df.insert(2, 'DOI Link', '')
            
            for _, row in df.iterrows():
                doi = row.get('DOI', '')
                title = row.get('Article Title', f"Unknown_{int(time.time())}")
                
                # 检查DOI是否有效
                if pd.isna(doi) or not str(doi).strip():
                    # DOI为空时，检查标题是否有效
                    if pd.isna(title) or not str(title).strip():
                        print(f"跳过无效记录: DOI和标题都为空")
                        skipped_count += 1
                        continue
                    else:
                        # 标题有效，DOI为空，仍然加入队列
                        print(f"添加无DOI记录: {title}")
                        doi_queue.put(("", title))  # DOI传空字符串
                        continue
                
                # 确保DOI是字符串类型
                doi = str(doi).strip()
                
                # 可选：使用validate_doi函数验证DOI格式
                if not validate_doi(doi):
                    print(f"跳过格式无效的DOI: {doi} | {title}")
                    skipped_count += 1
                    continue
                
                doi_queue.put((doi, title))
        except Exception as e:
            print(f"读取文件 {excel_file} 失败: {str(e)}")
            continue
    
    print(f"有效DOI数量: {doi_queue.qsize()} | 跳过记录数: {skipped_count}")
    
    # 启动线程池
    threads = []
    # 修改队列检查逻辑，确保在队列中有任务时才启动线程
    if doi_queue.qsize() > 0:
        for _ in range(min(MAX_THREADS, doi_queue.qsize())):
            t = threading.Thread(target=download_worker, 
                                args=(doi_queue, success_log, error_log, failed_dois))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # 进度监控
        print(f"▶️ 开始下载 {doi_queue.qsize()} 篇文献 | 线程数: {MAX_THREADS}")
        while any(t.is_alive() for t in threads):
            print(f"⏳ 剩余任务: {doi_queue.qsize()} | 成功: {len(success_log)} | 失败: {len(failed_dois)}")
            time.sleep(10)
    else:
        print("没有找到需要处理的文献记录，程序退出")
        return
    
    # 保存日志
    with open(f"logs/success_{int(time.time())}.log", 'w', encoding='utf-8') as f1, \
         open(f"logs/error_{int(time.time())}.log", 'w', encoding='utf-8') as f2, \
         open("logs/failed_dois.csv", 'w', encoding='utf-8', errors='ignore') as f3:
        
        # 修复TypeError: 将success_log中的元组转换为字符串
        success_log_strings = []
        for item in success_log:
            if isinstance(item, tuple):
                # 如果是元组，格式化为字符串
                title, doi_link = item
                success_log_strings.append(f"{title} | {doi_link}\n")
            else:
                # 如果已经是字符串，直接添加
                success_log_strings.append(item)
        
        f1.writelines(success_log_strings)
        f2.writelines(error_log)
        f3.write("DOI,Title\n")
        for doi, title in failed_dois:
            f3.write(f"{doi},{title}\n")
    
    # 第二次遍历：更新Excel文件中的DOI链接
    for excel_file in excel_files:
        try:
            df = pd.read_excel(excel_file)
            # 确保有DOI Link列
            if 'DOI Link' not in df.columns:
                df.insert(2, 'DOI Link', '')
            
            # 更新文献的DOI链接（包括成功和失败的）
            for item in success_log:
                if isinstance(item, tuple):
                    title, doi_link = item
                    mask = df['Article Title'] == title
                    # 只有当DOI链接不为空且不是'No DOI'时才更新
                    if doi_link and doi_link != 'No DOI':
                        df.loc[mask, 'DOI Link'] = doi_link
            
            # 保存更新（使用openpyxl引擎）
            df.to_excel(excel_file, index=False, engine='openpyxl')
            print(f"已更新文件: {excel_file}")
        except Exception as e:
            print(f"更新文件 {excel_file} 失败: {str(e)}")
    
    success_count = len(success_log)
    failed_count = len(failed_dois)
    total_count = success_count + failed_count
    
    if total_count > 0:
        success_rate = success_count * 100 / total_count
        print(f"✅ 任务完成! 成功率: {success_rate:.1f}%")
    else:
        print("✅ 任务完成! 没有可处理的任务")


if __name__ == "__main__":
    main()