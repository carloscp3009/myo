'''
    Utilidades
'''


def save_data_file(data, path):
    '''
      Guardar un array de datos en un archivo .txt
    '''
    from io import open
    with open(path, 'a') as f:

        for row in data:
            line = str(row[0])
            for el in row[1:]:
                line += ',' + str(el)

            f.write(line.decode('utf-8') + '\n')

    f.close()
