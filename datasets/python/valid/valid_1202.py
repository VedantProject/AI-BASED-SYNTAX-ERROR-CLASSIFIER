def build_scores(names, values):
    return {name: val for name, val in zip(names, values)}

names = ["alice", "bob", "carol"]
vals  = [46, 35, 81]
scores = build_scores(names, vals)
print(scores)
