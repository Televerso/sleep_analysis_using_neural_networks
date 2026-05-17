import os


if __name__ == '__main__':
    os.system("python setup.py build --build-lib=./lib")
    os.system("python setup.py install")
