from __future__ import division
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import glob
import random


# image sizes for the examples
SIZE = 256, 256
# regex for graphics file format
FILES_FORMAT_REGEX = '*.[JjPp]*[Gg]'


class LabelTool:
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("Generador de Reporte en Carpeta")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=False, height=False)
        

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.save_to_yolo_format = IntVar()
        self.entry_text = StringVar()
        self.entry_text2 = StringVar()
        self.entry_text3 = StringVar()
        self.entry_text4 = StringVar()
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.imagepath = ''
        self.labelname = ''
        self.labelfilename = ''
        self.file_will_not_remove = True
        self.tkimg = None
        self.folder = ''
        self.currentLabelclass = ''
        self.cla_can_temp_Clase = []
        self.cla_can_temp_Tipo = []
        self.cla_can_temp_Cardinal = []
        self.classcandidate_filename_Clase = 'Clase.txt'
        self.classcandidate_filename_Tipo = 'Tipo.txt'
        self.classcandidate_filename_Cardinal = 'Cardinal.txt'
        self.cls = 0

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0


        
        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text="Carpeta de Archivos:")
        self.label.grid(row=0, column=0, sticky=E)
        self.entry = Entry(self.frame, textvariable=self.entry_text)
        self.entry.grid(row=0, column=1, sticky=W+E)
        self.ldBtn = Button(self.frame, text="Buscar Carpeta", command=self.loadDir)
        self.ldBtn.grid(row=0, column=2, sticky=W+E)
        
        
        
        self.ConfigPanel=Frame(self.frame)
        self.ConfigPanel.grid(row = 2, column = 3, columnspan = 5, sticky = W)
        #Calle
        self.label = Label(self.ConfigPanel, text="Calle:")
        self.label.grid(row=2, column=2, sticky=E,padx = 5, pady = 10)
        self.entry_Calle = Entry(self.ConfigPanel, textvariable=self.entry_text2)
        self.entry_Calle.grid(row=2, column=3, sticky=W+E,padx = 5, pady = 10)
        #Carrera
        self.label = Label(self.ConfigPanel, text="Carrera:")
        self.label.grid(row=4, column=2, sticky=E,padx = 5, pady = 10)
        self.entry_Carrera = Entry(self.ConfigPanel, textvariable=self.entry_text3)
        self.entry_Carrera.grid(row=4, column=3, sticky=W+E,padx = 5, pady = 10)
        
        
        # Tipo de aforo
        self.label = Label(self.ConfigPanel, text="Tipo de línea de aforo:")
        self.label.grid(row=6, column=2, sticky=E+N,padx = 5, pady = 10)
        self.entry_Linea = Entry(self.ConfigPanel, textvariable=self.entry_text4)
        self.entry_Linea.grid(row=6, column=3, sticky=W+E+N,padx = 5, pady = 10)
#        self.ldBtn = Button(self.frame, text="Asignar", command=self.loadDir)
#        self.ldBtn.grid(row=1, column=5, sticky=W+E)


        # Acceso o salida
        self.classname_label = Label(self.ConfigPanel, text = 'Tipo de Conteo:')
        self.classname_label.grid(row=8,column =2, sticky=E+S,padx = 5, pady = 10)
        self.classcandidate_Type = ttk.Combobox(self.ConfigPanel, state='readonly')
        self.classcandidate_Type.grid(row=8, column=3, sticky=W+E+S,padx = 5, pady = 10)
        if os.path.exists(self.classcandidate_filename_Tipo):
            with open(self.classcandidate_filename_Tipo) as cf:
                for line in cf.readlines():
                    # print line
                    self.cla_can_temp_Tipo.append(line.strip('\n'))
        # print self.cla_can_temp
        self.classcandidate_Type['values'] = self.cla_can_temp_Tipo
        self.classcandidate_Type.bind("<<ComboboxSelected>>", self.setType)
        # self.btnclass = Button(self.frame, text='ComfirmClass', command=self.setClass)
        # self.btnclass.grid(row=2, column=2, sticky=W + E)


        

        # Clase a aforar
        self.classname_label = Label(self.ConfigPanel, text = 'Clase a aforar:')
        self.classname_label.grid(row=10,column =2, sticky=E,padx = 5, pady = 10)
        self.classcandidate_Class = ttk.Combobox(self.ConfigPanel, state='readonly')
        self.classcandidate_Class.grid(row=10, column=3, sticky=W+E,padx = 5, pady = 10)
        if os.path.exists(self.classcandidate_filename_Clase):
            with open(self.classcandidate_filename_Clase) as cf:
                for line in cf.readlines():
                    # print line
                    self.cla_can_temp_Clase.append(line.strip('\n'))
        # print self.cla_can_temp
        self.classcandidate_Class['values'] = self.cla_can_temp_Clase
        self.classcandidate_Class.bind("<<ComboboxSelected>>", self.setClass)
        # self.btnclass = Button(self.frame, text='ComfirmClass', command=self.setClass)
        # self.btnclass.grid(row=2, column=2, sticky=W + E)


        # Punto Cardinal
        self.classname_label = Label(self.ConfigPanel, text = 'Punto Cardinal:')
        self.classname_label.grid(row=12,column =2, sticky=E,padx = 5, pady = 10)
        self.classcandidate_Cardinal = ttk.Combobox(self.ConfigPanel, state='readonly')
        self.classcandidate_Cardinal.grid(row=12, column=3, sticky=W+E,padx = 5, pady = 10)
        if os.path.exists(self.classcandidate_filename_Cardinal):
            with open(self.classcandidate_filename_Cardinal) as cf:
                for line in cf.readlines():
                    # print line
                    self.cla_can_temp_Cardinal.append(line.strip('\n'))
        # print self.cla_can_temp
        self.classcandidate_Cardinal['values'] = self.cla_can_temp_Cardinal
        self.classcandidate_Cardinal.bind("<<ComboboxSelected>>", self.setCoord)
        # self.btnclass = Button(self.frame, text='ComfirmClass', command=self.setClass)
        # self.btnclass.grid(row=2, column=2, sticky=W + E)


     
        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')

        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 1, column= 1, rowspan = 4, sticky = W+S)


        self.info_box_ctr_panel = Frame(self.frame)
        self.info_box_ctr_panel.grid(row=4, column=1, sticky=W+E+S)
        self.info_box = Text(self.info_box_ctr_panel, height=14)
        self.info_box.pack(side=LEFT, fill=Y)
          
        
        



        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 5, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)
        self.btnRm = Button(self.ctrPanel, text='Guardar Configuración', command=self.Set_Settings)
        self.btnRm.pack(side = LEFT, padx = 25, pady = 3)
     


        # example pannel for illustration
        self.egPanel = Frame(self.frame, border = 10)
        self.egPanel.grid(row = 1, column = 0, rowspan = 5, sticky = N)
        self.tmpLabel2 = Label(self.egPanel, text = "Convención de aforos:")
        self.tmpLabel2.pack(side = TOP, pady = 5)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(Label(self.egPanel))
            self.egLabels[-1].pack(side = TOP)

        # display mouse position
#        self.disp = Label(self.ctrPanel, text='')
#        self.disp.pack(side = RIGHT)
        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

    def loadDir(self):
        folder = filedialog.askdirectory()
        self.imageDir = folder + os.sep
        self.entry_text.set(self.imageDir)
        # get image list
        self.imageList = glob.glob(os.path.join(self.imageDir, FILES_FORMAT_REGEX))
        
        print (self.imageList)
        if len(self.imageList) == 0:
            self.print_log('Files .jpg or .png NOT FOUND in the specified dir!')
            return
        if not len(self.imageList) == 0:
            Lineas_de_conteo_halladas="Se encontraron "+ str(len(self.imageList)) +" líneas de conteo" 
            
            self.print_log(Lineas_de_conteo_halladas)
            
        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

         
        # load example bboxes
        self.egDir = os.path.join(r'./Examples')
        if not os.path.exists(self.egDir):
            return
        filelist = glob.glob(os.path.join(self.egDir, FILES_FORMAT_REGEX))
        self.tmp = []
        self.egList = []
        random.shuffle(filelist)
        for (i, f) in enumerate(filelist):
            if i == 1:
                break
            im = Image.open(f)
            r = min(SIZE[0] / im.size[0], SIZE[1] / im.size[1])
            new_size = int(r * im.size[0]), int(r * im.size[1])
            self.tmp.append(im.resize(new_size, Image.ANTIALIAS))
            self.egList.append(ImageTk.PhotoImage(self.tmp[-1]))
            self.egLabels[i].config(image = self.egList[-1], width = SIZE[0], height = SIZE[1])
        self.loadImage()
        #self.print_log(str(self.total) + ' images loaded from ' + self.imageDir)

    def loadImage(self):
        # load image
        basewidth = 900
        self.imagepath = self.imageList[self.cur - 1]
        self.entry_text.set(self.imagepath)
        self.img = Image.open(self.imagepath)
        wpercent = (basewidth/float(self.img.size[0]))
        hsize = int((float(self.img.size[1])*float(wpercent)))
        img = self.img.resize((basewidth,hsize), Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(img)
        self.mainPanel.config(width = max(self.tkimg.width(), basewidth), height = max(self.tkimg.height(), basewidth))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

        
    def prevImage(self, event = None):

        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):

        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        elif self.cur == self.total:
            self.create_images_list()           
            messagebox.showinfo("Done", "That's All!")

    #remove picture
    def Set_Settings(self):
        if messagebox.askyesno("Guardar configuracion", "¿Está Seguro?"):
            message='La configuración de la linea de conteo '+ str(self.cur)+' ha sido almacenada correctamente'
            self.print_log(message)
            print("Carrera: ",self.entry_text2.get())
            print("Calle: ",self.entry_text3.get())
            print("Clase de Aforo: ", self.entry_text4.get())
            print("Actor Vial: ",self.classcandidate_Class.get())
            print("Tipo de vía: ",self.classcandidate_Type.get())
            print("Referencia Cardinal: ",self.classcandidate_Cardinal.get())
                
                


    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:

            self.cur = idx
            self.loadImage()

    def print_log(self, msg):
        self.info_box.insert(END, msg + '\n')
    
    
    def setClass(self, event):
        self.currentLabelclass = self.classcandidate_Class.get()
        print('set label class to : %s', self.currentLabelclass)
        
    def setType(self, event):
        self.currentLabelclass = self.classcandidate_Type.get()
        print('set label Type to : %s', self.currentLabelclass)
        
    def setCoord(self, event):
        self.currentLabelclass = self.classcandidate_Cardinal.get()
        print('set label Coordinate to : %s', self.currentLabelclass)


    def create_images_list(self):
         with open(self.imageDir + 'images_list.txt', 'w') as inFile:
             for im in self.imageList:
                inFile.write(im+'\n')
             

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width = True, height = True)
    root.mainloop()
