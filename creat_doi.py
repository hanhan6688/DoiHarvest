import pandas as pd
import os
import glob


def generate_doi_link(doi):
    """根据DOI生成论文链接"""
    if doi and str(doi).strip() != '':
        # 清理DOI，移除可能的前缀
        doi = str(doi).strip().replace("doi:", "").replace("DOI:", "")
        return f'https://doi.org/{doi}'
    return 'No DOI'


def update_excel_doi_column(excel_file_path):
    """更新单个Excel文件的DOI Link列"""
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file_path)
        
        # 确保有DOI列
        if 'DOI' not in df.columns:
            print(f"警告: 文件 {excel_file_path} 中没有找到DOI列")
            return False
        
        # 确保有Article Title列
        if 'Article Title' not in df.columns:
            print(f"警告: 文件 {excel_file_path} 中没有找到Article Title列")
            return False
        
        # 确保有DOI Link列（第三列）
        if len(df.columns) < 3:
            # 如果列数少于3列，添加DOI Link列
            df.insert(2, 'DOI Link', '')
        elif df.columns[2] != 'DOI Link':
            # 如果第三列不是DOI Link，添加新的DOI Link列
            df.insert(2, 'DOI Link', '')
        
        # 为每一行生成DOI链接
        for index, row in df.iterrows():
            doi = row.get('DOI', '')
            doi_link = generate_doi_link(doi)
            df.at[index, 'DOI Link'] = doi_link
        
        # 保存更新后的文件
        df.to_excel(excel_file_path, index=False, engine='openpyxl')
        print(f"已更新文件: {excel_file_path}")
        return True
        
    except Exception as e:
        print(f"处理文件 {excel_file_path} 时出错: {str(e)}")
        return False


def update_multiple_excel_files(data_directory="data"):
    """批量更新目录下所有Excel文件的DOI Link列"""
    # 获取所有Excel文件
    excel_files = glob.glob(os.path.join(data_directory, "*.xls")) + \
                  glob.glob(os.path.join(data_directory, "*.xlsx"))
    
    if not excel_files:
        print(f"在目录 {data_directory} 中没有找到Excel文件")
        return
    
    print(f"找到 {len(excel_files)} 个Excel文件")
    
    # 处理每个Excel文件
    success_count = 0
    for excel_file in excel_files:
        if update_excel_doi_column(excel_file):
            success_count += 1
    
    print(f"\n处理完成: {success_count}/{len(excel_files)} 个文件成功更新")


if __name__ == "__main__":
    # 更新data目录下的所有Excel文件
    update_multiple_excel_files()