from edgar import Edgar, Company, XBRL
import lxml
edgar = Edgar()

# ----------------------------------------------------------------------------------------------------------------------
edgar.get_cik_by_company_name('BAKER BROS. ADVISORS LP')
possible_companies = edgar.find_company_name("Baker Bro")

for c in possible_companies:
    print(c)


company = Company("BAKER BROS. ADVISORS LP", "0001263508")
tree = company.get_all_filings(filing_type="4")
docs = Company.get_documents(tree, no_of_documents=5)

# xbrl = XBRL(docs[0])
# xbrl.getchildren()

docs[0].text_content()

lxml.html.open_in_browser(docs[0])