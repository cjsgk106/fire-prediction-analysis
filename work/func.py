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
    data['legality'] = np.where((data['fr_wthr_fclt_dstnc']>140) & (data['dt_of_athrztn']>1992), 'illegal', 'legal') # 소방법 제44조에 따라 1992년 개정 이후에 최소 140m이내에 소방용수시설 필요.

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
    
    #기타
    data['bldng_us_clssfctn']=data['bldng_us_clssfctn'].fillna('기타')
    
    return data

     #건축면적 <= 건물 연면적 아닌 데이터 행 삭제.
def ar_pp(data):
    data=data[data['bldng_ar']<data['ttl_ar']]                         #건물면적 < 건물 연면적
    data.bldng_ar[(data.bldng_us.notnull())&(data.bldng_ar==0)]=135    #건물면적이 0인데 건물이 존재 -> 건물면적값 중간값(135) 대입
    data.lnd_ar[(data.bldng_us.notnull()) & (data.lnd_ar==0)]=230      #토지면적이 0인데 건물이 존재 -> 토지면적값 중간값(230) 대입
  
    return data

def rgnl_ar_nm_modi(data) : 
    data.loc[data['rgnl_ar_nm'].str.contains('주거지역', na = False), 'rgnl_ar_nm'] = 0  # 주거지역
    data.loc[data['rgnl_ar_nm'].str.contains('상업지역', na = False), 'rgnl_ar_nm'] = 1  # 상업지역
    data.loc[data['rgnl_ar_nm'].str.contains('공업지역', na = False), 'rgnl_ar_nm'] = 2  # 공업지역
    data.loc[data['rgnl_ar_nm'].str.contains('녹지지역', na = False), 'rgnl_ar_nm'] = 3  # 녹지지역
    data.loc[data['rgnl_ar_nm'].str.contains('관리지역', na = False), 'rgnl_ar_nm'] = 4  # 관리지역
    data.loc[data['rgnl_ar_nm'].str.contains('농림지역', na = False), 'rgnl_ar_nm'] = 5  # 농림지역
    data.loc[data['rgnl_ar_nm'].str.contains('자연환경보전지역', na = False), 'rgnl_ar_nm'] = 6  # 자연환경보전지역
    data.loc[data['rgnl_ar_nm'].str.contains('용도미지정', na = False), 'rgnl_ar_nm'] = 7  # 용도미지정
    data.loc[(data['rgnl_ar_nm'].isnull()) & (data['bldng_us_clssfctn'] == '주거용'), 'rgnl_ar_nm'] = 0 # 주거지역
    data.loc[(data['rgnl_ar_nm'].isnull()) & (data['bldng_us_clssfctn'] == '상업용'), 'rgnl_ar_nm'] = 1 #상업지역
    data.loc[(data['rgnl_ar_nm'].isnull()) & (data['bldng_us_clssfctn'] == '공업용'), 'rgnl_ar_nm'] = 2 #공업지역
    data.loc[(data['rgnl_ar_nm'].isnull()) & (data['rgnl_ar_nm2'] == '자연녹지지역'), 'rgnl_ar_nm' ] = 3  #녹지지역
    data.loc[(data['rgnl_ar_nm'].isnull()) & (data['rgnl_ar_nm2'] == '제1종일반주거지역'), 'rgnl_ar_nm' ] = 0  #주거지역
    data.loc[(data['rgnl_ar_nm'].isnull()) & (data['rgnl_ar_nm2'] == '지정되지않음'), 'rgnl_ar_nm' ] = 7  #지정되지않음

    return data
# categorical type으로 변경

def lnd_us_sttn_nm_modi1(data) :
    
    ind = []
    for i in data.lnd_us_sttn_nm :
        if (i == '단독') | (i == '연립') | (i == '다세대') | (i == '아파트') | (i == '주거나지') | (i == '주거기타'):
            ind.append('주거용')
        elif (i == '상업용') | (i == '업무용') | (i == '상업나지') | (i == '상업기타') | (i == '콘도미니엄') :
            ind.append('상업.업무용')
        elif (i =='주상용') | (i == '주상나지') | (i == '주상기타') :
            ind.append('주.상복합용')
        elif (i == '공업용') | (i == '공업나지') | (i == '공업기타'):
            ind.append('공업용')
        elif (i == '전') | (i == '과수원') | (i == '전기타') :
            ind.append('전')
        elif (i == '답') | (i == '답기타') :
            ind.append('답')
        elif (i == '조림') | (i == '자연림') | (i == '토지임야') | (i == '목장용지') | (i == '임야기타'):
            ind.append('임야')
        elif (i == '도로등') | (i == '하천등') | (i == '공원등') | (i == '운동장등') | (i == '주차장등') | (i == '위험시설') | (i == '유해.혐오시설') | (i == '발전소') : 
            ind.append('공공용지')
        elif (i == '유원지') | (i == '공원묘지') | (i == '골프장 대중제') | (i == '스키장') | (i == '특수기타') | (i == '골프장 회원제') | (i == '고속도로휴게소') | (i == '여객자동차터미널') : 
            ind.append('특수토지')
        else :
            ind.append(i)
    data.lnd_us_sttn_nm = ind

def lnd_us_sttn_nm_modi2(data) :
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '목'), 'lnd_us_sttn_nm'] = '임야'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '도'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '천'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '구'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '유'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '제'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '장'), 'lnd_us_sttn_nm'] = '공업용'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '답'), 'lnd_us_sttn_nm'] = '답'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '전'), 'lnd_us_sttn_nm'] = '전'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '차'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '공'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '묘'), 'lnd_us_sttn_nm'] = '공공용지'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '임'), 'lnd_us_sttn_nm'] = '임야'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '과'), 'lnd_us_sttn_nm'] = '전'
    data.loc[(data['lnd_us_sttn_nm'].isna()) & (data['jmk'] == '원'), 'lnd_us_sttn_nm'] = '특수토지'
    data.loc[(data['lnd_us_sttn_nm'].isnull()) & (data['bldng_us_clssfctn'] == '주거용'), 'lnd_us_sttn_nm'] = '주거용'
    data.loc[(data['lnd_us_sttn_nm'].isnull()) & (data['bldng_us_clssfctn'] == '상업용'), 'lnd_us_sttn_nm'] = '상업용'
    data.loc[(data['lnd_us_sttn_nm'].isnull()) & (data['bldng_us_clssfctn'] == '공업용'), 'lnd_us_sttn_nm'] = '공업용'
    data.loc[(data['lnd_us_sttn_nm'].isnull()) & (data['bldng_us_clssfctn'] == '공공용'), 'lnd_us_sttn_nm'] = '공공용지'
    return data


def emd_nm_modi(data) :
    data['emd_nm'] = data['emd_nm'].astype(str).apply(lambda x : x[4:] if x[:4]=='경상남도' else x )
    data['emd_nm_big'] = data['emd_nm'].apply(lambda x : x.split()[0] if x.split()[0]!='창원시' else x.split()[0]+x.split()[1])
    data['emd_nm_small'] = data['emd_nm'].apply(lambda x : x.split()[1] if (x.split()[0]!='창원시') & (x!='nan') else x)
    data['emd_nm_small'] = data['emd_nm_small'].apply(lambda x : x.split()[2] if x.split()[0]=='창원시' else x )

def emd_nm_modi2(data) :
    data['emd_nm'] = data['emd_nm'].astype(str).apply(lambda x : x[5:] if x[:4]=='경상남도' else x )
    data['emd_nm_big'] = data['emd_nm'].apply(lambda x : x.split()[0])
    data['emd_nm_small'] = data['emd_nm'].apply(lambda x : x.split()[1])

def hm_cnt_modi(data) :
    hm_cnt_mean = round(data.groupby('emd_nm_small')['hm_cnt'].mean())
    for i in range(0,len(hm_cnt_mean)) :
        data.loc[(data['hm_cnt'].isnull()) & (data['emd_nm_small'] == hm_cnt_mean.keys()[i]), 'hm_cnt'] = hm_cnt_mean.values[i]


