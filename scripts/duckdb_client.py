import duckdb

with duckdb.connect("tpch-sf1.db") as conn:
    conn.execute("INSTALL tpch; LOAD tpch;")
    print("clean tables...")
    conn.sql(""""
        DROP TABLE IF EXISTS customer;
        DROP TABLE IF EXISTS lineitem;
        DROP TABLE IF EXISTS nation;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS part;
        DROP TABLE IF EXISTS partsupp;
        DROP TABLE IF EXISTS region;
        DROP TABLE IF EXISTS supplier;
    """)
    print("gen sf1...")
    conn.execute("CALL dbgen(sf = 1);")