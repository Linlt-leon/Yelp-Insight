#!/bin/bash

# Define an array of locations
locations=(
    "Bishan+East" "Marymount" "Upper+Thomson"
    "Alexandra+Hill" "Alexandra+North" "Bukit+Ho+Swee" "Bukit+Merah" "City+Terminals" "Depot+Road" "Everton+Park"
    "Henderson+Hill" "Kampong+Tiong+Bahru" "Maritime+Square" "Redhill" "Singapore+General+Hospital"
    "Telok+Blangah+Drive" "Telok+Blangah+Rise" "Telok+Blangah+Way" "Tiong+Bahru" "Tiong+Bahru+Station"
    "Anak+Bukit" "Coronation+Road" "Farrer+Court" "Hillcrest" "Holland+Road" "Leedon+Park" "Swiss+Club" "Ulu+Pandan"
    "Anson" "Bayfront+Subzone" "Bugis" "Cecil" "Central+Subzone" "City+Hall" "Clifford+Pier" "Marina+Centre" "Maxwell"
    "Nicoll" "Phillip" "Raffles+Place" "Tanjong+Pagar"
    "Aljunied" "Geylang+East" "Kallang+Way" "Kampong+Ubi" "MacPherson"
    "Bendemeer" "Boon+Keng" "Crawford" "Geylang+Bahru" "Kallang+Bahru" "Kampong+Bugis" "Kampong+Java" "Lavender" "Tanjong+Rhu"
    "Marina+East"
    "Marina+South"
    "East+Coast" "Katong" "Marina+East" "Marine+Parade" "Mountbatten"
    "Bras+Basah" "Dhoby+Ghaut" "Fort+Canning"
    "Cairnhill" "Goodwood+Park" "Istana+Negara" "Monks+Hill" "Newton+Circus" "Orange+Grove"
    "Balestier" "Dunearn" "Malcolm" "Moulmein" "Mount+Pleasant"
    "Boulevard" "Somerset" "Tanglin"
    "China+Square" "Chinatown" "Pearls+Hill" "Peoples+Park"
    "Commonwealth" "Dover" "Ghim+Moh" "Holland+Drive" "Kent+Ridge" "Margaret+Drive" "Mei+Chin" "National+University+of+Singapore"
    "one-north" "Pasir+Panjang+1" "Pasir+Panjang+2" "Port" "Queensway" "Singapore+Polytechnic" "Tanglin+Halt"
    "Institution+Hill" "Leonie+Hill" "One+Tree+Hill" "Oxley" "Paterson"
    "Bencoolen" "Farrer+Park" "Kampong+Glam" "Little+India" "Mackenzie" "Mount+Emily" "Rochor+Canal" "Selegie" "Sungei+Road"
    "Victoria"
    "Boat+Quay" "Clarke+Quay" "Robertson+Quay"
    "Sentosa" "Southern+Group"
    "Straits+View" "Chatsworth" "Nassim" "Ridout" "Tyersall"
    "Bidadari" "Boon+Teck" "Braddell" "Joo+Seng" "Kim+Keat" "Lorong+8+Toa+Payoh" "Pei+Chun" "Potong+Pasir" "Sennett"
    "Toa+Payoh+Central" "Toa+Payoh+West" "Woodleigh"
    "Bedok" "Changi" "Changi+Bay" "Pasir+Ris" "Paya+Lebar" "Tampines"
    "Central+Water+Catchment" "Lim+Chu+Kang" "Mandai" "Sembawang" "Simpang" "Sungei+Kadut" "Woodlands" "Yishun"
    "Ang+Mo+Kio" "Hougang" "North-Eastern+Islands" "Punggol" "Seletar" "Sengkang" "Serangoon"
    "Boon+Lay" "Bukit+Batok" "Bukit+Panjang" "Choa+Chu+Kang" "Clementi" "Jurong+East" "Jurong+West" "Pioneer" "Tengah"
    "Tuas" "Western+Islands" "Western+Water+Catchment"
)

# Counter for crawled locations
total_locations=${#locations[@]}
crawled=0

# Loop through each location
for location in "${locations[@]}"
do
   echo "Crawling data for $location"
   scrapy crawl yelp_crawler -a location="$location+Singapore" -a category="" -a starting_num=0
   ((crawled++))
   percentage=$(echo "scale=2; $crawled*100/$total_locations" | bc)
   echo "Percentage of locations crawled: $percentage%"
done
