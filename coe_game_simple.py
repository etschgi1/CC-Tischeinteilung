import numpy as np
import pandas as pd
from pprint import pprint
import datetime

np.random.seed(42)
TISCHE_cap = [12, 4, 10, 10, 10, 16, 18, 7, 6]
Tischlabels = ["12er Tisch", "4er Tisch", "1. 10er Tisch", "2. 10er Tisch",
               "3. 10er Tisch", "16er Tisch", "18er Tisch", "7er Tisch", "6er Tisch"]
print("Tisches insgesamt: " + str(sum(TISCHE_cap)) + "\n")


def import_csv_as_dataframe(path):
    df = pd.read_csv(path, sep=";", nrows=81)  # usecols=[2, 3, 4, 5, 6, 7, 8]
    return df


data = (import_csv_as_dataframe("2.CC Liste.csv"))
# add empty tischnumber column
data["Tischnummer"] = np.nan
# add id column with ascending numbers
data["ID"] = np.arange(1, len(data) + 1)

counts = data["teilnahme"].value_counts()
print("Teilnahme results: " + str(counts))

# Tischeinteilung:


def random_tischeinteilung():
    plan = {k: [] for k in Tischlabels}
    cap = {k: v for k, v in zip(Tischlabels, TISCHE_cap)}
    people_ = [(name, lastname, year, id) for name, lastname, year, id in zip(
        data["Vorname"], data["Nachname"], data["Jahrgang"], data["ID"])]
    class_of_year = [person for person in people_ if person[2] == datetime.date.today().year ]
    other = [person for person in people_ if person[2] != datetime.date.today().year ]
    np.random.shuffle(class_of_year)
    np.random.shuffle(other)
    # 2023 fix setzten
    labels = ["12er Tisch", "1. 10er Tisch", "2. 10er Tisch",
              "3. 10er Tisch", "16er Tisch", "18er Tisch"] * 2 + ["18er Tisch", "7er Tisch", "6er Tisch"] * 2 + ["4er Tisch"]
    for i, label in enumerate(labels):
        plan[label] += [class_of_year[i]]
        data.at[class_of_year[i][3] - 1, "Tischnummer"] = label
        cap[label] -= 1
    for other_pers in other:
        for label in Tischlabels:
            if cap[label] > 0:
                plan[label] += [other_pers]
                data.at[other_pers[3] - 1, "Tischnummer"] = label
                cap[label] -= 1
                break
    # pprint(plan)
    print(data)
    return plan
    # for tisch in Tischlabels:


def random_number(groups=16, column_="Nummer 1.Runde"):
    group_cap = [6 for _ in range(16)]
    group_labels = ["Gruppe " + str(i) for i in range(1, 17)]
    # iterate of df and add nummer 1.Runde
    for index, row in data.iterrows():
        if row["teilnahme"] == "Ja":
            while True:
                rand_group = np.random.randint(1, 17)
                if group_cap[rand_group - 1] > 0:
                    group_cap[rand_group - 1] -= 1
                    data.at[index, column_] = int(rand_group)
                    break
    assert data[column_].isnull().sum() == 0


random_tischeinteilung()
random_number(column_="Nummer 1.Runde")
random_number(column_="Nummer 2.Runde")
random_number(column_="Nummer 3.Runde")
print(data)
# save data back
data.to_csv("1. Concentric Circles out 2023_csv.csv", sep=";", index=False)
