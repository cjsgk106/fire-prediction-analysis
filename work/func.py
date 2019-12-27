import numpy as np
import pandas as pd


def dt_of_fr_pp(data):
    data['dt_of_fr_yr'] = data['dt_of_fr'].astype('datetime64').apply(lambda x : x.year)
    data['dt_of_fr_mth'] = data['dt_of_fr'].astype('datetime64').apply(lambda x : x.month)
    return data

def dt_of_athrztn_pp(data):
    data['dt_of_athrztn'].fillna(0, inplace=True)
    data['dt_of_athrztn'] = data['dt_of_athrztn'].astype('str').apply(lambda x : x.replace(' ', ''))
    data['dt_of_athrztn'] = [float(('1'+w)[:4]) if w.startswith('9') & len(w)==7 else float(w) for w in data.dt_of_athrztn]
    data.loc[data['dt_of_athrztn'] == '971215', 'dt_of_athrztn'] == 1997
    data['dt_of_athrztn'] = data['dt_of_athrztn'].astype('int')
    return data

def season_pp(data):
    data['season'] = data['dt_of_fr_mth'].apply(lambda x : '봄'  if (x ==3) | (x==4) | (x==5)  else x)
    data['season'] = data['season'].apply(lambda x : '여름'  if (x ==6) | (x==7) | (x==8)  else x)
    data['season'] = data['season'].apply(lambda x : '가을'  if (x ==9) | (x==10) | (x==11)  else x)
    data['season'] = data['season'].apply(lambda x : '겨울'  if (x ==12) | (x==1) | (x==2)  else x)

def flr_pp(data):
    data['mean_grndflr_per_bldng'] = data['ttl_grnd_flr'] / data['bldng_cnt']
    data['mean_dwnflr_per_bldng'] = data['ttl_dwn_flr'] / data['bldng_cnt']
    data['sum_grnd_dwn_flr'] = data['ttl_grnd_flr'] + data['ttl_dwn_flr']
    return data

def bldng_us_pp(data):
    list1 = ['공동주택','단독주택','제1종근린생활시설','제2종근린생활시설','근린생활시설']
    data['bldng_us2'] = ['상대적분류' if w in list1 else '절대적분류' for w in data['bldng_us']]
    data = data.drop('bldng_us', axis=1)
    
def bldng_archtctr_pp(data):
    list1 = ['통나무구조','일반목구조','목구조','기타구조']
    list2 = ['기타조적구조','블록구조','석구조','벽돌구조','조적구조']
    data['bldng_archtctr2'] = ['목구조' if w in list1 else '석구조' if w in list2 else '철골콘크리트구조' for w in data['bldng_archtctr']]
    data = data.drop('bldng_archtctr', axis=1)

def fr_wthr_fclt_pp(data):
    data['legality'] = np.where((data['fr_wthr_fclt_dstnc']>140) & (data['dt_of_athrztn']>1992), 'illegal', 'legal')

def tbc_pp(data):
    # 담배 소매점과의 최소 거리
    data.loc[data['tbc_rtl_str_dstnc'] <= 527, 'tbc_rtl_str_dstnc'] = 0
    data.loc[(data['tbc_rtl_str_dstnc'] > 527) & (data['tbc_rtl_str_dstnc'] <= 2184), 'tbc_rtl_str_dstnc'] = 1
    data.loc[(data['tbc_rtl_str_dstnc'] > 2184) & (data['tbc_rtl_str_dstnc'] <= 4958), 'tbc_rtl_str_dstnc'] = 2
    data.loc[(data['tbc_rtl_str_dstnc'] > 4958), 'tbc_rtl_str_dstnc'] = 3
    
    # 금연구역과의 최소 거리
    data.loc[data['tbc_rtl_str_dstnc'] <= 527, 'tbc_rtl_str_dstnc'] = 0
    data.loc[(data['tbc_rtl_str_dstnc'] > 527) & (data['tbc_rtl_str_dstnc'] <= 2184), 'tbc_rtl_str_dstnc'] = 1
    data.loc[(data['tbc_rtl_str_dstnc'] > 2184) & (data['tbc_rtl_str_dstnc'] <= 4958), 'tbc_rtl_str_dstnc'] = 2
    data.loc[(data['tbc_rtl_str_dstnc'] > 4958), 'tbc_rtl_str_dstnc'] = 3
    
def bldng_clssfctn_pp(data):
    ## 주거용
    apt_idx = data[(data['lnd_us_sttn_nm']=='아파트') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='주거기타') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='다세대') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='주상용') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='주거나지') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='주상기타') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='연립') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='단독') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    apt_idx = data[(data['lnd_us_sttn_nm']=='주상나지') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('주거지역')) | (data['bldng_us'].str.contains('주택')))].index
    data.loc[apt_idx, 'bldng_us_clssfctn']='주거용'
    
    ##공업용
    factory_idx = data[(data['lnd_us_sttn_nm']=='공업용') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('공업지역')) | (data['bldng_us'].str.contains('공장')))].index
    data.loc[factory_idx, 'bldng_us_clssfctn']='공업용'
    factory_idx = data[(data['lnd_us_sttn_nm']=='공업기타') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('공업지역')) | (data['bldng_us'].str.contains('공장')))].index
    data.loc[factory_idx, 'bldng_us_clssfctn']='공업용'
    factory_idx = data[(data['lnd_us_sttn_nm']=='공업나지') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('공업지역')) | (data['bldng_us'].str.contains('공장')))].index
    data.loc[factory_idx, 'bldng_us_clssfctn']='공업용'
    
    
    ##상업용
    com_idx = data[(data['lnd_us_sttn_nm']=='상업용') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('상업지역')) | (data['bldng_us'].str.contains('근린생활시설')))].index
    data.loc[com_idx, 'bldng_us_clssfctn']='상업용'
    com_idx = data[(data['lnd_us_sttn_nm']=='주상용') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('상업지역')) | (data['bldng_us'].str.contains('근린생활시설')))].index
    data.loc[com_idx, 'bldng_us_clssfctn']='상업용'
    com_idx = data[(data['lnd_us_sttn_nm']=='주상기타') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('상업지역')) | (data['bldng_us'].str.contains('근린생활시설')))].index
    data.loc[com_idx, 'bldng_us_clssfctn']='상업용'
    com_idx = data[(data['lnd_us_sttn_nm']=='상업기타') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('상업지역')) | (data['bldng_us'].str.contains('근린생활시설')))].index
    data.loc[com_idx, 'bldng_us_clssfctn']='상업용'
    com_idx = data[(data['lnd_us_sttn_nm']=='주상나지') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('상업지역')) | (data['bldng_us'].str.contains('근린생활시설')))].index
    data.loc[com_idx, 'bldng_us_clssfctn']='상업용'
    com_idx = data[(data['lnd_us_sttn_nm']=='상업나지') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('상업지역')) | (data['bldng_us'].str.contains('근린생활시설')))].index
    data.loc[com_idx, 'bldng_us_clssfctn']='상업용'
    com_idx = data[(data['lnd_us_sttn_nm']=='여객자동차터미널') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('상업지역')) | (data['bldng_us'].str.contains('근린생활시설')))].index
    data.loc[com_idx, 'bldng_us_clssfctn']='상업용'
    
    ##농업용
    farm_idx = data[(data['lnd_us_sttn_nm']=='답') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('농림지역')))].index
    data.loc[farm_idx, 'bldng_us_clssfctn']='농수산용'
    farm_idx = data[(data['lnd_us_sttn_nm']=='과수원') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('농림지역')))].index
    data.loc[farm_idx, 'bldng_us_clssfctn']='농수산용'
    
    ##문교사회용
    cul_idx = data[(data['lnd_us_sttn_nm']=='공원등') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('녹지지역')))].index
    data.loc[cul_idx, 'bldng_us_clssfctn']='문교사회용'
    cul_idx = data[(data['lnd_us_sttn_nm']=='운동장등') & (data['bldng_us_clssfctn'].isnull()) & ((data['rgnl_ar_nm'].str.contains('녹지지역')))].index
    data.loc[cul_idx, 'bldng_us_clssfctn']='문교사회용'
    
    return data