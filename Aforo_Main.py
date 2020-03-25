from __future__ import division
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import glob
import random
from threading import Thread
import pickle
import ntpath

# image sizes for the examples
SIZE = 500 , 500
# regex for graphics file format
FILES_FORMAT_REGEX = '*.[JjPp]*[Gg]'
FILES_FORMAT_CSV = '*.[Cc][Ss][Vv]'

parallelo=0


class SumarDeA3:
    def __init__(self,archivoentrada,archivosalida):
        print("Generando Archivo recortado de a 15 min",archivoentrada, "Salida", archivosalida)
        
        fout=open(archivosalida,'w')
        
        with open(archivoentrada) as fp:
           line = fp.readline()
           fout.write(line)
           print ("depurando primera linea")
           while True:
               line1 = fp.readline()
               line2 = fp.readline()
               line3 = fp.readline()
               if not line1 or not line2 or not line3:
                   break
               segments1=line1.split(",")
               segments2=line2.split(",")
               segments3=line3.split(",")
               
               initowrite=segments1[0]+","+segments1[1]+","+segments1[2]+","+segments1[3]+","+segments1[4]+","+segments1[5]+","+segments1[6]
               
               peatones=str(int(segments1[7])+int(segments2[7])+int(segments3[7]))
               part=    str(int(segments1[8])+int(segments2[8])+int(segments3[8]))
               taxi=    str(int(segments1[9])+int(segments2[9])+int(segments3[9]))
               moto=   str(int(segments1[10])+int(segments2[10])+int(segments3[10]))
               bus=    str(int(segments1[11])+int(segments2[11])+int(segments3[11]))
               cam=    str(int(segments1[12])+int(segments2[12])+int(segments3[12]))
               mini=   str(int(segments1[13])+int(segments2[13])+int(segments3[13]))
               ci=     str(int(segments1[14])+int(segments2[14])+int(segments3[14]))
               tra=    str(int(segments1[15])+int(segments2[15])+int(segments3[15]))
               scoo=   str(int(segments1[16])+int(segments2[16])+int(segments3[16]))
               bici=   str(int(segments1[17])+int(segments2[17])+int(segments3[17]))
               
               linetowrite=initowrite+','+peatones+','+part+','+taxi+','+moto+','+bus+','+cam+','+mini+','+ci+','+tra+','+scoo+','+bici+'\n'
               fout.write(linetowrite)
        
               
        fout.close()
        print ("Archivo 15m creado")
        
               
               
               
               
        
        
class reporte:
    def __init__(self,folder,archivosalida):
        self.fl=open(folder+'/'+archivosalida,'w')
        self.nl='\n'
        self.first_time=True        
        
    def generar_reporte_linea(self,Via_Principal,Via_secundaria,Movimiento,Acceso,Salida,DD,MM,AAAA,periodo):    
        self.leyenda="FECHA,Calle,Carrera,Movimiento ,Acceso,Salida,Periodo,Peaton,Particular,Taxi,Motociclista,Bus,Camion,Minivan,Ciclista,Tractomula,Scooter,Bicitaxi,\n"
        self.periodo=str(periodo)
        self.Via_Principal=Via_Principal
        self.Via_secundaria=Via_secundaria
        self.Movimiento=Movimiento
        self.Acceso=Acceso
        self.Salida=Salida
        self.initlabel=str(DD)+str(MM)+str(AAAA)+','+str(self.Via_Principal)+','+str(self.Via_secundaria)+','+str(self.Movimiento)+','+str(self.Acceso)+','+str(self.Salida)+','+self.periodo+','
        # escribiendo leyenda en archivo si es la primera linea que se escribe en el mismo
        if self.first_time:
            self.fl.write(self.leyenda)
            self.first_time=False
        
    def cerrarArchivo(self):
        self.fl.close()
    
    def actualizarPeriodo(self,DD,MM,AAAA,periodo):
        self.periodo=str(periodo)
        self.initlabel=str(DD)+str(MM)+str(AAAA)+','+str(self.Via_Principal)+','+str(self.Via_secundaria)+','+str(self.Movimiento)+','+str(self.Acceso)+','+str(self.Salida)+','+self.periodo+','

    
    def agregarData(self,Data):
        if len(Data)==9:
            
            self.fl.write(self.initlabel)
            for i in range(9):
                self.fl.write(str(int(float(Data[i][1])))+',') # conteos por etiqueta
            self.fl.write(self.nl)
            
        elif len(Data)==11:
            
            self.fl.write(self.initlabel)
            for i in range(11):
                self.fl.write(str(int(float(Data[i][1])))+',') # conteos por etiqueta
            self.fl.write(self.nl)

        else:
            print (len(Data))
            print ("ERROR: el tamaño de los datos no es el adecuado")
            
def retornarNombreLinea(path,nombrevideo,numlinea,listnames):
    nombrevideo.rstrip()
    name=nombrevideo.split('.')[0]
    lineajpg=listnames[numlinea-1]
    linsplit=lineajpg.split("_")
    linname=path+'/'+name+'_'+linsplit[3]+'_'+linsplit[4][-5]+'.csv'
    if not os.path.isfile(linname):
        print ("***************************************ERROR el archivo "+linname+ "no existe, y se esperaba SALIENDO************************************")
    return linname
    
def getDataFromFile(filelin):
    fh=open(filelin,'r')
    countdata1=[]
    countdata2=[]
    countdata3=[]
    while True:
        # read line
        line = fh.readline()
        #print line
        if not line:
            print ("WARNING: saliendo por que se llego al final del archivo posible ERROR")
            break
        
        if line=="\n":
            #print "espacio en blanco detectado"
            continue
        if line.rstrip() == "AYUDA;manual  ; en ;https://docs.google.com/document/d/1Y2eYLjje2taNnJwVAONLIpsGVm4aj8_jssrNITejFd0/edit?usp=sharing":
            break
            #print "saliendo de archivo de manera correcta"
        if line.rstrip() =="Conteo definitivo;ambos sentidos":
            line = fh.readline().rstrip()
            for i in range (11):
                line = fh.readline().rstrip()
                countdata1.append(line.replace(',',';').split(';'))
        
        if line.rstrip() == "Conteo definitivo;direccion positiva":
            line = fh.readline().rstrip()
            for i in range (11):
                line = fh.readline().rstrip()
                countdata2.append(line.replace(',',';').split(';'))
        
        if line.rstrip() == "Conteo definitivo;direccion negativa":
            line = fh.readline().rstrip()
            for i in range (11):
                line = fh.readline().rstrip()
                countdata3.append(line.replace(',',';').split(';'))
    return countdata1,countdata2,countdata3
    
def getDataFromFile_old(filelin):
    fh=open(filelin,'r')
    countdata1=[]
    countdata2=[]
    countdata3=[]
    while True:
        # read line
        line = fh.readline()
        #print line
        if not line:
            print ("WARNING: saliendo por que se llego al final del archivo posible ERROR")
            break
        
        if line=="\n":
            #print "espacio en blanco detectado"
            continue
        if line.rstrip() == "AYUDA;manual  ; en ;https://docs.google.com/document/d/1Y2eYLjje2taNnJwVAONLIpsGVm4aj8_jssrNITejFd0/edit?usp=sharing":
            break
            #print "saliendo de archivo de manera correcta"
        if line.rstrip() =="Conteo definitivo;ambos sentidos":
            line = fh.readline().rstrip()
            for i in range (9):
                line = fh.readline().rstrip()
                countdata1.append(line.replace(',',';').split(';'))
        
        if line.rstrip() == "Conteo definitivo;direccion positiva":
            line = fh.readline().rstrip()
            for i in range (9):
                line = fh.readline().rstrip()
                countdata2.append(line.replace(',',';').split(';'))
        
        if line.rstrip() == "Conteo definitivo;direccion negativa":
            line = fh.readline().rstrip()
            for i in range (9):
                line = fh.readline().rstrip()
                countdata3.append(line.replace(',',';').split(';'))
    return countdata1,countdata2,countdata3


class LabelTool:
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("Generador de Reporte en Carpeta")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=False, height=False)
        

        self.rp=0 
        

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.fnlin=[]
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
        self.classname_label = Label(self.ConfigPanel, text = 'Los objetos cortan la linea de:')
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
        self.classname_label = Label(self.ConfigPanel, text = 'Origen del objeto que viene \n de Izquieda o de Arriba:')
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

        self.btnAuto = Button(self.ctrPanel, text='Generar todos los reportes', command=self.AutoGen)
        self.btnAuto.pack(side = LEFT, padx = 25, pady = 3)
        
        self.btnRm = Button(self.ConfigPanel, text='Guardar Configuración', command=self.Set_Settings)
        self.btnRm.grid(row=14, column=3, sticky=W+E,padx = 5, pady = 10)

     


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
        
        # Clear all button
        self.clBtn = Button(self.ConfigPanel, text="Vaciar todo", command=self.ClearAll)
        self.clBtn.grid(row=16, column=3, sticky=W+E,padx = 5, pady = 10)
        
    def ClearAll(self):
        self.entry_text2.set("")
        self.entry_text3.set("")
        self.entry_text4.set("")

        self.classcandidate_Class.set("")
        self.classcandidate_Type.set("")
        self.classcandidate_Cardinal.set("")   
        
        Preset_root=self.imageDir+"/Preset"+str(self.cur)+".pickle"
        
        try:
            
            os.remove(Preset_root)
            
            messagebox.showinfo("Configuración", "Se ha eliminado los archivos de configuracion por defecto")

        except (OSError, IOError) as e:
#            
            messagebox.showinfo("Configuración", "No existen archivos de configuracion por defecto")


    def AutoGen(self):
        Pickle_Ok=1
        self.cur=1
        print("Pickle: "+str(Pickle_Ok))    
        if messagebox.askyesno("Guardar configuracion", "¿Está Seguro?"):
            
            while(self.cur < self.total+1):       
                Preset_root=self.imageDir+"/Preset"+str(self.cur)+".pickle"
                self.cur=self.cur+1
                print(Preset_root)
                try:
                    Preset = pickle.load(open(Preset_root, "rb"))
                    print("Preset Loaded")
                    if (Preset[1] =="" or Preset[2] =="" or Preset[3] =="" or Preset[4] =="" or Preset[5] =="" or Preset[6] ==""):
                        messagebox.showinfo("Configuración", "Configuracion previa no valida")
                        Pickle_Ok=0
                        print("Pickle no valido")
                    if os.path.exists(Preset_root):
                        print("Pickle  valido")
                        
                    else:
                        Pickle_Ok=0 
                        messagebox.showinfo("Configuración", "Configuracion previa no existe")
                        
                except (OSError, FileNotFoundError) as e:
                    
                    Pickle_Ok=0
                    messagebox.showinfo("Configuración", "Preset not found")
                    
            print("Pickle: "+str(Pickle_Ok))    
            self.cur=1
            if(Pickle_Ok==1):
                messagebox.showinfo("Configuración", "Todas la configuraciones son válidas, se va a ejecutar el aforo")
                self.cur=1
                self.loadImage()
                self.Set_Settings()
                
                while(self.cur < self.total):
                    self.nextImage2()   
                    self.Set_Settings()

    def nextImage2(self, event = None):

        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
            Preset_root=self.imageDir+"/Preset"+str(self.cur)+".pickle"
            print(Preset_root)
            
            Preset = pickle.load(open(Preset_root, "rb"))
            print("Preset Loaded")
            
            self.entry_text2.set(Preset[1])
            self.entry_text3.set(Preset[2])
            self.entry_text4.set(Preset[3])
            
            self.classcandidate_Class.set(Preset[4])
            self.classcandidate_Type.set(Preset[5])
            self.classcandidate_Cardinal.set(Preset[6])
            
        elif self.cur == self.total:
            self.create_images_list()           
            messagebox.showinfo("Done", "That's All!")


    def loadDir(self):
        folder = filedialog.askdirectory()
        self.imageDir = folder
        self.rp=reporte(self.imageDir,"reporte_general_carpeta.csv") 
        self.entry_text.set(self.imageDir)
        # get image list
        self.imageList = glob.glob(os.path.join(self.imageDir, FILES_FORMAT_REGEX))
        self.imageList.sort()
        #print (self.imageList)
        if len(self.imageList) == 0:
            self.print_log('Files .jpg or .png NOT FOUND in the specified dir!')
            return
        if not len(self.imageList) == 0:
            Lineas_de_conteo_halladas="Se encontraron "+ str(len(self.imageList)) +" líneas de conteo" 
        print("Realizando diccionario de conversion")
        
        
        for pathpfile in self.imageList:
            self.fnlin.append(ntpath.basename(pathpfile))
        print (self.fnlin)
            
            
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
        
        Preset_root=self.imageDir+"/Preset"+str(self.cur)+".pickle"
        
        filereport=self.imageDir+'/'+'merge_video_sources_report.csv'    
        #FALTABA PACHO
        if not os.path.isfile(filereport):
            print("WARNING: LA CARPETA NO CONTIENE ARCHIVO DE REPORTE DE VIDEOS NVR SECRETARIA INTENTANDO GENERAR A PARTIR DE ARCHIVOS")
            #os.chdir(folder)
            listaarchivos2=glob.glob(os.path.join(self.imageDir, FILES_FORMAT_CSV))
            FILE_report_w  = open(filereport, 'w') 
            FILE_report_w.write("File_Name;Year;Month;Day;Start_Time;Duration;End_Time\n")
            listaarchivos2.sort()  
            
            listalinea1=[]
            cont=1
            for filea in listaarchivos2:
                if filea[-5]=="1":
                    listalinea1.append(ntpath.basename(filea))
                  
            listalinea1.sort()
            print (listalinea1)
            archivo_video_ant="0"
            for archivo in listalinea1:
                ar_split=archivo.split("_")
                archivo_video=ar_split[0]+"_"+ar_split[1]+"_"+ar_split[2]+".avi"
                
                if(archivo_video_ant!=archivo_video):
                    ano=ar_split[1][0:4]
                    mes=ar_split[1][4:6]
                    dia=ar_split[1][6:8]
                    start_time=ar_split[1][8:10]+":"+ar_split[1][10:12]+":"+ar_split[1][12:14]
                    Duration="05"# para videos de contrato monitoreo la duracion es cada 5 minutos. 
                    end_time=ar_split[1][8:10]+":"+ar_split[1][10:12]+":"+ar_split[1][12:14]     
                    towrite=archivo_video+";"+ano+";"+mes+";"+dia+";"+start_time+";"+Duration+";"+end_time+"\n"
                    FILE_report_w.write(towrite)
                    cont+=1
                archivo_video_ant=archivo_video
            FILE_report_w.close()
        #FALTABA PACHO
        
        
        try:
            Preset = pickle.load(open(Preset_root, "rb"))
            print(Preset)
            print("Preset Loaded")
            self.entry_text2.set(Preset[1])
            self.entry_text3.set(Preset[2])
            self.entry_text4.set(Preset[3])
            self.classcandidate_Class.set(Preset[4])
            self.classcandidate_Type.set(Preset[5])
            self.classcandidate_Cardinal.set(Preset[6])
            #messagebox.showinfo("Configuración", "Se ha cargado la configuración previa almacenada")

        except (OSError, IOError) as e:
#            
            self.entry_text2.set("")
            self.entry_text3.set("")
            self.entry_text4.set("")

            self.classcandidate_Class.set("")
            self.classcandidate_Type.set("")
            self.classcandidate_Cardinal.set("")
            foo={1:"",2:"",3:"",4:"",5:"",6:""}
            pickle.dump(foo, open(Preset_root, "wb"))
            print("Preset not found")
            
            
            
        #self.print_log(str(self.total) + ' images loaded from ' + self.imageDir)

    def loadImage(self):
        # load image
        basewidth = 500
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
        Preset_root=self.imageDir+"/Preset"+str(self.cur)+".pickle"
        
        try:
            Preset = pickle.load(open(Preset_root, "rb"))
            print("Preset Loaded")

            self.entry_text2.set(Preset[1])
            self.entry_text3.set(Preset[2])
            self.entry_text4.set(Preset[3])

            self.classcandidate_Class.set(Preset[4])
            self.classcandidate_Type.set(Preset[5])
            self.classcandidate_Cardinal.set(Preset[6])
            #messagebox.showinfo("Configuración", "Se ha cargado la configuración previa almacenada")

        except (OSError, IOError) as e:
            
            #self.entry_text2.set("")
            #self.entry_text3.set("")
            self.entry_text4.set("")

            self.classcandidate_Class.set("")
            self.classcandidate_Type.set("")
            self.classcandidate_Cardinal.set("")
            #foo={1:"",2:"",3:"",4:"",5:"",6:""}
            #pickle.dump(foo, open(Preset_root, "wb"))
            print("Preset not found")


    def nextImage(self, event = None):

        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        elif self.cur == self.total:
            self.create_images_list()           
            messagebox.showinfo("Done", "Cerrando Archivo Total De Reporte")
            self.rp.cerrarArchivo()
            SumarDeA3(self.imageDir+"/reporte_general_carpeta.csv",self.imageDir+"/reporte_general_carpeta_15m.csv")
        
        Preset_root=self.imageDir+"/Preset"+str(self.cur)+".pickle"
        print(Preset_root)
        
        try:
            Preset = pickle.load(open(Preset_root, "rb"))
            print("Preset Loaded")

            self.entry_text2.set(Preset[1])
            self.entry_text3.set(Preset[2])
            self.entry_text4.set(Preset[3])

            self.classcandidate_Class.set(Preset[4])
            self.classcandidate_Type.set(Preset[5])
            self.classcandidate_Cardinal.set(Preset[6])
            #messagebox.showinfo("Configuración", "Se ha cargado la configuración previa almacenada")

        except (OSError, IOError) as e:
            
            #self.entry_text2.set("")
            #self.entry_text3.set("")
            self.entry_text4.set("")

            self.classcandidate_Class.set("")
            self.classcandidate_Type.set("")
            self.classcandidate_Cardinal.set("")
            #foo={1:"",2:"",3:"",4:"",5:"",6:""}
            #pickle.dump(foo, open(Preset_root, "wb"))
            print("Preset not found")



    #remove picture
    def Set_Settings(self):
        #if messagebox.askyesno("Guardar configuracion", "¿Está Seguro?"):
        message='La configuración de la linea de conteo '+ str(self.cur)+' ha sido almacenada correctamente'
        self.print_log(message)
        print("Carrera: ",self.entry_text2.get())
        print("Calle: ",self.entry_text3.get())
        print("Clase de Aforo: ", self.entry_text4.get())
        print("Actor Vial: ",self.classcandidate_Class.get())
        print("Tipo de vía: ",self.classcandidate_Type.get())
        print("Referencia Cardinal: ",self.classcandidate_Cardinal.get())
          
        seleccion=self.classcandidate_Class.get()
        filereport=self.imageDir+'/'+'merge_video_sources_report.csv'    


        Preset = {1:str(self.entry_text2.get()),2:str(self.entry_text3.get()),3:str(self.entry_text4.get()),4:str(self.classcandidate_Class.get()),5:str(self.classcandidate_Type.get()),6:str(self.classcandidate_Cardinal.get())}

        Preset_root=self.imageDir+"/Preset"+str(self.cur)+".pickle"
        pickle_out = open(Preset_root,"wb")
        pickle.dump(Preset, pickle_out)
        pickle_out.close()
        
        
        """
        **********************VEHICULOS UNIDIRECCIONAL*******************************
        """    
        
        if seleccion == "Vehiculos-Unidireccional":
                        
            #Inician preguntas:
            # Es un acceso o una salida
            
            msg = "La linea Afora un Acceso o una Salida a interseccion"   
            choices = ["Acceso","Salida"]
            accOsal = self.classcandidate_Type.get()
            
            
            Acceso = self.classcandidate_Cardinal.get()
            Salida=""
            
            fieldValues = [self.entry_text2.get(),self.entry_text3.get()]  # we start with blanks for the values
                 
            
            if parallelo:
                p[-1].join()
            

            
            descripcion_via = self.entry_text4.get()
            
            
            FILE_report  = open(filereport, 'r') 
            for line in FILE_report:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(self.imageDir,lindata[0],self.cur,self.fnlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    # rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),str(fieldValues[2]),Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    self.rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    
                    self.rp.agregarData(Data1)
                else:
                    print ("depurado File_Name")
            
            message='El aforo la linea de conteo '+ str(self.cur)+' ha sido almacenado correctamente'
            self.print_log(message)
            
            
            """
            **********************CICLISTAS*******************************
            """
        elif seleccion == "Ciclistas":

            
            #Inician preguntas:
            # Es un acceso o una salida
            accOsal = self.classcandidate_Type.get()
            
            if accOsal=="Izquierda-Derecha":

                Acceso = self.classcandidate_Cardinal.get()
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
                    
            elif accOsal=="Arriba-Abajo":

                Acceso = self.classcandidate_Cardinal.get()
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"

            
            
            print ("pasa 3")

            fieldValues = [self.entry_text2.get(),self.entry_text3.get()]  # we start with blanks for the values

           
            
            descripcion_via = self.entry_text4.get()
            
            if parallelo:
                p[-1].join(15)
            FILE_report1  = open(filereport, 'r') 
            for line in FILE_report1:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(self.imageDir,lindata[0],self.cur,self.fnlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    self.rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    self.rp.agregarData(Data2)
                else:
                    print ("depurado File_Name")
            FILE_report1.close()        
            FILE_report2  = open(filereport, 'r') 
            for line in FILE_report2:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(self.imageDir,lindata[0],self.cur,self.fnlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    self.rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Salida,Acceso,lindata[3],lindata[2],lindata[1],lindata[4])
                    self.rp.agregarData(Data3)
                else:
                    print ("depurado File_Name")
            
            
            message='El aforo la linea de conteo '+ str(self.cur)+' ha sido almacenado correctamente'
            self.print_log(message)    
            
            """
            **********************PEATONES*******************************
            """
        elif seleccion == "Peatones":

            
   
            accOsal = self.classcandidate_Type.get()
            
            if accOsal=="Izquierda-Derecha":

                Acceso = self.classcandidate_Cardinal.get()
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
                    
            elif accOsal=="Arriba-Abajo":

                Acceso = self.classcandidate_Cardinal.get()
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"

            
            
            print ("pasa 3")

            fieldValues = [self.entry_text2.get(),self.entry_text3.get()]  # we start with blanks for the values

           
            
            descripcion_via = self.entry_text4.get()


            
            if parallelo:
                p[-1].join(15)
            FILE_report1  = open(filereport, 'r') 
            for line in FILE_report1:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(self.imageDir,lindata[0],self.cur,self.fnlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    self.rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    self.rp.agregarData(Data2)
                else:
                    print ("depurado File_Name")
            FILE_report1.close()        
            FILE_report2  = open(filereport, 'r') 
            for line in FILE_report2:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(self.imageDir,lindata[0],self.cur,self.fnlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    self.rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Salida,Acceso,lindata[3],lindata[2],lindata[1],lindata[4])
                    self.rp.agregarData(Data3)
                else:
                    print ("depurado File_Name")

            
            message='El aforo la linea de conteo '+ str(self.cur)+' ha sido almacenado correctamente'
            self.print_log(message)  
            
                
            """
            **********************VEHICULOS BIDIRECCIONAL*******************************
            """  
        elif seleccion == "Vehiculos-Bidireccional":
                        
            #Inician preguntas:
            # Es un acceso o una salida

            accOsal = self.classcandidate_Type.get()
            
            if accOsal=="Izquierda-Derecha":

                Acceso = self.classcandidate_Cardinal.get()
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"
                    
            elif accOsal=="Arriba-Abajo":

                Acceso = self.classcandidate_Cardinal.get()
                if Acceso=="Norte":
                    Salida="Sur"
                elif Acceso=="Sur":
                    Salida="Norte"
                elif Acceso=="Oriente":
                    Salida="Occidente"
                elif Acceso=="Occidente":
                    Salida="Oriente"

            
            
            print ("pasa 3")
            
            fieldValues = [self.entry_text2.get(),self.entry_text3.get()]  # we start with blanks for the values

                      
            descripcion_via = self.entry_text4.get()
            
            if parallelo:
                p[-1].join(15)
                
            FILE_report1  = open(filereport, 'r') 
            for line in FILE_report1:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(self.imageDir,lindata[0],self.cur,self.fnlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    self.rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Acceso,Salida,lindata[3],lindata[2],lindata[1],lindata[4])
                    self.rp.agregarData(Data2)
                else:
                    print ("depurado File_Name")
            FILE_report1.close()        
            FILE_report2  = open(filereport, 'r') 
            for line in FILE_report2:
                lindata=line.replace(',',';').split(';')
                if not (lindata[0]=='File_Name'):
                    #print lindata
                    linname=retornarNombreLinea(self.imageDir,lindata[0],self.cur,self.fnlin)
                    #print linname
                    Data1,Data2,Data3=getDataFromFile(linname)# Data1 ambos sentidos Data2 positivo, Data3, Negativo
                    
                    self.rp.generar_reporte_linea(str(fieldValues[0]),str(fieldValues[1]),descripcion_via,Salida,Acceso,lindata[3],lindata[2],lindata[1],lindata[4])
                    self.rp.agregarData(Data3)
                else:
                    print ("depurado File_Name")
                    
            message='El aforo la linea de conteo '+ str(self.cur)+' ha sido almacenado correctamente'
            self.print_log(message)  

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
