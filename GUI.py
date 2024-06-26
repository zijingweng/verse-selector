import os
import sys
import Selector
# import pypinyin

from PySide6.QtCore import Qt, QSortFilterProxyModel, QTimer
from PySide6.QtWidgets import QWidget, QApplication, QCompleter, QComboBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame
from PySide6.QtGui import QIntValidator, QClipboard, QIcon

book_names = {
    'EN': ['Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1 Samuel','2 Samuel','1 Kings','2 Kings','1 Chronicles','2 Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs','Ecclesiastes','Song of Solomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi','Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians','Galatians','Ephesians','Philippians','Colossians','1 Thessalonians','2 Thessalonians','1 Timothy','2 Timothy','Titus','Philemon','Hebrews','James','1 Peter','2 Peter','1 John','2 John','3 John','Jude','Revelation'],
    'FR': ['Genèse','Exode','Lévitique','Nombres','Deutéronome','Josué','Juges','Ruth','1 Samuel','2 Samuel','1 Rois','2 Rois','1 Chroniques','2 Chroniques','Esdras','Néhémie','Esther','Job','Psaumes','Proverbes','Ecclésiaste','Cantique des cantiques','Ésaïe','Jérémie','Lamentations','Ézéchiel','Daniel','Osée','Joël','Amos','Abdias','Jonas','Michée','Nahum','Habakuk','Sophonie','Aggée','Zacharie','Malachie','Matthieu','Marc','Luc','Jean','Actes','Romains','1 Corinthiens','2 Corinthiens','Galates','Éphésiens','Philippiens','Colossiens','1 Thessaloniciens','2 Thessaloniciens','1 Timothée','2 Timothée','Tite','Philémon','Hébreux','Jacques','1 Pierre','2 Pierre','1 Jean','2 Jean','3 Jean','Jude','Apocalypse'],
    'ZH': ['创世记','出埃及记','利未记','民数记','申命记','约书亚记','士师记','路得记','撒母耳记上','撒母耳记下','列王纪上','列王纪下','历代志上','历代志下','以斯拉记','尼希米记','以斯帖记','约伯记','诗篇','箴言','传道书','雅歌','以赛亚书','耶利米书','耶利米哀歌','以西结书','但以理书','何西阿书','约珥书','阿摩司书','俄巴底亚书','约拿书','弥迦书','那鸿书','哈巴谷书','西番雅书','哈该书','撒迦利亚书','玛拉基书','马太福音','马可福音','路加福音','约翰福音','使徒行传','罗马书','哥林多前书','哥林多后书','加拉太书','以弗所书','腓立比书','歌罗西书','帖撒罗尼迦前书','帖撒罗尼迦后书','提摩太前书','提摩太后书','提多书','腓利门书','希伯来书','雅各书','彼得前书','彼得后书','约翰一书','约翰二书','约翰三书','犹大书','启示录'],
}

# filter with chinese pinyin and first letters
class ExtendedQSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(ExtendedQSortFilterProxyModel, self).__init__(parent)

#     def filterAcceptsRow(self, source_row, source_parent):
#         model = self.sourceModel()
#         index0 = model.index(source_row, 0, source_parent)
#         data = model.data(index0)
#         pinyin = ''.join(pypinyin.lazy_pinyin(data))
#         letters = ''.join(pypinyin.lazy_pinyin(data, style=pypinyin.Style.FIRST_LETTER))

#         if self.filterRegularExpression().match(data).hasMatch():
#             return True
#         if self.filterRegularExpression().match(pinyin).hasMatch():
#             return True
#         if self.filterRegularExpression().match(letters).hasMatch():
#             return True
#         return False

# combobox with filter
class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setEditable(True)
        # add a filter model to filter matching items （uncomment to enable searching with chinese pinyin and first letters）
        self.pFilterModel = ExtendedQSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.setCompleter(completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer().activated.connect(self.on_completer_activated)

    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated.emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer().setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer().setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)
    

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.clipboard = QApplication.clipboard()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reset_button_color)
        
        self.col1 = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.col1.addLayout(self.row1)
        self.col1.addLayout(self.row2)

        self.langs = os.listdir('./bible')
        self.langCombo = QComboBox()
        self.langCombo.addItems(self.langs)
        self.langCombo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.langCombo.currentTextChanged.connect(self.on_lang_change)
        self.row1.addWidget(self.langCombo)
        
        self.versionCombo = QComboBox()
        self.versionCombo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.row1.addWidget(self.versionCombo)

        self.bookCombo = ExtendedComboBox()
        self.bookCombo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.row2.addWidget(self.bookCombo)

        self.chapterText = QLineEdit()
        self.chapterText.setValidator(QIntValidator(1, 200))
        self.chapterText.setMaxLength(3)
        self.chapterText.setFixedWidth(30)
        self.chapterText.mousePressEvent = lambda _ : self.chapterText.selectAll()
        self.chapterText.returnPressed.connect(self.on_copy)
        self.row2.addWidget(self.chapterText)

        self.row2.addWidget(QLabel(':'))

        self.verseStartText = QLineEdit()
        self.verseStartText.setValidator(QIntValidator(1, 200))
        self.verseStartText.setMaxLength(3)
        self.verseStartText.setFixedWidth(30)
        self.verseStartText.mousePressEvent = lambda _ : self.verseStartText.selectAll()
        self.verseStartText.returnPressed.connect(self.on_copy)
        self.row2.addWidget(self.verseStartText)

        self.row2.addWidget(QLabel('-'))

        self.verseEndText = QLineEdit()
        self.verseEndText.setValidator(QIntValidator(1, 200))
        self.verseEndText.setMaxLength(3)
        self.verseEndText.setFixedWidth(30)
        self.verseEndText.mousePressEvent = lambda _ : self.verseEndText.selectAll()
        self.verseEndText.returnPressed.connect(self.on_copy)
        self.row2.addWidget(self.verseEndText)

        self.copyButton = QPushButton('Copy')
        self.copyButton.clicked.connect(self.on_copy)

        self.section1 = QHBoxLayout()
        self.section1.addLayout(self.col1)
        self.section1.addWidget(self.copyButton)

        self.preview = QLabel('')
        self.preview.setFixedHeight(self.preview.sizeHint().height())
        self.preview.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))

        # main layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.section1)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(separator)

        self.layout.addWidget(self.preview)
        self.setLayout(self.layout)

        # init
        self.langCombo.setCurrentText('EN')
        # force update
        self.on_lang_change('EN')
        self.bookCombo.setCurrentIndex(42)
        self.chapterText.setText('1')
        self.verseStartText.setText('1')

    def on_lang_change(self, lang):
        self.versionCombo.clear()
        filenames = os.listdir('./bible/' + lang)
        versions = [os.path.splitext(i)[0] for i in filenames]
        self.versionCombo.addItems(versions)
        # default versions for each language
        if lang == 'EN':
            self.versionCombo.setCurrentText('KJV1850')
        elif lang == 'FR':
            self.versionCombo.setCurrentText('LSG1910')

        book = self.bookCombo.currentIndex()
        self.bookCombo.clear()
        self.bookCombo.addItems(book_names.get(lang))
        self.bookCombo.setCurrentIndex(book)

    def on_copy(self):
        lang = self.langCombo.currentText()
        version = self.versionCombo.currentText()
        book = self.bookCombo.currentIndex()
        chapter = self.chapterText.text()
        verseStart = self.verseStartText.text()
        verseEnd = self.verseEndText.text()
        try:
            res = Selector.verse_select(lang, 
                                        version, 
                                        book + 1, 
                                        int(chapter), 
                                        int(verseStart), 
                                        0 if verseEnd == '' else int(verseEnd))
            if res:
                self.clipboard.setText(res, QClipboard.Mode.Clipboard)
                self.preview.setText(res)
                self.copyButton.setStyleSheet('background-color: #7fff7f')
                self.timer.start(500)
            else: # error
                self.preview.setText('error')
                self.copyButton.setStyleSheet('background-color: #ff7f7f')
                self.timer.start(500)
        except:
            self.preview.setText('error')
            self.copyButton.setStyleSheet('background-color: #ff7f7f')
            self.timer.start(500)
    
    def reset_button_color(self):
        self.copyButton.setStyleSheet("background-color: light gray")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.svg'))
    # app.setStyle('Fusion')

    window = Window()
    window.setWindowTitle('Verse Selector')
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.setFixedSize(window.sizeHint())
    window.show()
    sys.exit(app.exec())
