"""
메인 로거 모듈
"""
import logging
from os import path
from logging.handlers import TimedRotatingFileHandler

from app.core.settings import settings
from app.utils.file import checkAndCreateDir

from app.constants.messages import loggerMessage

class Logger:
    def __init__(self):
        try:
            debug = settings.debug

            self.name = settings.appName
            self.logLevel = logging.DEBUG if debug else logging.INFO
            self.logFormat = logging.Formatter(settings.logFormat)

            self.fileName = f"{self.name}.log"
            self.filePath = settings.logFilePath
            self.fileFullPath = path.join(self.filePath, self.fileName)

            # 로거 생성
            self.logger = logging.getLogger(self.name)
            self.logger.setLevel(self.logLevel)    

            # 핸들러 추가
            self.logger.addHandler(self._fileHandler())
            if debug:
                self.logger.addHandler(self._streamHandler())
        except Exception as e:
            print(loggerMessage["initError"].format(error=e))

    def _fileHandler(self) -> TimedRotatingFileHandler:
        checkAndCreateDir(self.filePath)

        fileoConfig = {
            "filename": self.fileFullPath,
            "when": "midnight",
            "interval": 1,
            "backupCount": 15,
            "encoding": "utf-8"
        }
        fileHandler = TimedRotatingFileHandler(**fileoConfig)
        fileHandler.setLevel(self.logLevel)
        fileHandler.setFormatter(self.logFormat)

        return fileHandler
    
    def _streamHandler(self) -> logging.StreamHandler:
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(self.logLevel)
        streamHandler.setFormatter(self.logFormat)

        return streamHandler
    
    def writeLog(self, level: str, message: str):
        logMethod = getattr(self.logger, level.lower(), self.logger.info)
        logMethod(message)
    
    def shutdown(self):
        """로거 종료 및 리소스 정리"""
        try:
            # 모든 핸들러를 flush하고 close
            for handler in self.logger.handlers[:]:
                handler.flush()
                handler.close()
                self.logger.removeHandler(handler)
            print(loggerMessage["shutdownComplete"])
        except Exception as e:
            print(loggerMessage["shutdownError"].format(error=e))
    
logger = Logger()
