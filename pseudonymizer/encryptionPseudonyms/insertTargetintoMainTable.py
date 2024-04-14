from pseudonymizer.cryptocontainers.bundleMainTable import BundleMainTable
from pseudonymizer.cryptocontainers.bundleTargetTable import BundleTargetTable
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class InsertTargetintoMainTable(PyMySQLQuery):
    """원본 테이블에서 결합대상 가명정보를 복사하여 테이블을 생성하는 클래스"""
    bundleMainTable = BundleMainTable()
    bundleTargetTable = BundleTargetTable()

    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)
        self.dbtables = None
        
    
    def insertTargetIntoDB(self, tables, target_table, key_table):
        """
        결합키를 테이블에 입력하는 실행 메서드
        -----------------------------------
        tables: pd.DataFrame 원본 데이터
        key_table: List 결합키 생성항목 대상 컬럼 조합        

        """
        # 원본 테이블 및 결합키 스키마.테이블명 등 로드
        target_schema, target_tablename, main_schema, main_tablename = self.loadTableObject(tables, target_table)

        # 데이터베이스 내 결합키 컬럼 기존재 시 삭제 및 삽입 수행 
        super().dataQueryLanguage(f"DROP TABLE IF EXISTS {target_schema}.{target_tablename}")
        super().executeQuery()

        sql = f"CREATE TABLE {target_schema}.{target_tablename} AS SELECT * FROM {main_schema}.{main_tablename}"
        super().dataQueryLanguage(sql)
        super().executeQuery()
        super().commitTransaction()

        self.dropKeyColumn(target_schema, target_tablename, key_table)
        super().commitTransaction()

    @classmethod
    def loadTableObject(cls, tables, target_table):
        # 결합대상정보 등 스키마.테이블명 등 로드
        cls.bundleMainTable.selectTables(tables) # 원본 데이터
        cls.bundleTargetTable.selectTables(target_table) # 타겟 데이터
        cls.bundleTargetTable.getTableList()

        target_schema = cls.bundleTargetTable.getSchemas() # 타겟 테이블 스키마명
        target_tablename = cls.bundleTargetTable.getTables() # 타겟 테이블명

        # 원본 스키마.테이블명 로드
        main_schema = cls.bundleMainTable.getSchemas()
        main_tablename = cls.bundleMainTable.getTables()

        return target_schema, target_tablename, main_schema, main_tablename
     
    def dropKeyColumn(self, target_schema: str, target_tablename: str, key_table: list):
        """결합키 생성항목 원본 테이블에서 제거"""
        for column in key_table:
            drop_sql = f"ALTER TABLE {target_schema}.{target_tablename} DROP COLUMN {column}"
            super().dataQueryLanguage(drop_sql)
            super().executeQuery()