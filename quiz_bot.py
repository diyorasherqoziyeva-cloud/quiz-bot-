import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ===================== SOZLAMALAR =====================
BOT_TOKEN = "8836642459:AAGIIMtmp3XPU564l2wMVcrz4kdxZiweZ6E"  # @BotFather dan olingan token

# ===================== LOGGING =====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== SAVOLLAR =====================
QUESTIONS = [
    {"id": 1, "question": "Darsning boshlanishini tashkil etish uy vazifasini tekshirish, darsning  maqsadi  va vazifasini  bayon  qilish,  yangi  materiallarni tushuntirish, mustahkamlash, darsga yakun yasash va uyga vazifa berish» tuzilishidagi darsning tipini ko\u2019rsating:", "correct": "Kombinatsion (aralash) dars", "options": ["Kombinatsion (aralash) dars", "Bilimlarni takrorlash va mustahkamlash darsi", "Yangi bilimlarni o\u2019rganish darsi", "Umumiylashtirish darsi"]},
    {"id": 2, "question": "Eng qadimgi madaniy boyliklarning o\u2019rganishdagi manbalar qaysi javobda to\u2019liq o\u2019z aksini topgan?", "correct": "Xalq og\u2019zaki ijodi, buyuk adiblar, allomalarning asarlari, arxeo-logik qazilmalar natijasida topilgan ashyolar", "options": ["Xalq og\u2019zaki ijodi, buyuk adiblar, allomalarning asarlari, arxeo-logik qazilmalar natijasida topilgan ashyolar", "Etnografiya va arxeologiya materiallari", "Xalq og\u2019zaki ijodi materiallari", "Buyuk adiblar, allomalarning ijodiy merosi"]},
    {"id": 3, "question": "\u00abPedagogiya, ya\u2019ni bola tarbiyasining fani demakdir\u00bb. Pedagogikaga bu ta\u2019rif kim tomonidan berilgan?", "correct": "Avloniy", "options": ["Avloniy", "Shakuriy", "Hamza", "S.Ayniy"]},
    {"id": 4, "question": "\u201cTakrorlash bilimning asosidir\u201d.Ushbu ibora qaysi pedagog olimga tegishli?", "correct": "Ushinskiy", "options": ["Ushinskiy", "Shakuriy", "Hamza", "Komenskiy"]},
    {"id": 5, "question": "\u201cBuyuk didaktika\u201d asarining mullifi?", "correct": "Komenskiy", "options": ["Komenskiy", "Ushinskiy", "Suxomlinskiy", "Makarenko"]},
    {"id": 6, "question": "Quyidagi dars tiplaridan qaysi biri to\u2019g\u2019ri ko\u2019rsatilgan?", "correct": "Yangi bilim berish darsi, bilimlarni mustahkamlash darsi, malaka va ko\u2019nikmalarni shakllantirish darsi, bilimlarni takrorlash va tizimlashtirish darsi, kombinatsion dars", "options": ["Yangi bilim berish darsi, bilimlarni mustahkamlash darsi, malaka va ko\u2019nikmalarni shakllantirish darsi, bilimlarni takrorlash va tizimlashtirish darsi, kombinatsion dars", "Dars, laboratoriya mashg\u2019uloti, seminar", "Sinf-dars tizimi, kurs tizimi, amaliy mashg\u2019ulotlar", "Turlari"]},
    {"id": 7, "question": "O\u2019quv jarayonida o\u2019qituvchi va o\u2019quvchilarning birgalikdagi faoliyati usullariga nima deyiladi?", "correct": "Ta\u2019lim metodlari", "options": ["Ta\u2019lim metodlari", "Ta\u2019lim vositalari", "Ta\u2019lim shakllari", "Ta\u2019lim metodlari"]},
    {"id": 8, "question": "O\u2019zbekiston Respublikasida majburiy ta\u2019lim necha yilni tashkil qiladi?", "correct": "12 yil", "options": ["12 yil", "11 yil", "10 yil", "9 yil"]},
    {"id": 9, "question": "\u201cMen butun faoliyatimni shu ikki so\u2019z bilan ifodalay olaman\u201d degan kim?", "correct": "Suxomlinskiy", "options": ["Suxomlinskiy", "Ushinskiy", "Makarenko", "Bolani tarbiyalayman va o\u2019qitaman"]},
    {"id": 10, "question": "IX asrda yashab ijod etgan buyuk alloma, matematik, geograf, astronom, \u201cAlgebra\u201d kitobining muallifi?", "correct": "Al-Xorazmiy", "options": ["Al-Xorazmiy", "Al-Beruniy", "Al-Farg\u2019oniy", "Al-Farg\u2019oniy"]},
    {"id": 11, "question": "Pedagogikaning asosiy vazifalari nima?", "correct": "Tarbiya, ta\u2019lim va o\u2019qitish qonuniyatlarini o\u2019rganish", "options": ["Tarbiya, ta\u2019lim va o\u2019qitish qonuniyatlarini o\u2019rganish", "Faqat ta\u2019lim qonuniyatlarini o\u2019rganish", "Faqat tarbiya qonuniyatlarini o\u2019rganish", "Psixologik qonuniyatlarni o\u2019rganish"]},
    {"id": 12, "question": "Didaktika nima?", "correct": "Ta\u2019lim nazariyasi", "options": ["Ta\u2019lim nazariyasi", "Tarbiya nazariyasi", "Boshqaruv nazariyasi", "Psixologiya bo\u2019limi"]},
    {"id": 13, "question": "O\u2019quvchilarda bilim, ko\u2019nikma va malakalarni shakllantirishga qaratilgan maqsadli faoliyat nima deyiladi?", "correct": "Ta\u2019lim", "options": ["Ta\u2019lim", "Tarbiya", "Rivojlantirish", "Shakllantirish"]},
    {"id": 14, "question": "Tarbiyaning asosiy maqsadi nima?", "correct": "Barkamol shaxsni shakllantirish", "options": ["Barkamol shaxsni shakllantirish", "Bilim berish", "Ko\u2019nikma shakllantirish", "Malaka oshirish"]},
    {"id": 15, "question": "Jan Jak Russo qaysi davlat pedagogi?", "correct": "Frantsuz", "options": ["Frantsuz", "Nemis", "Ingliz", "Rus"]},
    {"id": 16, "question": "Pedagogika fani qachon mustaqil fan sifatida ajralib chiqdi?", "correct": "XVII asrda", "options": ["XVII asrda", "XVI asrda", "XVIII asrda", "XIX asrda"]},
    {"id": 17, "question": "Pedagogikada \u201cMetod\u201d so\u2019zi qaysi tildan olingan?", "correct": "Yunoncha", "options": ["Yunoncha", "Lotincha", "Arabcha", "Forscha"]},
    {"id": 18, "question": "O\u2019quv dasturi nima?", "correct": "O\u2019quv predmetining mazmunini belgilaydigan davlat hujjati", "options": ["O\u2019quv predmetining mazmunini belgilaydigan davlat hujjati", "O\u2019quv rejasi", "Darslik", "Metodik qo\u2019llanma"]},
    {"id": 19, "question": "O\u2019quv rejasi nima?", "correct": "O\u2019quv predmetlari ro\u2019yxati va ularning o\u2019qitilish tartibini belgilaydigan hujjat", "options": ["O\u2019quv predmetlari ro\u2019yxati va ularning o\u2019qitilish tartibini belgilaydigan hujjat", "O\u2019quv dasturi", "Darslik", "O\u2019quv materiali"]},
    {"id": 20, "question": "Shaxsga yo\u2019naltirilgan ta\u2019lim texnologiyasining asosiy g\u2019oyasi nima?", "correct": "O\u2019quvchini ta\u2019lim jarayonining markaziga qo\u2019yish", "options": ["O\u2019quvchini ta\u2019lim jarayonining markaziga qo\u2019yish", "O\u2019qituvchining rolini oshirish", "Bilimlarni tizimlashtirish", "Darslikka asoslanish"]},
    {"id": 21, "question": "Ta\u2019lim jarayonida o\u2019quvchilarning mustaqil ishini tashkil etish usuli nima deyiladi?", "correct": "Mustaqil ish metodi", "options": ["Mustaqil ish metodi", "Og\u2019zaki bayon metodi", "Ko\u2019rgazmali metod", "Amaliy metod"]},
    {"id": 22, "question": "Interfaol metodlar nima?", "correct": "O\u2019quvchilarning faol ishtirokini ta\u2019minlovchi o\u2019qitish metodlari", "options": ["O\u2019quvchilarning faol ishtirokini ta\u2019minlovchi o\u2019qitish metodlari", "O\u2019qituvchi markazli metodlar", "Faqat og\u2019zaki metodlar", "Faqat yozma metodlar"]},
    {"id": 23, "question": "Pedagogik texnologiya deganda nima tushuniladi?", "correct": "Ta\u2019lim-tarbiya jarayonini loyihalash va amalga oshirishning tizimli yondashuvi", "options": ["Ta\u2019lim-tarbiya jarayonini loyihalash va amalga oshirishning tizimli yondashuvi", "Faqat texnik vositalar", "Kompyuter texnologiyalari", "Audio-vizual vositalar"]},
    {"id": 24, "question": "Baholashning asosiy funksiyalari qaysilar?", "correct": "Nazorat, rag\u2019batlantirish, ma\u2019lumot berish", "options": ["Nazorat, rag\u2019batlantirish, ma\u2019lumot berish", "Faqat nazorat", "Faqat rag\u2019batlantirish", "Faqat ma\u2019lumot berish"]},
    {"id": 25, "question": "Dars o\u2019tishning asosiy bosqichlari qaysilar?", "correct": "Tashkiliy bosqich, asosiy bosqich, yakuniy bosqich", "options": ["Tashkiliy bosqich, asosiy bosqich, yakuniy bosqich", "Faqat asosiy bosqich", "Kirish va yakun", "Savol-javob va mustahkamlash"]},
    {"id": 26, "question": "O\u2019quvchilarga bilim berish jarayonining asosiy mantig\u2019i nima?", "correct": "Idrok etish, tushunish, eslab qolish, qo\u2019llash", "options": ["Idrok etish, tushunish, eslab qolish, qo\u2019llash", "Faqat idrok etish", "Faqat eslab qolish", "Faqat qo\u2019llash"]},
    {"id": 27, "question": "Sinf-dars tizimini kim yaratgan?", "correct": "Ya.A.Komenskiy", "options": ["Ya.A.Komenskiy", "J.J.Russo", "I.G.Pestalotstsi", "K.D.Ushinskiy"]},
    {"id": 28, "question": "Pedagogik muloqotning asosiy shakllari qaysilar?", "correct": "Og\u2019zaki, yozma, noverbal", "options": ["Og\u2019zaki, yozma, noverbal", "Faqat og\u2019zaki", "Faqat yozma", "Faqat noverbal"]},
    {"id": 29, "question": "O\u2019quv-tarbiya jarayonining ikki tomoni qaysilar?", "correct": "O\u2019qitish va o\u2019qish", "options": ["O\u2019qitish va o\u2019qish", "Tarbiya va o\u2019qitish", "Bilim va ko\u2019nikma", "Metod va shakl"]},
    {"id": 30, "question": "Pedagogik faoliyatning asosiy tarkibiy qismlari?", "correct": "Loyihalash, tashkil etish, kommunikativ, gnostik", "options": ["Loyihalash, tashkil etish, kommunikativ, gnostik", "Faqat o\u2019qitish", "Faqat tarbiya", "Faqat nazorat"]},
    {"id": 31, "question": "Blooming taksonomiyasining birinchi darajasi nima?", "correct": "Bilish (Knowledge)", "options": ["Bilish (Knowledge)", "Tushunish", "Qo\u2019llash", "Tahlil"]},
    {"id": 32, "question": "Xolistic baholash nima?", "correct": "Yaxlit, umumiy baholash", "options": ["Yaxlit, umumiy baholash", "Qisman baholash", "Raqamli baholash", "Og\u2019zaki baholash"]},
    {"id": 33, "question": "Formativ baholash qachon amalga oshiriladi?", "correct": "O\u2019quv jarayoni davomida", "options": ["O\u2019quv jarayoni davomida", "Yakunida", "Boshida", "Maxsus sessiyada"]},
    {"id": 34, "question": "Summativ baholash qachon amalga oshiriladi?", "correct": "O\u2019quv jarayoni yakunida", "options": ["O\u2019quv jarayoni yakunida", "Jarayon davomida", "Boshida", "Har kuni"]},
    {"id": 35, "question": "Differentsial ta\u2019lim nima?", "correct": "O\u2019quvchilarning individual xususiyatlarini hisobga olgan holda ta\u2019lim berish", "options": ["O\u2019quvchilarning individual xususiyatlarini hisobga olgan holda ta\u2019lim berish", "Bir xil ta\u2019lim berish", "Guruhga ta\u2019lim berish", "Masofaviy ta\u2019lim"]},
    {"id": 36, "question": "O\u2019quvchilarni o\u2019qishga motivatsiyalashning asosiy yo\u2019llari?", "correct": "Qiziqarli materiallar, muvaffaqiyat holati, rag\u2019batlantirish", "options": ["Qiziqarli materiallar, muvaffaqiyat holati, rag\u2019batlantirish", "Faqat baholash", "Faqat jazolash", "Faqat topshiriq berish"]},
    {"id": 37, "question": "O\u2019quvchilar bilimini og\u2019zaki tekshirishning asosiy shakllari?", "correct": "Individual so\u2019rov, frontal so\u2019rov, o\u2019zaro so\u2019rov", "options": ["Individual so\u2019rov, frontal so\u2019rov, o\u2019zaro so\u2019rov", "Faqat individual", "Faqat frontal", "Faqat test"]},
    {"id": 38, "question": "Pedagogikada \u201cindividual yondashuv\u201d deganda nima tushuniladi?", "correct": "Har bir o\u2019quvchining xususiyatlarini hisobga olish", "options": ["Har bir o\u2019quvchining xususiyatlarini hisobga olish", "Alohida dars o\u2019tish", "Faqat iqtidorli o\u2019quvchilar bilan ishlash", "Zaif o\u2019quvchilar bilan ishlash"]},
    {"id": 39, "question": "Tarbiyaviy ishning asosiy yo\u2019nalishlari?", "correct": "Axloqiy, aqliy, jismoniy, estetik, mehnat tarbiyasi", "options": ["Axloqiy, aqliy, jismoniy, estetik, mehnat tarbiyasi", "Faqat axloqiy", "Faqat aqliy", "Faqat jismoniy"]},
    {"id": 40, "question": "Pedagogik mahorat nima?", "correct": "O\u2019qituvchining yuqori darajada kasbiy tayyorgarligi va tajribasi", "options": ["O\u2019qituvchining yuqori darajada kasbiy tayyorgarligi va tajribasi", "Faqat bilim", "Faqat tajriba", "Faqat usul bilish"]},
    {"id": 41, "question": "Inson rivojlanishiga ta\u2019sir etuvchi asosiy omillar?", "correct": "Irsiyat, muhit, tarbiya va o\u2019z-o\u2019zini rivojlantirish", "options": ["Irsiyat, muhit, tarbiya va o\u2019z-o\u2019zini rivojlantirish", "Faqat irsiyat", "Faqat muhit", "Faqat tarbiya"]},
    {"id": 42, "question": "Pedagogik diagnostika nima?", "correct": "O\u2019quvchilarning bilim va rivojlanish darajasini aniqlash jarayoni", "options": ["O\u2019quvchilarning bilim va rivojlanish darajasini aniqlash jarayoni", "Tibbiy tekshiruv", "Psixologik test", "O\u2019quvchini kuzatish"]},
    {"id": 43, "question": "Loyihaviy ta\u2019lim texnologiyasi nima?", "correct": "O\u2019quvchilar mustaqil loyiha ustida ishlaydigan ta\u2019lim usuli", "options": ["O\u2019quvchilar mustaqil loyiha ustida ishlaydigan ta\u2019lim usuli", "O\u2019qituvchi loyiha tayyorlaydigan usul", "Guruh o\u2019qishi", "Individual o\u2019qish"]},
    {"id": 44, "question": "Kooperativ o\u2019qish nima?", "correct": "O\u2019quvchilar birgalikda ishlash orqali o\u2019rganadigan usul", "options": ["O\u2019quvchilar birgalikda ishlash orqali o\u2019rganadigan usul", "Individual o\u2019qish", "Raqobatli o\u2019qish", "Mustaqil o\u2019qish"]},
    {"id": 45, "question": "O\u2019qituvchining kasbiy kompetentligi nima?", "correct": "O\u2019qituvchining kasbiy vazifalarni sifatli bajarish qobiliyati", "options": ["O\u2019qituvchining kasbiy vazifalarni sifatli bajarish qobiliyati", "Faqat bilim", "Faqat diplom", "Faqat tajriba"]},
    {"id": 46, "question": "CLIL texnologiyasi nima?", "correct": "Mazmun va til integratsiyalangan o\u2019qish", "options": ["Mazmun va til integratsiyalangan o\u2019qish", "Faqat til o\u2019qitish", "Faqat mazmun o\u2019qitish", "Kompyuter orqali o\u2019qish"]},
    {"id": 47, "question": "Refleksiya nima?", "correct": "O\u2019z faoliyatini tahlil qilish va baholash", "options": ["O\u2019z faoliyatini tahlil qilish va baholash", "Boshqalarni baholash", "Dars rejalari", "Test natijalari"]},
    {"id": 48, "question": "Faol ta\u2019lim metodlari deganda nima tushuniladi?", "correct": "O\u2019quvchilarni ta\u2019lim jarayoniga faol jalb etuvchi metodlar", "options": ["O\u2019quvchilarni ta\u2019lim jarayoniga faol jalb etuvchi metodlar", "O\u2019qituvchi faol bo\u2019ladigan metodlar", "Kitob o\u2019qish metodlari", "Tinglash metodlari"]},
    {"id": 49, "question": "Muammoli ta\u2019lim nima?", "correct": "O\u2019quvchilar muammolarni mustaqil hal etish orqali o\u2019rganadigan ta\u2019lim turi", "options": ["O\u2019quvchilar muammolarni mustaqil hal etish orqali o\u2019rganadigan ta\u2019lim turi", "Muammosiz ta\u2019lim", "Faqat nazariy ta\u2019lim", "Raqamli ta\u2019lim"]},
    {"id": 50, "question": "Masofaviy ta\u2019lim nima?", "correct": "O\u2019qituvchi va o\u2019quvchi bir joyda bo\u2019lmasdan amalga oshiriladigan ta\u2019lim", "options": ["O\u2019qituvchi va o\u2019quvchi bir joyda bo\u2019lmasdan amalga oshiriladigan ta\u2019lim", "Faqat internet orqali ta\u2019lim", "Uyda ta\u2019lim", "TV orqali ta\u2019lim"]},
    {"id": 51, "question": "Pedagogika fanining predmeti nima?", "correct": "Tarbiya, ta\u2019lim va o\u2019qitish jarayonlari", "options": ["Tarbiya, ta\u2019lim va o\u2019qitish jarayonlari", "Faqat o\u2019qitish", "Faqat tarbiya", "Bola psixologiyasi"]},
    {"id": 52, "question": "Umumpedagogika nima o\u2019rganadi?", "correct": "Tarbiya, ta\u2019lim va o\u2019qitishning umumiy qonuniyatlari", "options": ["Tarbiya, ta\u2019lim va o\u2019qitishning umumiy qonuniyatlari", "Maktabgacha tarbiya", "Oliy ta\u2019lim", "Maxsus ta\u2019lim"]},
    {"id": 53, "question": "Ta\u2019lim tizimining asosiy bo\u2019g\u2019inlari?", "correct": "Maktabgacha, umumiy o\u2019rta, o\u2019rta maxsus, oliy ta\u2019lim", "options": ["Maktabgacha, umumiy o\u2019rta, o\u2019rta maxsus, oliy ta\u2019lim", "Faqat umumiy o\u2019rta", "Faqat oliy", "Faqat boshlang\u2019ich"]},
    {"id": 54, "question": "Pedagog etikasi nima?", "correct": "Pedagog faoliyatini tartibga soluvchi axloqiy me\u2019yorlar tizimi", "options": ["Pedagog faoliyatini tartibga soluvchi axloqiy me\u2019yorlar tizimi", "Faqat qoidalar", "Faqat huquqlar", "Ish vaqti"]},
    {"id": 55, "question": "Ta\u2019lim sifatini oshirishning asosiy yo\u2019llari?", "correct": "Zamonaviy metodlarni qo\u2019llash, moddiy-texnik bazani mustahkamlash, kadrlar tayyorlash", "options": ["Zamonaviy metodlarni qo\u2019llash, moddiy-texnik bazani mustahkamlash, kadrlar tayyorlash", "Faqat yangi darsliklar", "Faqat imtihonlar", "Faqat nazorat"]},
    {"id": 56, "question": "O\u2019quvchilar bilimini yozma tekshirishning asosiy shakllari?", "correct": "Nazorat ishi, diktant, insho, test", "options": ["Nazorat ishi, diktant, insho, test", "Faqat test", "Faqat diktant", "Faqat insho"]},
    {"id": 57, "question": "Inklyuziv ta\u2019lim nima?", "correct": "Maxsus ehtiyojli bolalarni umumta\u2019lim maktablarida o\u2019qitish", "options": ["Maxsus ehtiyojli bolalarni umumta\u2019lim maktablarida o\u2019qitish", "Faqat sog\u2019lom bolalar uchun ta\u2019lim", "Maxsus maktablarda ta\u2019lim", "Masofaviy ta\u2019lim"]},
    {"id": 58, "question": "Pedagogik kuzatish nima?", "correct": "O\u2019quv-tarbiya jarayonini maqsadli va rejali ravishda kuzatish", "options": ["O\u2019quv-tarbiya jarayonini maqsadli va rejali ravishda kuzatish", "Tasodifiy kuzatish", "Faqat o\u2019quvchi xatti-harakatini kuzatish", "Dars sifatini baholash"]},
    {"id": 59, "question": "Sokratik suhbat metodi nima?", "correct": "Savol-javob orqali o\u2019quvchini mustaqil fikrlashga undash metodi", "options": ["Savol-javob orqali o\u2019quvchini mustaqil fikrlashga undash metodi", "Ma\u2019ruza o\u2019qish", "Test o\u2019tkazish", "Insho yozish"]},
    {"id": 60, "question": "Pedagogikada \u201cskaffold\u201d nima?", "correct": "O\u2019quvchiga qiyin vazifani bajarishda ko\u2019rsatiladigan vaqtinchalik yordam", "options": ["O\u2019quvchiga qiyin vazifani bajarishda ko\u2019rsatiladigan vaqtinchalik yordam", "Doimiy yordam", "Qurilish termini", "Test turi"]},
    {"id": 61, "question": "Ta\u2019limning tarbiyaviy funksiyasi nima?", "correct": "O\u2019quvchilarda shaxsiy fazilatlarni shakllantirish", "options": ["O\u2019quvchilarda shaxsiy fazilatlarni shakllantirish", "Bilim berish", "Malaka oshirish", "Nazorat qilish"]},
    {"id": 62, "question": "Ta\u2019limning rivojlantiruvchi funksiyasi nima?", "correct": "O\u2019quvchilarning aqliy va jismoniy rivojlanishini ta\u2019minlash", "options": ["O\u2019quvchilarning aqliy va jismoniy rivojlanishini ta\u2019minlash", "Bilim berish", "Tarbiyalash", "Nazorat qilish"]},
    {"id": 63, "question": "O\u2019quv-kognitiv kompetentlik nima?", "correct": "O\u2019quvchining mustaqil o\u2019qish va bilim olish qobiliyati", "options": ["O\u2019quvchining mustaqil o\u2019qish va bilim olish qobiliyati", "Faqat bilim", "Faqat ko\u2019nikma", "Faqat malaka"]},
    {"id": 64, "question": "Axborot-kommunikatsiya texnologiyalari ta\u2019limdagi roli?", "correct": "Ta\u2019lim sifatini oshirish va jarayonni zamonaviylashtirish", "options": ["Ta\u2019lim sifatini oshirish va jarayonni zamonaviylashtirish", "Faqat kompyuter o\u2019rgatish", "O\u2019qituvchini almashtirish", "Faqat internet ishlatish"]},
    {"id": 65, "question": "Ta\u2019lim standartlari nima?", "correct": "Ta\u2019lim sifatiga qo\u2019yiladigan davlat talablari", "options": ["Ta\u2019lim sifatiga qo\u2019yiladigan davlat talablari", "Darslik talablari", "O\u2019qituvchi talablari", "Bino talablari"]},
    {"id": 66, "question": "Modulli ta\u2019lim nima?", "correct": "Ta\u2019lim mazmunini mustaqil o\u2019rganish bloklariga ajratish", "options": ["Ta\u2019lim mazmunini mustaqil o\u2019rganish bloklariga ajratish", "Faqat amaliy ta\u2019lim", "Masofaviy ta\u2019lim", "Guruhli o\u2019qish"]},
    {"id": 67, "question": "Pedagogik kommunikatsiya nima?", "correct": "O\u2019qituvchi va o\u2019quvchilar o\u2019rtasidagi muloqot jarayoni", "options": ["O\u2019qituvchi va o\u2019quvchilar o\u2019rtasidagi muloqot jarayoni", "Faqat og\u2019zaki muloqot", "Faqat yozishma", "Faqat ishoralar"]},
    {"id": 68, "question": "Ta\u2019lim muhiti nima?", "correct": "Ta\u2019lim jarayoni amalga oshiriladigan barcha shart-sharoit va resurslar majmui", "options": ["Ta\u2019lim jarayoni amalga oshiriladigan barcha shart-sharoit va resurslar majmui", "Faqat sinf xonasi", "Faqat maktab", "Faqat darslik"]},
    {"id": 69, "question": "Pedagogik eksperiment nima?", "correct": "Ta\u2019lim-tarbiya jarayonini o\u2019rganish uchun maxsus tashkil etilgan tajriba", "options": ["Ta\u2019lim-tarbiya jarayonini o\u2019rganish uchun maxsus tashkil etilgan tajriba", "Kimyo tajribasi", "Fizika tajribasi", "O\u2019quvchilarni sinash"]},
    {"id": 70, "question": "Pedagogik maqsad nima?", "correct": "Ta\u2019lim-tarbiya jarayonida erishilishi mo\u2019ljallangan natija", "options": ["Ta\u2019lim-tarbiya jarayonida erishilishi mo\u2019ljallangan natija", "Dars rejasi", "O\u2019quv dasturi", "Darslik"]},
    {"id": 71, "question": "Shaxsning rivojlanishi qanday jarayon?", "correct": "Miqdoriy va sifatiy o\u2019zgarishlar jarayoni", "options": ["Miqdoriy va sifatiy o\u2019zgarishlar jarayoni", "Faqat jismoniy o\u2019sish", "Faqat bilim ortish", "Faqat yosh ulg\u2019ayish"]},
    {"id": 72, "question": "Ontogenez nima?", "correct": "Organizmning tug\u2019ilishidan to o\u2019limiga qadar rivojlanish jarayoni", "options": ["Organizmning tug\u2019ilishidan to o\u2019limiga qadar rivojlanish jarayoni", "Irqiy rivojlanish", "Faqat bolalik davri", "Faqat o\u2039smirlik davri"]},
    {"id": 73, "question": "Filogenez nima?", "correct": "Insoniyatning tarixiy rivojlanish jarayoni", "options": ["Insoniyatning tarixiy rivojlanish jarayoni", "Individual rivojlanish", "Bolalik davri", "O\u2039smirlik davri"]},
    {"id": 74, "question": "Sensomotor rivojlanish davri qaysi yoshdagi bolalarga xos?", "correct": "0-2 yosh", "options": ["0-2 yosh", "2-7 yosh", "7-11 yosh", "11-15 yosh"]},
    {"id": 75, "question": "Piajet bo\u2019yicha operatsiyalardan oldingi davr qaysi yoshga to\u2019g\u2019ri keladi?", "correct": "2-7 yosh", "options": ["2-7 yosh", "0-2 yosh", "7-11 yosh", "11-15 yosh"]},
    {"id": 76, "question": "Yaqin rivojlanish zonasi konsepsiyasini kim yaratgan?", "correct": "L.S.Vigotskiy", "options": ["L.S.Vigotskiy", "J.Piaje", "E.Erikson", "A.Maslov"]},
    {"id": 77, "question": "Yaqin rivojlanish zonasi nima?", "correct": "Bola mustaqil bajara olmaydigan, lekin kattalar yordamida bajara oladigan vazifalar darajasi", "options": ["Bola mustaqil bajara olmaydigan, lekin kattalar yordamida bajara oladigan vazifalar darajasi", "Bola mustaqil bajara oladigan vazifalar", "Juda qiyin vazifalar", "Juda oson vazifalar"]},
    {"id": 78, "question": "Maslov ehtiyojlar piramidasining eng pastki darajasi?", "correct": "Fiziologik ehtiyojlar", "options": ["Fiziologik ehtiyojlar", "Xavfsizlik ehtiyoji", "Ijtimoiy ehtiyojlar", "O\u2019z-o\u2019zini namoyon etish"]},
    {"id": 79, "question": "Maslov ehtiyojlar piramidasining eng yuqori darajasi?", "correct": "O\u2019z-o\u2019zini namoyon etish", "options": ["O\u2019z-o\u2019zini namoyon etish", "Fiziologik ehtiyojlar", "Xavfsizlik ehtiyoji", "E\u2019tirof ehtiyoji"]},
    {"id": 80, "question": "Konstruktivizm ta\u2019lim nazariyasiga ko\u2019ra bilim qanday hosil bo\u2019ladi?", "correct": "O\u2019quvchi o\u2019z tajribasi orqali mustaqil ravishda", "options": ["O\u2019quvchi o\u2019z tajribasi orqali mustaqil ravishda", "O\u2019qituvchidan tayyor holda", "Darslikdan", "Yod olish orqali"]},
    {"id": 81, "question": "Behaviorizm ta\u2019lim nazariyasining asosiy g\u2019oyasi?", "correct": "Stimul-reaktsiya orqali xulq-atvorni shakllantirish", "options": ["Stimul-reaktsiya orqali xulq-atvorni shakllantirish", "Tafakkurni rivojlantirish", "Motivatsiyani oshirish", "Ijodkorlikni rivojlantirish"]},
    {"id": 82, "question": "Kognitivizm ta\u2019lim nazariyasining asosiy g\u2019oyasi?", "correct": "Bilish jarayonlari va aqliy rivojlanishni o\u2019rganish", "options": ["Bilish jarayonlari va aqliy rivojlanishni o\u2019rganish", "Xulq-atvorni shakllantirish", "Ijtimoiy ta\u2019sir", "Motivatsiya"]},
    {"id": 83, "question": "Ta\u2019limda \u201cflipped classroom\u201d (teskari sinf) nima?", "correct": "Uyda yangi material o\u2019rganib, sinfda amaliy mashq qilish", "options": ["Uyda yangi material o\u2019rganib, sinfda amaliy mashq qilish", "Sinfda yangi material, uyda mustahkamlash", "Faqat onlayn ta\u2019lim", "Faqat amaliy ta\u2019lim"]},
    {"id": 84, "question": "Gamifikatsiya ta\u2019limda nima?", "correct": "Ta\u2019lim jarayoniga o\u2019yin elementlarini kiritish", "options": ["Ta\u2019lim jarayoniga o\u2019yin elementlarini kiritish", "Faqat kompyuter o\u2019yinlari", "Sport o\u2019yinlari", "Faqat qiziqarli darslar"]},
    {"id": 85, "question": "Metakognitsiya nima?", "correct": "O\u2019z bilish jarayonini anglash va boshqarish qobiliyati", "options": ["O\u2019z bilish jarayonini anglash va boshqarish qobiliyati", "Yuqori bilim", "Ko\u2019p bilim", "Tez o\u2019rganish"]},
    {"id": 86, "question": "Ta\u2019limda \u201ctransfer\u201d nima?", "correct": "Bir vaziyatda o\u2019rganilganlarni boshqa vaziyatga ko\u2019chirish", "options": ["Bir vaziyatda o\u2019rganilganlarni boshqa vaziyatga ko\u2019chirish", "Bilim uzatish", "Ma\u2019lumot saqlash", "O\u2019quvchini o\u2019tkazish"]},
    {"id": 87, "question": "Kritik tafakkur nima?", "correct": "Ma\u2019lumotlarni tanqidiy tahlil qilish va asosli xulosa chiqarish qobiliyati", "options": ["Ma\u2019lumotlarni tanqidiy tahlil qilish va asosli xulosa chiqarish qobiliyati", "Faqat tanqid qilish", "Faqat tahlil qilish", "Ma\u2019lumot to\u2019plash"]},
    {"id": 88, "question": "XXI asr ko\u2019nikmalari deb nimalar ataladi?", "correct": "Kritik tafakkur, ijodkorlik, muloqot, hamkorlik (4C)", "options": ["Kritik tafakkur, ijodkorlik, muloqot, hamkorlik (4C)", "Faqat kompyuter ko\u2019nikmalari", "Faqat til ko\u2019nikmalari", "Faqat matematik ko\u2019nikmalar"]},
    {"id": 89, "question": "STEM ta\u2019limi nima?", "correct": "Fan, texnologiya, muhandislik va matematikani integratsiyalash", "options": ["Fan, texnologiya, muhandislik va matematikani integratsiyalash", "Faqat matematika", "Faqat fan", "Faqat texnologiya"]},
    {"id": 90, "question": "O\u2019quvchi markazli ta\u2019limning asosiy xususiyati?", "correct": "O\u2019quvchining faol ishtiroki va mustaqilligi", "options": ["O\u2019quvchining faol ishtiroki va mustaqilligi", "O\u2019qituvchi asosiy rol o\u2019ynaydi", "Kitob asosiy manba", "Test asosiy baholash vositasi"]},
    {"id": 91, "question": "Ta\u2019limda maqsad qo\u2019yishning SMART tamoyili nima?", "correct": "Aniq, o\u2019lchanadigan, erishish mumkin, real, vaqt chegaralangan", "options": ["Aniq, o\u2019lchanadigan, erishish mumkin, real, vaqt chegaralangan", "Faqat aniq va real", "Faqat o\u2019lchanadigan", "Faqat vaqt chegaralangan"]},
    {"id": 92, "question": "Peer assessment (tengdoshlar baholash) nima?", "correct": "O\u2019quvchilarning bir-birini baholashi", "options": ["O\u2019quvchilarning bir-birini baholashi", "O\u2019qituvchi baholashi", "Ota-ona baholashi", "Ekspert baholashi"]},
    {"id": 93, "question": "Portfolio ta\u2019limda nima?", "correct": "O\u2019quvchi ishlarining to\u2019plami, rivojlanishni ko\u2019rsatuvchi hujjat", "options": ["O\u2019quvchi ishlarining to\u2019plami, rivojlanishni ko\u2019rsatuvchi hujjat", "Faqat baholash varaqasi", "Test natijalari", "Diplom"]},
    {"id": 94, "question": "Rubrika (rubric) nima?", "correct": "Ishni baholash mezonlarini ko\u2019rsatuvchi jadval", "options": ["Ishni baholash mezonlarini ko\u2019rsatuvchi jadval", "Dars rejasi", "O\u2019quv dasturi", "Test savollari"]},
    {"id": 95, "question": "Ta\u2019limda differentsiatsiya strategiyalari qaysilar?", "correct": "Mazmun, jarayon, mahsulot va muhit bo\u2019yicha farqlash", "options": ["Mazmun, jarayon, mahsulot va muhit bo\u2019yicha farqlash", "Faqat mazmun bo\u2019yicha", "Faqat jarayon bo\u2019yicha", "Faqat natija bo\u2019yicha"]},
    {"id": 96, "question": "Aralash ta\u2019lim (blended learning) nima?", "correct": "An\u2019anaviy va onlayn ta\u2019limni birlashtirish", "options": ["An\u2019anaviy va onlayn ta\u2019limni birlashtirish", "Faqat onlayn ta\u2019lim", "Faqat an\u2019anaviy ta\u2019lim", "Masofaviy ta\u2019lim"]},
    {"id": 97, "question": "Pedagogik tadqiqotning bosqichlari?", "correct": "Muammoni aniqlash, maqsad qo\u2019yish, ma\u2019lumot to\u2019plash, tahlil, xulosa", "options": ["Muammoni aniqlash, maqsad qo\u2019yish, ma\u2019lumot to\u2019plash, tahlil, xulosa", "Faqat ma\u2019lumot to\u2019plash", "Faqat tahlil", "Faqat xulosa"]},
    {"id": 98, "question": "Action research (harakat tadqiqoti) nima?", "correct": "Amaliyotchilar o\u2019z ish joyida o\u2019z amaliyotini yaxshilash uchun o\u2019tkazadigan tadqiqot", "options": ["Amaliyotchilar o\u2019z ish joyida o\u2019z amaliyotini yaxshilash uchun o\u2019tkazadigan tadqiqot", "Laboratoriya tadqiqoti", "Nazariy tadqiqot", "Statistik tadqiqot"]},
    {"id": 99, "question": "Mentorlash ta\u2019limda nima?", "correct": "Tajribali o\u2019qituvchining yangi o\u2039qituvchiga qo\u2019llab-quvvatlash va yo\u2019naltirishi", "options": ["Tajribali o\u2019qituvchining yangi o\u2039qituvchiga qo\u2019llab-quvvatlash va yo\u2019naltirishi", "Faqat dars berish", "Faqat baholash", "Faqat nazorat"]},
    {"id": 100, "question": "Professional learning community (professional o\u2019quvchi hamjamiyat) nima?", "correct": "O\u2019qituvchilarning bir-biridan o\u2019rganish va hamkorlik qilish uchun birlashuvi", "options": ["O\u2019qituvchilarning bir-biridan o\u2019rganish va hamkorlik qilish uchun birlashuvi", "Faqat o\u2039qituvchilar uyushmasi", "Faqat kasbiy kurs", "O\u2039quvchilar hamjamiyati"]},
    {"id": 101, "question": "Ta\u2019lim falsafasi nima?", "correct": "Ta\u2019lim maqsadi, mohiyati va metodlari haqidagi falsafiy qarashlar tizimi", "options": ["Ta\u2019lim maqsadi, mohiyati va metodlari haqidagi falsafiy qarashlar tizimi", "Faqat ta\u2019lim tarixi", "Faqat ta\u2019lim qonunlari", "Faqat ta\u2019lim metodlari"]},
    {"id": 102, "question": "Ijtimoiy konstruktivizm kimning nazariyasi?", "correct": "L.S.Vigotskiy", "options": ["L.S.Vigotskiy", "J.Piaje", "B.Skinner", "J.Bruner"]},
    {"id": 103, "question": "Spiral o\u2019quv dasturi kimning g\u2019oyasi?", "correct": "J.Bruner", "options": ["J.Bruner", "J.Piaje", "L.Vigotskiy", "B.Skinner"]},
    {"id": 104, "question": "Spiral o\u2019quv dasturi nima?", "correct": "Mavzular vaqt o\u2019tgan sari chuqurlashib qayta-qayta ko\u2019rib chiqiladigan dastur", "options": ["Mavzular vaqt o\u2019tgan sari chuqurlashib qayta-qayta ko\u2019rib chiqiladigan dastur", "Faqat bir marta ko\u2019riladigan mavzular", "Spiral shaklda yoziladigan darslik", "Maxsus dars rejasi"]},
    {"id": 105, "question": "Ta\u2019limdagi motivatsiya turlari?", "correct": "Ichki motivatsiya va tashqi motivatsiya", "options": ["Ichki motivatsiya va tashqi motivatsiya", "Faqat ichki motivatsiya", "Faqat tashqi motivatsiya", "Faqat rag\u2019batlantirish"]},
    {"id": 106, "question": "O\u2019z-o\u2019zini tartibga solish (self-regulation) nima?", "correct": "O\u2019quvchining o\u2019z o\u2019qish jarayonini rejalashtirish, nazorat va baholash qobiliyati", "options": ["O\u2019quvchining o\u2019z o\u2019qish jarayonini rejalashtirish, nazorat va baholash qobiliyati", "Faqat o\u2019zini tutish", "Faqat nazorat", "Faqat rejalashtirish"]},
    {"id": 107, "question": "Kognitiv yuk nazariyasi (cognitive load theory) nima?", "correct": "Insonning ma\u2019lumot qayta ishlash qobiliyatining chegaralanganligiga oid nazariya", "options": ["Insonning ma\u2019lumot qayta ishlash qobiliyatining chegaralanganligiga oid nazariya", "Bilim yukini oshirish", "Ko\u2019p o\u2019rganish", "Tez o\u2019rganish"]},
    {"id": 108, "question": "Masofadan o\u2019qitishda sinxron ta\u2019lim nima?", "correct": "O\u2019qituvchi va o\u2019quvchilar bir vaqtda onlayn aloqada bo\u2019ladigan ta\u2019lim", "options": ["O\u2019qituvchi va o\u2019quvchilar bir vaqtda onlayn aloqada bo\u2019ladigan ta\u2019lim", "O\u2019z vaqtida o\u2019qish", "Video yozib qo\u2019yish", "Faqat yozishma"]},
    {"id": 109, "question": "Asinxron ta\u2019lim nima?", "correct": "O\u2019quvchi o\u2019z xohlaganida o\u2019qiy oladigan ta\u2019lim", "options": ["O\u2019quvchi o\u2019z xohlaganida o\u2019qiy oladigan ta\u2019lim", "Real vaqt ta\u2019lim", "Sinfda ta\u2019lim", "Guruhda ta\u2019lim"]},
    {"id": 110, "question": "LMS (Learning Management System) nima?", "correct": "Ta\u2019lim jarayonini boshqarish uchun onlayn platforma", "options": ["Ta\u2019lim jarayonini boshqarish uchun onlayn platforma", "Faqat test tizimi", "Faqat video platforma", "Kutubxona tizimi"]},
    {"id": 111, "question": "Universal dizayn ta\u2019limda nima?", "correct": "Barcha o\u2039quvchilar uchun qulay ta\u2039lim muhiti va materallarini loyihalash", "options": ["Barcha o\u2039quvchilar uchun qulay ta\u2039lim muhiti va materallarini loyihalash", "Faqat nogironlar uchun dizayn", "Faqat binolar dizayni", "Faqat darslik dizayni"]},
    {"id": 112, "question": "Pedagogik etika printsiplari?", "correct": "Hurmat, adolat, maxfiylik, professionallik", "options": ["Hurmat, adolat, maxfiylik, professionallik", "Faqat hurmat", "Faqat adolat", "Faqat professionallik"]},
    {"id": 113, "question": "Maktab psixologining vazifasi?", "correct": "O\u2019quvchilarning psixologik salomatligi va rivojlanishini qo\u2019llab-quvvatlash", "options": ["O\u2019quvchilarning psixologik salomatligi va rivojlanishini qo\u2019llab-quvvatlash", "Faqat diagnostika", "Faqat maslahat", "Faqat nazorat"]},
    {"id": 114, "question": "O\u2019qituvchi-o\u2019quvchi munosabatlarining asosi?", "correct": "Hurmat, ishonch va hamkorlik", "options": ["Hurmat, ishonch va hamkorlik", "Faqat intizom", "Faqat baholash", "Faqat talabchanlik"]},
    {"id": 115, "question": "Kompetensiyaviy ta\u2019lim nima?", "correct": "Bilim, ko\u2019nikma va munosabatlarni birgalikda rivojlantirishga yo\u2019naltirilgan ta\u2019lim", "options": ["Bilim, ko\u2019nikma va munosabatlarni birgalikda rivojlantirishga yo\u2019naltirilgan ta\u2019lim", "Faqat bilim berish", "Faqat ko\u2019nikma shakllantirish", "Faqat malaka oshirish"]},
    {"id": 116, "question": "Ta\u2019lim strategiyalari va metodlarining farqi nima?", "correct": "Strategiya umumiy yondashuv, metod esa uni amalga oshirishning aniq usuli", "options": ["Strategiya umumiy yondashuv, metod esa uni amalga oshirishning aniq usuli", "Ular bir xil", "Strategiya metod ichida", "Metod strategiya ichida"]},
    {"id": 117, "question": "Tasodifiy o\u2019qish (incidental learning) nima?", "correct": "Maxsus niyatsiz, hayot tajribasi orqali bilim olish", "options": ["Maxsus niyatsiz, hayot tajribasi orqali bilim olish", "Maqsadli o\u2019qish", "Formal ta\u2019lim", "Onlayn o\u2019qish"]},
    {"id": 118, "question": "Noresmi ta\u2019lim (informal learning) nima?", "correct": "Maktabdan tashqari, hayotiy tajriba va kundalik faoliyat orqali o\u2019qish", "options": ["Maktabdan tashqari, hayotiy tajriba va kundalik faoliyat orqali o\u2019qish", "Maktabda o\u2019qish", "Kursda o\u2019qish", "Universitetda o\u2019qish"]},
    {"id": 119, "question": "O\u2019qituvchining refleksiv amaliyoti nima?", "correct": "O\u2019qituvchining o\u2019z dars berishini tahlil qilib, yaxshilash jarayoni", "options": ["O\u2019qituvchining o\u2019z dars berishini tahlil qilib, yaxshilash jarayoni", "Faqat dars berish", "Faqat baholash", "Faqat nazorat"]},
    {"id": 120, "question": "Pedagogik innovatsiya nima?", "correct": "Ta\u2019lim-tarbiya jarayoniga yangi g\u2019oyalar va usullarni kiritish", "options": ["Ta\u2019lim-tarbiya jarayoniga yangi g\u2019oyalar va usullarni kiritish", "Faqat texnik yangiliklar", "Faqat yangi darsliklar", "Faqat yangi binolar"]},
    {"id": 121, "question": "Pedagogika sohasida \u201cekoloqiya\u201d tushunchasi nima?", "correct": "Ta\u2019lim muhiti va uning o\u2019quvchi rivojiga ta\u2019sirini o\u2019rganish", "options": ["Ta\u2019lim muhiti va uning o\u2019quvchi rivojiga ta\u2019sirini o\u2019rganish", "Tabiat haqida o\u2019qitish", "Atrof-muhitni himoya qilish", "Faqat tashqi muhit"]},
    {"id": 122, "question": "Inkluziv ta\u2019limda o\u2019qituvchining vazifasi?", "correct": "Barcha o\u2019quvchilar uchun qulay o\u2019qish muhiti va materiallarni ta\u2039minlash", "options": ["Barcha o\u2019quvchilar uchun qulay o\u2019qish muhiti va materiallarni ta\u2039minlash", "Faqat qiyin o\u2019quvchilar bilan ishlash", "Faqat oddiy o\u2019quvchilar bilan ishlash", "Faqat iqtidorlilar bilan ishlash"]},
    {"id": 123, "question": "Collaborative learning (hamkorlikda o\u2019qish) nima?", "correct": "O\u2019quvchilar birgalikda umumiy maqsadga erishish uchun o\u2039rganadilar", "options": ["O\u2019quvchilar birgalikda umumiy maqsadga erishish uchun o\u2039rganadilar", "Individual o\u2019qish", "Raqobatli o\u2019qish", "Mustaqil o\u2039qish"]},
    {"id": 124, "question": "Inquiry-based learning (so\u2039rovga asoslangan o\u2019qish) nima?", "correct": "O\u2019quvchilar savol va tadqiqot orqali bilim oladigan usul", "options": ["O\u2019quvchilar savol va tadqiqot orqali bilim oladigan usul", "O\u2039qituvchi barcha javoblarni beradi", "Faqat kitob o\u2019qish", "Faqat yod olish"]},
    {"id": 125, "question": "Pedagogikada \u201cproqram ta\u2019lim\u201d nima?", "correct": "Materiallarni kichik bosqichlarga bo\u2019lib, har bosqichda nazorat qilinadigan ta\u2019lim", "options": ["Materiallarni kichik bosqichlarga bo\u2019lib, har bosqichda nazorat qilinadigan ta\u2019lim", "Kompyuter dasturlash o\u2039rgatish", "Onlayn ta\u2019lim", "Moduli ta\u2019lim"]},
    {"id": 126, "question": "Mikro-ta\u2019lim (microteaching) nima?", "correct": "O\u2039qituvchi ta\u2039yorgarligi uchun qisqa darslarni mashq qilish texnikasi", "options": ["O\u2039qituvchi ta\u2039yorgarligi uchun qisqa darslarni mashq qilish texnikasi", "Juda qisqa darslar berish", "Faqat bolalar uchun qisqa darslar", "Onlayn mini darslar"]},
    {"id": 127, "question": "Pedagogikada \u2018debriefing\u2019 nima?", "correct": "Faoliyat yoki tajribadan so\u2019ng uni muhokama qilish va o\u2039rganish jarayoni", "options": ["Faoliyat yoki tajribadan so\u2019ng uni muhokama qilish va o\u2039rganish jarayoni", "Darsdan oldingi tayyorgarlik", "Test oldin o\u2039tkaziladigan tushuntirish", "Uy vazifasi tekshirish"]},
    {"id": 128, "question": "Simulyatsiya ta\u2019limda nima?", "correct": "Haqiqiy vaziyatlarni modellashtirish orqali o\u2039rganish", "options": ["Haqiqiy vaziyatlarni modellashtirish orqali o\u2039rganish", "Faqat kompyuter simulyatsiyasi", "Faqat video ko\u2039rish", "Faqat laboratoriya tajribalari"]},
    {"id": 129, "question": "Role-play (rol o\u2039ynash) ta\u2019limda nima?", "correct": "O\u2039quvchilar muayyan rollarga kirib, amaliy bilimlarni o\u2039rganadilar", "options": ["O\u2039quvchilar muayyan rollarga kirib, amaliy bilimlarni o\u2039rganadilar", "Faqat teatr o\u2039yini", "Faqat sport o\u2039yini", "Faqat uy o\u2039yini"]},
    {"id": 130, "question": "Case study (keis-study) ta\u2019limda nima?", "correct": "Real hayotiy vaziyatlarni tahlil qilish orqali o\u2039rganish", "options": ["Real hayotiy vaziyatlarni tahlil qilish orqali o\u2039rganish", "Faqat nazariy o\u2039qish", "Faqat test yechish", "Faqat ma\u2019ruza tinglash"]},
    {"id": 131, "question": "Brainstorming (miyani bo\u2039rg\u2019atish) ta\u2019limda nima?", "correct": "Tanqidsiz ravishda ko\u2039p g\u2019oya ishlab chiqarish texnikasi", "options": ["Tanqidsiz ravishda ko\u2039p g\u2039oya ishlab chiqarish texnikasi", "Faqat tanqid qilish", "Faqat yaxshi g\u2039oyalarni tanlash", "Faqat mustaqil fikr yuritish"]},
    {"id": 132, "question": "Mind-map (tafakkur xaritasi) nima?", "correct": "Markaziy g\u2039oya atrofida bog\u2039liq fikrlarni vizual tasvirlash usuli", "options": ["Markaziy g\u2039oya atrofida bog\u2039liq fikrlarni vizual tasvirlash usuli", "Shahar xaritasi", "O\u2039quv xonasi rejasi", "Darslik mundarijasi"]},
    {"id": 133, "question": "Jigsaw metodi ta\u2019limda nima?", "correct": "Har bir o\u2039quvchi bir qismni o\u2039rganib, guruhga o\u2039rgatadigan kooperativ usul", "options": ["Har bir o\u2039quvchi bir qismni o\u2039rganib, guruhga o\u2039rgatadigan kooperativ usul", "Individual o\u2039qish metodi", "Raqobatli o\u2039qish", "O\u2039qituvchi o\u2039rgatadigan metod"]},
    {"id": 134, "question": "Think-Pair-Share metodi nima?", "correct": "O\u2039quvchi yakkama-yakka o\u2039ylaydi, juft bilan muhokama qiladi, umumiy ulashadi", "options": ["O\u2039quvchi yakkama-yakka o\u2039ylaydi, juft bilan muhokama qiladi, umumiy ulashadi", "Faqat individual fikrlash", "Faqat guruh ishi", "Faqat umumiy muhokama"]},
    {"id": 135, "question": "Exit ticket (chiqish kartochkasi) ta\u2019limda nima?", "correct": "Dars oxirida o\u2039quvchilar nimalarni o\u2039rganganini qisqacha yozadigan formativ baholash", "options": ["Dars oxirida o\u2039quvchilar nimalarni o\u2039rganganini qisqacha yozadigan formativ baholash", "Sinfdan chiqish uchun ruxsatnoma", "Dars boshida o\u2039tkaziladigan test", "Uy vazifasi"]},
    {"id": 136, "question": "KWL jadvalida K nima bildiradi?", "correct": "Know - mavzu haqida nima bilamanki", "options": ["Know - mavzu haqida nima bilamanki", "Key - asosiy tushunchalar", "Kind - mavzu turi", "Keep - saqlanadigan ma\u2019lumot"]},
    {"id": 137, "question": "KWL jadvalida W nima bildiradi?", "correct": "Want to Know - nimani bilmoqchiman", "options": ["Want to Know - nimani bilmoqchiman", "Write - yozib olaman", "Work - qanday ishlaydi", "Wonder - hayron qolaman"]},
    {"id": 138, "question": "KWL jadvalida L nima bildiradi?", "correct": "Learned - nima o\u2039rgandim", "options": ["Learned - nima o\u2039rgandim", "Like - nima yoqdi", "Look - nima ko\u2039rdim", "Listen - nima eshitdim"]},
    {"id": 139, "question": "Sokratik seminar nima?", "correct": "Matn bo\u2039yicha o\u2039quvchilar orasidagi erkin muhokama shakli", "options": ["Matn bo\u2039yicha o\u2039quvchilar orasidagi erkin muhokama shakli", "O\u2039qituvchi boshqaradigan dars", "Individual ish", "Yozma ish"]},
    {"id": 140, "question": "Gallery walk (galereya yurishi) ta\u2019limda nima?", "correct": "O\u2039quvchilar xona bo\u2039ylab yurgan holda turli stansiyalarda o\u2039rganadilar", "options": ["O\u2039quvchilar xona bo\u2039ylab yurgan holda turli stansiyalarda o\u2039rganadilar", "Rasmlar ko\u2039rish", "San\u2019at galereyasiga borish", "Faqat muzey safari"]},
    {"id": 141, "question": "Flipped classroom ning afzalligi nima?", "correct": "Sinfda chuqurroq muhokama va amaliy faoliyat uchun vaqt bo\u2039ladi", "options": ["Sinfda chuqurroq muhokama va amaliy faoliyat uchun vaqt bo\u2039ladi", "O\u2039qituvchi kam ishlaydi", "O\u2039quvchilar uy vazifasi qilmaydi", "Darslar qisqaradi"]},
    {"id": 142, "question": "SMART maqsad qo\u2039yishda R nima bildiradi?", "correct": "Relevant/Realistic - tegishli/real bo\u2039lishi kerak", "options": ["Relevant/Realistic - tegishli/real bo\u2039lishi kerak", "Result - natija ko\u2039rsatishi", "Reach - erishish", "Report - hisobot berish"]},
    {"id": 143, "question": "Andragogika nima?", "correct": "Kattalar ta\u2039limi nazariyasi va amaliyoti", "options": ["Kattalar ta\u2039limi nazariyasi va amaliyoti", "Bolalar ta\u2039limi", "O\u2039smirlar ta\u2039limi", "Maktabgacha ta\u2039lim"]},
    {"id": 144, "question": "Kattalar ta\u2039limining asosiy tamoyillari (Noulz bo\u2039yicha)?", "correct": "Mustaqillik, tajriba, tayyorlik, yo\u2039nalish, motivatsiya", "options": ["Mustaqillik, tajriba, tayyorlik, yo\u2039nalish, motivatsiya", "Faqat mustaqillik", "Faqat tajriba", "Faqat motivatsiya"]},
    {"id": 145, "question": "Pedagogikada ijtimoiylashuv nima?", "correct": "Inson jamiyat me\u2039yorlari va qadriyatlarini o\u2039zlashtirib borishi jarayoni", "options": ["Inson jamiyat me\u2039yorlari va qadriyatlarini o\u2039zlashtirib borishi jarayoni", "Faqat maktab ta\u2039limi", "Faqat oila ta\u2039siri", "Faqat do\u2039stlar ta\u2039siri"]},
    {"id": 146, "question": "Axloqiy tarbiyaning asosiy yo\u2039nalishlari?", "correct": "Vijdon, burch, mas\u2019uliyat, vatanparvarlik, insonparvarlik", "options": ["Vijdon, burch, mas\u2019uliyat, vatanparvarlik, insonparvarlik", "Faqat intizom", "Faqat hurmat", "Faqat mehribonlik"]},
    {"id": 147, "question": "Estetik tarbiyaning maqsadi?", "correct": "O\u2039quvchilarda go\u2039zallikni his qilish va yaratish qobiliyatini shakllantirish", "options": ["O\u2039quvchilarda go\u2039zallikni his qilish va yaratish qobiliyatini shakllantirish", "Faqat san\u2019at o\u2039rgatish", "Faqat musiqa o\u2039rgatish", "Faqat rasm o\u2039rgatish"]},
    {"id": 148, "question": "Mehnat tarbiyasining asosiy vazifasi?", "correct": "Mehnatga ijobiy munosabat va mehnat ko\u2039nikmalarini shakllantirish", "options": ["Mehnatga ijobiy munosabat va mehnat ko\u2039nikmalarini shakllantirish", "Faqat kasb o\u2039rgatish", "Faqat pul topishni o\u2039rgatish", "Faqat fizik mehnat"]},
    {"id": 149, "question": "Jismoniy tarbiyaning asosiy maqsadi?", "correct": "Sog\u2039lom, jismonan rivojlangan shaxsni shakllantirish", "options": ["Sog\u2039lom, jismonan rivojlangan shaxsni shakllantirish", "Faqat sport o\u2039rgatish", "Faqat ozg\u2039in bo\u2039lish", "Faqat kuchli bo\u2039lish"]},
    {"id": 150, "question": "Ekologik tarbiyaning maqsadi?", "correct": "Tabiatga mas\u2019uliyatli munosabatni shakllantirish", "options": ["Tabiatga mas\u2019uliyatli munosabatni shakllantirish", "Faqat ekologiyani o\u2039rgatish", "Faqat atrof-muhitni tozalash", "Faqat o\u2039simliklarni parvarish qilish"]},
    {"id": 151, "question": "Iqtisodiy tarbiyaning maqsadi?", "correct": "Iqtisodiy savodxonlik va tejamkorlik ko\u2039nikmalarini shakllantirish", "options": ["Iqtisodiy savodxonlik va tejamkorlik ko\u2039nikmalarini shakllantirish", "Faqat pul sanashni o\u2039rgatish", "Faqat tadbirkorlikni o\u2039rgatish", "Faqat iqtisod fanini o\u2039qitish"]},
    {"id": 152, "question": "Huquqiy tarbiyaning maqsadi?", "correct": "O\u2039quvchilarda huquqiy bilim va huquqiy madaniyatni shakllantirish", "options": ["O\u2039quvchilarda huquqiy bilim va huquqiy madaniyatni shakllantirish", "Faqat qonunlarni o\u2039rgatish", "Faqat politsiya haqida o\u2039qitish", "Faqat jazo berishni o\u2039rgatish"]},
    {"id": 153, "question": "Vatanparvarlik tarbiyasining asosiy yo\u2039nalishlari?", "correct": "Milliy g\u2039urur, tarix va madaniyatni qadrlahs, vatanni sevish", "options": ["Milliy g\u2039urur, tarix va madaniyatni qadrlahs, vatanni sevish", "Faqat harbiy tayyorgarlik", "Faqat bayramlarni nishonlash", "Faqat milliy kiyim kiyish"]},
    {"id": 154, "question": "Oilaviy tarbiyaning asosiy xususiyati?", "correct": "Doimiy, individual, emotsional muhitda amalga oshirilishi", "options": ["Doimiy, individual, emotsional muhitda amalga oshirilishi", "Faqat maktabdagi tarbiya", "Faqat jamoaviy tarbiya", "Faqat rasmiy tarbiya"]},
    {"id": 155, "question": "Maktab va oila hamkorligi shakllari?", "correct": "Ota-onalar yig\u2039ilishi, individual suhbat, ota-onalar kuni", "options": ["Ota-onalar yig\u2039ilishi, individual suhbat, ota-onalar kuni", "Faqat yig\u2039ilishlar", "Faqat suhbatlar", "Faqat telefon qo\u2039ng\u2039iroqlari"]},
    {"id": 156, "question": "Sinfdan tashqari tarbiyaviy ishning shakllari?", "correct": "To\u2039garak, sayohat, bayram, sport musobaqa, jamoat ishlari", "options": ["To\u2039garak, sayohat, bayram, sport musobaqa, jamoat ishlari", "Faqat to\u2039garaklar", "Faqat bayramlar", "Faqat sport"]},
    {"id": 157, "question": "Bolalar jamoasi shakllanishining bosqichlari (Makarenko bo\u2039yicha)?", "correct": "Tuzilish, rivojlanish, barqarorlik, o\u2039z-o\u2039zini boshqarish", "options": ["Tuzilish, rivojlanish, barqarorlik, o\u2039z-o\u2039zini boshqarish", "Faqat tuzilish", "Faqat rivojlanish", "Faqat barqarorlik"]},
    {"id": 158, "question": "Sinfda psixologik muhitni yaxshilashning yo\u2039llari?", "correct": "Hurmat, ishonch, qo\u2039llab-quvvatlash, ijobiy muloqot", "options": ["Hurmat, ishonch, qo\u2039llab-quvvatlash, ijobiy muloqot", "Faqat intizom", "Faqat nazorat", "Faqat jazolash"]},
    {"id": 159, "question": "O\u2039quvchilarning kognitiv xilma-xilligi nima?", "correct": "O\u2039quvchilarning fikrlash va o\u2039rganish uslublaridagi farqlar", "options": ["O\u2039quvchilarning fikrlash va o\u2039rganish uslublaridagi farqlar", "Faqat bilim farqlari", "Faqat yosh farqlari", "Faqat jinsi farqlari"]},
    {"id": 160, "question": "Garner ko\u2039p intellekt nazariyasiga ko\u2039ra nechta asosiy intellekt turi bor?", "correct": "8 ta", "options": ["8 ta", "5 ta", "6 ta", "7 ta"]},
    {"id": 161, "question": "Garner nazariyasida lingvistik intellekt nima?", "correct": "Til bilan ishlash qobiliyati", "options": ["Til bilan ishlash qobiliyati", "Matematik qobiliyat", "Musiqa qobiliyati", "Harakat qobiliyati"]},
    {"id": 162, "question": "Garner nazariyasida logical-matematik intellekt nima?", "correct": "Mantiq va raqamlar bilan ishlash qobiliyati", "options": ["Mantiq va raqamlar bilan ishlash qobiliyati", "Til qobiliyati", "Musiqa qobiliyati", "Ijtimoiy qobiliyat"]},
    {"id": 163, "question": "O\u2039qish uslublari (learning styles) deganda nima tushuniladi?", "correct": "Har bir o\u2039quvchining o\u2039ziga xos ma\u2019lumot qabul qilish va qayta ishlash usuli", "options": ["Har bir o\u2039quvchining o\u2039ziga xos ma\u2019lumot qabul qilish va qayta ishlash usuli", "Faqat kitob o\u2039qish tezligi", "Faqat yozuv uslubi", "Faqat tinglash qobiliyati"]},
    {"id": 164, "question": "VARK modeli nima?", "correct": "Visual, Auditory, Reading/Writing, Kinesthetic - o\u2039qish uslublari modeli", "options": ["Visual, Auditory, Reading/Writing, Kinesthetic - o\u2039qish uslublari modeli", "O\u2039qitish texnologiyasi", "Baholash tizimi", "Dars strukturasi"]},
    {"id": 165, "question": "Kinestik o\u2039quvchi kim?", "correct": "Harakat va amaliy faoliyat orqali yaxshi o\u2039rganadigna o\u2039quvchi", "options": ["Harakat va amaliy faoliyat orqali yaxshi o\u2039rganadigna o\u2039quvchi", "Ko\u2039rib yaxshi o\u2039rganadigan", "Eshitib yaxshi o\u2039rganadigan", "O\u2039qib yaxshi o\u2039rganadigan"]},
    {"id": 166, "question": "Vizual o\u2039quvchi kim?", "correct": "Ko\u2039rgazmali materiallar va grafiklar orqali yaxshi o\u2039rganadigan o\u2039quvchi", "options": ["Ko\u2039rgazmali materiallar va grafiklar orqali yaxshi o\u2039rganadigan o\u2039quvchi", "Harakat orqali o\u2039rganadigan", "Eshitib o\u2039rganadigan", "Yozib o\u2039rganadigan"]},
    {"id": 167, "question": "Auditiv o\u2039quvchi kim?", "correct": "Eshitish orqali yaxshi o\u2039rganadigan o\u2039quvchi", "options": ["Eshitish orqali yaxshi o\u2039rganadigan o\u2039quvchi", "Ko\u2039rib o\u2039rganadigan", "Harakat orqali o\u2039rganadigan", "Yozib o\u2039rganadigan"]},
    {"id": 168, "question": "Iqtidorli o\u2039quvchilar bilan ishlash usullari?", "correct": "Boyitish, tezlashtirish, murakkablashtirish, maxsus dasturlar", "options": ["Boyitish, tezlashtirish, murakkablashtirish, maxsus dasturlar", "Faqat ko\u2039proq uy vazifasi", "Faqat alohida darslar", "Faqat maqtash"]},
    {"id": 169, "question": "O\u2039qishda qiyinchiligi bor o\u2039quvchilar bilan ishlashda nima muhim?", "correct": "Erta aniqlash, individual yondashuv va zarur qo\u2039llab-quvvatlash", "options": ["Erta aniqlash, individual yondashuv va zarur qo\u2039llab-quvvatlash", "Ko\u2039proq uy vazifasi berish", "Alohida sinfga o\u2039tkazish", "Faqat nazorat qilish"]},
    {"id": 170, "question": "Dysleksiya nima?", "correct": "O\u2039qish va yozishda qiyinchilik tug\u2039diradigan o\u2039rganish farqi", "options": ["O\u2039qish va yozishda qiyinchilik tug\u2039diradigan o\u2039rganish farqi", "Ko\u2039rish muammosi", "Eshitish muammosi", "Xotira muammosi"]},
    {"id": 171, "question": "ADHD ta\u2039limga qanday ta\u2039sir qiladi?", "correct": "Diqqatni jamlash, o\u2039tirish va vazifani bajarishda qiyinchiliklar chiqaradi", "options": ["Diqqatni jamlash, o\u2039tirish va vazifani bajarishda qiyinchiliklar chiqaradi", "Faqat harakat muammosi", "Faqat o\u2039qish muammosi", "Faqat ijtimoiy muammo"]},
    {"id": 172, "question": "Asperger sindromi bor o\u2039quvchi bilan ishlashda nima muhim?", "correct": "Aniq tuzilgan muhit, ijtimoiy ko\u2039nikmalarni o\u2039rgatish va kuchli tomonlardan foydalanish", "options": ["Aniq tuzilgan muhit, ijtimoiy ko\u2039nikmalarni o\u2039rgatish va kuchli tomonlardan foydalanish", "Faqat alohida o\u2039qitish", "Faqat intizomni oshirish", "Faqat ota-ona bilan ishlash"]},
    {"id": 173, "question": "Hayotiy ko\u2039nikmalar ta\u2039limi nima?", "correct": "Kundalik hayotda kerakli amaliy ko\u2039nikmalarni o\u2039rgatish", "options": ["Kundalik hayotda kerakli amaliy ko\u2039nikmalarni o\u2039rgatish", "Faqat kasb ko\u2039nikmalari", "Faqat akademik ko\u2039nikmalar", "Faqat sport ko\u2039nikmalari"]},
    {"id": 174, "question": "Ijtimoiy-emotsional o\u2039qish (SEL) nima?", "correct": "O\u2039quvchilarga o\u2039z his-tuyg\u2039ularini va munosabatlarini boshqarishni o\u2039rgatish", "options": ["O\u2039quvchilarga o\u2039z his-tuyg\u2039ularini va munosabatlarini boshqarishni o\u2039rgatish", "Faqat ijtimoiy fanlar", "Faqat san\u2019at ta\u2039limi", "Faqat sport"]},
    {"id": 175, "question": "Empatiya rivojlantirishning ta\u2039limdagi ahamiyati?", "correct": "O\u2039quvchilarda boshqalarni tushunish, muloqot va hamkorlik ko\u2039nikmalarini mustahkamlaydi", "options": ["O\u2039quvchilarda boshqalarni tushunish, muloqot va hamkorlik ko\u2039nikmalarini mustahkamlaydi", "Faqat ijtimoiy bo\u2039lishga yordam beradi", "Faqat do\u2039st topishga yordam beradi", "Ta\u2039limga aloqasi yo\u2039q"]},
    {"id": 176, "question": "O\u2039quvchilarda ijodkorlikni rivojlantirish usullari?", "correct": "Ochiq topshiriqlar, erkin ifoda, muammoli vaziyatlar, brainstorming", "options": ["Ochiq topshiriqlar, erkin ifoda, muammoli vaziyatlar, brainstorming", "Faqat san\u2019at darslari", "Faqat yozish", "Faqat rasm chizish"]},
    {"id": 177, "question": "O\u2039quvchilarda mustaqil fikrlashni rivojlantirish usullari?", "correct": "Savol berish, tahlil qilish, baholash va sintez qilishga undash", "options": ["Savol berish, tahlil qilish, baholash va sintez qilishga undash", "Faqat yod oldirish", "Faqat nazorat qilish", "Faqat ma\u2019ruza tinglash"]},
    {"id": 178, "question": "O\u2039quvchilarda axborot savodxonligini rivojlantirish nima?", "correct": "Ma\u2019lumotlarni topish, baholash va unumli foydalanishni o\u2039rgatish", "options": ["Ma\u2019lumotlarni topish, baholash va unumli foydalanishni o\u2039rgatish", "Faqat internet ishlatishni o\u2039rgatish", "Faqat kitob o\u2039qishni o\u2039rgatish", "Faqat kompyuter o\u2039rgatish"]},
    {"id": 179, "question": "O\u2039quvchilarda muammo yechish ko\u2039nikmalarini rivojlantirish usullari?", "correct": "Muammoli vaziyatlar, loyiha ishlari, amaliy mashqlar", "options": ["Muammoli vaziyatlar, loyiha ishlari, amaliy mashqlar", "Faqat nazariy bilim", "Faqat yod olish", "Faqat darslik o\u2039qish"]},
    {"id": 180, "question": "O\u2039quvchilarda liderlik ko\u2039nikmalarini rivojlantirish usullari?", "correct": "Guruh ishiga rahbarlik, loyiha boshqarish, javobgarlik topshirish", "options": ["Guruh ishiga rahbarlik, loyiha boshqarish, javobgarlik topshirish", "Faqat sport musobaqasi", "Faqat taqdirlash", "Faqat nazorat qilish"]},
    {"id": 181, "question": "O\u2039quvchilar o\u2039rtasidagi bullying (zo\u2039ravonlik) ga qarshi kurashish yo\u2039llari?", "correct": "Xavfsiz muhit, xabardorlik, qo\u2039llab-quvvatlash tizimi va aniq qoidalar", "options": ["Xavfsiz muhit, xabardorlik, qo\u2039llab-quvvatlash tizimi va aniq qoidalar", "Faqat jazolash", "Faqat nazorat", "Faqat ota-onaga xabar berish"]},
    {"id": 182, "question": "O\u2039quvchi motivatsiyasini oshirishning asosiy yo\u2039llari?", "correct": "Muvaffaqiyat holati, ijobiy baho, qiziqarli topshiriqlar, maqsad qo\u2039yish", "options": ["Muvaffaqiyat holati, ijobiy baho, qiziqarli topshiriqlar, maqsad qo\u2039yish", "Faqat baholash", "Faqat jazolash", "Faqat nazorat qilish"]},
    {"id": 183, "question": "O\u2039quvchilar orasidagi nizolarni hal etish usullari?", "correct": "Muloqot, vositachilik, muammoni birgalikda hal etish", "options": ["Muloqot, vositachilik, muammoni birgalikda hal etish", "Faqat jazolash", "Faqat ajratish", "Faqat ota-onaga yuborish"]},
    {"id": 184, "question": "Darsda intizomni saqlashning samarali yo\u2039llari?", "correct": "Aniq qoidalar, ijobiy mustahkamlash, tuzilgan muhit, hurmatli muloqot", "options": ["Aniq qoidalar, ijobiy mustahkamlash, tuzilgan muhit, hurmatli muloqot", "Faqat jazolash", "Faqat qattiq nazorat", "Faqat ota-onani chaqirish"]},
    {"id": 185, "question": "O\u2039qituvchining dars yozma rejaida nima bo\u2039lishi shart?", "correct": "Maqsad, mazmun, metodlar, vositalar, baholash va vaqt taqsimoti", "options": ["Maqsad, mazmun, metodlar, vositalar, baholash va vaqt taqsimoti", "Faqat maqsad", "Faqat mazmun", "Faqat metodlar"]},
    {"id": 186, "question": "Darsda vaqtni samarali boshqarish nima?", "correct": "Har bir bosqichga aniq vaqt ajratish va tartibga rioya qilish", "options": ["Har bir bosqichga aniq vaqt ajratish va tartibga rioya qilish", "Faqat tez o\u2039qitish", "Faqat qisqa dars o\u2039tish", "Faqat nazorat vaqtini ko\u2039paytirish"]},
    {"id": 187, "question": "Darslikni samarali ishlatishning asosiy yo\u2039llari?", "correct": "Darslik asosiy manba, lekin uni boshqa manbalar bilan boyitish kerak", "options": ["Darslik asosiy manba, lekin uni boshqa manbalar bilan boyitish kerak", "Faqat darslikni o\u2039qish", "Darsliksiz dars o\u2039tish", "Faqat darslik savollariga javob berish"]},
    {"id": 188, "question": "O\u2039qituvchining kasbiy rivojlanish yo\u2039llari?", "correct": "Kurslар, seminarlar, o\u2039z-o\u2039zini o\u2039qitish, hamkasblardan o\u2039rganish", "options": ["Kurslар, seminarlar, o\u2039z-o\u2039zini o\u2039qitish, hamkasblardan o\u2039rganish", "Faqat kurslar", "Faqat seminarlar", "Faqat tajriba"]},
    {"id": 189, "question": "Talabalar reyting tizimining afzalliklari?", "correct": "Doimiy motivatsiya, shaffoflik, adolatli baholash", "options": ["Doimiy motivatsiya, shaffoflik, adolatli baholash", "Faqat raqobat yaratish", "Faqat intizom", "Faqat nazorat"]},
    {"id": 190, "question": "O\u2039quvchilarga uy vazifasi berishning asosiy maqsadi?", "correct": "Bilimlarni mustahkamlash va mustaqil o\u2039qish ko\u2039nikmalarini rivojlantirish", "options": ["Bilimlarni mustahkamlash va mustaqil o\u2039qish ko\u2039nikmalarini rivojlantirish", "Faqat vaqt to\u2039ldirish", "Faqat ota-onani band qilish", "Faqat baholash uchun"]},
    {"id": 191, "question": "Uy vazifasini bajarishda o\u2039quvchilarga yordam berishning samarali usuli?", "correct": "Vazifani tushuntirish, zarur resurslarni ko\u2039rsatish, mustaqillikni rag\u2039batlantirish", "options": ["Vazifani tushuntirish, zarur resurslarni ko\u2039rsatish, mustaqillikni rag\u2039batlantirish", "Faqat javoblarni berish", "Faqat nazorat qilish", "Faqat jazolash"]},
    {"id": 192, "question": "O\u2039quvchilar bilimini testlash orqali baholashning afzalliklari?", "correct": "Tezlik, ob\u2019ektivlik, keng qamrov, statistik tahlil imkoni", "options": ["Tezlik, ob\u2019ektivlik, keng qamrov, statistik tahlil imkoni", "Faqat tezlik", "Faqat ob\u2019ektivlik", "Faqat qulaylik"]},
    {"id": 193, "question": "O\u2039quvchilar bilimini testlash orqali baholashning kamchiliklari?", "correct": "Chuqur tushunishni o\u2039lchamasligi, taxmin qilish imkoni, kreatiblikni o\u2039lchamasligi", "options": ["Chuqur tushunishni o\u2039lchamasligi, taxmin qilish imkoni, kreatiblikni o\u2039lchamasligi", "Faqat vaqt talabi", "Faqat narxi", "Faqat texnik muammolar"]},
    {"id": 194, "question": "O\u2039quvchilar ijodiy ishlarini baholashning eng samarali usuli?", "correct": "Rubrika asosida baholash (mezon asosida)", "options": ["Rubrika asosida baholash (mezon asosida)", "Faqat bahoning chiqishi", "Faqat o\u2039qituvchi kayfiyati", "Faqat solishtirish"]},
    {"id": 195, "question": "Sinfda o\u2039quvchilar sonining ta\u2039lim sifatiga ta\u2039siri?", "correct": "Kichik sinflar individual e\u2039tiborni oshiradi, sifat yaxshilanadi", "options": ["Kichik sinflar individual e\u2039tiborni oshiradi, sifat yaxshilanadi", "Sinf soni ahamiyatsiz", "Ko\u2039p o\u2039quvchi yaxshiroq", "Faqat o\u2039qituvchi ahamiyatli"]},
    {"id": 196, "question": "Maktabda psixologik xavfsizlik muhitini yaratish uchun nima kerak?", "correct": "Xato qilishga ruxsat, hurmat, ochiq muloqot va qo\u2039llab-quvvatlash", "options": ["Xato qilishga ruxsat, hurmat, ochiq muloqot va qo\u2039llab-quvvatlash", "Faqat qattiq intizom", "Faqat nazorat", "Faqat jazolash tizimi"]},
    {"id": 197, "question": "Pedagogik tadqiqotda sifatli va miqdoriy metodlarning farqi?", "correct": "Sifatli - chuqur tushunish, miqdoriy - raqamli o\u2039lchov va tahlil", "options": ["Sifatli - chuqur tushunish, miqdoriy - raqamli o\u2039lchov va tahlil", "Ular bir xil", "Sifatli yaxshiroq", "Miqdoriy yaxshiroq"]},
    {"id": 198, "question": "Ta\u2039lim siyosati deganda nima tushuniladi?", "correct": "Ta\u2039lim tizimini boshqarish uchun davlat tomonidan qabul qilinadigan qarorlar va yo\u2039nalishlar", "options": ["Ta\u2039lim tizimini boshqarish uchun davlat tomonidan qabul qilinadigan qarorlar va yo\u2039nalishlar", "Faqat qonunlar", "Faqat o\u2039quv dasturlari", "Faqat baholash tizimi"]},
    {"id": 199, "question": "Ta\u2039limda tenglik (equity) va tenglik (equality) ning farqi nima?", "correct": "Equality - hammaga bir xil, Equity - har kimga keragiga qarab berish", "options": ["Equality - hammaga bir xil, Equity - har kimga keragiga qarab berish", "Ular bir xil", "Equality yaxshiroq", "Equity yaxshiroq"]},
    {"id": 200, "question": "Global fuqarolik ta\u2039limi nima?", "correct": "O\u2039quvchilarga global muammolarni tushunish va hal etishga tayyorlash", "options": ["O\u2039quvchilarda global muammolarni tushunish va hal etishga tayyorlash", "Faqat ingliz tili o\u2039rgatish", "Faqat xorijda o\u2039qish", "Faqat xarita o\u2039rgatish"]},
]

# ===================== FSM HOLATLARI =====================
class QuizStates(StatesGroup):
    playing = State()
    finished = State()

# ===================== BOT VA DISPATCHER =====================
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ===================== FOYDALANUVCHI MA'LUMOTLARI =====================
user_data = {}

# ===================== YORDAMCHI FUNKSIYALAR =====================
def get_question_keyboard(options: list, q_index: int) -> InlineKeyboardMarkup:
    buttons = []
    for i, option in enumerate(options):
        buttons.append([InlineKeyboardButton(
            text=f"{chr(65+i)}) {option[:50]}{'...' if len(option) > 50 else ''}",
            callback_data=f"answer_{q_index}_{i}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Testni boshlash")],
            [KeyboardButton(text="📊 Natijam"), KeyboardButton(text="ℹ️ Yordam")]
        ],
        resize_keyboard=True
    )

# ===================== HANDLERS =====================
@dp.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user_data[user_id] = {"score": 0, "total": 0, "current_q": 0, "questions": []}
    
    await message.answer(
        f"🎓 *Umumiy Pedagogika Quiz Botiga xush kelibsiz!*\n\n"
        f"📚 Jami {len(QUESTIONS)} ta savol mavjud\n"
        f"✅ To'g'ri javob uchun +1 ball\n"
        f"❌ Noto'g'ri javob uchun ball berilmaydi\n\n"
        f"Boshlash uchun tugmani bosing! 👇",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "🎯 Testni boshlash")
async def start_quiz(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Savollarni tasodifiy tartibda olish (20 ta)
    questions = random.sample(QUESTIONS, min(20, len(QUESTIONS)))
    
    user_data[user_id] = {
        "score": 0,
        "total": len(questions),
        "current_q": 0,
        "questions": questions,
        "answered": []
    }
    
    await state.set_state(QuizStates.playing)
    await send_question(message, user_id, 0)

async def send_question(message: types.Message, user_id: int, q_index: int):
    data = user_data.get(user_id)
    if not data or q_index >= len(data["questions"]):
        return
    
    q = data["questions"][q_index]
    options = q["options"].copy()
    random.shuffle(options)
    
    # Aralashtirilgan variantlarni saqlash
    data["shuffled_options"] = options
    
    correct_index = options.index(q["correct"])
    data["correct_index"] = correct_index
    
    text = (
        f"📝 *Savol {q_index + 1}/{data['total']}*\n\n"
        f"{q['question']}\n\n"
        f"🔢 Ball: {data['score']}"
    )
    
    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=get_question_keyboard(options, q_index)
    )

@dp.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = user_data.get(user_id)
    
    if not data:
        await callback.answer("Yangi test boshlang!", show_alert=True)
        return
    
    parts = callback.data.split("_")
    q_index = int(parts[1])
    answer_index = int(parts[2])
    
    if q_index != data["current_q"]:
        await callback.answer("Bu savol allaqachon javoblangan!", show_alert=True)
        return
    
    q = data["questions"][q_index]
    correct_index = data["correct_index"]
    options = data["shuffled_options"]
    
    is_correct = (answer_index == correct_index)
    
    if is_correct:
        data["score"] += 1
        result_text = f"✅ *To'g'ri!*\n\n✔️ {options[correct_index]}"
    else:
        result_text = (
            f"❌ *Noto'g'ri!*\n\n"
            f"Siz tanladingiz: {options[answer_index]}\n"
            f"✔️ To'g'ri javob: {options[correct_index]}"
        )
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(result_text, parse_mode="Markdown")
    await callback.answer()
    
    data["current_q"] += 1
    
    # Keyingi savol yoki yakunlash
    if data["current_q"] < data["total"]:
        await asyncio.sleep(0.5)
        await send_question(callback.message, user_id, data["current_q"])
    else:
        await finish_quiz(callback.message, user_id, state)

async def finish_quiz(message: types.Message, user_id: int, state: FSMContext):
    data = user_data.get(user_id)
    if not data:
        return
    
    score = data["score"]
    total = data["total"]
    percentage = (score / total) * 100
    
    if percentage >= 90:
        emoji = "🏆"
        grade = "A'lo"
    elif percentage >= 75:
        emoji = "🥈"
        grade = "Yaxshi"
    elif percentage >= 60:
        emoji = "🥉"
        grade = "Qoniqarli"
    else:
        emoji = "📚"
        grade = "Qayta o'rganing"
    
    result_text = (
        f"{emoji} *Test yakunlandi!*\n\n"
        f"📊 Natija: {score}/{total}\n"
        f"📈 Foiz: {percentage:.1f}%\n"
        f"🎯 Baho: {grade}\n\n"
        f"Qayta urinish uchun 'Testni boshlash' tugmasini bosing!"
    )
    
    await state.clear()
    await message.answer(result_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@dp.message(F.text == "📊 Natijam")
async def show_stats(message: types.Message):
    user_id = message.from_user.id
    data = user_data.get(user_id)
    
    if not data or data.get("total", 0) == 0:
        await message.answer("Hali test yechmadingiz. Boshlash uchun 'Testni boshlash' tugmasini bosing!")
        return
    
    score = data["score"]
    total = data["total"]
    current = data.get("current_q", 0)
    
    if current < total:
        status = f"🔄 Test davom etmoqda: {current}/{total}"
    else:
        percentage = (score / total) * 100
        status = f"✅ Oxirgi test: {score}/{total} ({percentage:.1f}%)"
    
    await message.answer(f"📊 *Sizning natijangiz:*\n\n{status}", parse_mode="Markdown")

@dp.message(F.text == "ℹ️ Yordam")
async def help_handler(message: types.Message):
    await message.answer(
        "ℹ️ *Yordam*\n\n"
        "🎯 *Testni boshlash* - 20 ta tasodifiy savol bilan test boshlang\n"
        "📊 *Natijam* - so'nggi test natijangizni ko'ring\n\n"
        "📚 Savollar *Umumiy Pedagogika* fanidan olingan\n"
        "Jami 200 ta savol mavjud!",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await help_handler(message)

# ===================== MAIN =====================
async def main():
    logger.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
