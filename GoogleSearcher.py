from googlesearch import search


def GetArray(query):

    results = []
    # Perform the search
    for result in search(query, num_results=20):
        results.append(result)
    return results
    print(results)

#TestItem = GetArray("Tarts and things")
#print(TestItem)