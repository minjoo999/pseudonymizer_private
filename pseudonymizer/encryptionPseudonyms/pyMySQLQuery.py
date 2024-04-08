import pymysql
from pseudonymizer.encryptionPseudonyms.abstractPreprocessQuery import PreprocessQuery
from typing import *
from prettytable import PrettyTable
import pandas as pd

class PyMySQLQuery(PreprocessQuery):
    def __init__(self, pw):
        self._pw = pw
        self.connection = None
        self.DBconnection = ConnectMySQLserver(self._pw)
        self.cursor = None
        self.SQL = None
    
    def connectDatabase(self, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        """MySQL DBMS 데이터베이스에 접속하는 메서드"""
        self.DBconnection.connectDatabase(serverIP, port_num, user_name, database_name, kr_encoder)
    
    def dataQueryLanguage(self, sql):
        """SQL쿼리문 작성 메서드(데이터 추출 쿼리문 캡슐화)"""
        self.SQL = f"{sql}"

    def executeQuery(self):
        """SQL쿼리문 실행 및 예외처리 메서드(데이터베이스로 쿼리를 보내서 실행)"""
        try:
            # 데이터베이스에 연결되어 있지 않은 경우, 연결을 시도
            if self.DBconnection is None:
                raise pymysql.Error
            else:
            # 연결된 데이터베이스의 커서를 사용하여 쿼리를 실행
                self.DBconnection.cursor.execute(self.SQL)
                action_output = self.DBconnection.cursor.fetchall()
                return action_output
        
        except pymysql.Error as e:
            print(f"Error Executing Query: {e}")
        
    def executeQueryAsDataFrame(self):
        """SQL 쿼리를 실행한 결과를 판다스 데이터프레임으로 출력하는 메서드"""
        try:
            action_output = self.DBconnection.cursor.execute(self.SQL)
            records = self.DBconnection.cursor.fetchall()
            attributes = [i[0] for i in self.DBconnection.cursor.description]
            querydata = pd.DataFrame(records, columns = attributes)
            return querydata
        
        except pymysql.Error as e:
            print(f"Executing query error: {e}")

    def useFetchallQuery(self):
        """SQL 쿼리 실행 결과의 cursor.fetchall() 을 사용할 수 있도록 하는 메서드"""
        try:
            action_output = self.DBconnection.cursor.execute(self.SQL)
            records = self.DBconnection.cursor.fetchall()
            return records
        except pymysql.Error as e:
            print(f"Executing query error: {e}")
    
    def commitTransaction(self):
        """실행결과를 확정(트랜잭션을 커밋)하는 메서드"""
        self.DBconnection.connection.commit()
    
    def closeConnection(self):
        """데이터베이스와의 연결을 종료하는 메서드"""
        self.DBconnection.close_connection()

    def executeQueryAsDataFrame(self):
        """SQL 쿼리를 실행한 결과를 판다스 데이터프레임으로 출력하는 메서드"""
        try:
            action_output = self.DBconnection.cursor.execute(self.SQL)
            records = self.DBconnection.cursor.fetchall()
            attributes = [i[0] for i in self.DBconnection.cursor.description]
            querydata = pd.DataFrame(records, columns = attributes)
            return querydata
        
        except pymysql.Error as e:
            print(f"Executing query error: {e}")
        

class ConnectMySQLserver:
    def __init__(self, pw):
        self._pw = pw
        self.connection = None
        self.cursor = None
    
    def connectDatabase(self, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        """MySQL DBMS 데이터베이스에 접속 메서드
        : 서버IP주소, 사용자명, 계정 암호, 데이터베이스명, 한글 인코딩 방식"""
        try:
            self.connection = pymysql.connect(
                host=serverIP, port=port_num,
                user=user_name, password=self._pw,
                db=database_name, charset=kr_encoder
            )
            self.cursor = self.connection.cursor()
        except pymysql.Error as e:
            print(f"Error Connecting to MySQL from Python: {e}")
    
    def closeConnection(self):
        """연결 및 커서 닫기 메서드"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()