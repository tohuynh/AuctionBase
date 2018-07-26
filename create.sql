drop table if exists item;
create table item (
    item_id int not null,
    name text not null,
    currently real not null,
    buy_price real,
    first_bid real not null,
    number_of_bids int not null,
    started datetime not null,
    ends datetime not null,
    description text not null,
    seller_id text not null,
    primary key (item_id),
    foreign key (seller_id) references user(user_id),
    check(ends > started)
);

drop table if exists user;
create table user (
    user_id text not null,
    rating int not null,
    location text,
    country text,
    primary key (user_id)
);

drop table if exists category;
create table category (
    item_id int not null,
    category_name text not null,
    primary key (item_id, category_name),
    foreign key (item_id) references item(item_id)
);

drop table if exists bid;
create table bid (
    item_id int not null,
    bidder_id text not null,
    time datetime not null,
    amount real not null,
    primary key (item_id, time),
    foreign key (item_id) references item(item_id),
    foreign key (bidder_id) references user(user_id),
    unique (item_id, bidder_id, amount)
);

drop table if exists currenttime;
create table currenttime(cur_time datetime not null);
insert into currenttime values(datetime('2001-12-20 00:00:01'));
select cur_time from currenttime;