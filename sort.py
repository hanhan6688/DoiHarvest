import pandas as pd
import os
import glob

def sort_excel_by_download_status():
    """根据Download Status列对Excel文件进行排序，空值排在前面，值为111的排在最后"""
    # 获取所有Excel文件
    excel_files = glob.glob("data/*.xls") + glob.glob("data/*.xlsx")
    
    if not excel_files:
        print("未找到Excel文件")
        return
    
    print(f"找到 {len(excel_files)} 个Excel文件")
    
    # 处理每个Excel文件
    for excel_file in excel_files:
        try:
            # 读取Excel文件
            df = pd.read_excel(excel_file)
            
            # 检查是否存在Download Status列
            if 'Download Status' not in df.columns:
                print(f"文件 {excel_file} 中没有找到'Download Status'列")
                continue
            
            # 创建一个排序键列：
            # - 空值或NaN设为0（排在最前面）
            # - 非111的其他值设为1
            # - 111的值设为2（排在最后面）
            def create_sort_key(value):
                if pd.isna(value) or str(value).strip() == '':
                    return 0  # 空值排在最前面
                elif str(value).strip() in ['111','成功']:
                    return 2  # 111排在最后面
                else:
                    return 1  # 其他值排在中间
            
            # 应用排序键函数
            df['sort_key'] = df['Download Status'].apply(create_sort_key)
            
            # 根据排序键进行排序
            df_sorted = df.sort_values('sort_key', ascending=True)
            
            # 删除辅助排序列
            df_sorted = df_sorted.drop('sort_key', axis=1)
            
            # 保存排序后的数据到原文件
            df_sorted.to_excel(excel_file, index=False)
            print(f"已排序文件: {excel_file}")
            
        except Exception as e:
            print(f"处理文件 {excel_file} 时出错: {str(e)}")
    
    print("排序完成!")

def main():
    sort_excel_by_download_status()

if __name__ == "__main__":
    main()