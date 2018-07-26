--14. Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger14;
create trigger trigger14
before insert ON bid
for each row
when exists (
    select *
    from item
    where (new.amount <= currently)
    and item.item_id = new.item_id
)
begin
    select raise(rollback, 'Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.');
end;