import os
import requests
import base64
import argparse
import time
import mimetypes
from google import genai
from google.genai import types
import pyfiglet
from colorama import init, Fore, Style
import platform

GENAI_API_KEY = "" # Masukan API Key Gemini Anda di sini
client = genai.Client(api_key=GENAI_API_KEY)
MODEL_ID = "gemini-2.5-flash"

def extractFromFolder(folderPath):
    allCodes = set()
    validExtensions = ('.txt', '.pdf', '.png', '.jpg', '.jpeg')
    
    files = [f for f in os.listdir(folderPath) if f.lower().endswith(validExtensions)]
    
    if not files:
        print(f"[!] Tidak ada file valid yang ditemukan di folder: {folderPath}")
        return None

    print(f"[*] Ditemukan {len(files)} file di folder. Memulai ekstraksi AI...")

    for fileName in files:
        filePath = os.path.join(folderPath, fileName)
        print(f"[AI] Menganalisis {fileName}...", end="\r")
        
        try:
            if fileName.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                mimeType, _ = mimetypes.guess_type(filePath)
                if not mimeType:
                    mimeType = 'application/pdf' if fileName.lower().endswith('.pdf') else 'image/jpeg'

                with open(filePath, "rb") as f:
                    fileUpload = client.files.upload(
                        file=f,
                        config={'mime_type': mimeType}
                    )
                
                while fileUpload.state == "PROCESSING":
                    time.sleep(2)
                    fileUpload = client.files.get(name=fileUpload.name)

                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=[
                        "Please extract all 'Billing Codes' present in this document. "
                        "Provide only a list of numbers, separated by new lines without additional text.",
                        fileUpload
                    ]
                )
                client.files.delete(name=fileUpload.name)
            
            else:
                with open(filePath, "r") as f:
                    content = f.read()
                    response = client.models.generate_content(
                        model=MODEL_ID,
                        contents=f"Extract all billing code numbers from the following text:\n{content}"
                    )

            if response.text:
                extracted = [line.strip() for line in response.text.split('\n') if line.strip().isdigit()]
                allCodes.update(extracted)
            
        except Exception as e:
            print(f"\n[!] Gagal memproses {fileName}: {e}")

    outputTxt = "extracted_billing_list.txt"
    with open(outputTxt, "w") as f:
        f.write("\n".join(allCodes))
    
    print(f"\n[*] Ekstraksi selesai. {len(allCodes)} kode unik ditemukan dan disimpan di {outputTxt}")
    return outputTxt

def generatePosUrl(billingCode, date):
    rawStr = f'{{"k":"all","t":"idpel","r":"all","d":"{date}"}}::{billingCode}'
    base64String = base64.b64encode(rawStr.encode("ascii")).decode("ascii")
    return f"https://resi.posindonesia.co.id/resi/download/all/{base64String}"

def banner():

    asciiArt = '''
                        .="=.           POSFLOW AI   
                      _/.-.-.\_     _
                     ( ( o o ) )    ))
                      |/  "  \|    //
      .-------.        \'---'/    //
     _|~~ ~~  |_       /`"""`\\  ((
   =(_|_______|_)=    / /_,_\ \\  \\
     |:::::::::|      \_\\_'__/ \  ))
     |:::::::[]|       /`  /`~\  |//
     |o=======.|      /   /    \  /
     `"""""""""`  ,--`,--'\/\    /
                   '-- "--'  '--'
   '''
    
    init()
    
    print(f"{Fore.LIGHTYELLOW_EX}{asciiArt}")
    print(f"{Fore.LIGHTGREEN_EX}Automated POS Indonesia Billing Extractor & Downloader{Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}https://github.com/FebraS/PosFlowAI{Style.RESET_ALL}")
    print("\n")

def clearTerminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def main():

    clearTerminal()
    banner()

    parser = argparse.ArgumentParser(
        description="🚀 PosFlow AI: Solusi Otomasi Ekstraksi & Unduh Billing Pos Indonesia",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Contoh Penggunaan:\n"
               "  python posflow.py -r ./folder_nota -d 2026-05-20 -o folder_output --ai\n"
               "  python posflow.py -r daftar_kode.txt -d 2026-05-20 -o folder_output\n"
    )

    # Mengelompokkan argumen agar lebih terstruktur
    input_group = parser.add_argument_group('KONFIGURASI INPUT')
    input_group.add_argument(
        "-r", "--read", 
        required=True, 
        metavar="PATH",
        help="Path ke sumber data.\nBisa berupa FOLDER (berisi PDF/Gambar) atau FILE .txt (daftar kode)."
    )
    input_group.add_argument(
        "-d", "--date", 
        required=True, 
        metavar="YYYY-MM-DD",
        help="Parameter tanggal billing yang ingin diproses (Format: YYYY-MM-DD)."
    )

    output_group = parser.add_argument_group('KONFIGURASI OUTPUT')
    output_group.add_argument(
        "-o", "--output", 
        required=True, 
        metavar="FOLDER",
        help="Nama folder tujuan untuk menyimpan hasil unduhan file PDF."
    )

    ai_group = parser.add_argument_group('FITUR CERDAS')
    ai_group.add_argument(
        "--ai", 
        action="store_true", 
        help="Gunakan Gemini 2.5 Flash untuk ekstraksi otomatis dari dokumen visual."
    )

    args = parser.parse_args()

    inputPath = args.read
    if not os.path.exists(inputPath):
        print(f"[!] Kesalahan: Path '{inputPath}' tidak ditemukan.")
        return

    if os.path.isdir(inputPath):
        if args.ai:
            inputPath = extractFromFolder(inputPath)
            if not inputPath: return
        else:
            print("[!] Input adalah folder. Tambahkan flag --ai untuk memproses isinya.")
            return

    with open(inputPath, "r") as file:
        billingCodes = [line.strip() for line in file if line.strip().isdigit()]

    if not billingCodes:
        print("[!] Tidak ada kode billing valid yang ditemukan untuk diproses.")
        return

    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"[*] Membuat folder output: {args.output}")

    print(f"[*] Memulai proses pengunduhan untuk {len(billingCodes)} kode...")
    print("-" * 50)

    for billingCode in billingCodes:
        url = generatePosUrl(billingCode, args.date)
        savePath = os.path.join(args.output, f"billing_{billingCode}.pdf")

        try:
            print(f"[Proses] {billingCode}...", end="\r")
            response = requests.get(url, timeout=25)
            
            if response.status_code == 200 and len(response.content) > 1000:
                with open(savePath, "wb") as f:
                    f.write(response.content)
                print(f"[Berhasil] {billingCode} -> Tersimpan di {args.output}      ")
            else:
                print(f"[Gagal] {billingCode} -> Data tidak ditemukan (Cek Tanggal)  ")
                
        except Exception as e:
            print(f"\n[Kesalahan] Terjadi kesalahan untuk kode {billingCode}: {e}")

    print("-" * 50)
    print(f"[*] Selesai! Semua file yang ditemukan telah diproses.")

if __name__ == "__main__":
    main()
