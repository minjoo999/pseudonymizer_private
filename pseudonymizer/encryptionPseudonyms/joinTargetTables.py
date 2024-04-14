from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery
from typing import *


class JoinTargetTables(PyMySQLQuery):
    """매핑테이블의 일련번호를 기준으로 결합대상 가명정보를 결합하는 클래스"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            pw, serverIP, port_num, user_name, database_name, kr_encoder)
        self.target_tables = DBContainer()
        self.mapping_table = DBContainer()

    def joinTargetTables(self, combine_schema: str, combine_tablename: str, mapping_schema: str, mapping_tablename: str, target_schemas: List, target_tablenames: List, target_join_columns: List, serialnum_columns: str):
        schema, tablename = self.addCombineTable(combine_schema, combine_tablename)

        create_table_dql = f"CREATE TABLE {schema}.{tablename} AS "
        select_from_dql = self.createSelectQuery(mapping_schema, mapping_tablename, target_schemas, target_tablenames, target_join_columns, serialnum_columns)
        join_dql = f""

        for i in range(len(target_tablenames)):
            join_dql += f"INNER JOIN {target_schemas[i]}.{target_tablenames[i]} ON {target_schemas[i]}.{target_tablenames[i]}.{serialnum_columns[i]} = {mapping_schema}.{mapping_tablename}.{serialnum_columns[i]} "
        data_query_language = create_table_dql + select_from_dql + join_dql
        
        super().dataQueryLanguage(data_query_language)
        super().executeQuery()
        super().commitTransaction()

    @classmethod
    def createSelectQuery(self, mapping_schema: str, mapping_tablename: str, target_schemas: List, target_tablenames: List, target_join_columns: List):
        select_dql = "SELECT "
        for i, (schema, table) in enumerate(zip(target_schemas, target_tablenames)):
            for column in target_join_columns:
                select_dql += f"{schema}.{table}.{column} AS {i+1}_{column}, "
        select_dql += f"{mapping_schema}.{mapping_tablename}.*"
        from_dql = f"FROM {mapping_schema}.{mapping_tablename} "

        return select_dql + from_dql

    @classmethod
    def addCombineTable(cls, schema, tablename):
        # 매핑테이블의 스키마와 테이블명 DBContainer의 메서드 활용하여 생성 
        cls.combine_table = DBContainer()
        cls.combine_table.setSchemaTable(schema, tablename)
        schema = cls.combine_table.getSchema()
        tablename = cls.combine_table.getTable()

        return schema, tablename

    @classmethod
    def checkTargetTableInfo(cls):
        pass