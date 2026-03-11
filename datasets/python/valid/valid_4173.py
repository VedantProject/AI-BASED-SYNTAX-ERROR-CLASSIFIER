def build_scores(names, values):
    return {name: val for name, val in zip(names, values)}

names = ["alice", "bob", "carol"]
vals  = [33, 25, 58]
scores = build_scores(names, vals)
print(scores)
