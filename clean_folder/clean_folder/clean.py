import time
from pathlib import Path
import sys
import shutil

EXTENSIONS_DICT = {
    'images': ('.jpeg', '.png', '.jpg', '.svg', '.dng', '.bmp'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx', '.djvu', '.rtf', '.pub'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar'),
    'photoshop': ('.xmp', '.nef'),
    'books': ('.epub', '.fb2'),
    'other': ()
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
trans = {}

def main():

    global main_folder

    if len(sys.argv) < 2:
        print('Enter the path.')
        exit()
    
    current_folder = Path(sys.argv[1])

    if (not current_folder.exists()) or (not current_folder.is_dir()):
        print('Wrong path! ')
        exit()
    
    main_folder = current_folder
    
    to_translate()
    sort(current_folder)


def sort(iter_dirs: Path):

    for file in iter_dirs.iterdir():
        
        if file.name not in EXTENSIONS_DICT.keys() and file.is_dir():
            sort(file)
   
        elif file.is_file():
            change(file)
        
        if file.name not in EXTENSIONS_DICT.keys():
            try:
                if not any(file.iterdir()):
                    file.rmdir()
            
            finally:
                continue


def change(founded_file: Path):
        
    f_suffix = founded_file.suffix.lower()
    f_name = founded_file.stem

    for key, value in EXTENSIONS_DICT.items():
        
        if f_suffix in value:

            new_f_name = normalize(f_name)
            final_name = new_f_name + f_suffix
            end_folder = main_folder.joinpath(key)
            end_folder.mkdir(exist_ok=True)
            new_file_path = end_folder.joinpath(final_name)

            try:
                founded_file.rename(new_file_path)
            
            except FileExistsError:

                time_stamp = time.time()
                new_file_path = end_folder.joinpath(new_f_name + '_' + str(time_stamp) + f_suffix)
                founded_file.rename(new_file_path)

            except FileNotFoundError:
                continue
            
            if key == 'archives':

                base_archive_dir = end_folder.joinpath(new_f_name)
                base_archive_dir.mkdir(exist_ok=False)
                shutil.unpack_archive(new_file_path, base_archive_dir)

def normalize(correct_name: str) -> str:

    new_main_name = correct_name.translate(trans)

    for i in new_main_name:
        if not i.isdigit() or not i.isalpha() or i != '_':
            new_main_name = new_main_name.replace(i, '_')
    
        return new_main_name
        

def to_translate():

    for cyril, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans[ord(cyril)] = latin
        trans[ord(cyril.upper())] = latin.upper()


if __name__ == '__main__':
    main()
    print('Well done! ')
    exit()