from django.shortcuts import render
from django.http import HttpResponse
from freebible import read_web
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
import speech_recognition as sr





global web 
web= read_web()



def home(request):#This function returns default passage to be displayed when intially opened
    verses=[]
    bible={}
    chapter=1 #default chapter to be displayed
    verse=1 #default initial verse to be displayed

    for x in range(0,10): #stores the 10 verses to be displayed
        try:
            verses.append(web['Gen'][chapter][verse+x])
        except:
            break
    print(verses)
    bible['verses']=verses
    bible['book']=['Genesis',0]#Stores books full name and integer value
    bible['chapter']=str(chapter)
    bible['verse']=str(verse)
    bible['EndVerse']=str(verse+9)


    request.session['g_book']=0 #stores default data to global varibales to be accessed later
    request.session['g_chapter']=str(1)
    request.session['g_verse']=str(1)

    return render(request,'bible/home.html',bible)



def display(request):#This function displays passages to be when intially opened
    if request.method== 'POST':

        try:
            
            #accesses currently seected data from drop downs
            book = request.POST.get('book-selector')
            chapter = int(request.POST.get('chapter-selector')) 
            verse = int(request.POST.get('verse-selector'))
        
            CurrrentBibleData(request,book,chapter,verse)

        except: 
            try:

                #accesses previously saved global variable 
                book=int(request.session['g_book'])
                chapter= int(request.session['g_chapter'])
                verse= int(request.session['g_verse'])

            except:
                #sets book/chapter/verse value to a default value
                book=0
                chapter=0
                verse=0
        
        AbbrevietedBook=BookMapping(int(book))
        FullBook=FullBookMapping(int(book))
        verses=[]
        bible={}

        for x in range(0,10):
            try:
                verses.append(web[AbbrevietedBook][chapter][verse+x])
            except:
                break
        
        

        bible['verses']=verses
        bible['book']=[FullBook,book]
        bible['chapter']=str(chapter)
        bible['verse']=str(verse)
        bible['EndVerse']=str(verse+9)

        return render(request,'bible/home.html',bible)
    else:
        verses=[]
        bible={}
        chapter=1
        verse=1
        for x in range(0,10):
            try:
                verses.append(web['Gen'][chapter][verse+x])
            except:
                break
        print(verses)
        bible['verses']=verses
        bible['book']=['Genesis',0]
        bible['chapter']=str(chapter)
        bible['verse']=str(verse)
        bible['EndVerse']=str(verse+9)
        return render(request,'bible/home.html',bible)


def CurrrentBibleData(request,book,chapter,verse):  #Stores the data of the passage currently open in the single book screen to global variables to be accessed later.
    request.session['g_book']=book
    request.session['g_chapter']=str(chapter)
    request.session['g_verse']=str(verse)

    print("successful storage")


def nextpage(request):#This function displays the next 10 or avaliable verses in a chapter

    if request.method== 'POST':

        book= request.session.get('g_book')
        chapter = int(request.session.get('g_chapter'))
        verse =int(request.session.get('g_verse'))+10
        verses=[]
        bible={}
        f_verse=0
        AbbrevietedBook = BookMapping(int(book))
        FullBook=FullBookMapping(int(book))
        
        for x in range(0,10):

            try:
                verses.append(web[AbbrevietedBook][chapter][verse+x])
                f_verse=f_verse+1
            except Exception as e:
                break
        
        if len(verses)>0:

            bible['verses']=verses
            bible['book']=[FullBook,book]
            bible['chapter']=str(chapter)
            bible['verse']=str(verse)
            bible['EndVerse']=str(verse+(f_verse-1))

            CurrrentBibleData(request,book,chapter,verse)


            return render(request,'bible/home.html',bible)
        
        else:

            chapter=chapter+1
            verse=1
            
            for x in range(0,10):
                try:
                    verses.append(web[AbbrevietedBook][chapter][verse+x])
                    f_verse=f_verse+1
                except Exception as e:
                    break
            
            bible['verses']=verses
            bible['book']=[FullBook,book]
            bible['chapter']=str(chapter)
            bible['verse']=str(verse)
            bible['EndVerse']=str(verse+(f_verse-1))

            CurrrentBibleData(request,book,chapter,verse)

            

            if len(verses)==0:
                if AbbrevietedBook=='Rev':
                    chapter=1
                    verse=1
                    AbbrevietedBook = 'Rev'
                    FullBook='Revelation'
                    for x in range(0,10):
                        try:
                            verses.append(web[AbbrevietedBook][chapter][verse+x])
                            f_verse=f_verse+1
                        except Exception as e:
                            break
                    
                    bible['verses']=verses
                    bible['book']=[FullBook,book]
                    bible['chapter']=str(chapter)
                    bible['verse']=str(verse)
                    bible['EndVerse']=str(verse+(f_verse-1))

                    CurrrentBibleData(request,book,chapter,verse)

                    
                    return render(request,'bible/home.html',bible)
                else:
                    
                    chapter=1
                    verse=1
                    AbbrevietedBook = BookMapping(int(book)+1)
                    FullBook=FullBookMapping(int(book)+1)
                    for x in range(0,10):
                        try:
                            verses.append(web[AbbrevietedBook][chapter][verse+x])
                            f_verse=f_verse+1
                        except Exception as e:
                            break
                    bible['verses']=verses
                    bible['book']=[FullBook,book]
                    bible['chapter']=str(chapter)
                    bible['verse']=str(verse)
                    bible['EndVerse']=str(verse+(f_verse-1))

                    request.session['g_book']=int(book)+1
                    request.session['g_chapter']=str(chapter)
                    request.session['g_verse']=str(verse)

                    return render(request,'bible/home.html',bible)
            
       
        return render(request,'bible/home.html',bible)
   
    else:
        
        return render(request,'bible/home.html')

def BookIntMapping(book): #This function maps a bible books abbreviation to an integer value
    intmap={
    'gen': 0,
    'exo': 1,
    'lev': 2,
    'num': 3,
    'deut': 4,
    'josh': 5,
    'judg': 6,
    'rth': 7,
    '1 sam': 8,
    '2 sam': 9,
    '1 kgs': 10,
    '2 kgs': 11,
    '1 chron': 12,
    '2 chron': 13,
    'ezra': 14,
    'neh': 15,
    'esth': 16,
    'job': 17,
    'pslm': 18,
    'prov': 19,
    'eccles': 20,
    'song': 21,
    'isa': 22,
    'jer': 23,
    'lam': 24,
    'ezek': 25,
    'dan': 26,
    'hos': 27,
    'joel': 28,
    'amos': 29,
    'obad': 30,
    'jnh': 31,
    'micah': 32,
    'nah': 33,
    'hab': 34,
    'zeph': 35,
    'hag': 36,
    'zech': 37,
    'mal': 38,
    'matt': 39,
    'mark': 40,
    'luke': 41,
    'john': 42,
    'acts': 43,
    'rom': 44,
    '1 cor': 45,
    '2 cor': 46,
    'gal': 47,
    'eph': 48,
    'phil': 49,
    'col': 50,
    '1 thess': 51,
    '2 thess': 52,
    '1 tim': 53,
    '2 tim': 54,
    'titus': 55,
    'philem': 56,
    'hebrews': 57,
    'james': 58,
    '1 pet': 59,
    '2 pet': 60,
    '1 john': 61,
    '2 john': 62,
    '3 john': 63,
    'jude': 64,
    'rev': 65
}
    return intmap[book]

def BookMapping(book):#This function maps integer values to the corresponding acronyms
    
    book_mapping = {
                0: "Gen",
                1: "Exo",
                2: "Lev",
                3: "Num",
                4: "Deut",
                5: "Josh",
                6: "Judg",
                7: "Rth",
                8: "1 Sam",
                9: "2 Sam",
                10: "1 Kgs",
                11: "2 Kgs",
                12: "1 Chron",
                13: "2 Chron",
                14: "Ezra",
                15: "Neh",
                16: "Esth",
                17: "Job",
                18: "Pslm",
                19: "Prov",
                20: "Eccles",
                21: "Song",
                22: "Isa",
                23: "Jer",
                24: "Lam",
                25: "Ezek",
                26: "Dan",
                27: "Hos",
                28: "Joel",
                29: "Amos",
                30: "Obad",
                31:  "Jnh",
                32: "Micah",
                33: "Nah",
                34: "Hab",
                35: "Zeph",
                36: "Hag",
                37: "Zech",
                38: "Mal",
                39: "Matt",
                40: "Mark",
                41: "Luke",
                42: "John",
                43: "Acts",
                44: "Rom",
                45: "1 Cor",
                46: "2 Cor",
                47: "Gal",
                48: "Eph",
                49: "Phil",
                50: "Col",
                51: "1 Thess",
                52: "2 Thess",
                53: "1 Tim",
                54: "2 Tim",
                55: "Titus",
                56: "Philem",
                57: "Hebrews",
                58: "James",
                59: "1 Pet",
                60: "2 Pet",
                61: "1 John",
                62: "2 John",
                63: "3 John",
                64: "Jude",
                65: "Rev",
        }
    
    return book_mapping[int(book)]

def FullBookMapping(book):#Maps integer values to corresponding full book name
    
    fullbook_mapping = {
    0: 'Genesis',
    1: 'Exodus',
    2: 'Leviticus',
    3: 'Numbers',
    4: 'Deuteronomy',
    5: 'Joshua',
    6: 'Judges',
    7: 'Ruth',
    8: '1 Samuel',
    9: '2 Samuel',
    10: '1 Kings',
    11: '2 Kings',
    12: '1 Chronicles',
    13: '2 Chronicles',
    14: 'Ezra',
    15: 'Nehemiah',
    16: 'Esther',
    17: 'Job',
    18: 'Psalms',
    19: 'Proverbs',
    20: 'Ecclesiastes',
    21: 'Song of Solomon',
    22: 'Isaiah',
    23: 'Jeremiah',
    24: 'Lamentations',
    25: 'Ezekiel',
    26: 'Daniel',
    27: 'Hosea',
    28: 'Joel',
    29: 'Amos',
    30: 'Obadiah',
    31: 'Jonah',
    32: 'Micah',
    33: 'Nahum',
    34: 'Habakkuk',
    35: 'Zephaniah',
    36: 'Haggai',
    37: 'Zechariah',
    38: 'Malachi',
    39: 'Matthew',
    40: 'Mark',
    41: 'Luke',
    42: 'John',
    43: 'Acts',
    44: 'Romans',
    45: '1 Corinthians',
    46: '2 Corinthians',
    47: 'Galatians',
    48: 'Ephesians',
    49: 'Philippians',
    50: 'Colossians',
    51: '1 Thessalonians',
    52: '2 Thessalonians',
    53: '1 Timothy',
    54: '2 Timothy',
    55: 'Titus',
    56: 'Philemon',
    57: 'Hebrews',
    58: 'James',
    59: '1 Peter',
    60: '2 Peter',
    61: '1 John',
    62: '2 John',
    63: '3 John',
    64: 'Jude',
    65: 'Revelation',
}
    return fullbook_mapping[int(book)]

def voiceBookMapping(book): #Maps bible book from voice2text recognition to corresponding acronym
    bible_books = {
    "genesis": "Gen",
    "exodus": "Exo",
    "leviticus": "Lev",
    "numbers": "Num",
    "deuteronomy": "Deut",
    "joshua": "Josh",
    "judges": "Judg",
    "ruth": "Rth",
    "1 samuel": "1 Sam",
    "2 samuel": "2 Sam",
    "1 kings": "1 Kgs",
    "2 kings": "2 Kgs",
    "1 chronicles": "1 Chron",
    "2 chronicles": "2 Chron",
    "ezra": "Ezra",
    "nehemiah": "Neh",
    "esther": "Esth",
    "job": "Job",
    "psalms": "Pslm",
    "proverbs": "Prov",
    "ecclesiastes": "Eccles",
    "song of Solomon": "Song",
    "isaiah": "Isa",
    "jeremiah": "Jer",
    "lamentations": "Lam",
    "ezekiel": "Ezek",
    "daniel": "Dan",
    "hosea": "Hos",
    "joel": "Joel",
    "amos": "Amos",
    "obadiah": "Obad",
    "jonah": "Jnh",
    "micah": "Micah",
    "nahum": "Nah",
    "habakkuk": "Hab",
    "zephaniah": "Zeph",
    "haggai": "Hag",
    "zechariah": "Zech",
    "malachi": "Mal",
    "matthew": "Matt",
    "mark": "Mark",
    "luke": "Luke",
    "john": "John",
    "acts": "Acts",
    "romans": "Rom",
    "1 corinthians": "1 Cor",
    "2 corinthians": "2 Cor",
    "galatians": "Gal",
    "ephesians": "Eph",
    "philippians": "Phil",
    "colossians": "Col",
    "1 thessalonians": "1 Thess",
    "2 thessalonians": "2 Thess",
    "1 timothy": "1Tim",
    "2 timothy": "2Tim",
    "titus": "Titus",
    "philemon": "Philem",
    "hebrews": "Hebrews",
    "james": "James",
    "1 peter": "1 Pet",
    "2 peter": "2 Pet",
    "1 john": "1 John",
    "2 john": "2 John",
    "3 john": "3 John",
    "jude": "Jude",
    "revelation": "Rev"
}
    return bible_books[book]

def bookCheck(book):#This function actually checks whether book from voice2text recognition exists
    
    bible_book = [
    "genesis",
    "exodus",
    "leviticus",
    "numbers",
    "deuteronomy",
    "joshua",
    "judges",
    "ruth",
    "1 samuel",
    "2 samuel",
    "1 kings",
    "2 kings",
    "1 chronicles",
    "2 chronicles",
    "ezra",
    "nehemiah",
    "esther",
    "job",
    "psalms",
    "proverbs",
    "ecclesiastes",
    "Song of Solomon",
    "isaiah",
    "jeremiah",
    "lamentations",
    "ezekiel",
    "daniel",
    "hosea",
    "joel",
    "amos",
    "obadiah",
    "jonah",
    "micah",
    "nahum",
    "habakkuk",
    "zephaniah",
    "haggai",
    "zechariah",
    "malachi",
    "matthew",
    "mark",
    "luke",
    "john",
    "acts",
    "romans",
    "1 corinthians",
    "2 corinthians",
    "galatians",
    "ephesians",
    "philippians",
    "colossians",
    "1 thessalonians",
    "2 thessalonians",
    "1 timothy",
    "2 timothy",
    "titus",
    "philemon",
    "hebrews",
    "james",
    "1 peter",
    "2 peter",
    "1 john",
    "2 john",
    "3 john",
    "jude",
    "revelation"
]
    if book in bible_book:
        return True
    else:
        return False
    
def prevpage(request):#This function displays the previous 10 or avaliable verses in a chapter
    
    if request.method== 'POST':

        book= request.session.get('g_book')
        chapter = int(request.session.get('g_chapter'))
        verse =int(request.session.get('g_verse'))-10
        
        verses=[]
        bible={}
        f_verse=0

        AbbrevietedBook = BookMapping(book)
        FullBook=FullBookMapping(book)  
        
        for x in range(0,10):
            try:
                verses.append(web[AbbrevietedBook][chapter][verse+x])
                f_verse=f_verse+1
            except Exception as e:
                break
        
        if len(verses)>0:
            bible['verses']=verses
            bible['book']=[FullBook,book]
            bible['chapter']=str(chapter)
            bible['verse']=str(verse)
            bible['EndVerse']=str(verse+(f_verse-1))

            CurrrentBibleData(request,book,chapter,verse)

            
            return render(request,'bible/home.html',bible)
        
        else:
            
            chapter=chapter-1
            verse=1
            for x in range(0,10):
                
                try:
                    verses.append(web[AbbrevietedBook][chapter][verse+x])
                    f_verse=f_verse+1
                except Exception as e:
                    break
            
            bible['verses']=verses
            bible['book']=[FullBook,book]
            bible['chapter']=str(chapter)
            bible['verse']=str(verse)
            bible['EndVerse']=str(verse+(f_verse-1))

            CurrrentBibleData(request,book,chapter,verse)


            if len(verses)==0:
                if book=='Gen':
                    chapter=1
                    verse=1
                    AbbrevietedBook = 'Gen'
                    FullBook='Genesis'
                    for x in range(0,10):
                        try:
                            verses.append(web[AbbrevietedBook][chapter][verse+x])
                            f_verse=f_verse+1
                        except Exception as e:
                            break
                    bible['verses']=verses
                    bible['book']=[FullBook,book]
                    bible['chapter']=str(chapter)
                    bible['verse']=str(verse)
                    bible['EndVerse']=str(verse+(f_verse-1))

                    CurrrentBibleData(request,book,chapter,verse)

                    
                    return render(request,'bible/home.html',bible)
                
                else:
                    
                    chapter=1
                    verse=1
                    AbbrevietedBook = BookMapping(int(book)-1)
                    FullBook=FullBookMapping(int(book)-1)
                    
                    for x in range(0,10):
                        
                        try:
                            verses.append(web[AbbrevietedBook][chapter][verse+x])
                            f_verse=f_verse+1
                        
                        except Exception as e:
                            break
                    
                    bible['verses']=verses
                    bible['book']=[FullBook,book]
                    bible['chapter']=str(chapter)
                    bible['verse']=str(verse)
                    bible['EndVerse']=str(verse+(f_verse-1))

                    request.session['g_book']=int(book)-1
                    request.session['g_chapter']=str(chapter)
                    request.session['g_verse']=str(verse)

                    return render(request,'bible/home.html',bible)
        
        return render(request,'bible/home.html',bible)
    
    else:
        
        return render(request,'bible/home.html')

def split(request):#This function facilitates the split screen function where 2 seperate passages can be opened at the same time
    
    if request.method== 'POST':
        
        try:
            book = request.POST.get('book-selector')
            chapter = int(request.POST.get('chapter-selector'))
            verse = int(request.POST.get('verse-selector'))
            book2 = request.POST.get('book-selector2')
            chapter2 = int(request.POST.get('chapter-selector2'))
            verse2 = int(request.POST.get('verse-selector2'))
            print(book)
        except:
            book = 0
            chapter = 1
            verse = 1
            book2 = 0
            chapter2 = 1
            verse2 = 1
        
        if verse==0:
            verse=1
        if verse2==0:
            verse2=1
        if chapter==0:
            chapter=1
        if chapter2==0:
            chapter2=1

        left_AbbrevietedBook = BookMapping(int(book))
        left_FullBook=FullBookMapping(int(book))
        right_AbbrevietedBook=BookMapping(int(book2))
        right_FullBook=FullBookMapping(int(book2))

        verses=[]
        verses2=[]
        bible={}

        for x in range(0,10):
            try:
                verses.append(web[left_AbbrevietedBook][chapter][verse+x])
            except:
                break
        
        for x in range(0,10):
            try:
                verses2.append(web[right_AbbrevietedBook][chapter2][verse2+x])
            except:
                break
        
        bible['verses']=verses
        bible['verses2']=verses2
        bible['book']=[left_FullBook,book]
        bible['book2']=[right_FullBook,book2]
        bible['chapter']=str(chapter)
        bible['chapter2']=str(chapter2)
        bible['verse']=str(verse)
        bible['verse2']=str(verse2)
        bible['EndVerse']=str(verse+9)
        bible['EndVerse2']=str(verse2+9)


        return render(request,'bible/split.html',bible)
    
    else:
        
        verses=[]
        verses2=[]
        bible={}
        chapter=1
        verse=1
        for x in range(0,10):
            try:
                verses.append(web['Gen'][chapter][verse+x])
            except:
                break
        for x in range(0,10):
            try:
                verses2.append(web['Gen'][chapter][verse+x])
            except:
                break
        
        bible['verses']=verses
        bible['verses2']=verses2
        bible['book']=['Genesis',0]
        bible['book2']=['Genesis',0]
        bible['chapter']=str(chapter)
        bible['chapter2']=str(chapter)
        bible['verse']=str(verse)
        bible['verse2']=str(verse)
        bible['EndVerse']=str(verse+9)
        bible['EndVerse2']=str(verse+9)

        return render(request,'bible/split.html',bible)

def VoiceControl(request):#This function facilitates opening the bible with the voice
    bible={}
    NonDigitNumber={
    "first":1,
    "second":2,
    "third":3,
    "1st":1
    } 
    numbers=["first","second", "third","1st"] 

    r = sr.Recognizer()
    mic = sr.Microphone()
    listening = True

    with mic as source:
        r.adjust_for_ambient_noise(source)  # Optional: Adjust for ambient noise
    
        while listening:
            print("Listening for wake word...")
            audio = r.listen(source)

            try:
            # Use the speech recognition library to convert speech to text
                text = r.recognize_google(audio)
                print("You said:", text)
                speech_input=text.split(" ")

                if speech_input[0] in numbers:
                    try:
                        book=str(NonDigitNumber[speech_input[0]])+" "+speech_input[1].lower() #combines fiest word and second word to from full book name
                        chapter=int(speech_input[2])#chapter is ussually stored in third word
                        print(chapter)
                    except:
                        try:
                            book=str(NonDigitNumber[speech_input[0]])+" "+speech_input[1].lower()
                            chapter=1#if chapter is unable to be picked up default value of 1 is assigned to the chapter
                        except:
                            book="Genesis"
                            chapter=1
                            print("unable to open")#if both values are unable to be picked up default values are assigned to chapter and book
                            return render(request,'bible/home.html',bible)

                else:
                    try:
                        book=speech_input[0].lower()#book is usually first word in speech input list
                        chapter=speech_input[1]#chapter is usually second word in speech input list
                        if chapter=="one":#if chapter value is recorded in word form it is chaged to integer value, e.g. one->1
                            chapter=NonDigitNumber[chapter]
                    except:
                        book=speech_input[0].lower()
                        chapter=1
                
                try:
                    if bookCheck(book)==True:
                        print(book+"1")
                        print(voiceBookMapping("genesis"))
                        print(web[voiceBookMapping(book)][int(chapter)][1])
                        #BibleData=[voiceBookMapping(book),int(chapter),BookIntMapping(voiceBookMapping(book).lower()),speech_input[0]]
                        BibleData={
                            "book_acronym":voiceBookMapping(book),
                            "chapter":int(chapter),
                            "book_integer":BookIntMapping(voiceBookMapping(book).lower()),

                        }
                        print("data created")
                    
                     
                        print(BibleData)
                        listening = False
                        print("success")
                        verses=[]
                        bible={}

                        book=BibleData["book_acronym"]
                        chapter=int(BibleData["chapter"])
                        verse=1

                        for x in range(0,10):
                            try:
                                verses.append(web[book][chapter][verse+x])
                            except:
                                break
                        
                        bible['verses']=verses
                        bible['book']=[FullBookMapping(BookIntMapping(book.lower())),BibleData["book_integer"]]
                        bible['chapter']=str(chapter)
                        bible['verse']=str(verse)
                        bible['EndVerse']=str(verse+9)
    
                        CurrrentBibleData(request, BibleData["book_integer"],chapter,verse)
                        print("done")

                        return render(request,'bible/home.html',bible)
                    
                        
                except:
                    return render(request,'bible/home.html',bible)

                   
            
            except sr.UnknownValueError:
                print("Could not understand audio")
                return render(request,'bible/home.html',bible)

            except sr.RequestError as e:
                print("Error: {0}".format(e))
                return render(request,'bible/home.html',bible)




