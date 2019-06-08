from dao.file_storage_dao import FileStorageDAO


class DataOrganizer:

    @staticmethod
    def organize_tickers(tickers):
        for ticker in tickers:
            try:
                DataOrganizer.organizeTicker(ticker)
            except:
                print('Error organizing ticker: ' + str(ticker))

    @staticmethod
    def organize_ticker(ticker):
        income_statement = FileStorageDAO.get_income_statement(ticker)
        balance_sheet = FileStorageDAO.get_balance_sheet(ticker)
        cash_flow_statement = FileStorageDAO.get_cash_flow_statement(ticker)

        organized_data = {

        }

        FileStorageDAO.save_organized_data(ticker, organized_data)
