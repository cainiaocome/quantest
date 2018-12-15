#%%
from sklearn import linear_model, decomposition, ensemble, preprocessing, isotonic, metrics
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn_pandas import DataFrameMapper, cross_val_score
import sklearn.metrics as me 
import pandas as pd
import sys,os
import numpy as np
import logging
from datetime import *
import dateutil.relativedelta
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager, FontProperties  
import pickle
import seaborn as sns
from sklearn.preprocessing import Binarizer
import scipy.stats as stats  



def onehot_to_category(onehot):
    b = np.array([[0], [1], [2],[3],[4],[5]])
    return np.dot(onehot,b).flatten()

def load_X_train():
    '''
    path = '/Users/huiyang/Documents/quantest/data_Shared/tuShare/'
    X_train = pd.read_excel(path + "hist_data_W1.xlsx")
    X_train['code'] = X_train['code'].map(lambda x: str(x).zfill(6))
    X_train = X_train[X_train.date >= '2018-05-01']
    X_train.sort_values(by=['code' , 'date'], ascending=True, inplace=True)

    filename = 'X_train.xlsx'
    X_train.to_excel(path + filename)
    # generate Y
    X_train_with_Y = pd.DataFrame([])
    X_test = pd.DataFrame([])
    code_list = sorted(X_train.code.drop_duplicates().tolist())
    for code in code_list:
        #print(code)
        X_train_code = X_train[X_train.code == code]
        if len(X_train_code) >= 2:
            i = 0
            while i <= (len(X_train_code) - 1):
                if i == (len(X_train_code) - 1):
                    #输出最后一行到X_test，并从X_train集合删除
                    X_train_code.iloc[i,6] = None
                    X_train_code.iloc[i,7] = None
                    X_test = X_test.append(X_train_code.tail(1))
                    X_train_code = X_train_code.drop(X_train_code.index[i])
                else:
                    X_train_code.iloc[i,6] = X_train_code.iloc[i+1,6]    # price_change
                    X_train_code.iloc[i,7] = X_train_code.iloc[i+1,7]    # p_change
                i = i + 1
                
            X_train_with_Y = X_train_with_Y.append(X_train_code)

    filename = 'X_train_with_Y.xlsx'
    X_train_with_Y.to_excel(path + filename)
    filename = 'X_test.xlsx'
    X_test.to_excel(path + filename)
    '''

    '''
    # please note stock_basics_hist only contains data from 2016-08-09
    path = '/Users/huiyang/Documents/quantest/data_Shared/tuShare/'
    stock_basics_hist = pd.read_excel(path + "stock_basics_hist.xlsx")
    stock_basics_hist['code'] = stock_basics_hist['code'].map(lambda x: str(x).zfill(6))


    # testing purpose start
    path = '/Users/huiyang/Documents/quantest/data_Shared/tuShare/'
    X_train = pd.read_excel(path + "X_train_with_Y.xlsx")
    X_train['code'] = X_train['code'].map(lambda x: str(x).zfill(6))
    # testing purpose end
    stock_fundamentals_all = pd.read_excel(path + "stock_fundamentals_all.xlsx")
    stock_fundamentals_all['code'] = stock_fundamentals_all['code'].map(lambda x: str(x).zfill(6))
    X_train_with_fundamentals = pd.DataFrame([])
    for code, date in zip(X_train.code, X_train.date):
        stock_fundamentals = stock_fundamentals_all[(stock_fundamentals_all.code == code) \
                                                    & (stock_fundamentals_all.report_date <= date)]
        stock_basics_code = stock_basics_hist[(stock_basics_hist.code == code)  \
                                                    &(stock_basics_hist.date <= date)]
        if not stock_fundamentals.empty:
            stock_fundamentals.sort_values(by='report_date', ascending=True, inplace=True)
            stock_fundamentals = stock_fundamentals.tail(1)
            stock_basics_code.sort_values(by='date', ascending=True, inplace=True)
            stock_basics_code = stock_basics_code.tail(1)
            X_train_code = X_train[(X_train.code == code) \
                                    & (X_train.date == date)]
            X_train_code = pd.merge(X_train_code, stock_fundamentals, how='left', on=['code'])
            X_train_code = pd.merge(X_train_code, stock_basics_code, how='left', on=['code'])
            X_train_with_fundamentals = X_train_with_fundamentals.append(X_train_code)
    X_train_with_fundamentals.to_excel(path + 'X_train_with_fundamentals.xlsx')
    '''

    # testing purpose start
    path = '/Users/huiyang/Documents/quantest/data_Shared/tuShare/'
    X_train = pd.read_excel(path + "X_train_with_fundamentals.xlsx")
    X_train['code'] = X_train['code'].map(lambda x: str(x).zfill(6))

    # testing purpose end


    # get the volume for week

    # get the turnover ratio for week

    # need to check why no new stocks in the list.
    return X_train


def feature_engineering(X_train):
    #---------------------------------
    # Step 1: Select Data
    #----------------------------------
    #filter those timetomarket less than 60 days
    X_train = X_train.set_index(['code', 'date_x'], drop=False)
    print('total count before: ' + str(len(X_train)))
    for index, date, timetomarket in zip(X_train.index, X_train.date_x, X_train.timeToMarket_x):
        if date <= (datetime.strptime(timetomarket, '%Y-%m-%d') +  \
                dateutil.relativedelta.relativedelta(days=60)).date().isoformat():
            X_train = X_train.drop([index])
    X_train = X_train.reset_index(drop=True)
    print('total count after: ' + str(len(X_train)))

    # drop the unnecessary fields
    X_train.drop(
        ['code', 'date_x', 'open', 'high', 'low', \
        'name_x', 'report_date', 'quarter',  \
        'price_change', 'v_ma5', 'v_ma10', 'v_ma20',  \
        'volume', 'area_y', 'date_y', 'industry_y', 'name', 'timeToMarket_y'
        ], inplace=True, axis=1, errors='ignore')



    # industry filter
    #X_train = X_train[X_train.industry == '银行']
    #X_train.drop(
    #    ['industry', 'area', 'timeToMarket', 'currentratio', 'quickratio', \
    #    'cashratio', 'icratio', 'cashflowratio', 'cf_sales','arturnover', 'arturndays', \
    #    'inventory_turnover', 'inventory_days', 'currentasset_turnover', 'currentasset_days',   \
    #    'mbrg', 'rateofreturn', 'cf_nm', 'cf_liabilities', 'ma5', 'ma10', 'ma20'
    #    ], inplace=True, axis=1, errors='ignore')


    #---------------------------------
    # Step 2: Preprocess Data
    #----------------------------------
    X_train.rename(columns={'industry_x':'industry'}, inplace=True)
    X_train.rename(columns={'area_x':'area'}, inplace=True)
    X_train.rename(columns={'timeToMarket_x':'timeToMarket'}, inplace=True)

    
    #imputation of the missing values
    X_train['currentratio'] = X_train['currentratio'].map   \
            (lambda x: 'NaN' if x == '--' else x)
    X_train['quickratio'] = X_train['quickratio'].map   \
            (lambda x: 'NaN' if x == '--' else x)
    X_train['cashratio'] = X_train['cashratio'].map   \
            (lambda x: 'NaN' if x == '--' else x)
    X_train['icratio'] = X_train['icratio'].map   \
            (lambda x: 'NaN' if x == '--' else x)     
    X_train['currentratio'] = X_train['currentratio'].astype('float64')                                                                                                                        
    X_train['quickratio'] = X_train['quickratio'].astype('float64')                                                                                                                        
    X_train['cashratio'] = X_train['cashratio'].astype('float64')                                                                                                                        
    X_train['icratio'] = X_train['icratio'].astype('float64')                                                                                                                        

    # for distrib
    X_train['distrib'] = X_train['distrib'].map(lambda x: 0 if x is np.nan else 1)
    #pd.set_option('display.max_columns', None)
    X_train['distrib'] = X_train['distrib'].astype('uint8')                                                                                                                        

    #timeToMarket
    X_train['timeToMarket'] = X_train['timeToMarket'].map(lambda x: x[0:4])
    X_train['timeToMarket'] = X_train['timeToMarket'].astype('uint8')                                                                                                                        


    # value count - frequency distribution
    
    #print(sorted(X_train.industry.drop_duplicates().tolist()))
    print('Total of categories in - industry: ')
    print(X_train['industry'].value_counts().count())
    print('frequency distribution of each category: ')
    print(X_train['industry'].value_counts())

    '''
    [周期股：
    '专用机械', '机床制造', '电气设备', '轻工机械', '运输设备', '机械基件','电器仪表'
    '全国地产', '其他建材', '区域地产', '工程机械', '房产服务', 
    '园区开发', '建筑施工', '装修装饰', '水泥', '玻璃'
    '煤炭开采', '船舶', 
    '造纸', 
    '铁路',   '港口', '空运', '公路', '仓储物流', '水运', '路桥', '机场', '航空'
    '铅锌', '铜', '铝', '小金属', '普钢', '特种钢', '钢加工', '焦炭加工', '矿物制品'
    '汽车整车', , '汽车服务', '汽车配件', '橡胶'
    '石油加工', '石油开采', '石油贸易', '塑料', '化工原料', '化工机械', '化纤'
    , '水力发电',  '火力发电', '新型电力', '供气供热'
    , '保险', '银行', '证券', '多元金融', '黄金'
    '互联网', '元器件', '半导体', '电脑设备', '软件服务', '通信设备'

    非周期：
    '中成药',  '医疗保健', '医药商业', '化学制药', '生物制药'
    '乳制品', '农用机械',  '农药化肥', '种植业', '饲料'
    '公共交通', '其他商业', '农业综合', 
    , '商品城', '商贸代理', 
    '啤酒', '白酒', '红黄药酒'
    '家居用品', '家用电器', '纺织', '纺织机械', '染料涂料', '服饰', 
    '广告包装', '影视音像','出版业', '文教休闲', '旅游景点', '旅游服务', 
    '批发业', '摩托车',
     '林业', '水务', '渔业', '环境保护', '电信运营', 
    '电器连锁', '百货', '日用化工', '超市连锁', '软饮料', '酒店餐饮', '陶瓷', '食品',
    '综合类'
    ]
    '''
    periodic_stock = [
    '专用机械', '机床制造', '电气设备', '轻工机械', '运输设备', '机械基件','电器仪表',
    '全国地产', '其他建材', '区域地产', '工程机械', '房产服务', 
    '园区开发', '建筑施工', '装修装饰', '水泥', '玻璃',
    '煤炭开采', '船舶', 
    '造纸', 
    '铁路',   '港口', '空运', '公路', '仓储物流', '水运', '路桥', '机场', '航空',
    '铅锌', '铜', '铝', '小金属', '普钢', '特种钢', '钢加工', '焦炭加工', '矿物制品',
    '汽车整车', '汽车服务', '汽车配件', '橡胶',
    '石油加工', '石油开采', '石油贸易', '塑料', '化工原料', '化工机械', '化纤',
    '水力发电',  '火力发电', '新型电力', '供气供热',
    '保险', '银行', '证券', '多元金融', '黄金'
    '互联网', '元器件', '半导体', '电脑设备', '软件服务', '通信设备'
    ]
    X_train['industry'] = X_train['industry'].map(lambda x: '周期' if x in periodic_stock else '非周期')
    # One-Hot encoding

    #cat_df_onehot = X_train.copy()
    X_train = pd.get_dummies(X_train, columns=['industry'], prefix = ['industry'])

    
    #print(sorted(X_train.area.drop_duplicates().tolist()))
    print('Total of categories in - area: ')
    print(X_train['area'].value_counts().count())
    print(X_train['area'].value_counts())
    
    #东南：
    south_east = ['上海', '江苏','浙江', '福建', '深圳', '广东', '广西',       
    '山东', '海南']
    #中部：
    middle = ['河南', '安徽', '湖北', '江西', '湖南']
    #    西北：
    west_north = ['陕西', '甘肃', '青海', '宁夏', '新疆']
    #东北：
    east_north = ['吉林' , '辽宁', '黑龙江']
    #华北：
    china_north = ['北京', '天津', '河北', '内蒙', '山西']
    #云贵：
    yun_gui = ['云南', '贵州']
    #川藏：
    chuan_zang = ['四川', '重庆', '西藏']

    X_train['area'] = X_train['area'].map(lambda x: '东南' if x in south_east else x)
    X_train['area'] = X_train['area'].map(lambda x: '中部' if x in middle else x)
    X_train['area'] = X_train['area'].map(lambda x: '西北' if x in west_north else x)
    X_train['area'] = X_train['area'].map(lambda x: '东北' if x in east_north else x)
    X_train['area'] = X_train['area'].map(lambda x: '华北' if x in china_north else x)
    X_train['area'] = X_train['area'].map(lambda x: '云贵' if x in yun_gui else x)
    X_train['area'] = X_train['area'].map(lambda x: '川藏' if x in chuan_zang else x)
    X_train = pd.get_dummies(X_train, columns=['area'], prefix = ['area'])
    print(X_train)

    r, p=stats.pearsonr(X_train.eps_yoy,X_train.p_change)
    print (r)
    print (p)
    

    # drop the features with most of na values.
    X_train.drop(
    ['bvps_x', 'epcf'   \
    ], inplace=True, axis=1, errors='ignore')


    '''
    df = X_train.copy()
    #df.drop(['industry', 'area', 'timeToMarket' \
    #    ], inplace=True, axis=1, errors='ignore')
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    
    mapper_df = DataFrameMapper([
                    ('currentratio', imp.transform())
                    ], df_out=True)
    #df = imp.fit_transform(df)
    print(mapper_df)
    '''
    '''
    X_train['industry'] = X_train['industry'].astype('category')
    X_train['area'] = X_train['area'].astype('category')    
    #X_train['timeToMarket'] = X_train['timeToMarket'].astype('datetime64[D]')                                                                                                                        

    '''
    print(X_train.info())


    '''
    # estimate the score with or without imputation
    rng = np.random.RandomState(0)
    dataset = X_train
    X_full, y_full = dataset.currentratio, dataset.target
    n_samples = X_full.shape[0]
    n_features = X_full.shape[1]
    # Estimate the score on the entire dataset, with no missing values
    estimator = RandomForestRegressor(random_state=0, n_estimators=100)
    #score = cross_val_score(estimator, X_full, y_full).mean()
    #print("Score with the entire dataset = %.2f" % score)
    
    # Add missing values in 75% of the lines
    missing_rate = 0.75
    n_missing_samples = int(np.floor(n_samples * missing_rate))
    missing_samples = np.hstack((np.zeros(n_samples - n_missing_samples,
                                        dtype=np.bool),
                                np.ones(n_missing_samples,
                                        dtype=np.bool)))
    rng.shuffle(missing_samples)
    missing_features = rng.randint(0, n_features, n_missing_samples)
    
    # Estimate the score without the lines containing missing values
    X_filtered = X_full[~missing_samples, :]
    y_filtered = y_full[~missing_samples]
    estimator = RandomForestRegressor(random_state=0, n_estimators=100)
    score = cross_val_score(estimator, X_filtered, y_filtered).mean()
    print("Score without the samples containing missing values = %.2f" % score)

    # Estimate the score after imputation of the missing values
    X_missing = X_full.copy()
    X_missing[np.where(missing_samples)[0], missing_features] = 0
    y_missing = y_full.copy()
    estimator = Pipeline([("imputer", Imputer(missing_values=0,
                                            strategy="mean",
                                            axis=0)),
                        ("forest", RandomForestRegressor(random_state=0,
                                                        n_estimators=100))])
    score = cross_val_score(estimator, X_missing, y_missing).mean()
    print("Score after imputation of the missing values = %.2f" % score)
    '''
    # check the null values
    print('Total of null values:  ' + str(X_train.isnull().values.sum()))
    print('Column-wse distribution of null values: \n' + str(X_train.isnull().sum()))
    

    # boxplot the data
    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=9)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large = FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge = FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig_train_data, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 15))
    fig_train_data.suptitle('Train Data - boxplot',fontproperties=font_xlarge)

    axes = pd.DataFrame(X_train.pb).boxplot()
    xlabels = axes.get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(90)
        xlabel.set_fontproperties(font_small)
    ylabels = axes.get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    plt.show()

    

    '''
    industry_count = X_train['industry'].value_counts()
    sns.set(style="darkgrid")
    sns.barplot(industry_count.index, industry_count.values, alpha=0.9)
    plt.title('Frequency Distribution of Industry')
    plt.ylabel('Number of Occurrences', fontsize=12)
    plt.xlabel('Industry', fontsize=12)
    plt.draw()
    '''

    ################ procedure to clean the data#####################
    # fillna?
    # dropna?
    # Encoding Categorical Data:
    # Replacing values 
    #           (replace with int only, weighting a value improperly?)
    # Encoding labels 
    #           (replace with int only, weighting a value improperly?)
    # One-Hot encoding 
    #           (The basic strategy is to convert each category value 
    #           into a new column and assign a 1 or 0 (True/False) value 
    #           to the column, benefit of not weighting a value improperly.)
    # Binary encoding
    #           the categories are encoded as ordinal, 
    #           then those integers are converted into binary code, 
    #           then the digits from that binary string are split into separate columns.
    # Backward difference encoding
    #           the mean of the dependent variable for a level 
    #           is compared with the mean of the dependent variable for the prior level. 
    #           This type of coding may be useful for a nominal or an ordinal variable.
    #           http://www.statsmodels.org/dev/contrasts.html
    # Miscellaneous features
    #           split these ranges into two separate columns 
    #           or replace them with some measure like the mean of that range.
    # PCA 降维
    ################################################################################

    #import pdb      
    #pdb.set_trace()
    
    '''
    # Replacing values
    df_lc = df.copy()
    df_lc['industry'] = df_lc['industry'].astype('category')
    df_lc['area'] = df_lc['area'].astype('category')                                                              
    print(df_lc.dtypes)

    labels = df_lc['industry'].astype('category').cat.categories.tolist()
    replace_map_comp = {'industry' : {k: v for k,v in zip(labels,list(range(1,len(labels)+1)))}}
    print(replace_map_comp)

    df_replace = df_lc.copy()
    df_replace.replace(replace_map_comp, inplace=True)
    print(df_replace)

    # Encoding labels
    from sklearn.preprocessing import LabelEncoder
    lb_make = LabelEncoder()
    df_replace['area_code'] = lb_make.fit_transform(df_replace['area'])
    print(df_replace)
    '''

    #---------------------------------
    # Step 3: Transform Data
    #----------------------------------
    '''
    # Backward difference encoding
    cat_df_bd = df.copy()
    encoder = ce.BackwardDifferenceEncoder(cols=['area'])
    df_bd = encoder.fit_transform(cat_df_bd)

    print(df_bd.head())

    # Miscellaneous features
    cat_df_mis = df.copy()
    dummy_df_age = pd.DataFrame({'age': ['0-20', '20-40', '40-60','60-80']})
    dummy_df_age['start'], dummy_df_age['end'] = zip(*dummy_df_age['age'].map(lambda x: x.split('-')))

    dummy_df_age.head()

    '''
    X_train = X_train.dropna()
    print(X_train)

    '''
    # PCA 检测, can only detect for numeric fields
    df = df.dropna()
    pca_df = df.drop(['10days_percentage'], inplace=False, axis=1, errors='ignore')

    sc = preprocessing.StandardScaler()
    X_train_std = sc.fit_transform(pca_df)
    print(pd.DataFrame(X_train_std))
    pca = decomposition.PCA(n_components = 10)
    pca.fit(X_train_std)
    print (pca.explained_variance_ratio_)
    print (pca.explained_variance_)
    #print (pca.components_)
    #pandas.DataFrame(pca.transform(df), 
    # columns=['PCA%i' % i for i in range(n_components)], 
    # index=df.index)
    df = pd.DataFrame(pca.fit_transform(X_train_std), \
        columns=['PCA%i' % i for i in range(2)], \
        index=X_train_std.index)

    print(df)
    '''
    X_train_columns = X_train.columns.values.tolist()
    max_abs_scaler = preprocessing.MaxAbsScaler()
    X_train_MaxAbs = max_abs_scaler.fit_transform(X_train)
    X_train = pd.DataFrame(X_train_MaxAbs, columns=X_train_columns)
    print(X_train.p_change)
    ################################################################################

    # Y binary classification
    #bound = np.nanpercentile(cat_df_onehot['10days_percentage'], 20)

    #test = pd.DataFrame(Binarizer(threshold=0).fit_transform(df))
    #print(test)

    #bound = 20
    X_train.loc[(X_train['p_change'] < 0), 'Y_bin'] = -1
    X_train.loc[(X_train['p_change'] >= 0), 'Y_bin'] = 0
    X_train.loc[(X_train['p_change'] > 10), 'Y_bin'] = 1
    
    return X_train

def RF_train(X_train):

    # train dataframe split
    #logging.info(today_all)
    X = X_train.copy()
    Y = X.pop('Y_bin')
    X.pop('p_change')
    print(X)
    print(Y)
    train_size_perc = 0.8
    train_size = np.int16(np.round(train_size_perc * X.shape[0]))
    logging.info(train_size)
    X_train, Y_train = X.iloc[:train_size, :], Y.iloc[:train_size]    #?
    X_test, Y_test = X.iloc[train_size:,:], Y.iloc[train_size:]    #?
    # Random Forest train
    scaler = preprocessing.MinMaxScaler()
    X_train_trans = scaler.fit_transform(X_train)
    model = RF(n_estimators=800).fit(X_train_trans, Y_train)

    # save model file
    pkl_filename = sys.path[0] + '/' + 'RF_model' + '_' + version + '.pkl'
    print(pkl_filename)
    with open(pkl_filename, 'wb') as file:  
        pickle.dump(model, file)
        file.close()

    # validate the model
    Y_pred = model.predict(X_test)
    print (me.classification_report(Y_test, Y_pred))

    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    print(feature_importances)

    # plot show
    feature_importances.sort_values(ascending=False, inplace=True)

    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=9)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig_feature_importance, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 15))
    fig_feature_importance.suptitle('Feature Importances',fontproperties=font_xlarge)

    ax = feature_importances.plot(kind='bar')
    ax.set_xlabel('Features',fontproperties=font_medium)
    ax.set_ylabel('Importance (Gini Coefficient)',fontproperties=font_medium)

    xlabels = ax.get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_fontproperties(font_small)
    ylabels = ax.get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    plt.show()
    return

def load_X_test():
    df = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square.xlsx")
    return df

def RF_prediction(X, savedModel):
    ###########################predict#############################
    path = sys.path[0]
    pkl_filename = sys.path[0] + '/' + 'RF_model' + '_' + version + '.pkl'
    # Load from file
    with open(pkl_filename, 'rb') as file:  
        model = pickle.load(file)
    # RF prediction
    Y_pred = model.predict(X)
    #print (me.classification_report(X_test, Y_pred))

    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    print(feature_importances)

    return Y_pred



if __name__ == '__main__':    
    version = 'v1.1'
    
    X_train = load_X_train()

    train_df = feature_engineering(X_train=X_train)

    #####################################
    # for train and generate model
    RF_train(X_train=train_df)
    #for load model
    #model = load_model()
    #####################################

    #X_test = load_X_test()
    #RF_prediction(X=X_test, savedModel='RF_model.pkl')
    plt.show(block=False)