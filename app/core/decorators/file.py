from contextlib import contextmanager

@contextmanager
def fileContext(filePath, mode):
    f = open(filePath, mode)
    try:
        yield f
    except Exception as e:
        print(f"File Error: {e}")
    finally:
        f.close()
    