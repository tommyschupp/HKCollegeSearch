import pandas
newList = pandas.read_csv(r'unsortedSchoolFinal.csv')
schoolList = newList["Accreditor(s)"]
fourYearList = pandas.read_csv(r'fourYear.csv')["Accreditor(s)"]
technicalList = pandas.read_csv(r'technical.csv', error_bad_lines=False)["Accreditor(s)"]
theologicalList = pandas.read_csv(r'theological.csv')["Accreditor(s)"]

fourYearSchools = []
technicalSchools = []
theologicalSchools = []

for index, school in newList.iterrows():
    for thing in fourYearList:
        thing=str(thing)
        if thing.replace(' ', '') in str(school['Metadata']).replace(' ', ''): 
            fourYearSchools.append(school)
            break
    for thing in technicalList:
        thing=str(thing)
        if thing.replace(' ', '') in str(school['Metadata']).replace(' ', ''):
            technicalSchools.append(school)
            break

    for thing in theologicalList:
        thing=str(thing)
        if thing.replace(' ', '') in str(school['Metadata']).replace(' ', ''):
            theologicalSchools.append(school)
            break

pandas.DataFrame(list(fourYearSchools)).to_csv(r'fourYearResults.csv', index=False, header=True)
pandas.DataFrame(list(technicalSchools)).to_csv(r'technicalResults.csv', index=False, header=True)
pandas.DataFrame(list(theologicalSchools)).to_csv(r'theologicalResults.csv', index=False, header=True)


