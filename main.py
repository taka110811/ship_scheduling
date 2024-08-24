from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus

# パラメータの設定（仮の値）
ports = ['P1', 'P2', 'P3', 'P4']
distances = {
    ('P1', 'P2'): 668, ('P1', 'P3'): 1035, ('P1', 'P4'): 1336,
    ('P2', 'P3'): 491, ('P2', 'P4'): 912,
    ('P3', 'P4'): 599
}
costs = {
    ('P1', 'P2'): 70500, ('P2', 'P1'): 70500,
    ('P1', 'P3'): 83500, ('P3', 'P1'): 83500,
    ('P1', 'P4'): 94000, ('P4', 'P1'): 94000,
    ('P2', 'P3'): 65000, ('P3', 'P2'): 65000,
    ('P2', 'P4'): 79500, ('P4', 'P2'): 79500,
    ('P3', 'P4'): 68500, ('P4', 'P3'): 68500
}
ship_capacity = {'S1': 5000, 'S2': 3000, 'S3': 3000, 'S4': 3000}
demand = {
    'P1': 10000, 'P2': 8000, 'P3': 12000, 'P4': 15000
}
supply = {
    'P1': 15000, 'P2': 15000, 'P3': 15000, 'P4': 15000
}

# モデルの初期化
model = LpProblem(name="ship_allocation", sense=LpMaximize)

# 決定変数の作成
x = LpVariable.dicts("x", [(i, j, k) for i in ports for j in ports if i != j for k in ship_capacity], lowBound=0, cat="Continuous")

# 目的関数の定義（総利益の最大化）
model += lpSum([x[i, j, k] * costs[i, j] for i in ports for j in ports if i != j for k in ship_capacity])

# 制約条件1: 各航路における貨物量は船の輸送能力を超えない
for k in ship_capacity:
    for i, j in distances:
        model += x[i, j, k] <= ship_capacity[k], f"capacity_{k}_{i}_{j}"

# 制約条件2: 各港の総出荷量がその港の供給を超えない
for i in ports:
    model += lpSum([x[i, j, k] for j in ports if i != j for k in ship_capacity]) <= supply[i], f"supply_limit_{i}"

# 制約条件3: 各港の総出荷量がその港の需要を満たす
for i in ports:
    model += lpSum([x[i, j, k] for j in ports if i != j for k in ship_capacity]) >= demand[i], f"demand_satisfied_{i}"

# 問題の解決
model.solve()

# 結果の出力
print(f"Status: {LpStatus[model.status]}")
for var in x.values():
    if var.varValue > 0:
        print(f"{var.name} = {var.varValue}")

print(f"Total Profit: {model.objective.value()}")
