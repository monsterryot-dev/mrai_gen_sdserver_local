"""
공통 에러 또는 로그 메시지들을 정의하는 모듈
"""
appMessage = {
    "startup": "애플리케이션 시작 중...",
    "shutdown": "애플리케이션 종료 중..."
}

loggerMessage = {
    "initError": "Logger 초기화 중 오류 발생: {error}",
    "shutdownComplete": "Logger 종료 완료",
    "shutdownError": "Logger 종료 중 오류 발생: {error}"
}

routerLoadMessage = {
    "start": "라우터 '{name}' 로드 중...",
    "error": "라우터 '{name}' 로드 오류: {error}",
    "complete": "라우터 '{name}' 로드 완료."
}

endpointMessage = {
    "success": "엔드포인트 실행 성공: {function}",
    "error": "엔드포인트 에러: {error}"
}

fileMessage = {
    "error": "파일 오류: {error}"
}
