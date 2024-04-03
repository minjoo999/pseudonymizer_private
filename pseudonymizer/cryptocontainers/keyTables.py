from pseudonymizer.cryptocontainers.bundleTables import BundleTables
from pseudonymizer.cryptocontainers.initTables import InitTables


class KeyTables(BundleTables):
    """결합키 생성 테이블 저장 클래스"""
    init_tables = []
    key_tables = []
    columns = None
    serial_cols = []
    key_col = None

    @classmethod
    def addInitTables(cls, tables: InitTables):
        """원본테이블, 결합키 생성 테이블, 결합대상정보 테이블로 이루어진 InitTables 클래스 받기"""
        cls.init_tables.append(tables)

    @classmethod
    def addKeyCol(cls, key_col: str):
        """각 테이블에서 결합키가 놓일 컬럼명 더하기"""
        cls.key_col = key_col

    @classmethod
    def addColumns(cls, columns: list):
        """결합키 생성 항목 컬럼명 입력 메서드"""
        cls.columns = columns

    @classmethod
    def selectTables(cls):
        """InitTables에서 key_table만 골라내어 저장하기"""
        for table in cls.init_tables:
            cls.key_tables.append(table.key_table)
            cls.serial_cols.append(table.serial_col)

    @classmethod
    def getTableList(cls):
        """결합키 생성 테이블 출력"""
        return cls.key_tables
    
    @classmethod
    def getSchemas(cls):
        """스키마명만 모아서 출력"""
        schemas = []
        for table in cls.key_tables:
            schemas.append(table.getSchema())

        return schemas
    
    @classmethod
    def getTables(cls):
        """테이블명만 모아서 출력"""
        tables = []
        for table in cls.key_tables:
            tables.append(table.getTable())

    @classmethod
    def getSerialCols(cls):
        return cls.serial_cols
    
    @classmethod
    def reset(cls):
        """클래스 변수 초기화"""
        cls.init_tables = []
        cls.key_tables = []
        cls.columns = None
        cls.serial_cols = []
        cls.key_col = None