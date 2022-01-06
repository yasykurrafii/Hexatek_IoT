button = {}
with open('button.txt', 'r') as f:
    button_name = []
    new = True
    ip = ""
    for x in f:
        x = x.split(':')
        if new:
            key = x[0][:-1]
            button[key] = []
            ip = key
            new = False
        else:
            if x[-1][-1] == '\n':
                name = x[-1][:-1]
            else:
                name = x[-1]
            button[ip].append(name)
        if len(x) == 1 and x[0] == '\n':
            new = True
for x in button.keys():
    button[x] = button[x][:6]
print(button)