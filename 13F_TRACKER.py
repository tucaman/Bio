import os
from edgar import Edgar, Company, XBRL
import lxml
from sec_edgar_downloader import Downloader
import numpy as np
import pandas as pd
from lxml import etree
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------------------------
# Dictionary of Healthcare Specialist Funds
dict_cik = {'OrbiMed': '0001055951',
            'Baker Bros.': '0001263508',
            'Deerfield': '0001009258',
            'BB Biotech': '0000924223',
            'RA Capital Management': '0001346824',
            'BVF': '0001056807',
            'Avoro': '0001633313',
            'Great Point': '0001281446',
            'Cormorant': '0001583977',
            'Boxer': '0001465837',
            'Aviva': '0001603935',
            'Perceptive': '0001224962',
            'Redmile': '0001425738',
            'RTW': '0001493215',
            'EcoR1': '0001587114',
            'Consonance': '0001544773',
            'Palo Alto': '0001306923',
            'Frazier': '0000901664',
            'Camber': '0001444043',
            'Vivo': '0001674712',
            'Abingworth': '0001397144',
            'Tang': '0001232621',
            'Rock Springs': '0001595725',
            'Bellevue': '0001674546',
            'Omega Fund': '0001637359',
            'HealthCor': '0001343781',
            'Rhenman': '0001599882',
            'Sphera': '0001496201',
            'SectorGamma AS': '0001475373',
            'Third Security': '0001542294',
            'Sofinnova': '0001631134',
            'Broadfin': '0001511901',
            'Venrock (II)': '0001602263',
            'Acuta': '0001582844',
            'Casdin': '0001534261',
            'Ghost Tree': '0001595851',
            'Sarissa': '0001577524',
            'Foresite (III)': '0001645157',
            'Sio': '0001482416',
            'First Light': '0001600004',
            'JW Asset': '0001549738',
            'Sectoral': '0001274413',
            'Venrock (III)': '0001738053',
            'Foresite (IV)': '0001704132',
            'Opaleye': '0001595855',
            'Stonepine': '0001440771',
            'Sivik': '0001169869',
            'Pura Vida': '0001590144',
            'DAFNA': '0001389933',
            'Endurant': '0001633055',
            'Prosight': '0001617201',
            'Tavio': '0001672526',
            'Eversept': '0001697013',
            'Tamarack': '0001661462',
            'Sabby': '0001535610',
            'Birchview': '0001618205',
            'Aquilo': '0001591986',
            'Asymmetry': '0001657134',
            'Knoll': '0001325083',
            'Copernicus': '0001694620',
            'Healthcare Value': '0001458461'
            }





# ----------------------------------------------------------------------------------------------------------------------
#  Helper functions
def find_files_in_folder(path, file_type='.csv',
                         search_file_name=''):
    files = []
    for file in os.listdir(path):
        if file.endswith(".xlsx"):
            files.append(os.path.join(path, file))
        elif file.endswith(".csv"):
            files.append(os.path.join(path, file))
        elif file.endswith(".txt"):
            files.append(os.path.join(path, file))

    files = [f for f in files if f.endswith(file_type)]
    if search_file_name != '':
        files = [f for f in files if search_file_name in f]

    return (files)

# ----------------------------------------------------------------------------------------------------------------------
# request 13F for single fund

# What is the difference between 13F-HR and 13F-NT?
# 13F-HR is the 13F Holdings Report and is used when all of your applicable securities are on the report.
# The 13F-HR can also be the 13F Combination Report which is used when some of your applicable securities are on
# the report and some are on someone else’s report. 13F-NT is the 13F Notice and is used when none of your
# applicable securities are on the report and are on someone else’s report.
def request_edgar_files(cik='0001346824',
                        filing_type='13F-HR',
                        after_date='20191231',
                        include_amends=True):
    """
    Supported SEC Filings: 4, 8-K, 10-K, 10KSB, 10-Q, 13F-NT and 13F-HR, 20-F,  SC 13G,  SD,  S-1,  DEF 14A

    :param cik:  CIK to download filings for
    :param filing_type: type of filing to download
    :param after_date: date of form YYYYMMDD in which to download filings after
    :param include_amends:  denotes whether or not to include filing amends (e.g. 8-K/A)
    :return:
    """

    # create EDGAR request object
    # edgar = Edgar()
    # get the SEC company name
    # company_name = edgar.get_company_name_by_cik(cik)

    # Initialize download path
    _fd = os.getcwd()

    # Initialize a downloader instance.
    # If no argument is passed to the constructor, the package
    # will attempt to locate the user's downloads folder.
    dl = Downloader(_fd)
    # get all filings
    # dl.get("13F-HR", "0000102909")
    dl.get(filing_type=filing_type,
           ticker_or_cik=cik,
           after_date=after_date,
           include_amends=include_amends)

# ----------------------------------------------------------------------------------------------------------------------
# class for parsing XML structures to pandas dataframes
class XML2DataFrame:

    def __init__(self, xml_data):

        # ToDo: We need to find a more systematic way to remove empty tags
        xml_data = xml_data.replace('<flags></flags>', '')

        self.root = ET.XML(xml_data)

    def parse_root(self, root):
        """Return a list of dictionaries from the text and attributes of the
        children under this XML root."""
        return [self.parse_element(child) for child in root.getchildren()]

        # [child for child in root.getchildren()]

    def parse_element(self, element, parsed=None):
        """ Collect {key:attribute} and {tag:text} from thie XML
         element and all its children into a single dictionary of strings."""
        if parsed is None:
            parsed = dict()

        if len(element.getchildren()) == 0:
            if element.text:
                parsed[element.tag] = element.text
            else:
                raise ValueError('duplicate attribute {0} at element {1}'.format(element.tag,
                                                                                 element.getroottree().getpath(element)))

        """ Apply recursion"""
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self):
        """ Initiate the root XML, parse it, and return a dataframe"""
        structure_data = self.parse_root(self.root)

        dict_data = {}
        for d in structure_data:
            dict_data = {**dict_data, **d}
        df = pd.DataFrame(data=list(dict_data.values()), index=dict_data.keys()).T

        return df

# ----------------------------------------------------------------------------------------------------------------------
def create_13F_db(cik='0001346824',
                  f_save='C://Users//lenna//PycharmProjects//Bio//db_13f//',
                  l_reportcalendarorquarter=[]
                 ):
    '''
    The function will
    - find the 13F-HR reports for a given cik,
    - consolodate the info table containing the holdings as of the download date
    - assign the tickers using the CUSIP and the map for the repective quarter
    - store the processed info table in the directory; file name will by 13F_HR + cik + reportcalendarorquarter

    :param cik: the EDGAR company id for the fund of interest
    :param f_save: target directory for file database
    :param l_reportcalendarorquarter:   list of reporting quarters (YYYY + q + Q, e.g. 2020q2) to be processed;
                                        if empty ALL reports will be processed

    :return:
    '''

    # create target folder if it does not exist
    if not os.path.exists(f_save):
        os.makedirs(f_save)

    # parse downloaded 13F reports
    _fd = os.getcwd() + '//sec_edgar_filings//' + str(int(cik)) + '//13F-HR//'
    l_files = find_files_in_folder(path=_fd,
                                 file_type='.txt')

    #  we will process each file, we can decide later, if we want to keep the result or dismiss (i.e. no reprocessing)
    def parse_13F_info_table(_file):
        '''Extract and enrich the info table from the 13F-HR report.'''

        parser = etree.XMLParser(recover=True)
        tree = etree.parse(_file, parser)
        html = etree.tostring(tree, pretty_print=True)

        # create Beautiful Soup object allowing to extract infotables
        soup = BeautifulSoup(html, 'lxml')  # Parse the HTML as a string
        tables = soup.find_all('infotable')  # identify all infotables
        if len(tables) == 0:
            tables = soup.find_all('ns1:infotable')  # identify all infotables

        submission_type = soup.find_all('submissiontype')[0].text
        cik = soup.find_all('cik')[0].text
        try:
            isamendment = soup.find_all('isamendment')[0].text
        except IndexError:
            isamendment='false'

        # etree.parse(str(soup.find_all('coverpage')[0]), parser)

        df_13F_headerdata = XML2DataFrame(str(soup.find_all('headerdata')[0])).process_data()
        print(df_13F_headerdata.to_string())
        df_13F_headerdata = df_13F_headerdata.T.to_dict().get(0)

        # isamendment = soup.find_all('isamendment')[0].text
        reportcalendarorquarter = soup.find_all('reportcalendarorquarter')[0].text
        name = soup.find_all('name')[0].text

        df_13F_signatureblock = XML2DataFrame(str(soup.find_all('signatureblock')[0])).process_data()
        print(df_13F_signatureblock.to_string())
        df_13F_signatureblock = df_13F_signatureblock.T.to_dict().get(0)

        df_13F_info_table = pd.DataFrame()
        for table in tables:
            tmp = str(table).replace('ns1:', '')
            # break
            xml2df = XML2DataFrame(tmp)
            xml_dataframe = xml2df.process_data()
            # add header information
            xml_dataframe = xml_dataframe.assign(cik=df_13F_headerdata.get('cik'),
                                                 reportcalendarorquarter=reportcalendarorquarter,
                                                 submissiontype=df_13F_headerdata.get('submissiontype'),
                                                 isamendment=isamendment,
                                                 filer=name,
                                                 signaturedate=df_13F_signatureblock.get('signaturedate'))

            df_13F_info_table = df_13F_info_table.append(xml_dataframe)

        # print some info
        total_aum = df_13F_info_table.value.astype(float).sum() * 10 ** 3 / 10 ** 9
        print('Total AUM (long, non-derivative positions) in bln USD:', round(total_aum, 1))

        # return the info table
        return df_13F_info_table

    for _file in l_files:
        df_13F_info_table = parse_13F_info_table(_file)
        print('_file processed successfully', _file)
        # break
        # print(df_13F_info_table.to_string())

        # map CUSIPS to tickers (where possible)
        report_year_quarter = pd.to_datetime(df_13F_info_table.reportcalendarorquarter.drop_duplicates().values[0])
        report_year_quarter = str(report_year_quarter.year) + 'q' + str(report_year_quarter.quarter)

        if (l_reportcalendarorquarter == []) | (report_year_quarter in l_reportcalendarorquarter):

            try:
                # load map CUSIP <-> Ticker
                f_ticker_map = 'C://Users//lenna//PycharmProjects//Bio//'
                f_ticker_map += 'NASDAQ_bio_enriched_' + report_year_quarter + '.csv'
                ticker_map = pd.read_csv(f_ticker_map)
                dict_ticker_map = dict(zip(ticker_map['cusip'], ticker_map['ticker']))
                df_13F_info_table['ticker'] = df_13F_info_table['cusip'].map(lambda x: x[0: len(x)]).map(dict_ticker_map)
                # print(ticker_map.head().to_string())

                # Positions w/o ticker
                print('Positions without ticker')
                print(df_13F_info_table[df_13F_info_table['ticker'].isnull()].to_string())

                # Save the file to file db 13F-HR + cik + report_year_quarter
                f_ = '13F-HR-' + report_year_quarter + '-' + cik + '.csv'

                df_13F_info_table.to_csv(path_or_buf=f_save + f_, index=False)
            except FileNotFoundError:
                print('Failed to process 13F-HR for', report_year_quarter)

# ----------------------------------------------------------------------------------------------------------------------
# Control process
# ToDo: Boxer needs to be processed again
import timeit
# Download 13F reports from EDGAR
for f in dict_cik.keys():
    print('Processing EDGAR request for fund:', f)
    s_time = timeit.default_timer()

    cik = dict_cik.get(f)

    request_edgar_files(cik=cik,
                        filing_type='13F-HR',
                        after_date='20200630',
                        include_amends=True)

    try:
        create_13F_db(cik=cik,
                      f_save='C://Users//lenna//PycharmProjects//Bio//db_13f//',
                      l_reportcalendarorquarter=[]
                      )
        elapsed = timeit.default_timer() - s_time

        print('-----------------------------------------------------')
        print('Processing EDGAR for fund:', f, ' completed in', elapsed, 'seconds.')
        print('')
        print('-----------------------------------------------------')

    except FileNotFoundError:
        print('-----------------------------------------------------')
        print('WARNING: Processing EDGAR for fund:', f, ' FAILED')
        print('')
        print('-----------------------------------------------------')

# ----------------------------------------------------------------------------------------------------------------------
# Example: Get the AUM by fund for the most recent quarter
def consolidate_issuer_names(df):

    # cast all names to capital letters
    df['nameofissuer'] = df['nameofissuer'].str.upper()
    # # common replacements
    # for e in ['LTD.', 'INC.']:
    #     df['nameofissuer'] = df['nameofissuer'].str.replace(e, e[:3])
    # # special replacements
    # df['nameofissuer'] = df['nameofissuer'].str.replace('LABORATORIES', 'LABS')
    #
    #
    d = df[['cusip', 'nameofissuer']].drop_duplicates(subset=['cusip'], keep='first')\
        .set_index('cusip').to_dict().get('nameofissuer')

    update_value = lambda x: x if d.get(x) == None else d.get(x)
    df['nameofissuer'] = df['cusip'].apply(update_value).str.strip()

    return df

def consolidate_13F_reports(report_year_quarter='2020q3',
                            f_db_13F='C://Users//lenna//PycharmProjects//Bio//db_13f//'):

    l_files = find_files_in_folder(path=f_db_13F,
                                   search_file_name='13F-HR-' + report_year_quarter,
                                   file_type='csv')
    df_13F = pd.DataFrame()
    for f in l_files:
        tmp = pd.read_csv(f)
        df_13F = df_13F.append(tmp)

    df_13F = consolidate_issuer_names(df=df_13F)
    # df_13F.columns

    # AUM by fund
    tmp = df_13F.groupby('filer').agg({'value': 'sum'}).sort_values(by=['value'], ascending=False)/10**6
    tmp.columns = ['AUM (bln USD)']
    print(round(tmp, 2).head(10).to_string())
    df_aum = tmp.copy(deep=True)

    # add portfolio rank (in % of 13F holdings)
    df_13F['total_aum_filer'] = df_13F['filer'].map(df_aum.to_dict().get(df_aum.columns[0])) * 10**6
    df_13F['perc_of_13F_holdings'] = df_13F['value']/df_13F['total_aum_filer'] * 100

    return [df_13F, df_aum]

# create differences between consecutive quarters
df_13F_q1, df_aum_q1 = consolidate_13F_reports(report_year_quarter='2020q2',
                                               f_db_13F='C://Users//lenna//PycharmProjects//Bio//db_13f//')

df_13F_q2, df_aum_q2 = consolidate_13F_reports(report_year_quarter='2020q3',
                                               f_db_13F='C://Users//lenna//PycharmProjects//Bio//db_13f//')

# create dictionary of issuer names (map using CUSIP)
c = ['cusip', 'nameofissuer']
d_cusip_nameofissuer = consolidate_issuer_names(df_13F_q1[c].append(df_13F_q2[c]))\
    .set_index('cusip')\
    .to_dict().get('nameofissuer')

# ...differences total AUM
df_diff_aum = pd.merge(df_aum_q1, df_aum_q2, left_index=True, right_index=True,
                       how='outer', suffixes=['_q1', '_q2'])
df_diff_aum['diff'] = df_diff_aum.iloc[:, 1] - df_diff_aum.iloc[:, 0]
df_diff_aum['diff_perc'] = df_diff_aum['diff']/ df_diff_aum.iloc[:, 0] * 100
print(df_diff_aum.sort_values(by=['diff'], ascending=False).head().to_string())
print(df_diff_aum.sort_values(by=['diff_perc'], ascending=False).head().to_string())

# create list of funds that already have reported for eirher quarter
l_funds_reported_q1 = df_diff_aum[df_diff_aum.iloc[:, 0].notnull()].index.to_list()
l_funds_reported_q2 = df_diff_aum[df_diff_aum.iloc[:, 1].notnull()].index.to_list()
print('Funds that already reported in CURRENT quarter')
for c in l_funds_reported_q2:
    print(c)

# ----------------------------------------------------------------------------------------------------------------------
# ...differences in holdings
c_join = ['filer', 'cik', 'cusip', 'ticker', 'submissiontype']
df_diff_hldg = pd.merge(df_13F_q1, df_13F_q2,
                        on=c_join,
                        how='outer', suffixes=['_q1', '_q2'])

print(df_diff_hldg.head().to_string())

# ...consolidate columns
for c in ['nameofissuer', 'titleofclass']:
    df_diff_hldg[c] = df_diff_hldg[c + '_q1']
    df_diff_hldg[c] = df_diff_hldg[c].where(df_diff_hldg[c].notnull(), df_diff_hldg[c + '_q2'])

# ... select columns to keep
c = ['submissiontype', 'filer', 'cik', 'cusip', 'ticker', 'nameofissuer', 'titleofclass',
     'sshprnamt_q1', 'sshprnamt_q2','value_q1', 'value_q2',
     'total_aum_filer_q1', 'perc_of_13F_holdings_q1',
     'total_aum_filer_q2', 'perc_of_13F_holdings_q2'
     ]
df_diff_hldg = df_diff_hldg[c]
# update issuer names
update_values = lambda x: x if d_cusip_nameofissuer.get(x) == None else d_cusip_nameofissuer.get(x)
df_diff_hldg['nameofissuer'] = df_diff_hldg['cusip'].map(update_values)
# ...fill NaNs
dict_aum = df_diff_hldg.groupby('cik').agg({'total_aum_filer_q1': 'max',
                                            'total_aum_filer_q2': 'max'}).fillna(value=0).to_dict()

for c in ['total_aum_filer_q1', 'total_aum_filer_q2']:
    df_diff_hldg[c] = df_diff_hldg['cik'].map(dict_aum.get(c))
df_diff_hldg.fillna(value=0, inplace=True)

# If we show the differences, we need to aggregate across the cusips held by OTHER managers
c_index = ['submissiontype', 'filer', 'cik', 'cusip', 'ticker', 'nameofissuer', 'titleofclass']
dict_agg = dict([(c, 'sum') for c in df_diff_hldg.columns if c not in c_index])
df_diff_hldg = df_diff_hldg.groupby(c_index).agg(dict_agg).reset_index()

# ...add differences
for c in ['sshprnamt', 'value', 'perc_of_13F_holdings']:
    df_diff_hldg[c + '_diff'] = df_diff_hldg[c + '_q2'] - df_diff_hldg[c + '_q1']
# ...add changes in shares as percentages (relativ to Q1 holdings)
df_diff_hldg['sshprnamt_diff_perc'] = df_diff_hldg['sshprnamt_diff']/df_diff_hldg['sshprnamt_q1'] * 100


# only show funds that have already filed in CURRENT quarter
print(df_diff_hldg[df_diff_hldg.filer.isin(l_funds_reported_q2)].to_string())


print(df_diff_hldg[df_diff_hldg.cusip == '68622P109'].to_string())
print(df_diff_hldg[df_diff_hldg.nameofissuer.str.contains('TRICID').fillna(value=False)].to_string())
print(df_diff_hldg.loc[df_diff_hldg.ticker.str.contains('GBT').fillna(value=False), :].to_string())

print(df_diff_hldg.loc[df_diff_hldg.ticker.str.contains('SRRK').fillna(value=False), :].to_string())

# ToDo: This is the key filter - filter by FILER (cik) & analyze the changes)
print(df_diff_hldg[df_diff_hldg.cik ==1599882].sort_values('sshprnamt_diff_perc', ascending=False).to_string())

'SRRK' in list(df_diff_hldg.ticker)

filer = 'Redmile'

# TOP 10 ADDS
print('Top 10 ADDS for', [f for f in df_diff_hldg.filer.drop_duplicates() if f.__contains__(filer)][0])
print(df_diff_hldg[df_diff_hldg.filer.str.contains(filer)]
      .sort_values(by=['value_diff'], ascending=False).head(10).to_string())
print('Top 10 SELLS for', [f for f in df_diff_hldg.filer.drop_duplicates() if f.__contains__(filer)][0])
print(df_diff_hldg[df_diff_hldg.filer.str.contains(filer)]
      .sort_values(by=['value_diff'], ascending=False).tail(10).to_string())

df_diff_hldg[df_diff_hldg.filer.str.contains(filer)].value_q1.sum()
df_diff_hldg[df_diff_hldg.filer.str.contains(filer)].value_q2.sum()
print(df_diff_hldg[df_diff_hldg.filer.str.contains(filer)].to_string())


print(df_diff_hldg.head().to_string())
xx = df_diff_hldg[df_diff_hldg.filer.str.contains('PERCEPTIVE')]
xx.columns
print(xx.to_string())
xx.groupby(['isamendment']).aggregate({'value': 'sum'})

xx = df_13F_q2[df_13F_q2.filer.str.contains('Endurant')]
xx.columns
xx.groupby(['isamendment']).aggregate({'value': 'sum'})

# ----------------------------------------------------------------------------------------------------------------------
# ISSUER ANALYSIS:  Aggregation on issuers should be done only for issuers that have already filed
# IN THIS WAY IS MOST MEANINGFULL UNTIL ALL FUNDS HAVE FILLED;

# group by: cusip, nameofissuer and ticker
c_group = ['cusip', 'ticker']
tmp = df_13F_q1[df_13F_q1.filer.isin(l_funds_reported_q2)].groupby(c_group).agg({'value': ['sum'],
                                                                                 'sshprnamt': ['sum'],
                                                                                 'filer': ['nunique']})
tmp.columns = ['_'.join(e) for e in tmp.columns]
tmp['value_sum'] = round(tmp['value_sum'] / 10 ** 6, 1)
df_issuers_q1 = tmp.copy(deep=True)

tmp = df_13F_q2[df_13F_q2.filer.isin(l_funds_reported_q2)].groupby(c_group).agg({'value': ['sum'],
                                                                                 'sshprnamt': ['sum'],
                                                                                 'filer': ['nunique']})
tmp.columns = ['_'.join(e) for e in tmp.columns]
tmp['value_sum'] = round(tmp['value_sum'] / 10 ** 6, 1)
df_issuers_q2 = tmp.copy(deep=True)


# ...changes in popularity:
df_diff_issuers = pd.merge(df_issuers_q1, df_issuers_q2,
                           left_index=True, right_index=True,
                           how='outer', suffixes=['_q1', '_q2']).fillna(value=0)
print(df_diff_issuers.head().to_string())
c_keep = ['filer_nunique', 'value_sum', 'sshprnamt_sum']
for c in c_keep:
    df_diff_issuers[c + '_diff'] = (df_diff_issuers[c + '_q2'] - df_diff_issuers[c + '_q1']).astype(int)
df_diff_issuers = df_diff_issuers[[c + '_diff' for c in c_keep]].reset_index()
# add issuer names
update_values = lambda x: x if d_cusip_nameofissuer.get(x) == None else d_cusip_nameofissuer.get(x)
df_diff_issuers['nameofissuer'] = df_diff_issuers['cusip'].map(update_values)

# POPULARITY - TOP 10 - GAINERS
print('-------------------------------------------------------')
print('POPULARITY - TOP 10 - GAINERS by holding COUNTS')
print('TOTAL # of filers:', len(l_funds_reported_q2))
print(df_diff_issuers.sort_values(by=['filer_nunique_diff', 'sshprnamt_sum_diff'], ascending=False).head(10).to_string())
print('')
# POPULARITY - BOTTOM 10 - LOOSERS
print('POPULARITY - BOTTOM 10 - LOOSERS by holding COUNTS')
print('TOTAL # of filers:', len(l_funds_reported_q2))
print(df_diff_issuers.sort_values(by=['filer_nunique_diff', 'sshprnamt_sum_diff'], ascending=False).tail(10).to_string())
print('')
print('-------------------------------------------------------')


# ----------------------------------------------------------------------------------------------------------------------
# building a dashboard
# https://towardsdatascience.com/how-to-build-a-complex-reporting-dashboard-using-dash-and-plotl-4f4257c18a7f#4711


