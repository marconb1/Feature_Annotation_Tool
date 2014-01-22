# -*- coding: utf-8 -*-
#anotação
import platform
import codecs

from PyQt4.QtCore import *
from PyQt4.QtGui import *

SENTENCE, POLARITY, FEATURE, SUBFEATURE, SUBSUBFEATURE, EIMP = range(6)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1
global IndexFeatureEscolhida
global IndexSubFeatureEscolhida

class Table(object):

    def __init__(self, TSentence, TPolarity, TFeature, TSubFeature, TSubSubFeature, TEimp):
        self.TSentence = QString(TSentence)   
        self.TPolarity = QString(TPolarity)
        self.TFeature = QString(TFeature)
        self.TSubFeature = QString(TSubFeature)
        self.TSubSubFeature = QString(TSubSubFeature)
        self.TEimp = QString(TEimp)
        
    def __cmp__(self, other):
        return QString.localeAwareCompare(self.TSentence.toLower(),other.TSentence.toLower(),)
        
class TableModel(QAbstractTableModel):

    def __init__(self, filename=QString()):
        super(TableModel, self).__init__()
        self.filename = filename
        self.Set = []
        self.TPolarities = set()
        self.TFeatures = set()
        self.TSubFeatures = set()
        self.TSubSubFeatures = set()
        self.TEimps = set()
        
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)| Qt.ItemIsEditable) 
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.Set)):
            return QVariant()
        SetColumn = self.Set[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == SENTENCE:
                return QVariant(SetColumn.TSentence)
            elif column == POLARITY:
                return QVariant(SetColumn.TPolarity)
            elif column == FEATURE:
                return QVariant(SetColumn.TFeature)
            elif column == SUBFEATURE:
                return QVariant(SetColumn.TSubFeature)
            elif column == SUBSUBFEATURE:
                return QVariant(SetColumn.TSubSubFeature)
            elif column == EIMP:
                return QVariant(SetColumn.TEimp)              
        return QVariant()
   
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == SENTENCE:
                return QVariant("Sentence")
            elif section == POLARITY:
                return QVariant("Polarity")
            elif section == FEATURE:
                return QVariant("Feature")
            elif section == SUBFEATURE:
                return QVariant("SubFeature")
            elif section == SUBSUBFEATURE:
                return QVariant("SubSubFeature")
            elif section == EIMP:
                return QVariant("E/I")
        return QVariant(int(section + 1))

    def rowCount(self, index=QModelIndex()):
        return len(self.Set)

    def columnCount(self, index=QModelIndex()):
        return 6
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.Set):
            SetColumn = self.Set[index.row()]
            column = index.column()			
            if column == SENTENCE:
                SetColumn.TSentence = value.toString()
            elif column == POLARITY:
                SetColumn.TPolarity = value.toString()
            elif column == FEATURE:
                SetColumn.TFeature = value.toString()
            elif column == SUBFEATURE:
                SetColumn.TSubFeature = value.toString()
            elif column == SUBSUBFEATURE:
                SetColumn.TSubSubFeature = value.toString()
            elif column == EIMP:
                SetColumn.TEimp = value.toString()                
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,position + rows - 1)
        for row in range(rows):			
            self.Set.insert(position + row, Table(" "," "," "," "," "," "))
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.Set = self.Set[:position] + self.Set[position + rows:]
        self.endRemoveRows()
        return True

class TableDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(TableDelegate, self).__init__(parent)
        self.listaEimp = []
        self.listaFeature = []
        self.listaSubFeature = []
        self.listaSubSubFeature = []
        self.items = []
        self.parent = parent        
        
    @pyqtSlot(str)
    def on_comboBoxParent_Feature_currentIndexChanged(self, index):
        for i in range(-1,len(self.listaFeature)):
            items = self.listaFeature[(index)]
            self.comboboxFeature.addItems(items)
        global IndexFeatureEscolhida
        IndexFeatureEscolhida = self.comboboxFeature.currentIndex()

    @pyqtSlot(str)   
    def on_comboBoxParent_SubFeature_currentIndexChanged(self, index):      
        for i in range(-1,len(self.listaSubFeature)):
            items = self.listaSubFeature[(index)]
            self.comboboxSubFeature.addItems(items)
        global IndexSubFeatureEscolhida    
        IndexSubFeatureEscolhida = self.comboboxSubFeature.currentIndex()
        
    def createEditor(self, parent, option, index):
        if index.column() == EIMP:
            self.comboboxEimp = QComboBox(parent)
            self.comboboxEimp.addItems(sorted(index.model().TEimps))
            self.comboboxEimp.setEditable(True)
            arquivo = codecs.open("Lists/ln3.txt",encoding='utf-8',mode="r")  
            conTWordsdoEimp = arquivo.readlines()
            listaEimp = []
            for i in conTWordsdoEimp:
                listaEimp.append(i.replace("\n",""))
            self.comboboxEimp.addItems(sorted(listaEimp))
            return self.comboboxEimp
        elif index.column() == POLARITY: 
            self.comboboxPolarity = QComboBox(parent)
            self.comboboxPolarity.addItems(sorted(index.model().TPolarities))
            self.comboboxPolarity.setEditable(True)
            arquivo = codecs.open("Lists/ln2.txt",encoding='utf-8',mode="r")   
            conTWordsdoPolarity = arquivo.readlines()
            listaPolarity = []
            for i in conTWordsdoPolarity:
                listaPolarity.append(i.replace("\n",""))
            self.comboboxPolarity.addItems(sorted(listaPolarity))
            return self.comboboxPolarity
        elif index.column() == FEATURE: 
            self.comboboxFeature = QComboBox(parent)
            self.comboboxFeature.addItems(sorted(index.model().TFeatures))
            self.comboboxFeature.setEditable(True)           
            arquivo = codecs.open("Lists/ln1.txt",encoding='utf-8',mode="r")  
            conTWordsdoFeature = arquivo.readlines()
            listaFeature = []           
            for i in conTWordsdoFeature:
                listaFeature.append(i.replace("\n",""))
                self.listaFeature = listaFeature
            index = self.comboboxFeature.view().currentIndex()
            self.comboboxFeature.addItems(sorted(self.listaFeature))     
            self.comboboxFeature.currentIndexChanged.connect(self.on_comboBoxParent_Feature_currentIndexChanged)                       
            return self.comboboxFeature
        elif index.column() == SUBFEATURE:
            self.comboboxSubFeature = QComboBox(parent)
            self.comboboxSubFeature.addItems(sorted(index.model().TSubFeatures))
            self.comboboxSubFeature.setEditable(True)
            listaSubFeature = []
            if IndexFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/ln1-1.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/ln1-3.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/ln1-4.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5:
                arquivo = codecs.open("Lists/ln1-5.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 6:
                arquivo = codecs.open("Lists/ln1-6.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 7:
                arquivo = codecs.open("Lists/ln1-7.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8:
                arquivo = codecs.open("Lists/ln1-8.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9:
                arquivo = codecs.open("Lists/ln1-9.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 10:
                arquivo = codecs.open("Lists/ln1-10.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11:
                arquivo = codecs.open("Lists/ln1-11.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 12:
                arquivo = codecs.open("Lists/ln1-12.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13:
                arquivo = codecs.open("Lists/ln1-13.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 14:
                arquivo = codecs.open("Lists/ln1-14.txt",encoding='utf-8',mode="r")
            conTWordsdoSubFeature = arquivo.readlines()
            for i in conTWordsdoSubFeature:
                listaSubFeature.append(i.replace("\n",""))
                self.listaSubFeature = listaSubFeature
            self.comboboxSubFeature.addItems(sorted(self.listaSubFeature))
            index = self.comboboxSubFeature.view().currentIndex()            
            self.comboboxSubFeature.currentIndexChanged.connect(self.on_comboBoxParent_SubFeature_currentIndexChanged) 
            return self.comboboxSubFeature                
        elif index.column() == SUBSUBFEATURE:
            self.comboboxSubSub = QComboBox(parent)
            self.comboboxSubSub.addItems(sorted(index.model().TSubSubFeatures))
            self.comboboxSubSub.setEditable(True)
            listaSubSubFeature = []            
            global IndexSubFeatureEscolhida
            if  IndexFeatureEscolhida == 1 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/ln1-1-1.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 1 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/ln1-1-2.txt",encoding='utf-8',mode="r")
            elif  IndexFeatureEscolhida == 1 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/ln1-1-3.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 2 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")                
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 5:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 6:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 7:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 8:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 9:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 3 and IndexSubFeatureEscolhida == 10:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")  
            elif IndexFeatureEscolhida == 4 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 4 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 4 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 4 and IndexSubFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")    
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 5:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 6:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 7:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 8:
                arquivo = codecs.open("Lists/ln1-5-8.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 9:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 10:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 11:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 5 and IndexSubFeatureEscolhida == 12:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")                
            elif IndexFeatureEscolhida == 6 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 6 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 6 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 6 and IndexSubFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")   
            elif IndexFeatureEscolhida == 7 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 7 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/ln1-7-2.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 7 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/ln1-7-3.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 7 and IndexSubFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/ln1-7-4.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 7 and IndexSubFeatureEscolhida == 5:
                arquivo = codecs.open("Lists/ln1-7-5.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 5:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 6:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 7:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 8:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 9:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 10:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 11:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 12:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 13:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 14:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 15:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 16:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 17:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 8 and IndexSubFeatureEscolhida == 18:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 4:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 5:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 6:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 7:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 8:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 9 and IndexSubFeatureEscolhida == 9:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 1: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 2: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 3: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 4: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 5: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 6: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 7: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 8: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 9: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 10 and IndexSubFeatureEscolhida == 10: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r") 
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 1:  
                arquivo = codecs.open("Lists/ln1-11-1.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 3:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 4:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 5:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 6:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 7:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")           
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 8:    
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 9:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 10:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 11:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 12:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 13:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 14:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")      
            elif IndexFeatureEscolhida == 11 and IndexSubFeatureEscolhida == 15:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")                      
            elif IndexFeatureEscolhida == 12 and IndexSubFeatureEscolhida == 1:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 12 and IndexSubFeatureEscolhida == 2:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")   
            elif IndexFeatureEscolhida == 12 and IndexSubFeatureEscolhida == 3:
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")   
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 1:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 2: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 3: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 4: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 5: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 6: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 7: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")           
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 8: 
                arquivo = codecs.open("Lists/ln1-13-8.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 9: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 10: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 11: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 12: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 13: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 14: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")      
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 15: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")                     
            elif IndexFeatureEscolhida == 13 and IndexSubFeatureEscolhida == 16: 
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")   
            elif IndexFeatureEscolhida == 14 and IndexSubFeatureEscolhida == 1:  
                arquivo = codecs.open("Lists/ln1-14-1.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 14 and IndexSubFeatureEscolhida == 2:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 14 and IndexSubFeatureEscolhida == 3:  
                arquivo = codecs.open("Lists/ln1-14-3.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 14 and IndexSubFeatureEscolhida == 4:  
                arquivo = codecs.open("Lists/ln1-14-4.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 14 and IndexSubFeatureEscolhida == 5:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")
            elif IndexFeatureEscolhida == 14 and IndexSubFeatureEscolhida == 6:  
                arquivo = codecs.open("Lists/vazio.txt",encoding='utf-8',mode="r")                                
            conTWordsdoSubSub = arquivo.readlines()
            for i in conTWordsdoSubSub:
                listaSubSubFeature.append(i.replace("\n",""))
                self.listaSubSubFeature = listaSubSubFeature
            self.comboboxSubSub.addItems(sorted(self.listaSubSubFeature))            
            return self.comboboxSubSub      
        elif index.column() == SENTENCE:
            editor = QLineEdit(parent)
            return editor

    def setModelData(self, editor, model, index):
        if index.column() in (POLARITY, FEATURE, SUBFEATURE, SUBSUBFEATURE, EIMP):
            text = editor.currentText()            
            model.setData(index, QVariant(text))
        elif index.column() == SENTENCE:
            text = editor.text()
            model.setData(index, QVariant(text))
