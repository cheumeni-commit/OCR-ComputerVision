

def saveDataForCsvPoster(data, nameImage,*, path):
    '''
    :param nameFile: fichier de sortie des donnees (.csv)
    :param data: donnees a stocker dans le fichier
    :return:
    '''
    with open(path, 'a') as fp:
        for name in nameImage:
            fp.write((str(name) + ';'))
            for i in range(len(data[name])):
                if i < len(data[name])-1:
                    fp.write((str(data[name][i])+';'))
                else:
                    fp.write(str(data[name][i]))
            fp.write('\n')


def saveDataForCsvForm(data, *, path):
    '''
    :param nameFile: fichier de sortie des donnees (.csv)
    :param data: donnees a stocker dans le fichier
    :return:
    '''
    with open(path, 'a') as fp:
        fp.write((str(0) + ';'))
        for i in range(len(data)):
            if i < len(data) -1:
                fp.write((str(data[i])+';'))
            else:
                fp.write(str(data[i]))
        fp.write('\n')