#%%
from sklearn.decomposition import PCA
import pandas as pd
import sys,os



if __name__ == '__main__':    
    #path = sys.path[0]
    today_all = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_roe_pb.xlsx")
    #profit_data.drop(
    #['code', 'pubDate', 'statDate', 'gpMargin', 'MBRevenue', 'epsTTM'], inplace=True, axis=1, errors='ignore')
    #profit_data = profit_data.head(30)
    print(today_all)
    #import pdb      
    #pdb.set_trace()
    pca = PCA(n_components=0.01)
    pca.fit(today_all)
    print (pca.explained_variance_ratio_)
    print (pca.explained_variance_)

