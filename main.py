import pandas as pd
import sys

#sys.argv

KEY = 'fn'
BASE_NAMES = ['fn', 'name']
GRADE_NAMES = ['fn', 'grade']

def load_grade_table(file):
    grade_db = pd.read_excel(file)
    grade_db = grade_db.dropna().astype({KEY: 'str'})
    grade_db[KEY] = grade_db[KEY].str[-5:]
    grade_db = grade_db[grade_db[KEY].str.match('\d\d\d\d\d')]
    grade_db = grade_db.astype({KEY: 'int64'}).set_index(KEY)
    
    return grade_db

if (len(sys.argv) < 2):
    raise Exception("Wrong number of arguments!")

grade_db = load_grade_table(sys.argv[1])
grade_db['grade_1'] = grade_db['grade']

i = 2
while (i < len(sys.argv)):
    grade_db_temp = load_grade_table(sys.argv[i])
    grade_db = grade_db.join(grade_db_temp, rsuffix='_' + str(i))
    grade_db['grade'] += grade_db['grade_' + str(i)]
    i = i + 1

grade_db['grade'] /= i - 1
grade_db['grade'] += 2

base_db = pd.read_excel('databases/base.xlsx')
base_db[KEY] = base_db[KEY].str[-5:]
base_db = base_db.astype({KEY: 'int64'}).set_index(KEY)


combined_db = base_db.join(grade_db)
combined_db = combined_db.sort_values(by=["grade"], ascending=False)

combined_db = combined_db.reset_index().drop(KEY, axis=1)

print(combined_db.head(15))


