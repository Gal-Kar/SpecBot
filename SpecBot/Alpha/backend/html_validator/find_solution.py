from googlesearch import search

def search_google(query):
    search_results = []
    try:
        for j in search(query, tld="co.in", num=3, stop=3, pause=0):
            search_results.append(j)
    except:
        search_results.append("No solution due to googlesearch api limits")
    
    return search_results

def get_solution(msg):
    query = "rocket validator " + msg
    return search_google(query)
