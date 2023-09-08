#%%
import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
import seaborn as sbn
import scipy.stats as stats
import os

#========================================================================================================
#Load Data
rawData = pd.read_csv('C:/Users/Austin/Downloads/en.openfoodfacts.org.products.csv', sep='\t', nrows=1900210)
#rawData.dropna(inplace=True)
# desc = data.describe()
# head = data.head(20)
# #print(data.head(n=100))
# print(desc)
# print(head)

#========================================================================================================
#Create Working Dataframe
data = pd.DataFrame(rawData)
frame_Working = data.filter(['code',
                            'product_name',
                            # 'categories',# (dummy/parse needed')
                            # 'cateogries_tags',# (dummy/parse needed')
                            # 'origins',
                            # 'categories_en', #(dummy/parse needed
                            # 'origins_tags',
                            # 'origins_en',
                            # 'countries',
                            'countries_en',
                            # 'labels', #(dummy/parse needed')
                            # 'labels_tags',# (dummy/parse needed')
                            # 'labels_en',# (dummy/parse needed')
                            # 'quantity',
                            # 'ingredients_text',
                            # 'ingredients_tags',
                            # 'ingredients_analysis_tags',
                            # 'allergens',
                            'additives_n',
                            # 'additives',
                            # 'additives_tags',
                            # 'additives_en',
                            # 'pnns_groups_1',
                            # 'pnns_groups_2',
                            # 'food_groups',
                            # 'food_groups_tags',
                            # 'food_groups_en',
                            'data_quality_errors_tags',# (consider using rows only where this is null')
                            # 'main_category',
                            # 'main_category_en',
                            'energy-kcal_100g',
                            # 'energy_100g',
                            # 'fat_100g',
                            # 'saturated-fat_100g',
                            # 'carbohydrates_100g',
                            'sugars_100g',
                            # 'fiber_100g',
                            # 'proteins_100g',
                            # 'salt_100g',
                            'sodium_100g',
                            # 'vitamin-a_100g',
                            # 'vitamin-b1_100g',
                            # 'vitamin-b2_100g',
                            # 'vitamin-d_100g',
                            # 'vitamin-e_100g',
                            # 'vitamin-k_100g',
                            # 'vitamin-c_100g',
                            # 'vitamin-b6_100g',
                            # 'vitamin-b9_100g',
                            # 'vitamin-pp_100g',
                            # 'vitamin-b12_100g',
                            # 'folates_100g',
                            # 'calcium_100g',
                            # 'potassium_100g',
                            # 'iron_100g',
                            # 'magnesium_100g',
                            # 'zinc_100g',
                            # 'fruits-vegetables-nuts-estimate-from-ingredients_100g',
                            # 'nutritional_score-fr_100g'
                            ], axis=1)
frame_Working = frame_Working[frame_Working['data_quality_errors_tags'].isnull()]
# frame_Working = frame_Working.loc[frame_Working['additives_n'].isin(range(0,100))] # Bad record
# frame_Working = frame_Working.loc[frame_Working['additives_n'].isin(np.array([0,1,2,3,4,5,6,7,8,9,10,
#                                                                               11,12,13,14,15,16,17,18,19,20,
#                                                                               21,22,23,24,25,26,27,28,29,30,
#                                                                               31,32,33,34,35,36,37,38,39,40]))] # Bad record


# frame_Working = frame_Working.loc[frame_Working['code'] != 3596710517466] # Bad record
# print(frame_Working.describe)
# frame_Working.dropna(inplace=True)
# print(frame_Working.describe)


#========================================================================================================
#Plot Configurations
fig1, ax_sug = plt.subplots()
fig2, ax_add = plt.subplots()
fig3, ax_sod = plt.subplots()
fig4, ax_cal = plt.subplots()
ax_sug.set_xlim(0,125)
ax_sug.set_ylim(0,15000)
ax_add.set_xlim(0,20)
ax_add.set_ylim(0,150000)
ax_sod.set_xlim(0,50)
ax_sod.set_ylim(0,150000)
ax_cal.set_xlim(0,1000)
ax_cal.set_ylim(0,7500)

#========================================================================================================
#frame_Additives row 838075 needs to be dropped
frame_Additives = frame_Working.filter(['code','product_name','countries_en','additives_n'],axis=1)
frame_Additives.dropna(inplace=True)
frame_Additives = frame_Additives.loc[frame_Additives['additives_n'].isin(range(0,1000))]
# frame_Additives['additives_n'] = frame_Additives['additives_n'].astype('int')
frame_Additives = pd.DataFrame(frame_Additives.assign(isAmerica= np.where(frame_Additives['countries_en'] == 'United States', 1, 0)))
average_Additives = pd.DataFrame(frame_Additives.groupby(['isAmerica']).mean(['additives_n']))
sum_Additives = frame_Additives.groupby(['isAmerica']).sum(['additives_n']).astype(float)
count_Additives = frame_Additives[frame_Additives.columns[0]].count()
count_AdditivesAmerica = frame_Additives.groupby(['isAmerica']).count()

#Statistics
isAmerica = frame_Additives['isAmerica'] == 1 # Set condition

#Create new column based on condition to derive new array for statitical tests H0
series_AdditiveAmerica = frame_Additives
series_AdditiveAmerica = series_AdditiveAmerica.assign(isAmericaAddSeries = (np.where(series_AdditiveAmerica['isAmerica']==1, series_AdditiveAmerica['additives_n'], None)) )
series_AdditiveAmerica.dropna(inplace=True)
series_AdditiveAmerica = np.array(series_AdditiveAmerica['isAmericaAddSeries'])
# series_AdditiveAmerica = pd.to_numeric(series_AdditiveAmerica['additives_n'])
# series_AdditiveAmerica['additives_n'] = series_AdditiveAmerica['additives_n'].astype('int')
# print(frame_Additives)

#Create new column based on condition to derive new array for statitical tests H1
series_AdditiveNonAmerica = frame_Additives
series_AdditiveNonAmerica = series_AdditiveNonAmerica.assign(notAmericaAddSeries = (np.where(series_AdditiveNonAmerica['isAmerica']==0, series_AdditiveNonAmerica['additives_n'], None)) )
series_AdditiveNonAmerica.dropna(inplace=True)
series_AdditiveNonAmerica = np.array(series_AdditiveNonAmerica['notAmericaAddSeries'])
# series_AdditiveNonAmerica = pd.to_numeric(series_AdditiveAmerica['additives_n'])
# series_AdditiveNonAmerica['additives_n'] = series_AdditiveAmerica['additives_n'].astype('int')
# print(frame_Additives)
# print(series_AdditiveNonAmerica)

#OUTPUT
print('\n\n\n\n\n===================================================================')
print('Additives Describe Function')
print(frame_Additives.describe)

print('\nAverage Additives: Non-United States')
print(series_AdditiveNonAmerica.mean())
print('\nAverage Additives: United States')
print(series_AdditiveAmerica.mean())

print('\nAdditive Variance: Non-United States')
print(series_AdditiveNonAmerica.var())
print('\nAdditive Variance: United States')
print(series_AdditiveAmerica.var())

print('\nTotal Additive Count')
print(count_Additives)
print('\nAdditive Count: United States vs Non-United States')
print(count_AdditivesAmerica)

#Two Sample t-test
print('\nH0: μ(Average Count U.S. Food Additives) ≤  μ(Average Count Non-U.S. Food Additives)\n')
test = stats.ttest_ind(a=series_AdditiveAmerica, b=series_AdditiveNonAmerica, alternative='greater' ,equal_var=False)
print(test)

#Additive Visualization
sbn.histplot(data=frame_Additives, x = 'additives_n', color = 'blue', alpha = 1, binwidth=2, ax=ax_add, kde=True)

# #========================================================================================================
# frame_Sugars
frame_Sugars = frame_Working.filter(['code','product_name','countries_en','sugars_100g'],axis=1)
frame_Sugars.dropna(inplace=True)
frame_Sugars = frame_Sugars.assign(isAmerica= np.where(frame_Sugars['countries_en'] == 'United States', 1, 0))
average_Sugars = frame_Sugars.groupby(['isAmerica']).mean(['sugars_100g'])
count_Sugars = frame_Sugars[frame_Sugars.columns[0]].count()
count_SugarsAmerica = frame_Sugars.groupby(['isAmerica']).count()

#Statistics
isAmerica = frame_Sugars['isAmerica'] == 1 # Set condition

#Create new column based on condition to derive new array for statitical tests H0
series_SugarsAmerica = frame_Sugars
series_SugarsAmerica = series_SugarsAmerica.assign(isAmericaSugSeries = (np.where(series_SugarsAmerica['isAmerica']==1, series_SugarsAmerica['sugars_100g'], None)) )
series_SugarsAmerica.dropna(inplace=True)
series_SugarsAmerica = np.array(series_SugarsAmerica['isAmericaSugSeries'])

#Create new column based on condition to derive new array for statitical tests H1
series_SugarNonAmerica = frame_Sugars
series_SugarNonAmerica = series_SugarNonAmerica.assign(notAmericaSugSeries = (np.where(series_SugarNonAmerica['isAmerica']==0, series_SugarNonAmerica['sugars_100g'], None)) )
series_SugarNonAmerica.dropna(inplace=True)
series_SugarNonAmerica = np.array(series_SugarNonAmerica['notAmericaSugSeries'])

#OUTPUT
print('\n\n\n\n\n===================================================================')
print('Sugars Describe Function')
print(frame_Sugars.describe)

print('\nAverage Sugars: Non-United States')
print(series_SugarNonAmerica.mean())
print('\nAverage Sugars: United States')
print(series_SugarsAmerica.mean())

print('\nSugars Variance: Non-United States')
print(series_SugarNonAmerica.var())
print('\nSugars Variance: United States')
print(series_SugarsAmerica.var())

print('\nTotal Sugars Count')
print(count_Sugars)
print('\nSugars Count: United States vs Non-United States')
print(count_SugarsAmerica)

#Two Sample t-test
print('\nH0: μ(Average U.S. 100g Serving Sugar Count) ≤ μ(Average Non-U.S. 100g Serving Sugar Count)\n')
test = stats.ttest_ind(a=series_SugarsAmerica, b=series_SugarNonAmerica, alternative='greater' ,equal_var=False)
print(test)

#Sugars Visualizations
sbn.histplot(data=frame_Sugars, x = 'sugars_100g', color = 'red', alpha = 1, binwidth=1, ax=ax_sug, kde=True)

#========================================================================================================
# frame_Sodium
frame_Sodium = frame_Working.filter(['code','product_name','countries_en','sodium_100g'],axis=1)
frame_Sodium.dropna(inplace=True)
frame_Sodium = frame_Sodium.assign(isAmerica= np.where(frame_Sodium['countries_en'] == 'United States', 1, 0))
average_Sodium = frame_Sodium.groupby(['isAmerica']).mean(['sodium_100g'])
count_Sodium = frame_Sodium[frame_Sodium.columns[0]].count()
count_SodiumAmerica = frame_Sodium.groupby(['isAmerica']).count()

#Statistics
isAmerica = frame_Sodium['isAmerica'] == 1 # Set condition

#Create new column based on condition to derive new array for statitical tests H0
series_SodiumAmerica = frame_Sodium
series_SodiumAmerica = series_SodiumAmerica.assign(isAmericaSodSeries = (np.where(series_SodiumAmerica['isAmerica']==1, series_SodiumAmerica['sodium_100g'], None)) )
series_SodiumAmerica.dropna(inplace=True)
series_SodiumAmerica = np.array(series_SodiumAmerica['isAmericaSodSeries'])

#Create new column based on condition to derive new array for statitical tests H1
series_SodiumNonAmerica = frame_Sodium
series_SodiumNonAmerica = series_SodiumNonAmerica.assign(notAmericaSodSeries = (np.where(series_SodiumNonAmerica['isAmerica']==0, series_SodiumNonAmerica['sodium_100g'], None)) )
series_SodiumNonAmerica.dropna(inplace=True)
series_SodiumNonAmerica = np.array(series_SodiumNonAmerica['notAmericaSodSeries'])

#OUTPUT
print('\n\n\n\n\n===================================================================')
print('Sodium Describe Function')
print(frame_Sodium.describe)

print('\nAverage Sodium: Non-United States')
print(series_SodiumNonAmerica.mean())
print('\nAverage Sodium: United States')
print(series_SodiumAmerica.mean())

print('\nSodium Variance: Non-United States')
print(series_SodiumNonAmerica.var())
print('\nSodium Variance: United States')
print(series_SodiumAmerica.var())

print('\nTotal Sodium Count')
print(count_Sodium)
print('\nSodium Count: United States vs Non-United States')
print(count_SodiumAmerica)

#Two Sample t-test
print('\nH0: μ(Average U.S. 100g Serving Sodium Count) ≤ μ(Average Non-U.S. 100g Serving Sodium Count)\n')
test = stats.ttest_ind(a=series_SodiumAmerica, b=series_SodiumNonAmerica, alternative='greater' ,equal_var=False)
print(test)

#Sodium Visualizations
sbn.histplot(data=frame_Sodium, x = 'sodium_100g', color = 'green', alpha = 1, binwidth=1, ax=ax_sod, kde=True)

#========================================================================================================
# frame_Calories
frame_Calories = frame_Working.filter(['code','product_name','countries_en','energy-kcal_100g'],axis=1)
frame_Calories.dropna(inplace=True)
frame_Calories = frame_Calories.assign(isAmerica= np.where(frame_Calories['countries_en'] == 'United States', 1, 0))

average_Calories = frame_Calories.groupby(['isAmerica']).mean(['energy-kcal_100g'])
count_Calories = frame_Calories[frame_Calories.columns[0]].count()
count_CaloriesAmerica = frame_Calories.groupby(['isAmerica']).count()

#Statistics
isAmerica = frame_Calories['isAmerica'] == 1 # Set condition

#Create new column based on condition to derive new array for statitical tests H0
series_CaloriesAmerica = frame_Calories
series_CaloriesAmerica = series_CaloriesAmerica.assign(isAmericaCalSeries = (np.where(series_CaloriesAmerica['isAmerica']==1, series_CaloriesAmerica['energy-kcal_100g'], None)) )
series_CaloriesAmerica.dropna(inplace=True)
series_CaloriesAmerica = np.array(series_CaloriesAmerica['isAmericaCalSeries'])

#Create new column based on condition to derive new array for statitical tests H1
series_CaloriesNonAmerica = frame_Calories
series_CaloriesNonAmerica = series_CaloriesNonAmerica.assign(notAmericaCalSeries = (np.where(series_CaloriesNonAmerica['isAmerica']==0, series_CaloriesNonAmerica['energy-kcal_100g'], None)) )
series_CaloriesNonAmerica.dropna(inplace=True)
series_CaloriesNonAmerica = np.array(series_CaloriesNonAmerica['notAmericaCalSeries'])

#OUTPUT
print('\n\n\n\n\n===================================================================')
print('Calories Describe Function')
print(frame_Calories.describe)

print('\nAverage Calories: Non-United States')
print(series_CaloriesNonAmerica.mean())
print('\nAverage Calories: United States')
print(series_CaloriesAmerica.mean())

print('\nCalories Variance: Non-United States')
print(series_CaloriesNonAmerica.var())
print('\nCalories Variance: United States')
print(series_CaloriesAmerica.var())

print('\nTotal Calories Count')
print(count_Calories)
print('\nCalories Count: United States vs Non-United States')
print(count_CaloriesAmerica)

#Two Sample t-test
print('\nH0: μ(Average U.S. 100g Serving Caloric Count) ≤ μ(Average Non-U.S. 100g Serving Caloric Count)\n')
test = stats.ttest_ind(a=series_CaloriesAmerica, b=series_CaloriesNonAmerica, alternative='greater' ,equal_var=False)
print(test)

#Calories Visualizations
sbn.histplot(data=frame_Calories, x = 'energy-kcal_100g', color = 'purple', alpha = 1, binwidth=1, ax=ax_cal, kde=True)