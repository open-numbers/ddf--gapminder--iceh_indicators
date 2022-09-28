# %%
import pandas as pd

from ddf_utils.str import format_float_digits, to_concept_id
# %%
data = pd.read_stata('../source/Income deciles 20220921 LV.dta')
# %%
data.head()
# %%
data.info()
# %%
data.head()
# %%
income = data.set_index(['iso', 'year', 'deciles'])['income'].reset_index()
# %%
income = income.drop_duplicates(subset=['iso', 'year', 'deciles'])
# %%
income
# %%
synonyms = pd.read_csv('../../../ddf--open_numbers/ddf--synonyms--geo.csv')
# %%
synonyms_map = synonyms.set_index('synonym')['geo'].to_dict()
# %%
income['country'] = income['iso'].map(lambda x: synonyms_map[x])
# %%
synonyms_map['XKX']
# %%
synonyms[synonyms.synonym == 'Kosovo']
# %%
synonyms_map['XKX'] = 'kos'
# %%
income['country'] = income['iso'].map(lambda x: synonyms_map[x])
# %%
income 
# %%
income_deciles = income[['country', 'year', 'deciles']]
# %%
income_deciles
# %%
def income_by_deciles(data):
    res = data.set_index(['iso', 'year', 'level'])['income'].reset_index()
    res = res.drop_duplicates(subset=['iso', 'year', 'level'])
    res['country'] = res['iso'].map(lambda x: synonyms_map[x])
    
    res = res[['country', 'year', 'level', 'income']]
    res.columns = ['country', 'time', 'decile', 'income']
    
    res = res.sort_values(by=['country', 'time', 'decile'])
    
    res['decile'] = res['decile'].str.lower()
    
    return res
# %%
income_deciles = income_by_deciles(data)
# %%
income_deciles['income'] = income_deciles['income'].map(lambda x: format_float_digits(x, 4))
# %%
income_deciles
# %%
income_deciles.to_csv('../../ddf--datapoints--income--by--country--time--decile.csv', index=False)
# %%
data.head()
# %%
data['country'] = data['iso'].map(lambda x: synonyms_map[x])
# %%
gs = data.groupby('indic')
# %%
gs.get_group('cpmo')
# %%
for g, df in gs:
    dfg = df[['country', 'year', 'level', 'r']].copy()
    dfg.columns = ['country', 'time', 'decile', g]
    dfg[g] = dfg[g].map(lambda x: format_float_digits(x, 4))
    dfg['decile'] = dfg['decile'].str.lower()
    
    dfg = dfg.sort_values(by=['country', 'time', 'decile'])
    dfg.to_csv(f'../../ddf--datapoints--{g}--by--country--time--decile.csv', index=False)
# %%
data = pd.read_stata('../source/Income quintiles 20220921 LV.dta')
# %%
data['country'] = data['iso'].map(lambda x: synonyms_map[x])
# %%
data
# %%
gs = data.groupby('indic')
# %%
for g, df in gs:
    dfg = df[['country', 'year', 'level', 'r']].copy()
    dfg.columns = ['country', 'time', 'quintile', g]
    dfg[g] = dfg[g].map(lambda x: format_float_digits(x, 4))
    dfg['quintile'] = dfg['quintile'].str.lower()
    
    dfg = dfg.sort_values(by=['country', 'time', 'quintile'])
    dfg.to_csv(f'../../ddf--datapoints--{g}--by--country--time--quintile.csv', index=False)
# %%
def get_income(data):
    res = data.set_index(['country', 'year', 'level'])['income'].reset_index()
    res = res.drop_duplicates(subset=['country', 'year', 'level'])
    
    res = res[['country', 'year', 'level', 'income']]
    res.columns = ['country', 'time', 'quintile', 'income']
    
    res = res.sort_values(by=['country', 'time', 'quintile'])
    
    res['quintile'] = res['quintile'].str.lower()
    
    return res
# %%
incomeq = get_income(data)
# %%
incomeq
# %%
incomeq['income'] = incomeq['income'].map(lambda x: format_float_digits(x, 4))
# %%
incomeq.to_csv('../../ddf--datapoints--income--by--country--time--quintile.csv', index=False)
# %%
data = pd.read_stata('../source/National level estimates 20220921 LV.dta')
# %%
data
# %%
data['country'] = data['iso'].map(lambda x: synonyms_map[x])
# %%
gs = data.groupby('indic')
# %%
for g, df in gs:
    dfg = df[['country', 'year', 'r']].copy()
    dfg.columns = ['country', 'time', g]
    dfg[g] = dfg[g].map(lambda x: format_float_digits(x, 4))
    
    dfg = dfg.sort_values(by=['country', 'time')
    dfg.to_csv(f'../../ddf--datapoints--{g}--by--country--time.csv', index=False)
# %%
def get_income2(data):
    res = data.set_index(['country', 'year'])['income'].reset_index()
    res = res.drop_duplicates(subset=['country', 'year'])
    
    res = res[['country', 'year', 'income']]
    res.columns = ['country', 'time', 'income']
    
    res = res.sort_values(by=['country', 'time'])
    
    return res
# %%
incomen = get_income2(data)
# %%
incomen
# %%
incomeq['income'] = incomeq['income'].map(lambda x: format_float_digits(x, 4))
# %%
incomen.to_csv('../../ddf--datapoints--income--by--country--time.csv', index=False)
# %%
## Entities
# %%
decs = pd.DataFrame(range(1, 11))
# %%
decs
# %%
decs['decile'] = 'd' + decs[0].astype(str)
decs['name'] = 'decile ' + decs[0].astype(str)
# %%
decs
# %%
decs[['decile', 'name']].to_csv('../../ddf--entities--decile.csv', index=False)
# %%
quint = pd.DataFrame(range(1, 6))
quint['quintile'] = 'q' + decs[0].astype(str)
quint['name'] = 'quintile ' + decs[0].astype(str)
# %%
quint
# %%
quint[['quintile', 'name']].to_csv('../../ddf--entities--quintile.csv', index=False)
# %%
## concepts
concept_data1 = pd.read_excel('../source/ICEH indicator definitions 20220921 LV.xlsx', sheet_name='Indicators')
concept_data2 = pd.read_excel('../source/ICEH indicator definitions 20220921 LV.xlsx', sheet_name='Variables')
# %%
concept_data1
# %%
concept_data2
# %%
concept_data1.columns
# %%
c1 = concept_data1.set_index('VARIABLES')
# %%
concept_data2.columns
# %%
c2 = concept_data2.set_index('VARIABLE NAME IN DATASET')
# %%
c1.head()
# %%
c2.head()
# %%
c1.columns
# %%
c2.columns
# %%
c1.columns = c1.columns.str.strip()
c2.columns = c2.columns.str.strip()
# %%
cfull = c1.join(c2, rsuffix='2', lsuffix='1', how='outer')
# %%
cols = cfull.columns.copy()
cfull.columns = cfull.columns.map(to_concept_id)
# %%
cfull.columns
# %%
# cfull = cfull.rename(columns={'indicator_name': 'name'})
# %%
cfull.columns
# %%
cfull 
# %%
cfull.index.name = 'concept'
cfull['concept_type'] = 'measure'
# %%
cfull.columns
# %%
cfull = cfull[['concept_type', 'indicator_name', 'indicator_set', 'group', 'category1', 'description', 'sub_type',
       'denominator', 'numerator', 'stratfiers', 'diferences_dhs_mics',
       'observations1', 'category2', 'reference_period',
       'reference_unit', 'indicator_denominator', 'indicator_numerator',
       'unicef', 'observations2']].copy()
# %%
cfull.loc['income', 'concept_type'] = 'measure'
# %%
cfull.to_csv('../../ddf--concepts--continuous.csv')
# %%
cfull 
# %%
cols
# %%
cols_id = cols.map(to_concept_id)
# %%
cdf2 = pd.DataFrame({'concept': cols_id, 'name': cols})
# %%
cdf2
# %%
cdf2 = cdf2.set_index('concept')
# %%
cdf2['concept_type'] = 'string'
# %%
cdf2.loc['time'] = ['Time', 'time']
cdf2.loc['decile'] = ['Income Decile', 'entity_domain']
cdf2.loc['quintile'] = ['Income Quintile', 'entity_domain']
# %%
cdf2
# %%
oncdf = pd.read_csv('../../../ddf--open_numbers/ddf--concepts.csv', dtype=str, na_filter=None)
# %%
oncdf 
# %%
cdf3 = oncdf.set_index('concept')
# %%
cdf_full2 = pd.concat([cdf2, cdf3])
# %%
cdf_full2.to_csv('../../ddf--concepts--discrete.csv')
# %%
