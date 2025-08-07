import pandas as pd
import os
import glob

def convert_excel_to_markdown(excel_file_path, markdown_file_path):
    """将单个Excel文件转换为指定格式的Markdown"""
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file_path)
        
        # 创建新的Markdown内容
        markdown_lines = []
        
        # 遍历每一行数据
        for index, row in df.iterrows():
            title = row.get('Article Title', '')
            doi_link = row.get('DOI Link', '')
            download_status = row.get('下载状态', '未下载')  # 获取下载状态，默认为'未下载'
            
            # 确保标题和链接都存在
            if pd.notna(title) and pd.notna(doi_link) and title and doi_link:
                # 按照指定格式生成行，包含下载状态
                markdown_line = f"- **{title}** ([link]({doi_link}))-{download_status}"
                markdown_lines.append(markdown_line)
        
        # 将所有行连接成一个字符串
        markdown_content = "\n".join(markdown_lines)
        
        # 写入Markdown文件
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"已转换: {excel_file_path} -> {markdown_file_path}")
        return True
    except Exception as e:
        print(f"转换失败: {excel_file_path} - {str(e)}")
        return False

def convert_all_excel_files():
    """将data目录下所有Excel文件转换为指定格式的Markdown"""
    # 确保目标目录存在
    os.makedirs("data_md", exist_ok=True)
    
    # 获取所有Excel文件
    excel_files = glob.glob("data/*.xls") + glob.glob("data/*.xlsx")
    
    if not excel_files:
        print("未找到Excel文件")
        return
    
    print(f"找到 {len(excel_files)} 个Excel文件")
    
    # 转换每个Excel文件
    for excel_file in excel_files:
        # 生成目标Markdown文件路径
        filename = os.path.basename(excel_file)
        name, ext = os.path.splitext(filename)
        markdown_file = os.path.join("data_md", f"{name}.md")
        
        # 转换文件
        convert_excel_to_markdown(excel_file, markdown_file)
    
    print("转换完成!")

if __name__ == "__main__":
    convert_all_excel_files()