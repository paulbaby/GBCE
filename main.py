from stock import Stock, StockExchangeData, StockCalculations, StockTrade
import csv


def add_stock(stock_symbol, stock_type, last_divident, fixed_divident, par_value):
    stock_obj = Stock(stock_symbol, stock_type, last_divident, fixed_divident, par_value)

    StockExchangeData.add_stock(stock_obj)


if __name__ == "__main__":

    print("Loading Sample data...")

    with open('sample_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        int_fields = ['last_divident', 'fixed_divident', 'par_value']

        for row in reader:
            for key in int_fields:
                if key in row:
                    if row[key]:
                        row[key] = int(row[key])

            print("Loaded ",row)
            add_stock(row['stock_symbol'], row['type'], row['last_divident'], row['fixed_divident'], row['par_value'])


    while True:
        print("\n\n")
        print("Available options")
        print("1.Add a New Stock")
        print("2.List Available Stocks")
        print("3.Perfom Action on Stock")
        print("4.GBCE")
        print("5.List All Trades")
        print("6.Exit\n")

        choice = int(input("Enter your choice:"))

        if choice == 1:
            print("Not implemented")

        elif choice == 2:
            all_stocks = StockExchangeData.get_all_stocks()
            for stock in all_stocks:
                print(all_stocks[stock].stock_id)

        elif choice == 3:
            stock_code = input("Enter your stock code:").upper()
            if stock_code not in StockExchangeData.stocks:
                print("Wrong Stock Code.")
                continue

            stock = StockExchangeData.stocks[stock_code]

            while True:
                print("\n")
                print("Available options")
                print("1.Record Trade")
                print("2.Divident yield")
                print("3.P/E Ratio")
                print("4.Volume Weighted Stock Price for past 5 min")
                print("5.List trades")
                print("6.Exit to prev menu\n")

                stock_choice = int(input("Enter your choice:"))

                if stock_choice == 1:
                    trade_details = input("Enter quantity, trade_type (B/S), price")
                    try:
                        quantity, trade_type, price = trade_details.split(',')
                    except:
                        print("Trade data in wrong format")
                        continue

                    StockTrade().record_trade(stock.stock_id, int(quantity), trade_type, int(price))

                elif stock_choice == 2:
                    price = int(input("Enter price:"))
                    result = StockCalculations().get_divident_yield(stock.stock_id, price)
                    print(f"Divident Yield: {result}")

                elif stock_choice == 3:
                    price = int(input("Enter price:"))
                    result = StockCalculations().get_pe_ratio(stock.stock_id, price)
                    print(f"P/E Ratio: {result}")
                
                elif stock_choice == 4:
                    result = StockCalculations().volume_weighted_price(stock.stock_id)
                    print(f"Volume Weighted Price: {result}")

                elif stock_choice == 5:
                    trade_list = StockExchangeData.get_trade_record(stock.stock_id)
                    print("Trade List: ",trade_list)

                elif stock_choice == 6:
                    break

                else:
                    print("Wrong Choice")

        elif choice == 4:
            print("GBCE: ", StockCalculations().GBCE())

        elif choice == 5:
            trade_list = StockExchangeData.get_all_trade_records()
            print("Trade List: ",trade_list)

        elif choice == 6:
            break

        else:
            print("Wrong Choice")



        





