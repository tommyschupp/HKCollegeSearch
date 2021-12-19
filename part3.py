import pandas
newList = pandas.read_csv(r'unsortedSchoolFinal.csv')
accreditorList = newList["Accreditor(s)"]

accreditorSingles = []

for value in accreditorList:
    value = str(value)
    value = value.replace('"', '')
    value = value.replace('[', '')
    value = value.replace(']', '')

    value = value.split("' , '")

    for accreditor in value:
        if accreditor not in accreditorSingles:
            accreditorSingles.append(accreditor)
            print(accreditor)

results = pandas.DataFrame(list(accreditorSingles), columns = ["Accreditor(s)"])
results.to_csv(r'accreditorList.csv', index=False, header=True)
