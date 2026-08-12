import argparse

from config import connect


def run(query):
    with connect() as connection:
        connection.execute(query)


def schema():
    run("""
        CREATE SCHEMA IF NOT EXISTS lab AUTHORIZATION skala_user;
        ALTER DATABASE skala_db SET search_path TO lab, public;
        ALTER ROLE skala_user SET search_path TO lab, public;
        GRANT USAGE, CREATE ON SCHEMA lab TO skala_user;
        ALTER DEFAULT PRIVILEGES IN SCHEMA lab
          GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO skala_user;
        ALTER DEFAULT PRIVILEGES IN SCHEMA lab
          GRANT USAGE, SELECT ON SEQUENCES TO skala_user;
    """)
    print("schema 완료")


def tables():
    run("""
        DROP TABLE IF EXISTS lab.enroll, lab.orders, lab.emp,
                             lab.student, lab.customers CASCADE;
        CREATE TABLE lab.student (
          student_id INT PRIMARY KEY, name VARCHAR(50),
          major VARCHAR(50), gpa NUMERIC(3,2));
        CREATE TABLE lab.enroll (
          student_id INT, course VARCHAR(50), grade CHAR(1));
        CREATE TABLE lab.customers (
          customer_id INT PRIMARY KEY, customer_name VARCHAR(50));
        CREATE TABLE lab.orders (
          order_id INT PRIMARY KEY,
          customer_id INT REFERENCES lab.customers(customer_id),
          amount NUMERIC(10,2));
        CREATE TABLE lab.emp (
          emp_id INT PRIMARY KEY, name VARCHAR(50),
          manager_id INT REFERENCES lab.emp(emp_id));
    """)
    print("tables 완료")


def indexes():
    run("""
        CREATE INDEX IF NOT EXISTS ix_enroll_student ON lab.enroll(student_id);
        CREATE INDEX IF NOT EXISTS ix_orders_customer ON lab.orders(customer_id);
        CREATE INDEX IF NOT EXISTS ix_emp_manager ON lab.emp(manager_id);
    """)
    print("indexes 완료")


def seed():
    run("""
        TRUNCATE lab.enroll, lab.orders, lab.emp, lab.student, lab.customers CASCADE;
        INSERT INTO lab.student
        SELECT gs, 'Student_' || gs,
               CASE gs % 5 WHEN 0 THEN 'CS' WHEN 1 THEN 'EE'
                 WHEN 2 THEN 'ME' WHEN 3 THEN 'CE' ELSE 'BIO' END,
               ROUND(2.0 + (gs % 30) / 10.0, 2)
        FROM generate_series(1, 1000) gs;
        UPDATE lab.student SET major = 'HR' WHERE student_id BETWEEN 981 AND 1000;

        INSERT INTO lab.enroll
        SELECT s.student_id,
               CASE WHEN ((s.student_id + k) % 21) = 0 THEN 'DB'
                    ELSE 'Course_' || (((s.student_id + k) % 20) + 1) END,
               (ARRAY['A','B','C','D'])[((s.student_id + k) % 4) + 1]
        FROM lab.student s
        JOIN LATERAL generate_series(
          1, s.student_id % 3
        ) g(k) ON TRUE;
        INSERT INTO lab.enroll VALUES (1001, 'AI', 'A'), (1010, 'ML', 'B');

        INSERT INTO lab.customers
        SELECT gs, 'Customer_' || gs FROM generate_series(1, 500) gs;
        INSERT INTO lab.orders
        SELECT gs, (gs % 500) + 1,
               ROUND(5 + (gs * 13) % 5000 + (gs % 100) / 100.0, 2)
        FROM generate_series(1, 3000) gs;

        INSERT INTO lab.emp VALUES (1, 'CEO', NULL);
        INSERT INTO lab.emp
        SELECT 1 + gs, 'Mgr_' || (1 + gs), 1 FROM generate_series(1, 10) gs;
        INSERT INTO lab.emp
        SELECT 11 + gs, 'Dev_' || (11 + gs), 2 + ((gs - 1) % 10)
        FROM generate_series(1, 300) gs;
    """)
    print("seed 완료")


def verify():
    with connect() as connection:
        rows = connection.execute("""
            SELECT 'student', COUNT(*) FROM lab.student
            UNION ALL SELECT 'enroll', COUNT(*) FROM lab.enroll
            UNION ALL SELECT 'customers', COUNT(*) FROM lab.customers
            UNION ALL SELECT 'orders', COUNT(*) FROM lab.orders
            UNION ALL SELECT 'emp', COUNT(*) FROM lab.emp
            ORDER BY 1
        """).fetchall()
    for table, count in rows:
        print(f"{table:10} {count:>5}")


STEPS = {
    "schema": schema,
    "tables": tables,
    "indexes": indexes,
    "seed": seed,
    "verify": verify,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", nargs="?", default="all", choices=(*STEPS, "all"))
    step = parser.parse_args().step
    if step == "all":
        for function in STEPS.values():
            function()
    else:
        STEPS[step]()
