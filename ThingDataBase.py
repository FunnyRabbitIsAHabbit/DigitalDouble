"""
DataBase as one of Digital Double's Things.


@author: Stanislav Ermokhin
@GitHub: https://github.com/FunnyRabbitIsAHabbit
"""

from datetime import datetime
from numpy import genfromtxt

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float, Date

Base = declarative_base()


class ThingDataBase:
    """
    Double for actual database.

    """

    def __init__(self, db_engine=None, db_url=None):
        """
        Initialization method

        :param db_engine: engine to run double-DB on
        :param db_url: URL of double-DB
        """

        self.db_engine = db_engine or "sqlite"
        self.db_url = db_url or "jdbc:sqlite:thing_main.sqlite"

    @staticmethod
    def load_data(file_name):
        data = genfromtxt(file_name,
                          delimiter=",", skip_header=1,
                          converters={0: lambda s: s},
                          dtype=None, filling_values=None,
                          replace_space="_", encoding="utf-8")

        return data.tolist()

    @staticmethod
    def transform_date(date_str):
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    def csv_to_table(self):
        engine = create_engine(f"{self.db_engine}:///{self.db_url}",
                               echo=False)
        Base.metadata.create_all(engine)
        session = sessionmaker()
        session.configure(bind=engine)
        session1 = session()

        try:
            _file_name = "quotes.csv"
            dt = self.load_data(_file_name)

            for i in dt:
                record = PortfolioTransaction(**{
                    "symbol": i[0],
                    "open": i[5],
                    "high": i[6],
                    "low": i[7],
                    "volume": i[8],
                    "trade_date": datetime.strptime(self.transform_date(str(i[9])), "%Y-%m-%d").date(),
                    "purchase_price": i[10],
                    "quantity": i[11],
                    "commission": i[12],
                })
                session1.add(record)  # Add all the records

            session1.commit()  # Attempt to commit all the records

        except BaseException as error:
            session1.rollback()
            print(f"ERROR:{error}")  # Rollback the changes on error

        finally:
            session1.close()  # Close the connection

        results = session1.query(PortfolioTransaction).delete()

        return results

    def select_all(self):
        engine = create_engine(f"{self.db_engine}:///{self.db_url}",
                               echo=False)
        Base.metadata.create_all(engine)
        session = sessionmaker()
        session.configure(bind=engine)
        session1 = session()

        results = session1.query(PortfolioTransaction).all()

        return results

    def delete_all(self):
        engine = create_engine(f"{self.db_engine}:///{self.db_url}",
                               echo=False)
        Base.metadata.drop_all(bind=engine)

        return True


class PortfolioTransaction(Base):

    __tablename__ = "portfolio_transaction"
    id = Column(Integer, primary_key=True, nullable=False)

    symbol = Column(String)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    trade_date = Column(Date)
    purchase_price = Column(Float)
    quantity = Column(Float)
    commission = Column(Float)

    def __repr__(self):
        return "\n".join([f"{key}: {self.__dict__[key]}" for key in self.__dict__])


double_database = ThingDataBase()

print(double_database.delete_all())
print(double_database.select_all())
print(double_database.csv_to_table())
print(double_database.select_all())
