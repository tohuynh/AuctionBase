sqlite3 auction.db < create.sql
sqlite3 auction.db < load.txt
sqlite3 auction.db < constraints_verify.sql
sqlite3 auction.db < trigger08_add.sql
sqlite3 auction.db < trigger09_add.sql
sqlite3 auction.db < trigger11_add.sql
sqlite3 auction.db < trigger11a_add.sql
sqlite3 auction.db < trigger13_add.sql
sqlite3 auction.db < trigger14_add.sql
sqlite3 auction.db < trigger15_add.sql
sqlite3 auction.db < trigger16_add.sql

rm uuser.dat
rm uitem.dat
rm ucategory.dat
rm ubid.dat