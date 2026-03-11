def build_scores(names, values):
    return {name: val for name, val in zip(names, values)}

names = ["alice", "bob", "carol"]
vals  = [24, 21, 45]
scores = build_scores(names, vals)
print(scores)
