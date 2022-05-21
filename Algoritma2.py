from ast import operator
import sqlite3 as sql
import os

#database oluşturma
dbName = 'operators.db'
dbMevcut = os.path.exists(dbName)

db = sql.connect(dbName)
im = db.cursor()

#tablo oluşturma
im.execute("CREATE TABLE IF NOT EXISTS dakika (dakika_miktar,dakika_fiyat)")
im.execute("CREATE TABLE IF NOT EXISTS sms (sms_miktar,sms_fiyat)")
im.execute("CREATE TABLE IF NOT EXISTS internet (internet_miktar,internet_fiyat)")

if not dbMevcut:
    im.execute("INSERT INTO sms VALUES ('1000SMS','20 TL')")
    im.execute("INSERT INTO sms VALUES ('5000SMS','40 TL')")
    im.execute("INSERT INTO sms VALUES ('10000SMS','80 TL')")

    im.execute("INSERT INTO dakika VALUES ('100dk','40 TL')")
    im.execute("INSERT INTO dakika VALUES ('250dk','60 TL')")
    im.execute("INSERT INTO dakika VALUES ('500dk','80 TL')")

    im.execute("INSERT INTO internet VALUES ('1GB','50 TL')")
    im.execute("INSERT INTO internet VALUES ('5GB','60 TL')")
    im.execute("INSERT INTO internet VALUES ('10GB','100 TL')")

    db.commit()

class Operators():

    def __init__(self,paketName,miktar,fiyat):
        self.paketName = paketName
        self.miktar = miktar
        self.fiyat = fiyat
        self.smsData = ""
        self.dakikaData = ""
        self.internetData = ""

    def smsPaketOlustur(self):
        print("sms")
        im.execute("INSERT INTO sms (sms_miktar,sms_fiyat) values(?,?)",(self.miktar,self.fiyat))
        im.execute("SELECT * FROM sms")
        smsData = im.fetchall()
        

    def dakikaPaketOlustur(self):
        print("dakika")
        im.execute("INSERT INTO dakika (dakika_miktar,dakika_fiyat) values(?,?)",(self.miktar,self.fiyat))
        im.execute("SELECT * FROM dakika")
        dakikaData = im.fetchall()
        

    def internetPaketOlustur(self):
        print("internet")    
        im.execute("INSERT INTO internet (internet_miktar,internet_fiyat) values(?,?)",(self.miktar,self.fiyat))
        im.execute("SELECT * FROM internet")
        internetData = im.fetchall()
        

    def bilgileriGoster(self):
        return self.smsData, self.dakikaData, self.internetData,

class Paketler():

    operatorName = ["Turkcell","Vodafone","Türk telekom"]
    paketName = ["SMS","İnternet","Dakika"]  

    def bilgileriGoster(self):
        im.execute("SELECT * FROM sms")
        smsData = im.fetchall()
        im.execute("SELECT * FROM dakika")
        dakikaData = im.fetchall()
        im.execute("SELECT * FROM internet")
        internetData = im.fetchall()
        return smsData,dakikaData,internetData


#class kullanımları
operator = Operators("sms","10000SMS","100 TL")
operator.smsPaketOlustur()

paketler = Paketler()
datas = paketler.bilgileriGoster()
print(datas[0])
print(datas[1])
print(datas[2])

sms = datas[0]
dakika = datas[1]
internet = datas[2]

selectedOperator = ""
toplamTutar = ""
bakiyeArray = []

#steps
def islemler():
    
    yesOrNo = True
    while(yesOrNo):
        selectedOperator = operatorSecimi()
        if(selectedOperator == False):
            break
        print("\nDevam edilecek operatör: ",selectedOperator)
        #paket seçimi
        paket = paketSecimi()
        if(paket == False):
            break
        print("Yükleme yapılacak paket: ",paket)

        #miktar girişi
        if(paket == "SMS"):
            miktar = paketMiktarı("SMS")
            if(miktar == False):
                break
            print("Yükleme yapılacak miktar: ",miktar[0])
        elif(paket == "İnternet"):
            miktar = paketMiktarı("İnternet")
            if(miktar == False):
                break
            print("Yükleme yapılacak miktar: ",miktar[0])
        elif(paket == "Dakika"):
            miktar = paketMiktarı("Dakika")
            if(miktar == False):
                break
            print("Yükleme yapılacak miktar: ",miktar[0])

        #ödeme bilgileri
        print("\n\n***Yükleme Bilgileri:***\n")
        print("Yükleme Yapılacak Numara:",phoneNumber,"\n")
        print("Yükleme Yapılacak Operatör:",selectedOperator,"\n")
        print("Yükleme Yapılacak Paket Türü:",paket,"\n")
        print("Yükleme Yapılacak Miktar:",miktar[0],"\n")
        print("Ödenecek Tutar: ",miktar[1])

        print("\n\nLütfen Ödeme Bilgilerini Giriniz:\n")
        kartİsmi = input("Kart üzerindeki isim: ")
        karNumarası = input("Kart Numarası: ")
        sonTarih = input("Son kullanma tarihi: ")
        cvc = input("CVC numarası: ")

        if(int(miktar[1].split(" ")[0]) <= int(bakiyeArray[0])):
            new_bakiye =  int(bakiyeArray[0]) - int(miktar[1].split(" ")[0])
            bakiyeArray[0] = new_bakiye
            print("\n\nYükleme işlemi başarılı\n")
            print("\n\nKalan bakiye:\n",bakiyeArray[0])
            cıkıs = input("Başka bir işlem yapmak istiyor musunuz?(Y/N): ")
            if(cıkıs == "Y"):
                continue
            else:
                yesOrNo = False
        else:
            print("Yükleme işlemi başarısız. Bakiye yetersiz, lütfen yükleme yapınız.\n")
            print("Ana sayfaya yönlendiriliyorsunuz...")
            islemler()

    return new_bakiye

def operatorSecimi():
    print("\n***Operatör Menüsü***\n")
    print("Operatör Listesi:\n")
    #operatör isimlerinin yayınlanması
    count = 1
    for i in paketler.operatorName:
        print(i,"için",count,"\n")
        count += 1

    selected = input("Lütfen işlem yapmak istediğiniz operatörü tuşlayınız(Çıkış yapmak için X'e basınız): ")
    if(selected == "1"):
        selectedOperator = "Turkcell"
    elif(selected == "2"):
        selectedOperator = "Vodafone"
    elif(selected == "3"):
        selectedOperator = "Türk telekom"
    elif(selected == "X"):
        selectedOperator = False
    else:
        selectedOperator = False    
    return selectedOperator

def paketSecimi():
    print("\n\n***Paket Menüsü***\n")
    print("Paket Listesi:\n")
    #paket isimlerinin yayınlanması
    count = 1
    for i in paketler.paketName:
        print(i,"için",count,"\n")
        count += 1
        
    selected = input("Lütfen yüklemek istediğiniz paket türünü seçiniz.(Çıkış yapmak için X'e basınız): ")
    if(selected == "1"):
        selectedPaket = "SMS"
    elif(selected == "2"):
        selectedPaket = "İnternet"    
    elif(selected == "3"):
        selectedPaket = "Dakika"
    elif(selected == "X"):
        selectedPaket = False
    else:
        selectedPaket = False

    return selectedPaket


def paketMiktarı(paketType):
    print("\n\n***Tarife Menüsü***\n")
    print("Tarife Listesi:\n")
    if(paketType == "SMS"):
        count = 1
        for i in sms:
            print(i,"için",count,"\n")
            count += 1
        selected = input("Lütfen işlem yapmak istediğiniz operatörü tuşlayınız(Çıkış yapmak için X'e basınız): ")
        if(selected == "1"):
            paket = sms[0][0]
            toplam_tutar = sms[0][1]
        elif(selected == "2"):
            paket = sms[1][0]
            toplam_tutar = sms[1][1]
        elif(selected == "3"):
            paket = sms[2][0]
            toplam_tutar = sms
        elif(selected == "X"):
            paket = False
        else:
            paket = False

    elif(paketType == "İnternet"):
        count = 1
        for i in internet:
            print(i,"için",count,"\n")
            count += 1
        selected = input("Lütfen işlem yapmak istediğiniz operatörü tuşlayınız(Çıkış yapmak için X'e basınız): ")
        if(selected == "1"):
            paket = internet[0][0]
            toplam_tutar = internet[0][1]
        elif(selected == "2"):
            paket = internet[1][0]
            toplam_tutar = internet[1][1]
        elif(selected == "3"):
            paket = internet[2][0]
            toplam_tutar = internet[2][1]
        elif(selected == "X"):
            paket = False
        else:
            paket = False   
    
    elif(paketType == "Dakika"):
        count = 1
        for i in dakika:
            print(i,"için",count,"\n")
            count += 1
        selected = input("Lütfen işlem yapmak istediğiniz operatörü tuşlayınız(Çıkış yapmak için X'e basınız): ")
        if(selected == "1"):
            paket = dakika[0][0]
            toplam_tutar = dakika[0][1]
        elif(selected == "2"):
            paket = dakika[1][0]
            toplam_tutar =  dakika[1][1]
        elif(selected == "3"):
            paket = dakika[2][0]
            toplam_tutar =  dakika[2][1]
        elif(selected == "X"):
            paket = False
        else:
            paket = False

    return paket,toplam_tutar


#kullanıcıdan işlem numarasını alıyoruz
print("OPERATÖR İŞLEMLERİNE HOŞGELDİNİZ.")
bakiye = input("Lütfen mevcut kart bakiyenizi giriniz: ")
bakiyeArray.append(bakiye)
phoneNumber = input("İşlem yapmak istediğiniz telefon numarasını giriniz(Başında 0 olmadan): ")
if(len(phoneNumber)==10):
    islemler()
else:
    print("Doğru formatta giriş yapılmadı\n")
    newNum = input("Lütfen tekrar telefon numaranızı tekrar giriniz: ")
    phoneNumber = newNum
    bakiye = islemler()