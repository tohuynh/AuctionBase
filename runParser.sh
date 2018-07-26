#python my_parser.py ebay_data/items-*.json
python my_parser.py items-p3.json

sort -u item.dat > uitem.dat
sort -u user.dat > uuser.dat
sort -u category.dat > ucategory.dat
sort -u bid.dat > ubid.dat

rm item.dat
rm user.dat
rm category.dat
rm bid.dat