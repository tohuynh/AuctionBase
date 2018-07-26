--11a. No new bid after buy_price has been met (i.e. currently >= buy_price)
PRAGMA foreign_keys = ON;
drop trigger if exists trigger11a;
create trigger trigger11a
before insert ON bid
for each row
when exists (
    select *
    from item
    where currently >= buy_price
    and item.item_id = new.item_id
)
begin
    select raise(rollback, 'No new bid after buy_price has been met');
end;