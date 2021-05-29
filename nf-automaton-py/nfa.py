def dfs(node, letter_idx):
    global steps, finish, target_word, found
    if node in finish and letter_idx == len(target_word):
        found = True
        return None
    if node in steps and letter_idx < len(target_word):
        for pair in steps[node]:
            if target_word[letter_idx] in pair[1]:
                dfs(pair[0], letter_idx + 1)


info_file = open("nfa.txt", 'r')
start = info_file.readline().split('\n')[0]
finish = set(info_file.readline().split())
found = False
steps = {}
for line in info_file.readlines():
    data = line.split()
    if data[0] not in steps:
        steps[data[0]] = []
    steps[data[0]].append((data[1], set(data[2:])))
target_word = input()
dfs(start, 0)
print(found)
