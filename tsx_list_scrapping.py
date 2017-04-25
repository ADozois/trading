import requests
import bs4 as bs
import pickle


def get_site_to_soup(url):
    req = requests.get(url)
    soup = bs.BeautifulSoup(req.text, 'lxml')
    return soup


def get_first_colum_table(table_name):
    return soup.find('table', {'class': table_name})

if __name__ == '__main__':

    stock_list = []
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
              'W', 'X', 'Y', 'Z']
    site = 'http://eoddata.com/stocklist/TSX/'
    htm = '.htm'

    for letter in letters:
        soup = get_site_to_soup(site+letter+htm)
        quotes_table = get_first_colum_table('quotes')

        for row in quotes_table.findAll('tr')[1:]:
            quote_name = row.findAll('td')[0].text
            stock_list.append(quote_name)

    with open("data/tsx_stock_list.pickle", "wb") as f:
        pickle.dump(stock_list, f)
