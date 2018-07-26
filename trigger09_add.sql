--9. A user may not bid on an item he or she is also selling.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger09;
create trigger trigger09
before insert ON bid
for each row
when exists (
    select *
    from item
    where seller_id = new.bidder_id
    and item.item_id = new.item_id
)
begin
    select raise(rollback, 'A user may not bid on an item he or she is also selling');
end;