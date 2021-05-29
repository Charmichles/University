def dfs(node, letter_idx):
    global steps, finish, target_word, found
    if node in finish and letter_idx == len(target_word):
        found = True
        return None
    if node in steps and letter_idx < len(target_word):
        for pair in steps[node]:
            if target_word[letter_idx] in pair[1]:
                dfs(pair[0], letter_idx + 1)

info_file = open("gramatica.txt", 'r')
steps = {}
finish = set()
for line in info_file.readlines():
    data = line.split()
    if data[0] not in steps:
        steps[data[0]] = []
    if data[1][-1].isupper():
        steps[data[0]].append((data[1][-1], data[1][:-1]))
    else:
        if data[1][0] != '~':
            steps[data[0]].append(('~', data[1][0]))
        else:
            finish.add(data[0])
finish.add('~')
print(steps, finish)
n = int(input("Nr. cuvinte = "))
while n:
    target_word = input("Cuvant = ")
    found = False
    dfs("S", 0)
    print(target_word, found)
    n -= 1
