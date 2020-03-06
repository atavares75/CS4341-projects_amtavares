import ggplot

def scores_from_csv(file_path):
    datalist = []
    for file in file_list:
        datalist.append(pd.read_csv(file))

    return datalist