import paho.mqtt.client as mqtt
import os
import json
import datetime


def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("Tersambung dengan client")
    else:
        print("Error connect code :" + str(rc))

def on_message(client,userdata, message):
    print("Notifikasi Terbaru dari LionAIR pada Topic:" + message.topic)
    jsonData = message.payload.decode("utf-8")
    messageObj = json.loads(jsonData)
    if cekKode(messageObj["kode"]):
        print("Notifikasi untuk Kode Penerbangan" +messageObj["kode"]+"telah tersedia")
        time.sleep(4)
        client.disconnect()
    else:
        print("Kode Penerbangan      :", messageObj["kode"])
        print("Asal                  :", messageObj["kotaAsal"])
        print("Tujuan                :", messageObj["kotaTujuan"])
        print("Tanggal Keberangkatan :", messageObj["tanggal"])
        print("Waktu Keberangkatan   :", messageObj["waktu"])
        print("Dibuat pada           :", messageObj["dibuat"])
        

        global arrOfMsgObj
        arrOfMsgObj.append(messageObj)

        waktuTerima = datetime.datetime.now()

        # tulis jadwal baru ke dalam file "boarding.txt" (waktu keberangkatan)

        with open('boarding.txt', 'a') as f:
            f.write("Kode Penerbangan : "+messageObj["kode"]+"\n"
                    "Tanggal Keberangkatan : "+messageObj["tanggal"]+"\n"
                    "Diterima pada : "+ waktuTerima +"\n")
            

        # tulis jadwal baru ke dalam file "lokasi.txt" (kota tujuan dan asal penerbangan)
        with open('lokasi.txt', 'a') as f:
            f.write("Kode Penerbangan : "+messageObj["kode"]+"\n"
                    "Asal : "+messageObj["kotaAsal"]+"\n"
                    "Tujuan : "+messageObj["kotaTujuan"]+"\n"
                    "Diterima pada : "+ waktuTerima +"\n")


def cekKode(kodePenerbangan):
    """
    fungsi untuk mengecek apakah kode penerbangan telah 
    ada pada array

    return True apabila ada
    return False apabila belum ada

    """
    global arrOfMsgObj
    for msgObj in arrOfMsgObj:
        if kodePenerbangan in msgObj["kode"]:
            return True
        else:
            return False


# fungsi publish subscribe

def publish(client,topic,msg,qos):
    client.publish(topic,msg,qos)

def subscribe(client,topic,qos) :
    client.subscribe(topic,qos)


# buat client
client = mqtt.Client("Client", clean_session = False)
client.on_connect = on_connect
client.on_message = on_message

# menghubungkan client ke Publisher
client.connect("broker.hivemq.com", 1883)

# melakukan subscribe 
subscribe(client,"my/LionAIR/Notifikasi",1)

# definisikan fungsi menu() untuk menampilkan menu
# yang dapat dpilih penumpang
def menu():
    print("(1) Dapatkan Notifikasi")

#definisikan fungsi getNotif() untuk mendapatkan notifikasi

def getNotif():
    global arrOfMsgObj
    print("Terdapat "+str(len(arrOfMsgObj))+"notifikasi untuk saat ini")
    for messageObj in arrOfMsgObj:
        print("Kode Penerbangan      :", messageObj["kode"])
        print("Asal                  :", messageObj["kotaAsal"])
        print("Tujuan                :", messageObj["kotaTujuan"])
        print("Tanggal Keberangkatan :", messageObj["tanggal"])
        print("Waktu Keberangkatan   :", messageObj["waktu"])
        print("Dibuat pada           :", messageObj["dibuat"])
        print("-----------------------------------------------\n")

   

# main

menu()
inputan = int(input("Menu yang akan dipilih (0 untuk mengakhiri):"))
while inputan != 0:
    getNotif()
    inputan = input(int("Menu yang akan dipilih (0 untuk mengakhiri):"))
 










    
