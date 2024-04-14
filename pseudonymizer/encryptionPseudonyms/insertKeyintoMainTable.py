from pseudonymizer.cryptocontainers.bundleMainTable import BundleMainTable
from pseudonymizer.cryptocontainers.bundleKeyTable import BundleKeyTable
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class InsertKeyintoMainTable(PyMySQLQuery):
    """원본 테이블에서 결합키 생성항목으로 결합키 테이블을 생성하는 클래스"""
    bundleMainTable = BundleMainTable()
    bundleKeyTable = BundleKeyTable()

    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)
        self.dbtables = None
        
    
    def insertKeyIntoDB(self, tables, key_table_info, key_table, join_key, salt_value, salt_column, serial_column, serial_text):
        """
        결합키를 테이블에 입력하는 실행 메서드
        -----------------------------------
        tables: pd.DataFrame 원본 데이터
        key_table_info: 결합키 생성항목 테이블 스키마, 테이블명 (DBContainer 타입)
        key_table: List 결합키 생성항목 대상 컬럼 조합
        key_column: str 생성할 결합키 컬럼명
        salt_value: str 일방향 암호화 해시값
        salt_column: str 외부에서 입력받을 해시값 컬럼명
        """
        # 원본 테이블 및 결합키 스키마.테이블명 등 로드
        key_schema, key_tablename, main_schema, main_tablename = self.loadTableObject(tables, key_table_info, join_key)

        # 결합키 컬럼 생성
        key_column = self.joinKeyColumn(key_table)
            # INPUT 결합키 생성 컬럼 -> OUTPUT 결합키 컬럼명
            
        # 데이터베이스 내 결합키 컬럼 기존재 시 삭제 및 삽입 수행 
        super().dataQueryLanguage(f"DROP TABLE IF EXISTS {key_schema}.{key_tablename}")
        super().executeQuery()

        sql = f"CREATE TABLE {key_schema}.{key_tablename} AS SELECT {serial_column}, {key_column} FROM {main_schema}.{main_tablename}"
        super().dataQueryLanguage(sql)
        super().executeQuery()
        super().commitTransaction()

        self.addKeyColumn(key_schema, key_tablename, join_key, key_column)
        self.addSaltColumn(key_schema, key_tablename, salt_value, salt_column)

        super().commitTransaction()

    @classmethod
    def loadTableObject(cls, tables, key_table_info, join_key):
        # 결합키 스키마.테이블명 등 로드
        
        cls.bundleKeyTable.addDBTables(tables) # 원본 데이터
        cls.bundleKeyTable.selectTables(key_table_info) # 키 데이터
        cls.bundleKeyTable.addKeyColumn(join_key) # 결합키 컬럼명
        cls.bundleKeyTable.getTableList()

        key_schema = cls.bundleKeyTable.getSchemas() # 키 테이블 스키마명
        key_tablename = cls.bundleKeyTable.getTables() # 키 테이블명

        # 원본 스키마.테이블명 로드
        cls.bundleMainTable.selectTables(tables)

        main_schema = cls.bundleMainTable.getSchemas()
        main_tablename = cls.bundleMainTable.getTables()

        return key_schema, key_tablename, main_schema, main_tablename
    
     
    @classmethod
    def joinKeyColumn(cls, key_column):
        return ", ".join(key_column)

    def addKeyColumn(self, key_schema, key_result, join_key, join_columns):
        """결합키 컬럼 만드는 클래스 메서드"""
        super().dataQueryLanguage(f"ALTER TABLE {key_schema}.{key_result} ADD COLUMN {join_key} VARCHAR(1000)")
        super().executeQuery()

        super().dataQueryLanguage(f"UPDATE {key_schema}.{key_result} SET {join_key} = CONCAT({join_columns})")
        super().executeQuery()
        super().commitTransaction()

    def addSaltColumn(self, key_schema, key_result, salt_value, salt_column):
        """SALT값 컬럼 만드는 클래스 메서드"""
        super().dataQueryLanguage(f"ALTER TABLE {key_schema}.{key_result} ADD COLUMN {salt_column} VARCHAR(1000)")
        super().executeQuery()

        super().dataQueryLanguage(f"UPDATE {key_schema}.{key_result} SET SALT = '{salt_value}'")
        super().executeQuery()