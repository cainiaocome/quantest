#%%
from sklearn import linear_model, decomposition, ensemble, preprocessing, isotonic, metrics
from sklearn.ensemble import RandomForestClassifier as RF
import sklearn.metrics as me 
import pandas as pd
import sys,os
import numpy as np
import logging
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager, FontProperties  
import pickle
import seaborn as sns
from sklearn.preprocessing import Binarizer



def onehot_to_category(onehot):
    b = np.array([[0], [1], [2],[3],[4],[5]])
    return np.dot(onehot,b).flatten()

def load_X_train():
    path = sys.path[0]
    today_all = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-07-04.xlsx")
    '''
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-07-03.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-07-02.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-29.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-28.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-27.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-26.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-25.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-22.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-21.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-20.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-19.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-15.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-14.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-13.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all_prev = pd.read_excel(io="/Users/huiyang/Documents/SPSS modeler/复盘/today_all_R_square_2018-06-12.xlsx")
    today_all = today_all.append(today_all_prev)
    today_all = today_all[today_all.industry == '普钢']
    #today_all = today_all[['trade', 'per', 'mktcap', 'nmc', 'pe', 'pb', 'gpr', 'npr',  \
    #                        'holders', 'roe/pb', 'roe_mean', '10days_percentage']]
    '''
    today_all = today_all[['trade', 'turnoverratio', 'per', 'mktcap', 'nmc', 'industry', 'area', 'pe', 'pb', 'gpr', 'npr',  \
                            'holders', 'roe/pb', 'roe_mean', '10days_percentage']]

    return today_all


def feature_engineering(df):
    print(df.info())

    # check the null values
    print('Total of null values:  ' + str(df.isnull().values.sum()))
    print('Column-wse distribution of null values: \n' + str(df.isnull().sum()))

    # boxplot the data
    font_small = FontProperties(fname='/Library/Fonts/Songti.ttc',size=9)
    font_medium = FontProperties(fname='/Library/Fonts/Songti.ttc',size=10)
    font_large=FontProperties(fname='/Library/Fonts/Songti.ttc', size=12)
    font_xlarge=FontProperties(fname='/Library/Fonts/Songti.ttc', size=14)

    plt.style.use('ggplot')
    fig_train_data, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 15))
    fig_train_data.suptitle('Train Data - boxplot',fontproperties=font_xlarge)

    axes = df.boxplot()
    xlabels = axes.get_xticklabels()
    for xlabel in xlabels:
        xlabel.set_rotation(90)
        xlabel.set_fontproperties(font_small)
    ylabels = axes.get_yticklabels()
    for ylabel in ylabels:
        ylabel.set_fontproperties(font_small)

    plt.draw()

    # value count - frequency distribution
    print('Total of categories in - industry: ')
    print(df['industry'].value_counts().count())
    print('frequency distribution of each category: ')
    print(df['industry'].value_counts())

    print('Total of categories in - area: ')
    print(df['area'].value_counts().count())
    print(df['area'].value_counts())

    '''
    industry_count = df['industry'].value_counts()
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

    # One-Hot encoding

    cat_df_onehot = df.copy()
    cat_df_onehot = pd.get_dummies(cat_df_onehot, columns=['industry'], prefix = ['industry'])
    cat_df_onehot = pd.get_dummies(cat_df_onehot, columns=['area'], prefix = ['area'])
    #print(cat_df_onehot)

    df = cat_df_onehot

    '''
    # Binary encoding
    cat_df_ce = cat_df_onehot.copy()
    import category_encoders as ce

    encoder = ce.BinaryEncoder(cols=['area'])
    df_binary = encoder.fit_transform(cat_df_ce)

    print(df_binary.head())

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
    df = df.dropna()
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
    ################################################################################

    # Y binary classification
    #bound = np.nanpercentile(cat_df_onehot['10days_percentage'], 20)

    #test = pd.DataFrame(Binarizer(threshold=0).fit_transform(df))
    #print(test)

    bound = 0
    df.loc[(df['10days_percentage'] > bound), 'Y_bin'] = 1
    df.loc[(df['10days_percentage'] <= bound), 'Y_bin'] = -1

    return df

def RF_train(df):

    # train dataframe split
    #logging.info(today_all)
    X = df.copy()
    Y = X.pop('Y_bin')
    X.pop('10days_percentage')
    train_size_perc = 0.8
    train_size = np.int16(np.round(train_size_perc * X.shape[0]))
    logging.info(train_size)
    X_train, Y_train = X.iloc[:train_size, :], Y.iloc[:train_size]    #?
    X_test, Y_test = X.iloc[train_size:,:], Y.iloc[train_size:]    #?
    # Random Forest train
    scaler = preprocessing.MinMaxScaler()
    X_train_trans = scaler.fit_transform(X_train)
    model = RF(n_estimators=100).fit(X_train_trans, Y_train)

    # save model file
    path = sys.path[0]
    pkl_filename = path + '/' + "RF_model.pkl" 
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
    fig_feature_importance, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
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
    pkl_filename = path + '/' + savedModel
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
    logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    
    X_train = load_X_train()

    train_df = feature_engineering(df=X_train)

    #####################################
    # for train and generate model
    RF_train(df=train_df)
    #for load model
    #model = load_model()
    #####################################

    #X_test = load_X_test()
    #RF_prediction(X=X_test, savedModel='RF_model.pkl')
    plt.show(block=False)