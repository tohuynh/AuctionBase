--2. All sellers and bidders must already exist as users.
--forein key constraint on seller_id in item table, and on bidder_id in bid table, where both references user_id in user table
select *
from item, bid
where item.item_id = bid.item_id
    and (seller_id not in (select user_id from user) or bidder_id not in (select user_id from user));

--4. Every bid must correspond to an actual item.
--foreign key constraint on item_id in bid table that references item_id in item table
select *
from bid
where item_id not in (
    select item_id
    from item
);

--5. The items for a given category must all exist.
--foreign key constraint on item_id in category table that references item_id in item table
select *
from category
where item_id not in (
    select item_id
    from item
);