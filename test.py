import json
import sqlparse

f = open("bugs.json", "r")
bug_entries = json.loads(f.read())

sql_statements = []

for entry in bug_entries:
    statements = entry['test']
    sql_statements.append('\n'.join(entry['test']))

print(sql_statements) # a list of the concatenated SQL statements

print('statement splitting')
print('###################')
print(sqlparse.split(sql_statements[1]))
print(sqlparse.split("""SELECT 1 + 'SELECT 1;' UNION SELECT "SELECT 1; SELECT;;---"" " INTERSECT SELECT 1 + '''a;'''; --- SELECT 1; """))


print('pretty printing')
print('###############')
print(sqlparse.format('SELECT * FROM t0 JOIN t1 ON c0=c1 WHERE c0 > 5 GROUP BY c2 HAVING SUM(c3) > 3', reindent=True, keyword_case='upper'))
# SELECT *
# FROM t0
# JOIN t1 ON c0=c1
# WHERE c0 > 5
# GROUP BY c2
# HAVING SUM(c3) > 3

print('classify statements')
print('###################')
print([s.get_type() for s in sqlparse.parse(sql_statements[1])])
# CREATE TABLE test (c1 TEXT PRIMARY KEY) WITHOUT ROWID; -- CREATE
# CREATE INDEX index_0 ON test(c1 COLLATE NOCASE); -- CREATE
# INSERT INTO test(c1) VALUES ('A'); -- INSERT
# INSERT INTO test(c1) VALUES ('a'); -- INSERT
# SELECT * FROM test; -- SELECT

print('unsupported statements')
print('######################')
for test_case in sql_statements:
    for statement in sqlparse.parse(test_case):
        if statement.get_type() == 'UNKNOWN':
            print(statement)

print('analyze query')
print('#############')
for test_case in sql_statements:
    for statement in sqlparse.parse(test_case):
        if statement.get_type() == 'SELECT':
            for token in statement.tokens:
                if isinstance(token, sqlparse.sql.Where):
                    print(token)
                    for wheretoken in token.flatten():
                        print(wheretoken.ttype)
                if 'JOIN' in token.value:
                    print(statement)
                    print(statement.token_next(statement.token_index(token))[1])
