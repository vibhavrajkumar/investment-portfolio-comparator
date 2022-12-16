from app import db

"""
TMP global variables
"""
GBL_User_id = 0 ##global adam sandler variable

def filter_portfolios(filter : str) -> dict:
    """
    args: takes in a search filter
    return: items dictionary
    """
    ## Right row, we support only InvestmentName:<investment-name>, TODO: support more
    columnid,search = filter.split(':')
    # print(columnid)
    ## TODO: what if filter is not a string but an int
    global GBL_User_id
    conn = db.connect()
    query = f"""
                SELECT InvestmentsID, PortfolioName, Type, Ticker, Name, Quantity, PurchasePrice, PurchaseDate, NetGain, EspenseRatio
                FROM Users NATURAL JOIN Portfolio NATURAL JOIN Investments
                WHERE UserID = {GBL_User_id} AND {columnid} = '{search}'
                ORDER BY InvestmentsID DESC;
    """
    query_results = conn.execute(query).fetchmany(15)
    conn.close()
    portfolio_items = []
    for result in query_results:
        item = {
            "id": result[0],
            "PortfolioName": result[1],
            "Type": result[2],
            "Ticker": result[3],
            "Name" : result[4],
            "Quantity": result[5],
            "PurchasePrice": result[6],
            "PurchaseDate": result[7],
            "NetGain": result[8],
            "ExpenseRatio": result[9]
        }
        portfolio_items.append(item)
    return portfolio_items

def display_portfolio() -> dict:
    """
    Display Portfolio for a given user
    
    Args:
        username (str): username to display


    Returns:
        None
    """
    global GBL_User_id
    conn = db.connect()

    # TODO: update net gain and expense ratio before call

    query = f"""
                SELECT InvestmentsID, PortfolioName, Type, Ticker, Name, Quantity, PurchasePrice, PurchaseDate, NetGain, EspenseRatio
                FROM Users NATURAL JOIN Portfolio NATURAL JOIN Investments
                WHERE UserID = {GBL_User_id}
                ORDER BY InvestmentsID DESC;
    """
    query_results = conn.execute(query).fetchmany(15)
    conn.close()
    portfolio_items = []
    for result in query_results:
        item = {
            "id": result[0],
            "PortfolioName": result[1],
            "Type": result[2],
            "Ticker": result[3],
            "Name" : result[4],
            "Quantity": result[5],
            "PurchasePrice": result[6],
            "PurchaseDate": result[7],
            "NetGain": result[8],
            "ExpenseRatio": result[9]
        }
        portfolio_items.append(item)
    return portfolio_items
    
def create_portfolio(portfolio_name: str, isPrivate: int) -> int:
    conn = db.connect()
    query = f"Insert Into Portfolio(PortfolioName, UserID, isPrivate) VALUES('{portfolio_name}', {GBL_User_id}, {isPrivate});"
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    portfolio_id = query_results[0][0]
    conn.close()

    return portfolio_id



def insert_investment(investment: str) -> int:
    """
    Insert an investment in a users portfolio
    
    Args:
        investment (string): sting in the form:
            "PortfolioName,InvestmentType,InvestmentTicker,InvestmentName,InvestmentQuant,PurchasePrice,PurchaseDate,NetGain,ExpenseRatio"
    Return:
        investment_id
    """
    
    invest_array = investment.split(',')
    dict_keys = "PortfolioName,InvestmentType,InvestmentTicker,InvestmentName,InvestmentQuant,PurchasePrice,PurchaseDate,NetGain,ExpenseRatio".split(',')
    investment_dict = {dict_keys[k] : invest_array[k] for k in range(len(invest_array))}
    conn = db.connect()
    get_portfolioID = f"SELECT PortfolioID from Portfolio WHERE UserID = {GBL_User_id} AND PortfolioName='{investment_dict['PortfolioName']}';"
    result = conn.execute(get_portfolioID).fetchone()
    if result is None:
        # insert new portfolio ID, setting is private to 0
        portfolio_id = create_portfolio(investment_dict['PortfolioName'], 0)
        pass
    else:
        portfolio_id = result[0]
    investments_insertion = f"""
    INSERT INTO Investments(PortfolioID, Name, Ticker, Type, Quantity, PurchasePrice, NetGain, EspenseRatio)
    VALUES (
        {portfolio_id}, 
        '{investment_dict['InvestmentName']}', 
        '{investment_dict['InvestmentTicker']}', 
        '{investment_dict['InvestmentType']}', 
        {investment_dict['InvestmentQuant']}, 
        {investment_dict['PurchasePrice']}, 
        {investment_dict['NetGain']},
        {investment_dict['ExpenseRatio']});
    """
    query_results = conn.execute(investments_insertion)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    investment_id = query_results[0][0]
    conn.close()
    return investment_id
    
def delete_investment_by_ID(investment_id: int) -> bool:
    conn = db.connect()
    query = f"Delete From Investments where InvestmentsID={investment_id};"
    conn.execute(query)
    conn.close()
    return False

def delete_portfolio_by_ID(portfolio_id: int):
    conn = db.connect()
    query = f"Delete From Investments where id={portfolio_id};"
    conn.execute(query)
    conn.close()


def update_stock_api_ticker(ticker: str, update_value:int):
    conn = db.connect()
    update_stock_api = f"UPDATE `IlliniInvest`.`StockAPI` SET `CurrentPrice` = '{update_value}' WHERE (`Ticker` = '{ticker}');"
    conn.execute(update_stock_api)
    conn.close()


def update_portfolio_name(investment_id: int, new_name: str):
    """
    Updates the name of a given portfolio for the current user

    Args:
        old_name (str): name of portfolio user wants to change
        new_name (str): new name of the portfolio

    Return:
        True on successful update
    """
    print('in port update')
    conn = db.connect()
    get_portfolioID = f"SELECT PortfolioID from Investments WHERE InvestmentsID = {investment_id};"
    portfolio_id = conn.execute(get_portfolioID).fetchone()[0]
    print("Portfolio ID:", portfolio_id)
    print("new name", new_name)
    update_portname_query = f"UPDATE Portfolio SET PortfolioName = '{new_name}' WHERE UserID = {GBL_User_id} and PortfolioID = {portfolio_id};"
    conn.execute(update_portname_query)
    conn.close()
    
    # # perform query to check that the table is updated properly 
    # validate_new_name_query = f"SELECT * FROM Portfolio WHERE PortfolioName = {new_name} and UserID = 0;"
    # new_name_results = conn.execute(validate_new_name_query)
    # conn.close()

    # if new_name_results == None:
    #     return False
    # return True

def advanced_query_one()->dict:
    """
    Runs Advanced Query 1 as specified by the instructions for the midpoint. 
    This query will find all portfolios that have a net gain above 100 dollars. 

    Args: 
    None

    Return:
    True upon successful query 
    """

    conn = db.connect() 
    query_net_gain = f"""SELECT Username, PortfolioID, SUM(CurrentPrice) as PortfolioValue, SUM(Quantity) as TotalShares
                            FROM Users NATURAL JOIN Portfolio NATURAL JOIN Investments i JOIN StockAPI s USING(Ticker)
                            GROUP BY PortfolioID
                            ORDER BY PortfolioID;"""
    query_results = conn.execute(query_net_gain).fetchall()
    conn.close() 
    portfolio_items = []
    for result in query_results:
        item = {
            "Username": result[0],
            "PortfolioID": result[1],
            "PortfolioValue": result[2],
            "TotalShares": result[3]
        }
        portfolio_items.append(item)
    return portfolio_items


def advanced_query_two()->dict: 
    """
    Runs Advanced Query 2 as specified by the instructions for the midpoint. 

    Args: 
    None

    Return:
    True upon successful query 
    """
    conn = db.connect() 
    query_users_apple = f"""
                        SELECT DISTINCT Username, PortfolioID, PortfolioName
                        FROM Users NATURAL JOIN Portfolio NATURAL JOIN Investments i JOIN StockAPI s
                        WHERE (SELECT AVG(s1.CurrentPrice) FROM StockAPI s1 WHERE s.Ticker = s1.Ticker) > 400
                        ORDER BY PortfolioID;"""
    query_results=conn.execute(query_users_apple).fetchall()
    conn.close() 
    portfolio_items = []
    for result in query_results:
        item = {
            "Username": result[0],
            "PortfolioID": result[1],
            "PortfolioName" : result[2]
        }
        portfolio_items.append(item)
    return portfolio_items  


def stored_procedure(topStock:bool)->dict:
    conn = db.connect()
    if topStock:
        conn.execute("call portfolioInfo(TRUE);")
        query_results = conn.execute("select * from portfolioInfo NATURAL JOIN portfolioTopStock;").fetchall()
        conn.close()
        portfolio_items = []
        for result in query_results:
            item = {
                "PortfolioID": result[0],
                "PortfolioName" : result[1],
                "totalValue": result[2],
                "totalNetGain": result[3],
                "avgNetGain": result[4],
                "numDistinctStocks": result[5],
                "topStock": result[6],
                "netGain": result[7]
            }
            portfolio_items.append(item)
        return portfolio_items
    else:
        conn.execute("call portfolioInfo(FALSE);")
        query_results = conn.execute("select * from portfolioInfo;").fetchall()
        conn.close()
        portfolio_items = []
        for result in query_results:
            item = {
                "PortfolioID": result[0],
                "PortfolioName" : result[1],
                "totalValue": result[2],
                "totalNetGain": result[3],
                "avgNetGain": result[4],
                "numDistinctStocks": result[5],
            }
            portfolio_items.append(item)
        return portfolio_items
