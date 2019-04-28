# Deploy Guide

#### Deploy(배포)를 위한 참고사항
- 파이썬 가상 환경 만들고 pip3 install -r requirements.txt
- Django에서 쓰는 database는 기본값인 sqlite 말고 다른 것을 사용
- Nginx + Gunicorn 조합으로 간단하게 운용 가능
- Nginx에서 reverse proxy 형태로 Gunicorn 연결하고 static 파일도 따로 연결
- Gunicorn은 데몬으로 실행 (<http://docs.gunicorn.org/en/stable/deploy.html> 참고)
- Gunicorn의 worker class는 비동기로 설정 (gevent 추천)
- Gunicorn 로그 설정 (logrotate로 로그 관리, Nginx 로그는 끄기)
- certbot을 이용해 ssl 인증서 자동 갱신 및 https 설정 (certbot.timer 활성화 시키기)
- 정기적인 재부팅 설정 (crontab 등 이용)

<br/>

개인적으로 참고하기 위한 용도로 작성된 문서입니다.
