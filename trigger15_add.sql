--15. All new bids must be placed at the time which matches the current time of your AuctionBase system.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger15;
create trigger trigger15
before insert ON bid
for each row
when exists (
    select *
    from currenttime
    where new.time <> cur_time
)
begin
    select raise(rollback, 'All new bids must be placed at the time which matches the current time of your AuctionBase system');
end;