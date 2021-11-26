import unittest
import axyl_stats_db as axdb


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.conn = axdb.Connection(db_name="test_db")

        self.conn.execute("DROP TABLE IF EXISTS test_table")
        self.conn.execute("DROP TABLE IF EXISTS test_table2")
        self.conn.execute("DROP TABLE IF EXISTS repo_stats")

        self.conn.execute("""CREATE TABLE test_table
                             (
                               textrow text,
                               numrow integer
                             )""")

    def test_connection_commits(self):
        self.conn.execute("""INSERT INTO test_table (textrow, numrow)
                             VALUES ('The testing!', 50)""")

        rows: list = self.conn.execute("SELECT * FROM test_table")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('The testing!', 50))

    def test_multiple_row_results(self):
        self.conn.execute("""INSERT INTO test_table (textrow, numrow)
                             VALUES ('Foo', 100),
                                    ('Bar', 120),
                                    ('Baz', 160)""")

        rows: list = self.conn.execute("SELECT * FROM test_table")

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows,
                         [('Foo', 100), ('Bar', 120), ('Baz', 160)])

    def test_statement_without_results(self):
        rows: list = self.conn.execute("""CREATE TABLE test_table2
                                          (yum integer)""")

        self.assertEqual(rows, [])

    def test_one_placeholder(self):
        self.conn.execute("CREATE TABLE test_table2 (day integer)")
        day: int = 4

        # Insert into the database with a placeholder
        self.conn.execute("INSERT INTO test_table2 (day) VALUES (%s)", (day,))

        rows: list = self.conn.execute("SELECT * FROM test_table2")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (day,))

    def test_many_placeholders(self):
        self.conn.execute("""CREATE TABLE test_table2
                                          (
                                           event text,
                                           month integer,
                                           day integer
                                          )""")

        event: str = "Outing with friends"
        month: int = 11
        day: int = 20

        self.conn.execute("""INSERT INTO test_table2
                             (event, month, day)
                             VALUES
                             (%s, %s, %s)""",
                          (event, month, day))

        rows: list = self.conn.execute("""SELECT * FROM test_table2""")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (event, month, day))

    def test_insert_into_database(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS repo_stats
                             (
                              repo text,
                              total_downloads integer,
                              latest_downloads integer,
                              stars integer,
                              watchers integer,
                              forks integer,
                              date timestamp
                             )""")

        repo_name = 'angelofallars/pomoff'
        total_downloads = 20
        latest_downloads = 3
        stars_count = 6
        watchers_count = 6
        forks_count = 3
        axdb.insert_into_database(self.conn,
                                  repo_name,
                                  total_downloads,
                                  latest_downloads,
                                  stars_count,
                                  watchers_count,
                                  forks_count)

        rows: list = self.conn.execute("""SELECT * FROM repo_stats LIMIT 1""")

        # [0] to get the first result
        # [:-1] to exclude the date/time column at the end
        self.assertEqual(rows[0][:-1], (repo_name, total_downloads,
                                        latest_downloads, stars_count,
                                        watchers_count, forks_count))

    def tearDown(self):
        self.conn.execute("DROP TABLE IF EXISTS repo_stats")
        self.conn.execute("DROP TABLE IF EXISTS test_table")
        self.conn.execute("DROP TABLE IF EXISTS test_table2")


class TestAPITools(unittest.TestCase):

    def test_download_stats(self):
        downloads, latest_downloads = axdb.fetch_download_count("axyl-os",
                                                                "axyl-iso")

        self.assertEqual(type(downloads), int)
        self.assertEqual(type(latest_downloads), int)
        self.assertEqual(downloads >= latest_downloads, True)


if __name__ == "__main__":
    unittest.main()
