from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class UpdateSerialNumColumn(PyMySQLQuery):
    """원본 테이블에 결합키 생성을 위한 일련번호 컬럼을 생성하기 위한 쿼리를 날리는 클래스"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)
    
    def addSerialNumColumn(self, tables: DBContainer, serial_column, serial_text, identifier_column):
        """결합키 연계정보(매핑테이블) 생성에 활용될 각 결합신청자의 테이블별 일련번호 생성하는 실행 메서드"""
        schema = tables.getSchema()
        table = tables.getTable()
        if identifier_column is None:  
            # 컬럼명 중복시 해당 컬럼 삭제
            super().dataQueryLanguage(f"ALTER TABLE {schema}.{table} DROP COLUMN {serial_column}")  
            super().executeQuery()
            super().commitTransaction()

            # 일련번호 컬럼 생성
            super().dataQueryLanguage(f"ALTER TABLE {schema}.{table} ADD COLUMN {serial_column} VARCHAR(1000)")
            super().executeQuery()
            super().commitTransaction()

            # 0으로 초기화 후 @counter를 이용하여 1 더하여 일련번호 컬럼에 값 할당
            super().dataQueryLanguage("SET @counter = 0;")
            super().executeQuery()
            super().commitTransaction()

            super().dataQueryLanguage(f"UPDATE {schema}.{table} SET {serial_column} = CONCAT('{serial_text}', @counter := @counter + 1);")
            super().executeQuery()
            super().commitTransaction()
        else:
            pass