# Smart QR - Android WebView App

`https://bhseol15.github.io/` (Smart QR - 스마트 QR 메이커) 사이트를 보여주는 전체화면 안드로이드 웹뷰 앱입니다.

컴퓨터에 안드로이드 스튜디오가 없어도 **GitHub Actions CI/CD**를 통해 클릭 한 번 또는 Git Push만으로 즉시 설치 가능한 APK 파일을 빌드하고 다운로드할 수 있습니다.

---

## 📱 주요 기능

- **몰입형 전체화면 (Immersive Fullscreen)**:
  - 상단 상태바 및 하단 네비게이션 바를 자동으로 숨겨 화면을 100% 온전히 웹앱으로 활용합니다.
  - 화면 상/하단을 스와이프하면 일시적으로 시스템 바가 나타나는 트랜지언트 모드가 적용되어 있습니다.
- **QR 이미지 다운로드 완벽 지원**:
  - 웹 브라우저에서 생성된 QR 코드(`data:image/...`, `blob:`, 일반 HTTP 다운로드)를 감지하여 안드로이드 기기의 다운로드 폴더(`Downloads`)에 안전하게 저장합니다.
- **로고 업로드 지원 (File Chooser)**:
  - QR 코드 중앙에 로고 이미지를 삽입할 때 안드로이드 사진 갤러리/파일 탐색기가 정상적으로 열립니다.
- **스와이프 새로고침 (Pull-to-Refresh)**:
  - 페이지 최상단에서 아래로 당겨 언제든지 새로고침할 수 있습니다.
- **오프라인 / 연결 오류 처리**:
  - 네트워크 연결이 끊어졌을 때 기본 브라우저 에러창 대신 세련된 다크 테마 에러 화면과 "다시 시도" 버튼을 제공합니다.
- **뒤로 가기 제어**:
  - 웹 페이지 탐색 기록이 있으면 이전 페이지로 이동하고, 첫 화면에서는 2초 내에 두 번 눌러야 종료되도록 안내 토스트를 띄웁니다.
- **맞춤형 전용 앱 아이콘**:
  - Smart QR의 보라/인디고/핑크 그라데이션과 QR 패턴을 결합한 고해상도 앱 아이콘(기본, 원형, 안드로이드 8.0+ 적응형 Adaptive Icon, 512x512 고화질 아이콘)이 탑재되어 있습니다.

---

## 🚀 GitHub Actions로 APK 빌드 및 다운로드 방법

로컬 PC에 안드로이드 스튜디오나 SDK가 없어도 GitHub을 통해 바로 APK를 얻을 수 있습니다.

### 1. GitHub 저장소로 코드 푸시
```bash
git init
git add .
git commit -m "feat: Initial Smart QR Android WebView App"
git branch -M main
git remote add origin https://github.com/<본인-깃허브-아이디>/<저장소-이름>.git
git push -u origin main
```

### 2. GitHub Actions 자동 빌드 확인
1. GitHub 저장소 상단의 **`Actions`** 탭을 클릭합니다.
2. `Build Android APK` 워크플로우가 자동으로 실행되는 것을 볼 수 있습니다. (약 1~2분 소요)
3. 수동으로 실행하고 싶다면 좌측의 **`Build Android APK`** 선택 후 우측의 **`Run workflow`** 버튼을 누르면 됩니다.

### 3. APK 파일 다운로드
1. 완료된 워크플로우 실행 내역을 클릭합니다.
2. 페이지 하단의 **`Artifacts`** 섹션을 확인합니다:
   - **`SmartQR-debug-apk`**: 스마트폰에 즉시 설치하여 테스트할 수 있는 Debug APK
   - **`SmartQR-release-apk`**: 서명된 Release APK
3. 원하는 APK zip 파일을 다운로드하여 압축을 풀고, 안드로이드 스마트폰에 넣거나 카카오톡/드라이브 등을 통해 전송하여 설치하시면 됩니다!

> 💡 **안내**: 스마트폰에 처음 설치할 때 "출처를 알 수 없는 앱 설치 허용" 팝업이 뜨면 "허용"을 선택하시면 바로 실행됩니다.

---

## 📂 프로젝트 구조

```
├── .github/workflows/
│   └── build.yml               # GitHub Actions CI 빌드 자동화 스크립트
├── app/
│   ├── build.gradle            # 앱 빌드 설정 및 의존성
│   └── src/main/
│       ├── AndroidManifest.xml # 권한 및 액티비티 설정
│       ├── ic_launcher-playstore.png # 512x512 고화질 아이콘
│       ├── java/com/bhseol/smartqr/
│       │   └── MainActivity.kt # 전체화면 웹뷰, 다운로드, 파일첨부 처리
│       └── res/                # 아이콘 및 리소스 레이아웃
├── gradle/wrapper/             # Gradle Wrapper 파일
├── gradlew / gradlew.bat       # Gradle 빌드 실행 스크립트
├── build.gradle                # 루트 빌드 설정
└── settings.gradle             # 프로젝트 모듈 설정
```
