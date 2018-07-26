--11. No auction may have a bid before its start time or after its end time.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger11;
create trigger trigger11
before insert ON bid
for each row
when exists (
    select *
    from item
    where (ends < new.time or started > new.time)
    and item.item_id = new.item_id
)
begin
    select raise(rollback, 'No auction may have a bid before its start time or after its end time');
end;