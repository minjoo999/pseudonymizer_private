from pseudonymizer.cryptocontainers.initTables import InitTables
from pseudonymizer.cryptocontainers.tableContainer import TableContainer


class MakeInitTables:
    """InitTables 채우는 클래스"""
    def __init__(self, original_table: tuple, key_table: tuple, target_table: tuple):
        self.original_table = original_table
        self.key_table = key_table
        self.target_table = target_table

    def makeTable(self, schema: str, table: str):
        """TableContainer 클래스를 활용하여 스키마 및 테이블명을 집어넣는 메서드"""
        table_container = TableContainer()
        table_container.setSchemaTable(schema=schema, table=table)
        return table_container
    
    def makeInitTables(self, columns: list, serial_col: str, serial_text: str, join_key: str):
        """InitTables 클래스를 활용하여 원본, 결합키, 결합대상정보 스키마/테이블 모으는 메서드"""
        init_tables = InitTables()
        
        # 원본 스키마/테이블 모으기
        original_container = self.makeTable(schema=self.original_table[0], table=self.original_table[1])
        init_tables.addOriginalTable(original_table=original_container)

        # 결합키 스키마/테이블 모으기
        key_container = self.makeTable(schema=self.key_table[0], table=self.key_table[1])
        init_tables.addKeyTable(key_table=key_container)

        # 결합대상정보 스키마/테이블 모으기
        target_container = self.makeTable(schema=self.target_table[0], table=self.target_table[1])
        init_tables.addTargetTable(target_table=target_container)

        # 결합키 및 일련번호 관련정보 모으기
        init_tables.addKeyColInfo(columns)
        init_tables.addSerialColInfo(serial_col, serial_text, join_key)

        return init_tables