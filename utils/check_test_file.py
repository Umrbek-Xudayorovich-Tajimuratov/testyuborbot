import codecs
import chardet
from loader import bot


def q_check(q, index,lang):
    if lang=='uz':
        definition= "Savolda xato bor!"
    elif lang=='ru':
        definition= "Есть ошибка в вопросе!"
    elif lang=='en':
        definition= "There is an error in the question!"

    if q[0].isalpha() and q[0:2].endswith("."):
        errors.append({"index":index, "definition": definition})
    

def a_check(a, is_a,index,lang):
    if lang=='uz':
        definition= f"Bu qatorda {is_a} aniqlanmadi."
        definition1= f"{is_a} rus/krill yozilgan"
    elif lang=='ru':
        definition= f"{is_a} не было определено в этой строке."
        definition1= f"{is_a} написано на русском языке/криль"
    elif lang=='en':
        definition= f"{is_a} was not defined in this line."
        definition1= f"{is_a} is written in Russian/Krill"

    if not a[0].isalpha() or not a.startswith(is_a):
        errors.append({"index":index, "definition": definition})
    if not a[0].isascii():
        errors.append({"index":index, "definition": definition1})
    

def ta_check(a, is_a,index,lang):
    if lang=='uz':
        definition= f"Bu qatorda {is_a} aniqlanmadi."
        definition1= f"ANSWER: {a[7:].strip()} rus/krill yozilgan"
    elif lang=='ru':
        definition= f"{is_a} не было определено в этой строке."
        definition1= f"ANSWER: {a[7:].strip()} написано на русском языке/криль"
    elif lang=='en':
        definition= f"{is_a} was not defined in this line."
        definition1= f"ANSWER: {a[7:].strip()} is written in Russian/Krill"

    if not a.startswith(is_a):
        errors.append({"index":index, "definition": definition})
    if not a[7:].strip().isascii() and len(a[7:].strip())!=0  and len(a[7:].strip())<=2:
        errors.append({"index":index, "definition": definition1})       


async def check_tests(file_path, bot_language):

    f = codecs.open(file_path, encoding='utf-8', errors='strict')
    
    i=1
    for index, line in enumerate(f):
        line = line.strip()
        if len(line) != 0:
            if(i%6==1):      q_check(q=line, index=index+1,lang=bot_language)
            elif(i%6==2):    a_check(a=line,is_a="A.",index=index+1,lang=bot_language)
            elif(i%6==3):    a_check(a=line,is_a="B.",index=index+1,lang=bot_language)
            elif(i%6==4):    a_check(a=line,is_a="C.",index=index+1,lang=bot_language)
            elif(i%6==5):    a_check(a=line,is_a="D.",index=index+1,lang=bot_language)
            elif(i%6==0):    ta_check(a=line, is_a="ANSWER:",index=index+1, lang=bot_language)
            i+=1

    return errors[:10]



async def check_utf(given_file, file_path):
    global errors
    errors=[]

    await bot.download(file=given_file, destination=file_path)

    try:
        with open(file_path, "rb") as f:
            byte_data = f.read()

        encoding = chardet.detect(byte_data)["encoding"]
        if encoding == "utf-8" or encoding == "UTF-8-SIG":
            # return "The file is encoded in UTF-8."
            return True
        else:
            # return f"The file is not encoded in UTF-8. Detected encoding: {encoding}"
            return False
    except Exception as e:
        return  f"An error occurred: {e}"
