def build_scores(names, values):
    return {name: val for name, val in zip(names, values)}

names = ["alice", "bob", "carol"]
vals  = [2, 6, 8]
scores = build_scores(names, vals)
print(scores)
