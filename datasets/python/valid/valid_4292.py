def build_scores(names, values):
    return {name: val for name, val in zip(names, values)}

names = ["alice", "bob", "carol"]
vals  = [22, 45, 67]
scores = build_scores(names, vals)
print(scores)
