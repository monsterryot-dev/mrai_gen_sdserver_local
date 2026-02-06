"""
핸들러 메세지 상수 정의 모듈
"""
defaultMessage = "알 수 없는 오류가 발생했습니다."

handlerMessage = {
    400: "잘못된 요청입니다.",
    401: "인증이 필요합니다.",
    422: "요청 데이터가 유효하지 않습니다.",
    403: "접근이 금지되었습니다.",
    404: "요청하신 리소스를 찾을 수 없습니다.",
    500: "서버 내부 오류가 발생했습니다."
}

validationMessage = {
    "missing": "필수 입력 {key}이(가) 누락되었습니다.",
    "int_parsing": "입력 받은 값 {key}이(가) 정수만 허용됩니다.",
    "literal_error": "입력 받은 값 {key}이(가) 올바르지 않습니다.[사용 가능한 값: {expected}]",
    "value_error": "입력 받은 값 {key}이(가) 잘못된 값입니다. [사용 가능한 값: {error}]",
    "greater_than_equal": "입력 받은 값 {key}이(가) {ge} 이상이어야 합니다.",
    "greater_than": "입력 받은 값 {key}이(가) {gt} 초과이어야 합니다.",
    "less_than_equal": "입력 받은 값 {key}이(가) {le} 이하이어야 합니다.",
    "less_than": "입력 받은 값 {key}이(가) {lt} 미만이어야 합니다.",
}