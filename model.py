import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
import pickle

def get_ratio(row):
    name = row['AccName']
    name1 = row['DLName']
    r = fuzz.token_set_ratio(name, name1)
    if r == 100:
        return 1
    else:
        return 0

if __name__ == "__main__":
    df = pd.read_csv('dataL1.csv')

    df['Ratio'] = df.apply(get_ratio, axis=1)

    X = df[['Ratio']].values
    y = df['Match'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, \
                                                        random_state=4, stratify=y)

    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)

    model = LogisticRegression(C=100.0, random_state=1)

    model.fit(X_train_std, y_train)

    pickle.dump(model, open('model2.pkl', 'wb'))

    y_pred = model.predict(X_test_std)
    print("LogisticRegression")
    print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
    print('F1-score: %.2f' % f1_score(y_test, y_pred))
    print("\n")
    print(classification_report(y_test, y_pred, labels=[1, 0], target_names=['match', 'no-match']))
