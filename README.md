# Verse Selector
![GUI on Windows 10](https://github.com/jimmywengzj/verse-selector/assets/100853043/306aa919-8a3e-4444-9c02-ab735f77e9e8)

A simple offline Bible verse selector for formatting and copying to the clipboard. 

## Usage
Make sure that you have `Python` and `pip` installed first. 
```
pip install PySide6
python GUI.py
```

## Add Bible versions
For copyright reasons, this tool only comes with two versions : KJV 1850 revision and LSG 1910, both in public domain. Feel free to add versions yourself. 

The Bible format used is a minimalist XML format [Beblia](https://beblia.com), and you can download hundreds of versions in their [repository](https://github.com/Beblia/Holy-Bible-XML-Format). However, there are errors in their files, and to make sure that you have the correct version of Bible without missing words, I highly recommand you to download Bibles in other formats and use [BibleMultiConverter](https://github.com/schierlm/BibleMultiConverter) to convert them to `BebliaXML` format. I choose to downloaded [MyBible](https://mybible.zone) modules using `MyBibleZoneListDownloader` tool from `BibleMultiConverter`. There were some minor issues with the conversion process that are solved manually. 

After you have your `BebliaXML` files, put them in `./bible/language/`, re-run the Python script and they should show up in the menu. 

## Languages
By default this selector supports English, French, and Chinese. If you use Chinese Bibles, you can do `pip install pypinyin`, and uncomment `import pypinyin` and the code in `ExtendedQSortFilterProxyModel`, to allow auto-complete with full pinyin and first letters of pinyin. 

To add a language, create a folder in `./bible/` named with the language code. Then you have to modify the source code of `GUI.py` and `Selector.py` to add the book names and their abbreviations, as they are hard-coded. 
