# Напишите программу обработки папки "Хлам", которая сортирует файлы в указанной папке по расширениям
# с использованием нескольких потоков. Ускорьте обработку больших каталогов с большим количеством вложенных папок и файлов,
# за счет параллельного выполнения обхода всех папок в отдельных потоках. Наиболее затратным по времени будет перенос файла
# и получение списка файлов в папке (итерация по содержимому каталога). Чтобы ускорить перенос файлов, его можно выполнять
# в отдельном потоке или пуле потоков. Это тем более удобно, что результат этой операции вы в приложении не обрабатываете
# и можно не собирать никакие результаты. Чтобы ускорить обход содержимого каталога с несколькими уровнями вложенности,
# вы можете обработку каждого подкаталога выполнять в отдельном потоке или передавать обработку в пул потоков.

import threading 
# from threading import Thread#thread

import time
# from time import time, sleep #thread
import logging #thread

# import concurrent.futures
from random import randint


from pathlib import Path, PurePath
import shutil
import sys
# import clean_folder.file_parser as parser
# from clean_folder.normalize import normalize

import file_parser as parser
from normalize import normalize



def handle_other(filename: Path, target_folder: Path):
   
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))
   
  
def handle_media(filename: Path, target_folder: Path):

    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

#-----------------------------------------------------
       
def handle_documents(filename:Path, target_folder:Path): # THREADS
    
    logging.info("Thread %s: starting", filename)#  
    
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

       
    time.sleep(3)
    logging.info("Thread %s: finishing", filename)
   
#-------------------------------------------------------


def handle_archive(filename: Path, target_folder: Path):
    # Создаем папку для архивов
    target_folder.mkdir(exist_ok=True, parents=True)
    #  Создаем папку куда распаковываем архив

    # Берем суффикс у файла и убираем replace(filename.suffix, '')
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))

    #  создаем папку для архива с именем файла

    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Это не архив {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Не удалось удалить папку {folder}')
   

def main(folder: Path):
    parser.scan(folder)

   
    for file in parser.JPEG_IMAGES:
        # pathjoin(str(folder), 'images', 'JPEG')
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')

    for file in parser.OTHER:
        handle_other(file, folder / 'OTHER')
    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')

    for file in parser.AVI_VIDEO:
        handle_media(file, folder/'video'/'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder/'video'/'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder/'video'/'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder/'video'/'MKV')

    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')

    for file in parser.DOC_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'XLSX')
    for file in parser.PPTX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'PPTX')

    for file in parser.GZ_ARCHIVES:
        handle_archive(file, folder / 'GZ_archives')
    for file in parser.TAR_ARCHIVES:
        handle_archive(file, folder / 'TAR_archives')

    # Выполняем реверс списка для того, чтобы все папки удалить.
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def start():
    
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())



if __name__ == '__main__':

    format = "%(asctime)s: %(message)s" # THREADS
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=start, args=())
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    x.join()
    logging.info("Main    : all done") # THREADS
    
   
     