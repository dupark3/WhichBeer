#Which Beer App
Take a picture of a beer menu, and the app will search through untappd for users with similar taste as you based on your beer ratings on untappd. Using collaborative filtering, beers that users similar to you love will be recommended out of the menu. 

Todo:
☑ Request an Untappd API account for client id and key 
☐ Connect Tessaract to take a jpg and convert to a string
☐ Create algorithm to parse the string and return a list of beer names 
☐ Create API call and parsing to take a list of beer names and return a list of beer ids
☐ Sort similar users based on similarity index
☐ Search similar users for menu beers, returning an ordered list of recommendations