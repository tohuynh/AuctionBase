--8. The Current Price of an item must always match the Amount of the most recent bid for that item.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger08;
create trigger trigger08
after insert ON bid
for each row
begin
    update item
    set currently = new.amount
    where item.item_id = new.item_id;
end;