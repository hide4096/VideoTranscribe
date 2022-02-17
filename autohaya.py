import haya

def ReadURLtxt(name):
    with open(name) as i:
        for url in i:
            haya.ConvertYoutube2txt(url)

if __name__ == '__main__':
    name = input('filename:')
    ReadURLtxt(name)
    print('Completed')
