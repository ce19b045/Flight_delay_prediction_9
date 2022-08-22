{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "289aa939",
   "metadata": {},
   "outputs": [],
   "source": [
    "import math\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "55faaeb0",
   "metadata": {},
   "outputs": [],
   "source": [
    "train = pd.read_csv('../input/pokemon-datasets-for-ml/train_pokemon.csv')\n",
    "test = pd.read_csv('../input/pokemon-datasets-for-ml/test_pokemon.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3507aaa6",
   "metadata": {},
   "outputs": [],
   "source": [
    "train.head(3)\n",
    "train.shape\n",
    "train.describe()\n",
    "# describe(include = ['O']) will show the descriptive statistics of object data types.\n",
    "train.describe(include=['O'])\n",
    "# check for missing values\n",
    "sns.heatmap(train.isnull(),yticklabels=False,cbar=False,cmap='viridis')\n",
    "def fill_type_2(cols):\n",
    "    type_2 = cols[0]\n",
    "    if pd.isnull(type_2):\n",
    "        return \"None\"\n",
    "    else:\n",
    "        return type_2\n",
    "    train['Type_2'] = train[['Type_2']].apply(fill_type_2,axis=1)\n",
    "    train.drop(columns=['Egg_Group_2'], inplace=True)\n",
    "    sns.heatmap(train.isnull(),yticklabels=False,cbar=False,cmap='viridis')\n",
    "    legendary = train[train['isLegendary'] == 1]\n",
    "not_legendary = train[train['isLegendary'] == 0]\n",
    "\n",
    "print(\"Legendary: %i (%.1f%%)\"%(len(legendary), float(len(legendary))/len(train)*100.0))\n",
    "print(\"Not Legendary: %i (%.1f%%)\"%(len(not_legendary), float(len(not_legendary))/len(train)*100.0))\n",
    "print(\"Total: %i\"%len(train))\n",
    "plt.figure(figsize=(25,10))\n",
    "train2 = train.drop(['Number','Name','hasGender','shuffle'], axis=1)\n",
    "sns.heatmap(train2.corr(), vmin= -1, vmax=1, square=True, annot=True)\n",
    "\n",
    "#boxplot of Attack vs. Legendary\n",
    "plt.figure(figsize=(8, 4))\n",
    "sns.boxplot(x='isLegendary',y='Attack',data=train, palette='rainbow')\n",
    "\n",
    "#stripplot of Attack vs. Legendary\n",
    "plt.figure(figsize=(15, 4))\n",
    "sns.stripplot(x='Type_1',y='Total',data=train, jitter=True,hue='isLegendary',palette=['r','b'],dodge=False).set_title('Type_1 Distribution on Legendary')\n",
    "\n",
    "#stripplot of Attack vs. Legendary\n",
    "plt.figure(figsize=(15, 4))\n",
    "sns.stripplot(x='Type_2',y='Total',data=train, jitter=True,hue='isLegendary',palette=['r','b'],dodge=False).set_title('Type_2 Distribution on Legendary')\n",
    "\n",
    "type_1 = train[['Type_1','isLegendary']].groupby(['Type_1'], as_index=False).mean().set_index('Type_1')\n",
    "type_1.sort_values(by='isLegendary',ascending=False).plot(kind='bar')\n",
    "\n",
    "\n",
    "\n",
    "type_2 = train[['Type_2','isLegendary']].groupby(['Type_2'], as_index=False).mean().set_index('Type_2')\n",
    "type_2.sort_values(by='isLegendary',ascending=False).plot(kind='bar')\n",
    "\n",
    "train_test_data = [train, test]\n",
    "for dataset in train_test_data:\n",
    "    dataset['isLegendary'] = dataset['isLegendary'].map({True: 1, False: 0}).astype(int)\n",
    "    \n",
    "    type_1.sort_values(by='isLegendary',ascending=False)\n",
    "    \n",
    "    type_1_mapping = {\"Fire\": 1, \"Dragon\": 2, \"Electric\": 3, \"Fighting\": 4, \"Ice\": 5, \"Flying\": 6, \"Water\": 7, \"Ghost\": 8, \"Steel\": 9, \"None\": 10, \"Fairy\": 11, \"Psychic\": 12, \"Ground\": 13, \"Rock\": 14, \"Bug\": 15, \"Poison\": 16, \"Normal\": 17, \"Dark\": 18, \"Grass\": 19}\n",
    "for dataset in train_test_data:\n",
    "    dataset['Type_1'] = dataset['Type_1'].map(type_1_mapping)\n",
    "    dataset['Type_1'] = dataset['Type_1'].fillna(0)\n",
    "    \n",
    "    type_2_mapping = {\"Fire\": 1, \"Dragon\": 2, \"Electric\": 3, \"Fighting\": 4, \"Ice\": 5, \"Flying\": 6, \"Water\": 7, \"Ghost\": 8, \"Steel\": 9, \"None\": 10, \"Fairy\": 11, \"Psychic\": 12, \"Ground\": 13, \"Rock\": 14, \"Bug\": 15, \"Poison\": 16, \"Normal\": 17, \"Dark\": 18, \"Grass\": 19}\n",
    "for dataset in train_test_data:\n",
    "    dataset['Type_2'] = dataset['Type_2'].map(type_2_mapping)\n",
    "    dataset['Type_2'] = dataset['Type_2'].fillna(0)\n",
    "    \n",
    "    for dataset in train_test_data:\n",
    "    pr_male_avg = dataset['Pr_Male'].mean()\n",
    "    pr_male_std = dataset['Pr_Male'].std()\n",
    "    pr_male_null_count = dataset['Pr_Male'].isnull().sum()\n",
    "    \n",
    "    pr_male_null_random_list = np.random.uniform(pr_male_avg - pr_male_std, pr_male_avg + pr_male_std, pr_male_null_count)\n",
    "    dataset['Pr_Male'][np.isnan(dataset['Pr_Male'])] = pr_male_null_random_list\n",
    "    dataset['Pr_Male'] = dataset['Pr_Male'].astype(int)\n",
    "    \n",
    "train['Pr_Male_Band'] = pd.cut(train['Pr_Male'], 5)\n",
    "\n",
    "print(train[['Pr_Male_Band', 'isLegendary']].groupby(['Pr_Male_Band'], as_index=False).mean())\n",
    "\n",
    "for dataset in train_test_data:\n",
    "    dataset.loc[ dataset['Pr_Male'] <= 0.2, 'Pr_Male'] = 0\n",
    "    dataset.loc[(dataset['Pr_Male'] > 0.2) & (dataset['Pr_Male'] <= 0.4), 'Pr_Male'] = 1\n",
    "    dataset.loc[(dataset['Pr_Male'] > 0.4) & (dataset['Pr_Male'] <= 0.6), 'Pr_Male'] = 2\n",
    "    dataset.loc[(dataset['Pr_Male'] > 0.6) & (dataset['Pr_Male'] <= 0.8), 'Pr_Male'] = 3\n",
    "    dataset.loc[ dataset['Pr_Male'] >= 1, 'Pr_Male'] = 4\n",
    "    \n",
    "   for dataset in train_test_data:\n",
    "    attack_avg = dataset['Attack'].mean()\n",
    "    attack_std = dataset['Attack'].std()\n",
    "    attack_null_count = dataset['Attack'].isnull().sum()\n",
    "    \n",
    "    attack_null_random_list = np.random.randint(attack_avg - attack_std, attack_avg + attack_std, attack_null_count)\n",
    "    dataset['Attack'][np.isnan(dataset['Attack'])] = attack_null_random_list\n",
    "    dataset['Attack'] = dataset['Attack'].astype(int)\n",
    "    \n",
    "train['Attack_Band'] = pd.cut(train['Attack'], 5)\n",
    "\n",
    "print(train[['Attack_Band', 'isLegendary']].groupby(['Attack_Band'], as_index=False).mean())\n",
    "\n",
    "for dataset in train_test_data:\n",
    "    dataset.loc[ dataset['Attack'] <= 36, 'Attack'] = 0\n",
    "    dataset.loc[(dataset['Attack'] > 36) & (dataset['Attack'] <= 67), 'Attack'] = 1\n",
    "    dataset.loc[(dataset['Attack'] > 67) & (dataset['Attack'] <= 98), 'Attack'] = 2\n",
    "    dataset.loc[(dataset['Attack'] > 98) & (dataset['Attack'] <= 129), 'Attack'] = 3\n",
    "    dataset.loc[ dataset['Attack'] >= 129, 'Attack'] = 4\n",
    "    \n",
    "    for dataset in train_test_data:\n",
    "    defense_avg = dataset['Defense'].mean()\n",
    "    defense_std = dataset['Defense'].std()\n",
    "    defense_null_count = dataset['Defense'].isnull().sum()\n",
    "    \n",
    "    defense_null_random_list = np.random.randint(defense_avg - defense_std, defense_avg + defense_std, defense_null_count)\n",
    "    dataset['Defense'][np.isnan(dataset['Defense'])] = defense_null_random_list\n",
    "    dataset['Defense'] = dataset['Defense'].astype(int)\n",
    "    \n",
    "train['Defense_Band'] = pd.cut(train['Defense'], 5)\n",
    "\n",
    "print(train[['Defense_Band', 'isLegendary']].groupby(['Defense_Band'], as_index=False).mean())\n",
    "\n",
    "for dataset in train_test_data:\n",
    "    dataset.loc[ dataset['Defense'] <= 50, 'Defense'] = 0\n",
    "    dataset.loc[(dataset['Defense'] > 50) & (dataset['Defense'] <= 95), 'Defense'] = 1\n",
    "    dataset.loc[(dataset['Defense'] > 95) & (dataset['Defense'] <= 140), 'Defense'] = 2\n",
    "    dataset.loc[(dataset['Defense'] > 140) & (dataset['Defense'] <= 230), 'Defense'] = 3\n",
    "    dataset.loc[ dataset['Defense'] >= 230, 'Defense'] = 4\n",
    "    \n",
    "for dataset in train_test_data:\n",
    "    cr_avg = dataset['Catch_Rate'].mean()\n",
    "    cr_std = dataset['Catch_Rate'].std()\n",
    "    cr_null_count = dataset['Catch_Rate'].isnull().sum()\n",
    "    \n",
    "    cr_null_random_list = np.random.randint(cr_avg - cr_std, cr_avg + cr_std, cr_null_count)\n",
    "    dataset['Catch_Rate'][np.isnan(dataset['Catch_Rate'])] = cr_null_random_list\n",
    "    dataset['Catch_Rate'] = dataset['Catch_Rate'].astype(int)\n",
    "    \n",
    "train['Catch_Rate_Band'] = pd.cut(train['Catch_Rate'], 5)\n",
    "\n",
    "print(train[['Catch_Rate_Band', 'isLegendary']].groupby(['Catch_Rate_Band'], as_index=False).mean())\n",
    "\n",
    "for dataset in train_test_data:\n",
    "    dataset.loc[ dataset['Catch_Rate'] <= 53, 'Catch_Rate'] = 0\n",
    "    dataset.loc[(dataset['Catch_Rate'] > 53) & (dataset['Catch_Rate'] <= 104), 'Catch_Rate'] = 1\n",
    "    dataset.loc[(dataset['Catch_Rate'] > 104) & (dataset['Catch_Rate'] <= 154), 'Catch_Rate'] = 2\n",
    "    dataset.loc[(dataset['Catch_Rate'] > 154) & (dataset['Catch_Rate'] <= 204), 'Catch_Rate'] = 3\n",
    "    dataset.loc[ dataset['Catch_Rate'] >= 255, 'Catch_Rate'] = 4\n",
    "    \n",
    "train.columns\n",
    "    \n",
    "train_drop = ['Number', 'Name', 'Total', 'HP', 'Sp_Atk', 'Sp_Def', 'Speed', 'Generation','Color', 'hasGender', 'Egg_Group_1', 'hasMegaEvolution','Height_m', 'Weight_kg', 'Body_Style', 'shuffle','Pr_Male_Band', 'Attack_Band', 'Defense_Band', 'Catch_Rate_Band']\n",
    "train = train.drop(train_drop, axis=1)\n",
    "\n",
    "test_drop = ['Number', 'Name', 'Total', 'HP', 'Sp_Atk', 'Sp_Def', 'Speed', 'Generation',\n",
    "       'Color', 'hasGender', 'Egg_Group_1', 'Egg_Group_2', 'isLegendary',\n",
    "       'hasMegaEvolution', 'Height_m', 'Weight_kg', 'Body_Style',\n",
    "       'shuffle']\n",
    "test = test.drop(test_drop, axis=1)\n",
    "\n",
    "\n",
    "  \n",
    "X_train = train.drop('isLegendary', axis=1)\n",
    "y_train = train['isLegendary']\n",
    "X_test = test.copy()\n",
    "\n",
    "X_train.shape, y_train.shape, X_test.shape\n",
    "\n",
    "# Importing Classifier Modules\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.svm import SVC, LinearSVC\n",
    "from sklearn.neighbors import KNeighborsClassifier\n",
    "from sklearn.tree import DecisionTreeClassifier\n",
    "from sklearn.ensemble import RandomForestClassifier\n",
    "from sklearn.naive_bayes import GaussianNB\n",
    "from sklearn.linear_model import Perceptron\n",
    "from sklearn.linear_model import SGDClassifier\n",
    "\n",
    "\n",
    "clf = LogisticRegression()\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_log_reg = clf.predict(X_test)\n",
    "acc_log_reg = round( clf.score(X_train, y_train) * 100, 2)\n",
    "print(str(acc_log_reg) + ' percent)\n",
    "      \n",
    "clf = SVC()\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_svc = clf.predict(X_test)\n",
    "acc_svc = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_svc)\n",
    "      \n",
    "clf = KNeighborsClassifier(n_neighbors = 3)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_knn = clf.predict(X_test)\n",
    "acc_knn = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_knn)\n",
    "      \n",
    "clf = DecisionTreeClassifier()\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_decision_tree = clf.predict(X_test)\n",
    "acc_decision_tree = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_decision_tree)\n",
    "      \n",
    "clf = RandomForestClassifier(n_estimators=100)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_random_forest = clf.predict(X_test)\n",
    "acc_random_forest = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_random_forest)\n",
    "\n",
    "clf = GaussianNB()\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_gnb = clf.predict(X_test)\n",
    "acc_gnb = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_gnb)\n",
    "    \n",
    "clf = Perceptron(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_perceptron = clf.predict(X_test)\n",
    "acc_perceptron = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_perceptron)\n",
    "\n",
    "clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)\n",
    "      \n",
    "clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)clf = SGDClassifier(max_iter=5, tol=None)\n",
    "clf.fit(X_train, y_train)\n",
    "y_pred_sgd = clf.predict(X_test)\n",
    "acc_sgd = round(clf.score(X_train, y_train) * 100, 2)\n",
    "print (acc_sgd)\n",
    "      \n",
    "models = pd.DataFrame({\n",
    "    'Model': ['Logistic Regression', 'Support Vector Machines', \n",
    "              'KNN', 'Decision Tree', 'Random Forest', 'Naive Bayes', \n",
    "              'Perceptron', 'Stochastic Gradient Decent'],\n",
    "    \n",
    "    'Score': [acc_log_reg, acc_svc, \n",
    "              acc_knn,  acc_decision_tree, acc_random_forest, acc_gnb, \n",
    "              acc_perceptron, acc_sgd]\n",
    "    })\n",
    "\n",
    "models.sort_values(by='Score', ascending=False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
