
import numpy as np
import pandas as pd 
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score, recall_score
from sklearn.model_selection import RandomizedSearchCV

cols2=['id'] 
class dropper(BaseEstimator,TransformerMixin):
    def fit(self,x,y=None):
        return self
    def transform(self,x):
        x=x.drop(cols2,axis=1)
        return x

city_type_order=['Rural','Suburban','Urban']
home_charging_order=['No','Yes']
subsidy_order=['No','Yes']
range_order=['Low','Medium','High']
cols3=['City_Type','Home_Charging_Possible','Subsidy_Available','Range_Anxiety_Level']
class ordinalencoder(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        self.oe = OrdinalEncoder(
            categories=[
                city_type_order,
                home_charging_order,
                subsidy_order,
                range_order
            ]
        )
        self.oe.fit(x[cols3])
        return self
    def transform(self, x):
        x[cols3] = self.oe.transform(x[cols3])
        return x

ohe_cols = ['Gender','Current_Car_Type']
class OHEEncoder(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        self.encoder = OneHotEncoder(
            drop='first',
            sparse_output=False,
            handle_unknown='ignore'
        )
        self.encoder.fit(x[ohe_cols])
        return self
    def transform(self, x):
        encoded = self.encoder.transform(x[ohe_cols])
        encoded_df = pd.DataFrame(
            encoded,
            columns=self.encoder.get_feature_names_out(ohe_cols),
            index=x.index
        )
        x = x.drop(ohe_cols, axis=1)
        x = pd.concat([x, encoded_df], axis=1)
        return x