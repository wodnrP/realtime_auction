# 개발 주의사항

---

**프로젝트 pull할 경우**
- pull 이후, 프로젝트 폴터(config)와 동일한 위치에 .env 파일 생성
- https://djecrety.ir/ 에서 django secret_key 생성 후 .env/SECRET_KEY에 복사
```
DEBUG=...
SECRET_KEY=...
```