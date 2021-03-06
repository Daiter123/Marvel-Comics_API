#imports
import urllib.parse
import requests
from tabulate import tabulate

#Authentication
ts = "1" # Default 1
apikey = "" # public key
hash = "" # This is an md5 hash (generated by dropping the following info in an md5 generator: 'ts+apikey+privatekey' you need to do this manually)

while True: #exit the while loop if user-input for one of the values is 'q' or 'quit'
 
    characterRequest = input("\nSearch a comic book character: ")
    if characterRequest == 'quit' or characterRequest == 'q':
        break
 
    #building the url and printing it to control parameters
    main_api = "http://gateway.marvel.com/v1/public/characters?"
    url = main_api + urllib.parse.urlencode({"ts":ts, "apikey":apikey, "hash":hash,"nameStartsWith":characterRequest})
    # printing it for testing purposes
    print("URL:" + (url))
 
    # Making the API call request
 
    json_data = requests.get(url).json() # Our json data
    json_status = json_data["code"] # Our json status codes
 
    if json_status == 200: #if API call is succesful
 
        # Default table layout
        menuTable = "="*(42+len(characterRequest))
   
        #Use the data
 
        print("\n" + menuTable)
        print("You requested info for Marvel character - " + str(characterRequest))
        print(menuTable + "\n")
 
        #declare required lists
        names = []
        descriptions = []
        seriesCount=[]
        comicCount=[]
        eventCount=[]
        popularity=[]
        
        for each in json_data['data']['results']:  # Getting the general data from the requested characters
           
            name = each['name'] # character name
 
            series_count = each['series']['available'] #series in which this character appears
            comic_count = each['comics']['available'] #comics which feature this character.
            event_count = each['events']['available'] #events in which this character appears
            sumPopularity = int(event_count) + int(series_count) + int(comic_count) # Indicator for character popularity
           
            # get description of each character, if they don't have one we will create a link to marvel fandom wiki
            description = each['description']
 
            if description == '':
                description = "No description found visit -> https://marvel.fandom.com/wiki/" + name.replace(" ","_")
 
 
            # Add items to list so we can use them with tabulate
            names.append(name)
            popularity.append(sumPopularity)
            seriesCount.append(series_count)
            comicCount.append(comic_count)
            eventCount.append(event_count)
            
            # for testing purposes as tabulate tempts to mess up the layout with a long description (but it works)
            if "No description found visit" in description:
                descriptions.append("/") #COMMENT THIS IF YOU WANT TO SEE DESCRIPTIONS
            else:
                #descriptions.append(description) #UNCOMMENT THIS IF YOU WANT TO SEE DESCRIPTIONS
                descriptions.append("/")
         

        # popularity indicator (extra functionality)
        
        popularityName = []
        for i in range(len(popularity)):
            if popularity[i] > 500:
                popularityName.append("Extremely popular")
            elif popularity[i] > 150 and popularity[i] <= 500:
                popularityName.append("Very popular")
            elif popularity[i] > 50 and popularity[i] <= 150:
                popularityName.append("Popular")
            elif popularity[i] > 10 and popularity[i] <= 50:
                popularityName.append("Common")
            elif popularity[i] >= 0 and popularity[i] <= 10:
                popularityName.append("Uncommon")
            else:
                popularityName.append("/")
        
        #Outside the for loop, we will check if our query got a result, if yes we will prepare our data for tabulate
        if len(names) > 0:
            tableData = []
            for i in range(len(names)):
                tableData.append([names[i], descriptions[i], seriesCount[i], comicCount[i], eventCount[i],popularityName[i]])
                

            #Using Tabulate to display our chosen data
            print(tabulate(tableData,headers=["Name", "Desc", "Series", "Comics", "Events","Popularity"],tablefmt="orgtbl")) #grid
        else:
            print("Geen resultaten") #print no result if search term had no results
 
    # if API call status is not OK then print custom error page.
    elif json_status == 402:
        print(menuTable)
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one of the parameters.")
        print(menuTable)
 
    elif json_status == 409:
        print(menuTable)
        print("Status Code: " + str(json_status) + "; Missing an entry for one of the parameters.")
        print(menuTable)
   
    else:
        print(print)
        print("status Code: " + str(json_status) + "; Following link may provide an answer to your problem.")
        print("https://developer.marvel.com/documentation/authorization")
        print(menuTable + "\n")
