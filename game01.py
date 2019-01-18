#!/usr/bin/python3
import re
import sys
import base64

cmdIn=base64.b64decode(sys.argv[1].encode()).decode()
correct = [False for i in range(5)]

#rule 1
#at least one misspelled word
for word in re.findall(r"([a-z]+)",cmdIn,re.I):
    invalid = True
    with open("/usr/share/dict/web2") as f:
        for check in f:
            if word.lower() in check.lower():
                invalid = False
                break
    if invalid:
        correct[0] = True
        break

#rule 2
#even number of words
correct[1] = (len(cmdIn.split(" ")) % 2) == 0

#rule 3
#reference the bouncer
correct[2] = bool(re.search(r"(you|bounce[r])",cmdIn,re.I))

#rule 4
#remain under 140 characters, fit it in a tweet
correct[3] = len(cmdIn) <= 140

#rule 5
#use two commas
correct[4] = cmdIn.count(",") == 2

out = ""
outList = ["**Rule {0}**".format(i+1) for i in range(5) if correct[i]]
if len(outList) == 0:
    out = "**No Rules**"
elif len(outList) == 1:
    out = outList[0]
else:
    out = ", ".join(outList[:-1])
    out += " and " + outList[-1]
print("Passes {0}".format(out))

