#! python3
# coding=utf-8

from tkinter import *
import zipfile
import os

version = '1.0'

def readNameInFileIOS(zipFile):
    name_list = zipFile.namelist()
    pattern = re.compile(r'Payload/[^/]*.app/.*.mobileprovision') #mobileprovision
    for orginPath in name_list:
        path = orginPath.encode('cp437').decode('GBK')
        m = pattern.match(path)
        if m is not None:
            data = zipFile.read(orginPath)
            data = str(data)
            rex = re.compile(r'application-identifier</key>\\n\\t\\t<string>.+?</string>\\n\\t\\t<key>com.apple.developer')
            r = rex.search(data)
            if r is not None:
                result = r.group()
                result = result[42:-39]
                print(result)
                return result
            return 'Not Found'

def readNameInFileAndroid(apkPath):

    appPackageAdb = os.popen('aapt dump badging ' + apkPath,'r') #aapt
    try:
        appPackageAdb = appPackageAdb.readline()
        rex = re.compile(r'name=.*versionCode=')
        result = rex.search(appPackageAdb)
        if result is None:
            return 'Not found'
        result = result.group()
        result = result[6:-14]
        print(result)
        return result
    except:
        return 'Not Found'

def readNameInFile(filename):
    print(filename)

    file = zipfile.ZipFile(filename)
    ext = os.path.splitext(filename)[1]
    if ext == '.ipa':
        return readNameInFileIOS(file);
    elif ext == '.apk':
        return readNameInFileAndroid(filename);
    return 'Invalid File'
    


def chooseClicked():
    packageContent.set('')
    filename = filedialog.askopenfilenames()
    pathContent.set(filename)

    result = readNameInFile(filename[0])
    packageContent.set(result)
    pass


uiRoot = Tk()
uiRoot.geometry('400x180')
uiRoot.title("PACKAGE NAME READER v%s" % (version,))

frameL = Frame(uiRoot)
btn = Button(frameL,text="choose your apk/ipa file",command=chooseClicked)
btn.pack()

pathContent = StringVar()
pathText = Entry(frameL,width = 54, textvariable = pathContent,state='readonly') 
pathText.pack(side=TOP,pady=10)

lb = Label(frameL,text = 'Package/Bundle ID：')
lb.pack(side=TOP,pady=10)

packageContent = StringVar()
packageText = Entry(frameL,width = 30, textvariable = packageContent,state='readonly') 
packageText.pack(side=TOP)

frameL.pack(side=TOP, pady=20)

uiRoot.mainloop()