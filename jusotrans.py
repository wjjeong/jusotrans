import glob
from builtins import print

from pyproj import CRS
from pyproj import Transformer

# 우편번호 경로 설정
path = "C:\post\*"
file_list = glob.glob(path)

# txt 파일만 변수에 저장
file_list_txt = [file for file in file_list if file.endswith(".txt")]

# grs80 좌표계설정
projGRS80 = CRS.from_proj4("+proj=tmerc +lat_0=38 +lon_0=127.5 +k=0.9995 +x_0=1000000 +y_0=2000000 +ellps=GRS80 +units=m +no_defs")

# transformer 설정  grs80 -> wgs84
transformer = Transformer.from_crs("EPSG:4326", projGRS80)

for file_txt in file_list_txt:
    # main Logic
    # 1. file open
    fi_juso = open(file_txt, 'r')
    fo_juso = open(file_txt+".wgs84.out", 'w')
    # 2. 변환
    while True:
        line = fi_juso.readline()
        if not line: break
        la=""
        lo=""
        str2 = line.split("|")
        # print(line)
        # print(str2[16])
        # print(str2[17])
        if len(str2[16]) > 0 and len(str2[17]) > 0:
            # grs80 좌표에서 위경도 좌표로 변환
            result = transformer.transform(str2[16], str2[17])

            la = str(result[0])
            lo = str(result[1])
            # print(la)
            # print(lo)
        out_juso = line.replace("\n","")+"|"+la+"|"+lo+"\n"
        fo_juso.write(out_juso)

    # 3. 결과 파일 저장
    fi_juso.close()
    fo_juso.close()
