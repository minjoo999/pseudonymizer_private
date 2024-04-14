from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.encryptionPseudonyms.encrypttoKeyColumn import EncryptoKeyColumn
from pseudonymizer.encryptionPseudonyms.insertKeyintoMainTable import InsertKeyintoMainTable
from pseudonymizer.encryptionPseudonyms.insertTargetintoMainTable import InsertTargetintoMainTable
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery
from pseudonymizer.encryptionPseudonyms.updateSerialNumColumn import UpdateSerialNumColumn


class UpdateEncryptedKeyIntoDB(PyMySQLQuery):
    """결합키 암호화 및 결합대상정보 테이블 생성 클래스"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str, 
                 main_tablename: str, key_schema: str, key_tablename: str,
                 target_schema: str, target_tablename: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)
        DQL = f"SELECT * FROM {main_tablename}"
        super().dataQueryLanguage(DQL)
        self.table = super().executeQueryAsDataFrame()
        super().commitTransaction()

        self.main_table = DBContainer()
        self.main_table.setSchemaTable(schema=database_name, table=main_tablename)

        self.key_table = DBContainer()
        self.key_table.setSchemaTable(schema=key_schema, table=key_tablename)

        self.target_table = DBContainer()
        self.target_table.setSchemaTable(schema=target_schema, table=target_tablename)

        self.updateSerialNumColumn = UpdateSerialNumColumn(pw, serverIP, port_num, user_name, database_name, kr_encoder)
        self.insertKeyintoMainTable = InsertKeyintoMainTable(pw, serverIP, port_num, user_name, database_name, kr_encoder)
        self.insertTargetintoMainTable = InsertTargetintoMainTable(pw, serverIP, port_num, user_name, database_name, kr_encoder)
        self.encryptoKeyColumn = EncryptoKeyColumn(pw, serverIP, port_num, user_name, database_name, kr_encoder)
    
    def __str__(self):
        return self.table.info()

    def UpdateintoDBTables(self, key_table, key_column, serial_column, serial_text, identifier_column, salt_value, salt_column, key_schema, hash_byte_type):
        """일련번호 컬럼 생성, 결합키 생성항목 및 결합 대상정보 테이블 입력, 결합키 암호화 실행 메서드"""
        self.updateSerialNumColumn.addSerialNumColumn(tables = self.main_table, serial_column = serial_column, 
                                serial_text = serial_text, 
                                identifier_column = identifier_column)
        
        self.insertKeyintoMainTable.insertKeyIntoDB(tables = self.main_table,
                                                    key_table_info = self.key_table, 
                                                    key_table = key_table, 
                                                    join_key = key_column,
                                                    salt_value = salt_value, 
                                                    salt_column = salt_column,
                                                    serial_column = serial_column, 
                                                    serial_text = serial_text)
        
        self.insertTargetintoMainTable.insertTargetIntoDB(tables = self.main_table,
                                                          target_table = self.target_table, 
                                                          key_table = key_table)
        
        self.encryptoKeyColumn.encryptoKeytoHashvalue(hash_byte_type = hash_byte_type, 
                                                     key_schema = key_schema, 
                                                     key_table = self.key_table.getTable(), 
                                                     key_column = key_column, 
                                                     salt_column = salt_column)
        
    def printKeyTablesInfo(cls, schema_tablename: dict):
        """테이블 컬럼명 확인절차 실행 메서드"""
        # 키테이블명 딕셔너리 = {key(키 스키마) : value(키 테이블)}
        schema = schema_tablename.keys()
        tablename = schema_tablename.values()

        # 키테이블의 컬럼명(결합키, 일련번호, 솔트) 반환
        sql = f"SHOW COLUMNS FROM {schema}.{tablename}"
        super().dataQueryLanguage(sql)
        key_schema_tablenames = super().executeQueryAsDataFrame()["Field"].tolist()
        
        return key_schema_tablenames