import pandas as pd
import os

data_dir = 'data'
for file_name in os.listdir(data_dir):
    if file_name.endswith('.xls'):
        # 读取.xls文件
        xls_path = os.path.join(data_dir, file_name)
        df = pd.read_excel(xls_path)
        
        # 保存为.xlsx文件
        xlsx_file_name = file_name.replace('.xls', '.xlsx')
        xlsx_path = os.path.join(data_dir, xlsx_file_name)
        df.to_excel(xlsx_path, index=False)
        
        # 删除原始.xls文件（可选）
        os.remove(xls_path)
        print(f"Converted {file_name} to {xlsx_file_name}")