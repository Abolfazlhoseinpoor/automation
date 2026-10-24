import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
import shutil

def create_folder():
    folder = input("lotfan esm folder ro vared konid: ")
    if folder == "":
        print("shoma esm folder ro vared nakardid!")
        return
    try:
        folder_name = Path(folder)
        if not folder_name.exists():
            folder_name.mkdir()
            print("folder mored nazar sakhte shod!")
        else:
            print("in folder az ghabl vojod dasht!")
    except PermissionError:
        print("shoma dastrasi be sakhtan file nadardid!")
        return

def create_file_in_folder():
    folder = input("lotfan esm folder ro vared konid: ")
    if folder == "":
        print("shoma esm folder ro vared nakardid!")
        return
    folder_name = Path(folder)
    if not folder_name.exists():
        print("hamchin folderi vojod nadarad!")
        return
    
    tedad_file = input("chnd ta file mikhahid dar folder mored nazar khod sakhte shavad?: ")
    if tedad_file == "":
        print("shoma maloom nakardid ke chnd file mikhahid besazid pass ma 1 done file dar nazar migirim!")
        tedad_file = 1
    
    try:
        tedad_file = int(tedad_file)
    except ValueError:
        print("lotfan tedad file ke mikhahid besazid ro be addad vared konid!")
        return

    
    for count in range(1, tedad_file + 1):
        file = input(f"lotfan esm file shomare {count} ro vared konid ba passvand.txt : ")
        if file == "":
            print(f"shoma esm file shomare {count} ro vared nakardid!")
            return
        if not file.endswith(".txt"):
            print("shoma passvand .txt ro faramosh kardid!")
            return
        
        file_name = folder_name / file
        try: 
            file_name.write_text("In yek log test ast", encoding="utf-8")
        except PermissionError:
            print("shoma dastrasi be sakhtan file nadardid!")
            return
            
    print("file ha sakhte shodan va matn dar har file zakhire shod!")

def show_file():
    folder = input("lotfan esm folder ro vared konid: ")
    if folder == "":
        print("shoma esm folder ro vared nakardid!")
        return
    folder_name = Path(folder)
    if not folder_name.exists():
        print("hamchin folderi vojod nadarad!")
        return
    
    file = input("lotfan esm file mored nazar khod ro vared konid ba passvand .txt: ")
    if file == "":
        print("shoma esm file ro vared nakardid!")
        return
    if not file.endswith(".txt"):
        print("passvand file ro faramosh kardid!")
        return
    
    file_path = folder_name / file
    
    if not file_path.exists():
        print("hamchin file dar in folder vojod nadarad!")
        return
    
    read_file = file_path.read_text(encoding="utf-8")
    if not read_file:
        print("file mored nazar khali ast!")
        return
    print(f"mohtavaye dakhel file mored nazar : \n{read_file}")

def copy_file():
    folder = input("lotfan esm folder ro vared konid: ")
    if folder == "":
        print("shoma esm folder ro vared nakardid!")
        return
    folder_name = Path(folder)
    if not folder_name.exists():
        print("hamchin folderi vojod nadarad!")
        return
    
    file = input("lotfan esm file mored nazar khod ro vared konid ba passvand .txt: ")
    if file == "": return
    if not file.endswith(".txt"):
        print("passvand file ro faramosh kardid!")
        return
    
    source_file = folder_name / file
    if not source_file.exists():
        print("file mabda (source) vojod nadarad!")
        return
        
    copy_name = input("lotfan esm file ke mikhahid copy bashad ro vared konid: ")
    if copy_name == "": return
    if not copy_name.endswith(".txt"):
        print("passvand file copy ro faramosh kardid!")
        return
        
    try:
        copy_file_name = folder_name / copy_name
        shutil.copy(source_file, copy_file_name)
        print("file mored nazar copy gerefte shod!")
    except PermissionError:
        print("shoma dastrasi be copy kardan file nadardid!")
        return

def show_list_file():
    folder = input("lotfan esm folder ro vared konid: ")
    if folder == "":
        print("shoma esm folder ro vared nakardid!")
        return
    folder_name = Path(folder)
    if not folder_name.exists():
        print("hamchin folderi vojod nadarad!")
        return
    
    list_file = list(folder_name.glob("*.txt"))
    if not list_file:
        print("dar in folder hich file .txt vojod nadarad!")
        return
    
    print(f"esm file hayi ke dar in folder vojod darad: {list_file}") 
while True:
    print("="*30)
    print("gozine 1 == sakhtan folder " 
          "\ngozine 2 == sakhtan file dar folder " 
          "\ngozine 3 == namayesh dakhel file mored nazar" 
          "\ngozine 4 == copy file " 
          "\ngozine 5 == namayesh file haye txt dar poshe mored nazar" 
          "\ngozine 6 == exit")
    print("="*30)
    
    choice = input("lotfan gozine mored nazar khod ro vared konid: ")
    
    if choice == "":
        print("shoma gozine ie ro entekhab nakardid!")
        continue
        
    if choice == "1":
        print("shoma gozine 1 ro entekhab kardid!")
        create_folder()
    elif choice == "2":
        print("shoma gozine 2 ro entekhab kardid!")
        create_file_in_folder()
    elif choice == "3":
        print("shoma gozine 3 ro entekhab kardid!")
        show_file()
    elif choice == "4":
        print("shoma gozine 4 ro entekhab kardid!")
        copy_file()
    elif choice == "5":
        print("shoma gozine 5 ro entekhab kardid!")
        show_list_file()
    elif choice == "6":
        print("shoma gozine 6 ro entekhab kardid va az barnam ekharej shodid!")
        break
    else:
        print("lotfan az gozine 1 ta 6 ro entekhab konid!")
        continue