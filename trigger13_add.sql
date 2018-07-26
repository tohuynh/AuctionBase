--13. In every auction, the Number of Bids attribute corresponds to the actual number of bids for that particular item.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger13;
create trigger trigger13
after insert ON bid
for each row
begin
    update item
    set number_of_bids = number_of_bids + 1
    where item.item_id = new.item_id;
end;