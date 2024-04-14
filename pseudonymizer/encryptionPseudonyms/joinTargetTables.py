from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery
from typing import *


class JoinTargetTables(PyMySQLQuery):
    """매핑테이블의 일련번호를 기준으로 결합대상 가명정보를 결합하는 클래스"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)
        self.target_tables = DBContainer()
        self.mapping_table = DBContainer()

    def joinTargetTables(self, combine_schema: str, combine_tablename: str, mapping_schema: str, mapping_tablename: str, target_schemas: List, target_tablenames: List, serialnum_columns: List):
        """최종 병합 스키마.테이블에 결합연계정보(일련번호)를 활용하여 결합대상 가명정보 테이블 간 내부 조인을 수행하는 실행 메서드"""
        target_join_columns = []
        schema, tablename = self.addCombineTable(combine_schema, combine_tablename)
        for i in range(len(target_tablenames)):
            target_join_columns.append(self.returnTablesColumns(target_schemas[i], target_tablenames[i]))

        create_table_dql = f"CREATE TABLE {schema}.{tablename} AS "
        select_from_dql = self.createSelectQuery(mapping_schema, mapping_tablename, target_schemas, target_tablenames, target_join_columns)
        join_dql = f""

        for i in range(len(target_tablenames)):
            join_dql += f"INNER JOIN {target_schemas[i]}.{target_tablenames[i]} ON {target_schemas[i]}.{target_tablenames[i]}.{serialnum_columns[i]} = {mapping_schema}.{mapping_tablename}.{serialnum_columns[i]} "
        data_query_language = create_table_dql + select_from_dql + join_dql
        
        super().dataQueryLanguage(data_query_language)
        super().executeQuery()
        super().commitTransaction()

    @classmethod
    def createSelectQuery(cls, mapping_schema: str, mapping_tablename: str, target_schemas: List, target_tablenames: List, target_join_columns: List):
        """매핑테이블에서 결합대상정보 테이블의 일련번호 컬럼을 조인키로 활용하여 2개 이상의 결합대상정보 테이블을 병합하는 쿼리 중 조회 구문을 반환하는 메서드"""
        select_dql = "SELECT "
        for i, (schema, table) in enumerate(zip(target_schemas, target_tablenames)):
            for column in target_join_columns[i]:
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

    def returnTablesColumns(self, schema: str, tablename: str):
        """테이블 컬럼명 확인절차 및 반환 실행 메서드"""
        sql = f"SHOW COLUMNS FROM {schema}.{tablename}"
        super().dataQueryLanguage(sql)
        targettable_columns = super().executeQueryAsDataFrame()["Field"].tolist()

        return targettable_columns