import sys # sys 모듈 가져오기
import binascii # binascii 모듈 가져오기
import os

def tjtp(r):
    owd = os.getcwd()
    rtx = os.path.basename(r)
    rty = os.path.splitext(rtx)
    rtz = rty[0]
    c=1 # 카운터 생성
    f=open(r,"rb") # 파일 열기
    
    try:
        os.mkdir(rtz)
    except FileExistsError:
        print('경고. ' + rtz + ' 폴더가 이미 있습니다. ' '프로그램이 아마도 오작동할 수 있습니다. ' + rtz + ' 폴더를 삭제해주세요.')  
    os.chdir(rtz)
    
    f.seek(2) # 2바이트로 이동한다
    vv=f.read(5) # 버전을 읽는다
    if vv != b'\x56\x31\x2E\x30\x31': # V1.01 인가?
        print("추출가능한 버전이 아닙니다. 장비를 정지합니다.") # 아니면 못함
        sys.exit(1) # ㅅㄱ
    while True: # 마지막 파일 위치 확인기
        f.seek(28+128*c-(16-4*(c-1)))
        fh=f.read(16)
        if fh != b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            break
        c=c+1
    da=48+128*c-(16-4*(c-1))+20
    c=1 # 카운터 초기화
    print("준비 완료!")
    while True: # 반복 시작
        f.seek(28+128*c-(0-4*(c-1))-128) # 이름 위치로 이동한다
        n1=f.read(128) # 128바이트 만큼 이름을 읽는다
        f.seek(28+128*c-(16-4*(c-1))) # 마지막 파일 확인기 시작
        ph=f.read(16)
        if ph != b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            os.chdir(owd)
            break # 마지막 16바이트가 안 비어있으면 반복 종료
        n=n1.split(b'\0',1)[0] # 이름에서 \x00 부분을 제거 (인터넷에서 주워옴)
        m=n.decode('ascii') # 이름을 텍스트로 변환
        mm=m.split('\\') # 디렉토리 삭제 시작
        mmm=mm[-1] # 디렉토리 삭제 완료
        z=open(mmm,'bw') # 파일 생성
        f.seek(28+128*c-(16-4*(c-1))+16) # 파일 크기로 이동한다
        y=f.read(4) # 파일 크기가 있는 구간 기록
        x=binascii.hexlify(y) # 파일 위치와 크기가 있는 데이터 변환
        w=x.decode('ascii') # 데이터를 텍스트로 변환
        f1=w[0:2] # 파일 크기 4구간
        f2=w[2:4] # 파일 크기 3구간
        f3=w[4:6] # 파일 크기 2구간
        f4=w[6:8] # 파일 크기 1구간
        fs=f4+f3+f2+f1 # 파일 크기 산출
        ds=int(fs, base=16) # 파일 크기를 10진수로 변환
        f.seek(da-152) # 파일 위치로 이동
        data=f.read(ds) # 파일 크기만큼 파일을 읽음
        z.write(data) # 읽은 파일을 생성한 파일에 기록
        z.close() # 파일 저장
        da=da+ds # 파일 위치 기록
        c=c+1 # 카운터 1 추가 (그리고 반복으로 이동)
        
rrr = sys.argv[1]
tjtp(rrr)        