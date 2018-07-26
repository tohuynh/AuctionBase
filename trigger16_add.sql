--16. The current time of your AuctionBase system can only advance forward in time, not backward in time.

PRAGMA foreign_keys = ON;
drop trigger if exists trigger16_insert;
create trigger trigger16_insert
before insert ON currenttime
for each row
when exists (
    select *
    from currenttime
)
begin
    select raise(rollback, 'Cannot insert new currenttime, please update existing currenttime');
end;

PRAGMA foreign_keys = ON;
drop trigger if exists trigger16_delete;
create trigger trigger16_delete
before delete ON currenttime
for each row
begin
    select raise(rollback, 'Cannot delete existing currenttime');
end;

PRAGMA foreign_keys = ON;
drop trigger if exists trigger16_update;
create trigger trigger16_update
before update ON currenttime
for each row
when new.cur_time <= old.cur_time
begin
    select raise(rollback, 'The current time of your AuctionBase system can only advance forward in time, not backward in time.');
end;