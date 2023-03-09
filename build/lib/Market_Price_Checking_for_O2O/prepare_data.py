import pandas as pd
from datetime import date
# import sys
# sys.path.append(r'R:\CPALL\MER\Mer_Market_Price_Checking_for_O2O\Script\Market_Price_Checking_for_O2O\Market_Price_Checking_for_O2O')
# import sharepoint_tools


class PreareData():
    def __init__(self):
        pass

    def product(self,file_path,sheet_name):
        self.file = file_path
        self.df = pd.read_excel(self.file,sheet_name=sheet_name)
        return self.df
    
    # def get_file_master(self):
    #     site = 'MST-MarketPriceCheckingforO2O'
    #     loc_file = r"D:\Downloads"
    #     loc_share = r"Documents->Master Files"
    #     file_names = ['Order_files.xlsx']
    #     Option = "Download"
    #     sharepoint_tools.sharepoint_document(site, loc_share, loc_file,
    #                                         Option, file_names)
    
    def get_master(self):
        data = ["น้ำปลา","พัดลม","น้ำตาล","ผงชูรส","วาสลีน","นม","กีต้า"]
        df = pd.DataFrame(data,columns = ["Group Product"])
        # print(df["Group Product"])
        return df["Group Product"]


if __name__ == "__main__":        
    p = PreareData()
    p.get_master()

