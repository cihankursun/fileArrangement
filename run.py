import time
import logging
import os
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
document_extensions = [".doc", ".docx", ".odt",".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
zip_extensions = [".zip",".rar"]
js_extensions = [".js"]

class MoverHandlerOwnPath(FileSystemEventHandler):
    def on_modified(self, event):
        currentFolder = os.getcwd()
        editedFileName = event.src_path.split(currentFolder+'\\')[1]
        with os.scandir(currentFolder) as entries:
            for entry in entries:
                if(editedFileName == entry.name):
                    name = entry.name
                    self.check_js_files(currentFolder,entry,name)
                    self.check_video_files(currentFolder,entry, name)
                    self.check_image_files(currentFolder,entry, name)
                    self.check_document_files(currentFolder,entry, name)
                    self.check_zip_files(currentFolder,entry,name)

    def make_unique(self,path,dest):
        filename, extension = os.path.splitext(path)
        filename = filename.split('\\')[len(filename.split('\\'))-1]
        counter = 1
        while True:
            if not os.path.exists(f"{dest}\\{filename}({counter}){extension}"):
                filename = f"{filename}({counter}){extension}"
                break
            else: 
                counter += 1
        return filename

    def move_file(self,dest, entry, name):
        global dumpName,uniqueDumpName
        dumpName = name
        currPath = os.getcwd()
        try:
            if os.path.exists(f"{dest}\\{name}"):
                unique_name = self.make_unique(currPath+'\\'+name,dest)
                newName = os.path.join(dest+'\\',unique_name)
                move(currPath+'\\'+name,newName)
            else:
                try:
                    if name.index(" ") > 0:
                        dumpName = name.replace(" ","_",name.count(" "))
                except ValueError as ve:
                    pass
                if os.path.exists(f"{dest}\\{dumpName}"):
                    uniqueDumpNameArr = self.make_unique(currPath+'\\'+dumpName,dest)
                    uniqueDumpName = uniqueDumpNameArr.split("\\")[len(uniqueDumpNameArr.split("\\"))-1]
                else:
                    uniqueDumpName = dumpName
                srcName = os.path.join(currPath+'\\',name)
                newName = os.path.join(dest+'\\',uniqueDumpName)
                move(srcName,newName)
        except FileNotFoundError as fe:
            #print(fe)
            pass
        except PermissionError as pe:
            #print(pe)
            pass
        
    def check_js_files(self, currentFolder, entry, name): 
        for js_extension in js_extensions:
            if name.endswith(js_extension) or name.endswith(js_extension.upper()):
                self.move_file(currentFolder+'\\js_files', entry, name)
                logging.info(f"Moved js file: {name} to js_files folder")

    def check_video_files(self, currentFolder, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                self.move_file(currentFolder+'\\video_files', entry, name)
                logging.info(f"Moved video file: {name} to {currentFolder}\\video_files folder")

    def check_image_files(self, currentFolder, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                self.move_file(currentFolder+'\\images_files', entry, name)
                logging.info(f"Moved image file: {name} to {currentFolder}\\images_files folder")

    def check_document_files(self, currentFolder, entry, name):
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                self.move_file(currentFolder+'\\documents_files', entry, name)
                logging.info(f"Moved document file: {name} to {currentFolder}\\documents_files folder")

    def check_zip_files(self, currentFolder, entry,name):
        for zip_extension in zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                self.move_file(currentFolder+'\\zip_files', entry, name)
                logging.info(f"Moved document file: {name} to {currentFolder}\\zip_files folder")

class MoverHandlerCustomPath(FileSystemEventHandler):
    def on_modified(self, event):
        crFlArr = event.src_path.split("\\")
        crFlArr.remove(crFlArr[len(crFlArr)-1])
        currentFolder = "\\".join(crFlArr)
        editedFileName = event.src_path.split(currentFolder+'\\')[1]
        with os.scandir(currentFolder) as entries:
            for entry in entries:
                #if(editedFileName == entry.name):
                name = entry.name
                self.check_js_files(currentFolder,entry,name)
                self.check_video_files(currentFolder,entry, name)
                self.check_image_files(currentFolder,entry, name)
                self.check_document_files(currentFolder,entry, name)
                self.check_zip_files(currentFolder,entry,name)

    def make_unique(self,path,dest):
        filename, extension = os.path.splitext(path)
        filename = filename.split('\\')[len(filename.split('\\'))-1]
        counter = 1
        while True:
            if not os.path.exists(f"{dest}\\{filename}({counter}){extension}"):
                filename = f"{filename}({counter}){extension}"
                break
            else: 
                counter += 1
        return filename

    def move_file(self,dest, entry, name):
        global dumpName,uniqueDumpName
        dumpName = name
        crFlArr = dest.split("\\")
        crFlArr.remove(crFlArr[len(crFlArr)-1])
        currPath = "\\".join(crFlArr)
        try:
            if os.path.exists(f"{dest}\\{name}"):
                unique_name = self.make_unique(currPath+'\\'+name,dest)
                newName = os.path.join(dest+'\\',unique_name)
                move(currPath+'\\'+name,newName)
            else:
                try:
                    if name.index(" ") > 0:
                        dumpName = name.replace(" ","_",name.count(" "))
                except ValueError as ve:
                    pass
                if os.path.exists(f"{dest}\\{dumpName}"):
                    uniqueDumpNameArr = self.make_unique(currPath+'\\'+dumpName,dest)
                    uniqueDumpName = uniqueDumpNameArr.split("\\")[len(uniqueDumpNameArr.split("\\"))-1]
                else:
                    uniqueDumpName = dumpName
                srcName = os.path.join(currPath+'\\',name)
                newName = os.path.join(dest+'\\',uniqueDumpName)
                move(srcName,newName)
        except FileNotFoundError as fe:
            #print(fe)
            pass
        except PermissionError as pe:
            #print(pe)
            pass
        
    def check_js_files(self, currentFolder, entry, name): 
        for js_extension in js_extensions:
            if name.endswith(js_extension) or name.endswith(js_extension.upper()):
                self.move_file(currentFolder+'\\js_files', entry, name)
                logging.info(f"Moved js file: {name} to js_files folder")

    def check_video_files(self, currentFolder, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                self.move_file(currentFolder+'\\video_files', entry, name)
                logging.info(f"Moved video file: {name} to {currentFolder}\\video_files folder")

    def check_image_files(self, currentFolder, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                self.move_file(currentFolder+'\\images_files', entry, name)
                logging.info(f"Moved image file: {name} to {currentFolder}\\images_files folder")

    def check_document_files(self, currentFolder, entry, name):
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                self.move_file(currentFolder+'\\documents_files', entry, name)
                logging.info(f"Moved document file: {name} to {currentFolder}\\documents_files folder")

    def check_zip_files(self, currentFolder, entry,name):
        for zip_extension in zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                self.move_file(currentFolder+'\\zip_files', entry, name)
                logging.info(f"Moved document file: {name} to {currentFolder}\\zip_files folder")

if __name__ == "__main__":
    path = ""
    try:
        userSelection = int(input("Enter 0 for your own path, 1 for given path to arrange: "))
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        observer = Observer()
        if userSelection == 0:
            if not os.path.exists('js_files'):
                os.makedirs('js_files')
            if not os.path.exists('video_files'):
                os.makedirs('video_files')
            if not os.path.exists('documents_files'):
                os.makedirs('documents_files')
            if not os.path.exists('images_files'):
                os.makedirs('images_files')
            if not os.path.exists('zip_files'):
                os.makedirs('zip_files')
            path = os.getcwd()
            logging.info("{} path is being listened...".format(path))
            event_handler = MoverHandlerOwnPath()
            observer.schedule(event_handler,path,recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(10)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
        elif userSelection == 1:
            print(r"Example: C:\Users\User\Desktop\folder")
            path = input("Please give your full path: ")
            if not os.path.exists(path+'\\js_files'):
                os.makedirs(path+'\\js_files')
            if not os.path.exists(path+'\\video_files'):
                os.makedirs(path+'\\video_files')
            if not os.path.exists(path+'\\documents_files'):
                os.makedirs(path+'\\documents_files')
            if not os.path.exists(path+'\\images_files'):
                os.makedirs(path+'\\images_files')
            if not os.path.exists(path+'\\zip_files'):
                os.makedirs(path+'\\zip_files')
            logging.info("{} path is being listened...".format(path))
            event_handler = MoverHandlerCustomPath()
            observer.schedule(event_handler,path,recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(10)
            except KeyboardInterrupt:
                observer.stop()
            
            observer.join()
        else:
            logging.info("Only 0 and 1 are choosen")
            quit()
    except ValueError as ve:
        logging.info("Error: {}, only integer values are given".format(ve))
        quit()
    
    
    
    