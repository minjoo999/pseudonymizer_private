import binascii
import os
from pseudonymizer.cryptocontainers.initTables import InitTables
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class EncryptKeyCol(PyMySQLQuery):
    """결합키 암호화 클래스 : InitTables에 들어있는 key_table의 join_key에 적용"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        self.kr_encoder = kr_encoder
        super().__init__(pw = pw)
        super().connectDatabase(serverIP, port_num, user_name, database_name, kr_encoder)
        
        self.init_tables = None
        self.key_tables = None
        self.salt_col = None

    def addInitTables(self, init_tables: InitTables):
        """원본 테이블, 결합키 테이블, 결합대상정보 테이블 객체 통해 입력"""
        self.init_tables = init_tables
        self.serial_col = self.init_tables.serial_col
        self.serial_text = self.init_tables.serial_text
        self.salt_col = self.init_tables.salt_col

    def encryptKeyCol(self, func: str):
        """self.init_tables에 저장된 모든 key_table을 대상으로 암호화를 실행하는 메서드"""
        schema = self.init_tables.key_table.getSchema()
        table = self.init_tables.key_table.getTable()
        self.createKey(func, schema, table, self.init_tables.join_key, self.salt_col)

    def createKey(self, func: str, schema: str, table: str, key_col: str, salt_col: str):
        """결합키 암호화 방식을 선택하여 실행시키는 메서드"""
        if func == "SHA256":
            self.applySHA256(schema, table, key_col, salt_col)
        elif func == "SHA512":
            self.applySHA512(schema, table, key_col, salt_col)
        else:
            print("SHA256과 SHA512 중 하나를 입력하십시오")

    def applySHA256(self, schema: str, table: str, key_col: str, salt_col: str):
        """SHA256 해시함수를 통해 결합키 컬럼을 암호화하는 메서드"""
        sql = f"UPDATE {schema}.{table} SET {key_col} = SHA2(CONCAT({key_col}, {salt_col}), 256)"
        super().dataQueryLanguage(sql)
        super().executeQuery()
        super().commitTransaction()

    def applySHA512(self, schema: str, table: str, key_col: str, salt_col: str):
        """SHA512 해시함수를 통해 결합키 컬럼을 암호화하는 메서드"""
        sql = f"UPDATE {schema}.{table} SET {key_col} = SHA2(CONCAT({key_col}, {salt_col}), 512)"
        super().dataQueryLanguage(sql)
        super().executeQuery()
        super().commitTransaction()