import os

search_words = [
    'CovidVaccine'
    'pfizer',
    'SzczepionkaNarodowa',
    'programszczepien',
    'szczepienia',
    'NieSzczepimySię',
    'PfizerVaccine',
    'AstraZeneca',
    'szczepionkiprzeciwCOVID19',
    'szczepionkiAstraZeneca',
    'szczepionkę',
    'NarodowyProgramSzczepien',
    'Szczepionka',
    'narodowyprogramszczepien',
    'szczepionka',
    'szczepionką',
    'COVIDVaccine',
    'krotkiodstepmiedzydawkami',
    'COVID19Vaccine',
    'szczepimysię',
    'Szczepień',
    'moderna'
]

data_scrap_dir = 'data_from_scrap'
for since_date, until_date in [("2021-02-01", "2021-03-01")]:
    for query_word in search_words:
        print(f"Getting data with query: {query_word}, since date: {since_date}, until date: {until_date}")
        data_dir = f"data_from_scrap/{since_date}_{until_date}"

        try:
            os.makedirs(data_dir)
        except FileExistsError:
            # directory already exists
            pass

        data_file = f"{data_dir}/{query_word}.json"
        os.system(
            f'snscrape --jsonl --progress --since {since_date} twitter-search "{query_word} until:{until_date} lang:pl"> {data_file}')
