
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class fuzzypayment():
    def load_data(self, url1, url2):
        self.df1 = pd.read_csv(url1, delimiter= ',')
        self.df2 = pd.read_csv(url2, delimiter=',')
        return self
    
    def nulled_value(self, df1,df2):
        df1_null = df1.isnull().sum()
        df2_null = df2.isnull().sum()
        return df1_null, df2_null
    
    def compare_fuzzy(self, Provider_Address,Address):
        return fuzz.partial_ratio(Provider_Address,Address)

    def find_match(self, Facility, Address):
        potential_match = self.df2[self.df2['Provider Name'] == Facility]
        result = []
        for Provider_Num, Provider_Address in zip(potential_match['Provider_Num'], potential_match['Provider Street Address']):
            if Provider_Address == Address:
                result.append(Provider_Num)
            elif Provider_Address != Address:
                score = self.compare_fuzzy(Provider_Address,Address)
                if score > 85:
                    result.append(Provider_Num)
                else:
                    pass
        return result

    def final_clean(self, list1, list2):
        final_result = pd.DataFrame()
        final_result['Account_Num'] = list1
        final_result['Provider_Num'] = list2
        for k, v in final_result['Provider_Num'].iteritems():
            if v == []:
                final_result.drop(index=k,inplace=True)
        final_result.reset_index(drop=True,inplace=True)
        return final_result


    def get_int(self, value):
        value = [str(integer) for integer in value]
        value = ''.join(value)
        value = int(value)
        return value 
    
    def account_payed(self, result_val):
        provider_val = self.df2.merge(result_val, on='Provider_Num')
        account_val = self.df1[['Account_Num','Facility Name','Address','City','State']]
        merge_val = provider_val.merge(account_val, on='Account_Num')
    
        return merge_val