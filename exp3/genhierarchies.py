import pandas as pd


hierarchies_prefix = 'data/hierarchies_gen/adult_hierarchy_'

# 这个函数是自己生成的层级

def gen_hierarchies(df, name):
    filename = hierarchies_prefix + name + '.csv'
    data = df[name]
    max_val = data.max()
    min_val = data.min()
    median = int((max_val - min_val) / 2.0)
    lines = []
    memo = {}
    for line in data:
        if line < median:
            cur = f'{line};{min_val}~{median};*\n'
            if cur in memo:
                continue
            lines.append(cur)
            memo[cur] = True
        else:
            cur = f'{line};{median}~{max_val};*\n'
            if cur in memo:
                continue
            lines.append(cur)
            memo[cur] = True

    with open(filename, 'w') as f:
        f.writelines(lines)


x = pd.read_csv('./data/adult.csv', delimiter=';')
gen_hierarchies(x, 'fnlwgt')
gen_hierarchies(x, 'education-num')
gen_hierarchies(x, 'capital-gain')
gen_hierarchies(x, 'capital-loss')
gen_hierarchies(x, 'hours-per-week')
