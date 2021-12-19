import pandas
newList = pandas.read_csv(r'accreditorList.csv')
accreditorList = newList["Accreditor(s)"]
dirtyList = []
cleanList = []
for accreditor in accreditorList:
    accreditor = str(accreditor)

    accreditor = accreditor.split("', '")


    for value in accreditor:
            value = value = str(value)
            value = value.replace("'", "")
            value = value.replace("(1)", "")
            value = value.replace("(2)", "")
            value = value.replace("(3)", "")
            dirtyList.append(value)

cleanList = [] 
[cleanList.append(x) for x in dirtyList if x not in cleanList]

results = pandas.DataFrame(list(cleanList), columns = ["Accreditor(s)"])
results.to_csv(r'accreditorList2.csv', index=False, header=True)
