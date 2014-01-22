# -*- coding: utf-8 -*-

####
#### The script runs on python 2.7. All the information is printed on the screen
####

#### Authors: Marco Nemetz Bochernisan e Larissa Astrogildo de Freitas
#### Version: 1.0
#### Date: 15/01/14

# Import Libraries
# Necessary PyQt4 library

import sys
import qrc_resources
import table
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s:s

class MainWindow(QMainWindow):
    NextId = 1 
    Instances = set() 
    TEXTO = ""
    FILE = ""
    def __init__(self, filename = QString(), parent=None):       
        super(MainWindow, self).__init__(parent)       
        self.setAttribute(Qt.WA_DeleteOnClose)
        MainWindow.Instances.add(self)      
        self.text = QLabel(self)
        self.text.setGeometry(QRect(60,60,50,50))
        self.text.setObjectName(_fromUtf8("text"))
        self.text.setText(QApplication.translate("Manual Annotation", "", None, QApplication.UnicodeUTF8))          
        self.tabWidget = QTabWidget(self) 
        self.tabWidget.setGeometry(QRect(20,70,1260,800))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))        
        self.tabNotepad = QWidget() 
        self.tabNotepad.setObjectName(_fromUtf8("tabNotepad"))        
        self.editor = QTextEdit(self.tabNotepad)                    
        self.editor.setGeometry(50,50,500,680)
        self.model = table.TableModel(QString("table.dat"))
        self.tab = QTableView(self.tabNotepad)	
        self.tab.setGeometry(QRect(560,100,630,630))
        self.tab.setModel(self.model)
        self.tab.setItemDelegate(table.TableDelegate(self))
        self.addLineButton = QPushButton(self.tabNotepad)
        self.addLineButton.setGeometry(QRect(600,50,100,37))
        self.addLineButton.setText(QApplication.translate("None","Add", None, QApplication.UnicodeUTF8))        
        self.removeLineButton = QPushButton(self.tabNotepad)
        self.removeLineButton.setGeometry(QRect(700,50,100,37))
        self.removeLineButton.setText(QApplication.translate("None","Remove", None, QApplication.UnicodeUTF8))
        self.exportButton = QPushButton(self.tabNotepad)
        self.exportButton.setGeometry(QRect(800,50,100,37))        
        self.exportButton.setText(QApplication.translate("None","Export", None, QApplication.UnicodeUTF8))        
        self.connect(self.addLineButton, SIGNAL("clicked()"), self.addLine)
        self.connect(self.removeLineButton, SIGNAL("clicked()"), self.removeLine)
        self.connect(self.exportButton, SIGNAL("clicked()"), self.export)        
        self.setWindowTitle("Program (delegate)")
        self.tabWidget.addTab(self.tabNotepad, _fromUtf8(""))        
        fileNewAction = self.createAction("&New", self.fileNew, QKeySequence.New, "filenew", "Create a text file") 	
        fileOpenAction = self.createAction("&Open", self.fileOpen, QKeySequence.Open, "fileopen", "Open an existing text file")                            
        fileSaveAction = self.createAction("&Save", self.fileSave, QKeySequence.Save, "filesave", "Save the text")                         
        fileCloseAction = self.createAction("&Close", self.close, QKeySequence.Close, "fileclose", "Close this text editor")                   
        fileQuitAction = self.createAction("&Quit", self.fileQuit, "Ctrl+m", "filequit", "Close the application")                 
        editCopyAction = self.createAction("&Copy", self.editor.copy, QKeySequence.Copy, "editcopy", "Copy text to the clipboard") 
        editCutAction = self.createAction("&Cut", self.editor.cut, QKeySequence.Cut, "editcut", "Cut text to the clipboard")                  
        editPasteAction = self.createAction("&Paste", self.editor.paste, QKeySequence.Paste, "editpaste", "Paste in the clipboard's text")
        editInsertAction = self.createAction("&Insert", self.addLineTable, QKeySequence.Print,"Insert", "Insert in the clipboard's text")
        fileMenu = self.menuBar().addMenu("&File") 
        self.addActions(fileMenu, (fileNewAction, fileOpenAction, fileSaveAction, None, fileCloseAction, fileQuitAction))                
        editMenu = self.menuBar().addMenu("&Edit")        
        self.addActions(editMenu, (editCopyAction, editCutAction, editPasteAction, editInsertAction))
        self.windowMenu = self.menuBar().addMenu("&Window")        
        self.connect(self.windowMenu, SIGNAL("aboutToShow()"), self.updateWindowMenu)
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction, editPasteAction))
        self.connect(self, SIGNAL("destroyed(QObject*)"), MainWindow.updateInstances)
        self.resize(1500, 1200)
        self.scroll(400,400)
        self.setWindowTitle(QApplication.translate("Form", filename, None, QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNotepad), QApplication.translate("Form", "Manual Annotation", None, QApplication.UnicodeUTF8))
        self.filename = filename
        if self.filename.isEmpty():
            self.filename = QString("Unnamed-%d.txt" %  MainWindow.NextId)
            MainWindow.NextId += 1
            self.editor.document().setModified(False)
            self.setWindowTitle("Manual Annotation  - %s" % self.filename)
        else:
            self.loadFile()

    @staticmethod
    def updateInstances(qobj):
        MainWindow.Instances = set([window for window in MainWindow.Instances if isAlive(window)])     

    def fileOpen(self):
        filename = QFileDialog.getOpenFileName(self,"Manual Annotation -- Open File")
        if not filename.isEmpty():
            if not self.editor.document().isModified() and self.filename.startsWith("Unnamed"):
                self.filename = filename
                self.loadFile() 
            else:
                MainWindow(filename).show()        
       
    def loadFile(self):
        global text
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            text = stream.readAll()
            self.TEXTO = text
            self.FILE = self.filename
            self.editor.setPlainText(text)
            self.editor.document().setModified(False)
        except (IOError, OSError), e:
            QMessageBox.warning(self, "Manual Annotation -- Load Error", "Failed to load %s: %s" % (self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        self.editor.document().setModified(False)
        self.setWindowTitle("Main Window - %s" % QFileInfo(self.filename).fileName())    
        return text        
        
    def addLine(self):                      
        row = self.model.rowCount()   
        self.model.insertRows(row)
        index = self.model.index(row, 0)
        tabView = self.tab        
        tabView.setFocus()
        tabView.setCurrentIndex(index)
        tabView.edit(index)
      
    def removeLine(self):
        tabView = self.tab
        index = tabView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        TSentence = self.model.data(self.model.index(row, table.SENTENCE)).toString()                    
        TPolarity = self.model.data(self.model.index(row, table.POLARITY)).toString()
        TFeature = self.model.data(self.model.index(row, table.FEATURE)).toString()
        TSubFeature = self.model.data(self.model.index(row, table.SUBFEATURE)).toString()
        TSubSubFeature = self.model.data(self.model.index(row, table.SUBSUBFEATURE)).toString()        
        TEimp = self.model.data(self.model.index(row, table.EIMP)).toString()
        if QMessageBox.question(self, "Line - Remove", 
                QString("Remove %1 %2 %3 %4 %5 %6?").arg(TSentence).arg(TPolarity).arg(TFeature).arg(TSubFeature).arg(TSubSubFeature).arg(TEimp),
                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        self.model.removeRows(row)
        
    def addLineTable(self):        
        row = self.model.rowCount()  
        self.model.insertRows(row)
        column = 0
        index = self.model.index(row, column)        
        tabView = self.tab            
        tabView.setFocus()
        tabView.setCurrentIndex(index)
        cursor = self.editor.textCursor()
        format = cursor.charFormat()
        format.setBackground(Qt.yellow)
        format.setForeground(Qt.gray)  
        cursor.setCharFormat(format)
        textSelected = cursor.selectedText()  
        self.model.setData(index, QVariant(textSelected)) 
    
    def export(self):        
        Filename = "Filename"
        filename = unicode(QFileDialog.getSaveFileName(self, "Document - Choose Export File", Filename+".xml"))
        if not filename:
                return
        erro = 0 
        fh = None
        try:            
                fh = QFile(filename)
                if not fh.open(QIODevice.WriteOnly):                     
                    raise IOError, unicode(fh.errorString())
                stream = QTextStream(fh)
                stream.setCodec("UTF-8")              
                for row in range(self.model.rowCount()):
                    TSentence = self.model.data(
                    self.model.index(row, table.SENTENCE)).toString()
                    TPolarity = self.model.data(   
                    self.model.index(row, table.POLARITY)).toString()
                    TFeature = self.model.data(
                    self.model.index(row, table.FEATURE)).toString()
                    TSubFeature = self.model.data(
                    self.model.index(row, table.SUBFEATURE)).toString()
                    TSubSubFeature = self.model.data(
                    self.model.index(row, table.SUBSUBFEATURE)).toString()
                    TEimp = self.model.data(
                    self.model.index(row, table.EIMP)).toString()                    
                    stream << "<document id="+str(row)+">" << "\n" <<text<< "\n" << "\t"<< "<sentence id="+str(row)+"> " <<"\n" \
                    <<"\t"<<"\t"<< TSentence <<"\n"<<"\t"<<"\t"<<"\t"<< "<feature id="+str(row)+">"<<"\t"<< TFeature << "\t"<< "</feature>" << "\n"<<"\t"<<"\t"<<"\t" << "<subfeature id="+str(row)+">"<<"   "<< TSubFeature << "\t"<<"</subfeature>"<< "\n" <<"\t" \
                    <<"\t" <<"\t"<< "<subsubfeature id="+str(row)+">"<<"   "<< TSubSubFeature << "\t"<<"</subsubfeature>"<< "\n" <<"\t" \
                    <<"\t" <<"\t"<<"<polarity id="+str(row)+">"<<"\t"<<TPolarity <<"\t"<< "</polarity>"<<"\n"<<"\t"<<"\t"<<"\t"<<"<ei id="+str(row)+">"<<"\t"<<TEimp <<"\t"<< "</ei>"<<"\n"<<"\t"<<"</sentence>" <<"\n"<<"</document>"<<"\n"<<"\n"                       
                    if ((TEimp == " ") or (TSentence == " ") or (TPolarity == " ") or (TSubFeature == " ") or (TSubSubFeature == " ") or (TFeature == " ")):                        
                        QMessageBox.warning(self, "Cell - Error","Ops, there is something missing.")
                        erro = 1     
        except (IOError, OSError), e:
            QMessageBox.warning(self, "Text - Error", "Failed to export: %s" % e)     
        if (erro == 0):              
            QMessageBox.warning(self, "Text - Export","Successfully exported text to %s" % filename)            
        else:
           QMessageBox.warning(self, "Cell - Error","Check if all the fields are filled.")  

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):        
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):         
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
    
    def fileQuit(self):        
        QApplication.closeAllWindows()

    def fileNew(self):        
        MainWindow().show()

    def fileSave(self):        
        if self.filename.startsWith("Text"):
            return self.fileSaveAs()
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QTextStream(fh) 
            stream.setCodec("UTF-8")
            stream << self.editor.toPlainText()
            self.editor.document().setModified(False) 
        except (IOError, OSError), e:         
            QMessageBox.warning(self, "TEXTS PROGRAM-- Save Error", "Failed to save %s: %s" % (self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        return True 

    def updateWindowMenu(self):        
        self.windowMenu.clear()
        for window in MainWindow.Instances:
            if isAlive(window):
                self.windowMenu.addAction(window.windowTitle(),self.raiseWindow)

    def raiseWindow(self):        
        action = self.sender()
        if not isinstance(action, QAction):
            return
        for window in MainWindow.Instances:
            if isAlive(window) and window.windowTitle() == action.text():  
                window.activateWindow()
                window.raise_()
                break
           
def isAlive(qobj):    
    import sip
    try:
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True

app = QApplication(sys.argv)
MainWindow().show()
app.setWindowIcon(QIcon(":/icon.png")) 
app.exec_()