
import csv
import requests
from bs4 import BeautifulSoup
import urllib
import datetime
import re

from urlparse import urljoin


def getEachHospitalUrl(base,suffix):
    return urljoin(base, suffix)

def getSoap(url):
    try:
        page = urllib.urlopen(url).read()
        return BeautifulSoup(page, "html.parser")
    except:
        r = requests.get(url.format('1'))
        return BeautifulSoup(r.content, 'html.parser')

def csv_file_name_generation(csvFile):
    csvFileName =  datetime.datetime.now().strftime("%I%M%S%p_%B%d_%Y")+ '_' + csvFile
    return open(csvFileName, 'w')



def generate_csv(hName,address,noOfAprov,writer):
    try:
        writer.writerow({'HospitalName' : hName, 'Address' : address, 'NoOfAffiliatedProvider': noOfAprov})
    except:
        print('error found')
        pass



def parse_each_page(hospitalUrl,writer):
    eachHospitalPage = getSoap(hospitalUrl)
    try:
        hName = eachHospitalPage.find_all(attrs={'class' : 'summary-hero-address'})
        hospitalName =  hName[0].find('h1').text
    except:
        hospitalName = 'N/A'
        print 'No hospital name found'
        pass
    try:
        haddress = eachHospitalPage.find_all(attrs={'itemprop' : 'address'})
        parsedhAddress =  haddress[0].text
        hAddress = ''
        for a in parsedhAddress.split(','):
            if '\n' in a:
                hAddress = hAddress + ',' + a.strip().replace('\n',',')
                continue
            hAddress = hAddress + ',' + a.strip()
    except:
        hAddress = [',']
        pass
    try:
        afprovider = eachHospitalPage.find_all(attrs={'class' : 'results-header'})
        noOfAffiliatedProvider = re.findall(r'\d+', afprovider[0].text )
    except:
        pass
    generate_csv(hospitalName, hAddress[1:], int(noOfAffiliatedProvider[0]), writer)


def go_to_next_page(url,writer):
    soup = getSoap(url)
    Hospitals =  soup.find_all('a', attrs={'class' : 'providerSearchResultSelectAction'})
    for hospital in Hospitals:
        if 'clinic-directory' not in hospital['href']:
            eachHospitalUrl =   getEachHospitalUrl(url,hospital['href'])
            parse_each_page(eachHospitalUrl,writer)
    try:
        pagination = soup.find_all('span', attrs={'class': 'nextPage'})[0].find('a')
        nextPageUrl = pagination[0]['href']
        go_to_next_page(nextPageUrl,writer)
    except:
        return


def runParser(searchSyntax,location,csvName):
    fieldnames = ['HospitalName', 'Address', 'NoOfAffiliatedProvider']
    csvF = csv_file_name_generation(csvName)
    writer = csv.DictWriter(csvF, fieldnames=fieldnames)
    writer.writeheader()
    soup = getSoap(searchSyntax)
    Hospitals =  soup.find_all('a', attrs={'class' : 'providerSearchResultSelectAction'})
    for hospital in Hospitals:
        if 'clinic-directory' not in hospital['href']:
            eachHospitalUrl =   getEachHospitalUrl(searchSyntax,hospital['href'])
            parse_each_page(eachHospitalUrl,writer)
    #
    try:
        pagination = soup.find_all('span', attrs={'class' : 'nextPage'})[0].find('a')
        nextPageUrl =  pagination[0]['href']
        go_to_next_page(nextPageUrl,writer)
    except:
        pass
    csvF.close()
runParser('https://www.healthgrades.com/hospital-directory/search/HospitalsResults?loc=New+York%2C+NY','new york,ny','healthgrade.csv')



<div class="listingInformationColumn">
<div class="listingHeader">
<div class="listingHeaderLeftColumn">
<h2>
<a class="providerSearchResultSelectAction" data-hgoname="fsr-result-facility-name" href="/hospital-directory/new-york-ny-manhattan/mount-sinai-beth-israel-hgste20a7b36330169">Mount Sinai Beth Israel</a>
</h2>
<div class="addresses">
<div class="address">1st Avenue at 16th street, New York, NY 10003</div>
</div>
</div>
<div class="listingHeaderRightColumn">
<div class="save-share-buttons">
<script type="text/javascript">
    var jsonData_684F5B = {"Id":"684f5b","Url":"/hospital-directory/new-york-ny-manhattan/mount-sinai-beth-israel-hgste20a7b36330169","RemoverHeader":"Remove Mount Sinai Beth Israel?","Name":"Mount Sinai Beth Israel","FullName":"Mount Sinai Beth Israel","RemoveText":"This action will remove Mount Sinai Beth Israel from your dashboard of saved hospitals.","SaveType":"facility","EmailShare":{"ShareType":3,"OfficeGuid":null,"ToAddress":null,"FromAddress":null,"CustomMessage":null,"EmailShareId":"684F5B","RequestUrlAuthority":null,"OmnitureSaveType":"facility","ShareTypeText":"FacilityProfile","Source":null,"SuppressSend":false,"BeaconTrackingId":null,"SentToSelf":true},"TargetId":"684f5b","HospitalUrl":null,"HospitalBlockClass":"displayNone","RateDoctorUrl":null,"SuppressSave":false,"SuppressShare":false,"SuppressSurvey":"false"};
</script>
<div class="save-favorites" data-save-id="684f5b">
<a class="btn action-button save-favorites-action" data-save-hgoname="save-facility" data-save-hospital-id="684f5b" data-target-id="684F5B" title="Save facility to your account">Save</a>
<a class="btn action-button remove-favorites-action" data-remove-id="684f5b" data-save-hospital-id="684f5b" data-target-id="684F5B" title="Click to remove from your account."><i class="hg-icon hg-check"></i>Saved</a>
</div>
<span class="share-button-hide-shadow">
<a class="btn share-button" data-share-id="684f5b" data-target="#SaveShareButtons" data-target-id="684F5B" title="Share">
            Share
        </a>
</span>
</div>
</div>
</div>
<div class="listingBody clearfix">
<div class="listingCenterColumn">
<div class="listingProfileContent">
                        Mount Sinai Beth Israel has:
                        <ul>
<li class="dataDebug"><a data-hgoname="fsr-result-five-star-ratings" href="/hospital-directory/new-york-ny-manhattan/mount-sinai-beth-israel-hgste20a7b36330169#FacilityRatingsbyCategory_anchor">7 Healthgrades 5-Star Ratings</a></li>
<li class="dataDebug"><a data-hgoname="fsr-result-awards" href="/hospital-directory/new-york-ny-manhattan/mount-sinai-beth-israel-hgste20a7b36330169#Ratings-Awards">2 Healthgrades Quality Awards</a></li>
<li class="dataDebug"><a data-hgoname="fsr-result-affiliated-providers" href="/hospital-directory/new-york-ny-manhattan/affiliated-physicians-HGSTE20A7B36330169">1040 Affiliated Providers</a></li>
</ul>
<input class="provLatLonHid" type="hidden" value="40.73267, -73.981621">
</input></div>
</div>
<div class="listingRightColumn">
<div class="listingPreferenceMatchContainer">
<div class="listingPreferenceMatchContainerInner">
<span class="matchCheckIconBig"></span>
<span class="hgHighlightContainer">
<span class="hgHighlightCheck"></span>
<span class="hgHighlightLabel" title="1.83 miles from New York, NY">1.83 miles from New York, NY</span>
</span>
</div>
</div>
</div>
</div>
</div>

