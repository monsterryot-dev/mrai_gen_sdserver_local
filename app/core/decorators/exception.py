from contextlib import contextmanager

@contextmanager
def serverStartContext():
    print("서버 시작 중...")
    try:
        yield
    except KeyboardInterrupt:
        print("서버 중지 요청 받음.")
    except Exception as e:
        print(f"서버 오류: {e}")
    finally:
        print("서버 중지.")