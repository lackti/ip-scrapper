import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

webpages = {
'https://www.socks-proxy.net': {'id': 'proxylisttable'},
 'https://www.proxyscan.io': {'id': 'proxyTable'},
 'https://free-proxy-list.net': {'id': 'proxylisttable'},
 'https://www.us-proxy.org': {'id': 'proxylisttable'},
 'https://free-proxy-list.net/anonymous-proxy.html': {'id':'proxylisttable'},
 'https://www.sslproxies.org': {'id':'proxylisttable'},
 'https://www.proxynova.com/proxy-server-list':{'id':'tbl_proxy_list'},
 'https://free-proxy-list.net/uk-proxy.html':{'id':'proxylisttable'},
 'https://www.proxydocker.com':{'class':'table proxylist_table'}
}


def get_ip(url,div):
    page = requests.get(url,timeout=(3.05, 27))
    soup = BeautifulSoup(page.content, 'html.parser')
    tbl = soup.find("table",div)
    df = pd.read_html(str(tbl))[0]
    df.dropna(how='all', inplace=True)
    all_columns = [col.lower() for col in list(df.columns)]
    df.columns = all_columns
    if 'port' in all_columns:
        df["ipPort"] = df[all_columns[0]].apply(lambda x: str(x))+ ":" + df[all_columns[1]].apply(lambda x: str(int(x)))
        df = df.rename(columns={all_columns[0]:"ip",all_columns[1]:"port"})
    else:
        df = df.rename(columns={all_columns[0]:"ipPort"})
        df["ip"] = df.ipPort.apply(lambda x: x.split(":")[0])
        df["port"] = df.ipPort.apply(lambda x: x.split(":")[1])
    
    features = ["ipPort", "ip", "port", "country"]
    new_df = df[features]
    return new_df

print("Welcome to ip scrapping ! \n")

print("""---> Output format :\n
Please insert 1 for CSV format\n
Please insert 2 for TEXT format\n
Please insert 3 for both TEXT and CSV format\n""")

save_format = input("Enter your choice: ")

pdList = [] # all df will be socked here

for url, div in webpages.items():
    web = url.split("//")[1]
    try:
        df = get_ip(url,div)
        print("successful download proxies from ({})".format(web))
        pdList.append(df)
    except:
        print("Faild to download proxies from ({})".format(web))


print("Trying to add all the proxies together")

df_all_proxies = pd.concat(pdList) # conactenate all df in one df

time.sleep(2)
print("\nCheck for duplicates ...")

dup_nbr = df_all_proxies[df_all_proxies.duplicated()].shape[0]

df_all_proxies.drop_duplicates(subset="ipPort",inplace=True) # remove all duplicates

prox_unq = df_all_proxies.shape[0]

time.sleep(2)

print("{} duplicates was removed successfully".format(dup_nbr))

if save_format == "1":
	df_all_proxies.to_csv("all_ip.csv")
	print("Successful {} were found\nall ips are saved to all_ip.csv".format(prox_unq))

elif save_format == "2":
	df_all_proxies.ipPort.to_csv("all_ip.txt",index=False,sep='\n')
	print("Successful {} were found\nall ips are saved to all_ip.txt".format(prox_unq))

elif save_format == "3":
	df_all_proxies.to_csv("all_ip.cvs")
	df_all_proxies.ipPort.to_csv("all_ip.txt",index=False,sep='\n')
	print("Successful {} were found\nall ips are saved to all_ip.csv and all_ip.txt".format(prox_unq))

else:
	df_all_proxies.to_csv("all_ip.csv")
	print("Successful {} were found\nall ips are saved to all_ip.csv".format(prox_unq))




