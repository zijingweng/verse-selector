import xml.etree.ElementTree as ET

spacings = {
    'EN': ' ',
    'FR': ' ',
    'ZH': '',
}

bookAbbr = {
    'EN': ['Gen','Exo','Lev','Num','Deu','Josh','Judg','Ruth','1Sam','2Sam','1Kin','2Kin','1Chr','2Chr','Ezr','Neh','Esth','Job','Ps','Prov','Eccl','Song','Isa','Jer','Lam','Ezek','Dan','Hos','Joel','Am','Oba','Jona','Mic','Nah','Hab','Zeph','Hag','Zech','Mal','Mat','Mar','Luk','John','Acts','Rom','1Cor','2Cor','Gal','Eph','Phil','Col','1Ths','2Ths','1Tim','2Tim','Tit','Phlm','Heb','Jam','1Pet','2Pet','1Jn','2Jn','3Jn','Jud','Rev'],
    'FR': ['Gn','Ex','Lv','Nb','Dt','Js','Jg','Rt','1S','2S','1R','2R','1Ch','2Ch','Esd','Ne','Est','Jb','Ps','Pr','Ec','Ct','Es','Jr','La','Ez','Da','Os','Jl','Am','Ab','Jon','Mi','Na','Ha','So','Ag','Za','Ma','Mt','Mc','Lc','Jn','Ac','Rm','1Co','2Co','Ga','Ep','Ph','Col','1Th','2Th','1Ti','2Ti','Tt','Phm','He','Jc','1P','2P','1Jn','2Jn','3Jn','Jd','Ap'], 
    'ZH': ['创','出','利','民','申','书','士','得','撒上','撒下','王上','王下','代上','代下','拉','尼','斯','伯','诗','箴','传','歌','赛','耶','哀','结','但','何','珥','摩','俄','拿','弥','鸿','哈','番','该','亚','玛','太','可','路','约','徒','罗','林前','林后','加','弗','腓','西','帖前','帖后','提前','提后','多','门','来','雅','彼前','彼后','约一','约二','约三','犹','启'],
}

def to_sup(s):
    sups = {u'0': u'\u2070',
            u'1': u'\xb9',
            u'2': u'\xb2',
            u'3': u'\xb3',
            u'4': u'\u2074',
            u'5': u'\u2075',
            u'6': u'\u2076',
            u'7': u'\u2077',
            u'8': u'\u2078',
            u'9': u'\u2079',
            u'-': u'\u207B',}
    return ''.join(sups.get(char, char) for char in s)

def verse_select(lang, version, book, chapter, verseStart, verseEnd = 0):
    if verseEnd == 0:
        verseEnd = verseStart

    spacing = spacings.get(lang, ' ')

    tree = ET.parse('bible/' + lang + '/' + version + '.xml')
    root = tree.getroot()

    if book <= 39:
        testamentIndex = 0
        bookIndex = book - 1
    else:
        testamentIndex = 1
        bookIndex = book - 40
    chapterIndex = chapter - 1

    # special treatment for skipped or merged verse
    # [verses[], text]
    verseList = []

    # get whole chapter
    for verse in root[testamentIndex][bookIndex][chapterIndex]:
        num = int(verse.get('number'))

        # special case (merged verse)
        if version == '新标点和合本1988' and verse.text == '并于上节':
            verseList[-1][0].append(num)
            continue

        verseList.append([[num], verse.text])

    # select the verses and format them
    output = ''
    start = 10000
    end = -1

    for verse in verseList:
        if verse[0][0] >= verseStart and verse[0][0] <= verseEnd:
            # effective output verse range
            start = min(start, verse[0][0])
            end = max(end, verse[0][-1])

            # single verse
            if output == '' and verse[0][-1] >= verseEnd:
                output = verse[1]
                break

            # normal verse
            if verse[0][0] == verse[0][-1]:
                output += to_sup(str(verse[0][0])) + verse[1] + spacing
            else: # merged verse
                output += to_sup(str(verse[0][0]) + '-' + str(verse[0][-1])) + verse[1] + spacing

    label = bookAbbr.get(lang)[book - 1] + spacing + str(chapter) + ':' + str(start)
    if start != end:
        label += '-' + str(end)
    label += '  '

    if start == 10000 or end == -1:
        return ''
    
    return label + output
