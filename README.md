# mrai sd local 서버
## 필수버전
python = 3.12+
## service 파일 설치 및 실행
### windows 환경
관리자 환경에서 실행해야 합니다.
```
# 빌드
python {빌드 정보 파일} build

# 서비스 설치
.\build\exe.win-amd64-3.xx\{설치파일} install

# 서비스 시작
.\build\exe.win-amd64-3.xx\{설치파일} start

# 서비스 중단
.\build\exe.win-amd64-3.xx\{설치파일} stop

# 서비스 제거
.\build\exe.win-amd64-3.xx\{설치파일} remove

# window 명령어
# 서비스 상태 확인
Get-Service -Name "{서비스 이름}"

# 서비스 시작
Get-Service -Name "{서비스 이름}" | Start-Service
# 서비스 중단
Get-Service -Name "{서비스 이름}" | Stop-Service
# 서비스 재시작
Get-Service -Name "{서비스 이름}" | Restart-Service
# 서비스 시작 유형 변경
Get-Service -Name "{서비스 이름}" -StartupType Automatic
# 상세 정보 확인
Get-Service -Name "{서비스 이름}" | Format-List *
```