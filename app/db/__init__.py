# from pymongo import MongoClient

# from app.core.settings import settings

# # BUILD: 배포시 mongodb 계정 정보 추가 필요
# # BUILD: 배포시 mongodb port 번호 변경해야 할 수 있음
# class MongoManager:
#     def __init__(self):
#         self.client = MongoClient(
#             settings.MongoDB,
#             maxPoolSize=50,
#             minPoolSize=10,
#             maxIdleTimeMS=60000, # 60초 - 사용 안함 동안 커넥션에서 자동 제거
#             connectTimeoutMS=2000, # 2초  - 커넥션 타임아웃 설정
#             serverSelectionTimeoutMS=3000,
#             heartbeatFrequencyMS=10000, # 10초 - 서버 상태 체크 주기
#         )
#         self.db = self.client[settings.Database]

#     def getCol(self, colName: str):
#         return self.db[colName]
    
#     def inster(self, colName: str, data: dict):
#         return self.getCol(colName).insert_one(data)
    
#     def insterMany(self, colName: str, dataList: list[dict]):
#         return self.getCol(colName).insert_many(dataList)
    
#     def findData(self, colName: str, query: dict):
#         return self.getCol(colName).find_one(query)
    
#     def findDataMany(self, colName: str, query: dict):
#         return self.getCol(colName).find(query)
    
#     def update(self, colName: str, query: dict, values: dict):
#         return self.getCol(colName).update_one(query, {"$set": values})
    
#     def updateMany(self, colName: str, query: dict, values: dict):
#         return self.getCol(colName).update_many(query, {"$set": values})
    
#     def delete(self, colName: str, query: dict):
#         return self.getCol(colName).delete_one(query)

#     def deleteMany(self, colName: str, query: dict):
#         return self.getCol(colName).delete_many(query)

# mongoManager = MongoManager()