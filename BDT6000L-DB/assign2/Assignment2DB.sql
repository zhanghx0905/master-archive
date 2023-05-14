/* MSBD 6000L: Assignment 2 – Fanclub Management System Sample Database */

drop table Remark;
drop table RegistersFor;
drop table Hosts;
drop table MemberOf;
drop table Event;
drop table Clubmember;
drop table RegisteredUser;
drop table Fanclub;
drop table Employee;

create table Employee(
	employeeId      smallint primary key,
	employeeName    varchar(30) not null,
	post            varchar(20) not null,
	username        char(10) not null unique check (regexp_like(rtrim(username),'^[a-z]{6,10}$')));

create table Fanclub(
	clubId          smallint primary key,
	clubName		varchar(50) not null,
    description     varchar(150) not null,
	establishedDate	date not null);

create table RegisteredUser(
	username		char(10) primary key check (regexp_like(rtrim(username),'^[a-z]{6,10}$')),
	firstName	    varchar(15) not null,
    lastName	    varchar(20) not null,
	gender			char(1) not null check (gender in ('M','F')),
	phoneNo			char(8) not null check (regexp_like(phoneNo,'^\d{8}$')),
    email           varchar(30) not null unique);

create table Clubmember(
	username 		char(10) primary key references RegisteredUser(username) on delete cascade,
	birthdate		date not null,
	occupation		varchar(25) not null,
	educationLevel  char(13) not null check (educationLevel 
    				in ('none','primary','secondary','tertiary','post tertiary')));

create table Event(
	eventId			smallint primary key,
	eventName		varchar(50) not null,
	eventDate		date not null,
    eventTime       char(4) not null check (regexp_like(eventTime, '^([01]\d|2[0-3])[0-5]\d$')),
	venue			varchar(50) not null,
	memberFee		number(7,2) default 0 not null check (memberFee>=0),
	nonmemberFee	number(7,2) default 0 not null check (nonmemberFee>=0),
    quota           smallint not null check (quota>0),
    status          char(11) default 'unavailable' not null 
    				check (status in ('available', 'cancelled', 'ended', 'full', 'unavailable')),
	eventType		char(9) default 'nonmember' not null check (eventType in ('member','nonmember')),
	employeeId		smallint not null references Employee(employeeId) on delete cascade);

create table MemberOf(
	clubId			smallint references Fanclub(clubId) on delete cascade,
	username		char(10) references Clubmember(username) on delete cascade,
	joinDate		date not null,
	howInformed	    char(15) not null 
					check (howInformed in ('friend','print ad','social media','web ad','other')),
    primary key(clubId, username));

create table Hosts(
	clubId          smallint references Fanclub(clubId) on delete cascade,
	eventId         smallint references Event(eventId) on delete cascade,
	primary key(clubId, eventId));

create table RegistersFor(
	eventId         smallint references Event(eventId) on delete cascade,
	username        char(10) references RegisteredUser(username) on delete cascade,
	paidFee         char(1) default 'N' not null check (paidFee in ('Y','N')),
	attended        char(1) check (attended in ('Y','N')),
    primary key(eventId, username));
	
create table Remark(
	remarkId                smallint primary key,
	subject			        varchar(50) not null,
	text			        varchar(150) not null,
	submissionDate	        date not null,
	status			        char(10) check(status in ('read','processing','done')),
	actionTaken		        varchar(50),
	remarkType		        char(5) not null check(remarkType in ('club','event')),
	clubOReventId           smallint not null,
    username                char(10) not null references RegisteredUser(username) on delete cascade,
	employeeId              smallint references Employee(employeeId) on delete set null);

/********** Employee table **********/
insert into Employee values (1,'Michelle Cafa','Manager','empcafa');
insert into Employee values (2,'Eric Chen','Event Coordinator','empchen');
insert into Employee values (3,'Nelson Ray','Event Coordinator','empray');
insert into Employee values (4,'Bill Hsu','Fanclub Relations','emphsu');
insert into Employee values (5,'Judy Wang','Fanclub Relations','empwang');

/********** Fanclub table **********/
insert into Fanclub values (1,'Dan Brown Fanclub','Share and discover content and connect with other fans of Dan Brown.','05-DEC-85');
insert into Fanclub values (2,'STARFLEET','STARFLEET offers members a wealth of resources related to the Star Trek universe.','05-DEC-85');
insert into Fanclub values (3,'Superman Fanclub','A club for people who are fans of the Man of Steel, the first and best comic book superhero.','25-JUL-95');
insert into Fanclub values (4,'Jay-Z Fanclub','Share, discover content and connect with other fans of Jay-Z. Find Jay-Z videos, photos, wallpapers, forums, polls, news and more.','12-AUG-98');
insert into Fanclub values (5,'Pottermore','Pottermore provides a forum for discussing everything related to the Harry Potter books and movies.','01-NOV-00');
insert into Fanclub values (6,'The Beyhive','The Beyhive provides Beyonce fans access to news, special experiences, exclusive merchandise and more.','10-OCT-03');
insert into Fanclub values (7,'The Swifters','Sign up to register for exclusive access to Taylor Swift photos, videos, news and updates.','13-SEP-07');
insert into Fanclub values (8,'Drake Fanclub','Sign up to get access to the latest Drake news, music, exclusive photos, videos as well as fantastic products.','05-DEC-10');
insert into Fanclub values (9,'BTS Fanclub','Share and discover content and connect with other fans of the K-pop group BTS.','15-MAY-14');
insert into Fanclub values (10,'MCU Fanclub','The best place to connect with other fans and get news about comics'' greatest super-heroes: Iron Man, Thor, Captain America, the X-Men, and more.','01-APR-15');
insert into Fanclub values (11,'New Kids','Connect with other fans and get news about upcoming concert tours for the group New Kids on the Block.','01-OCT-19');

/********** RegisteredUser table **********/
insert into RegisteredUser values ('adamau','Adam','Au','M','93467812','adamau@nomail.com');
insert into RegisteredUser values ('brianmak','Brian','Mak','M','94467812','brianmak@nomail.com');
insert into RegisteredUser values ('carolchen','Carol','Chen','F','66891204','carolchen@nomail.com');
insert into RegisteredUser values ('fredfan','Fred','Fan','M','93788769','fredfan@nomail.com');
insert into RegisteredUser values ('henryho','Henry','Ho','M','94678835','henryho@nomail.com');
insert into RegisteredUser values ('ireneip','Irene','Ip','F','68340820','ireneip@nomail.com');
insert into RegisteredUser values ('jennyjones','Jenny','Jones','F','99205718','jennyjones@nomail.com');
insert into RegisteredUser values ('kathyko','Kathy','Ko','F','64539876','kathyko@nomail.com');
insert into RegisteredUser values ('larrylai','Larry','Lai','M','69871062','larrylai@nomail.com');
insert into RegisteredUser values ('lesterlo','Lester','Lo','M','93456789','lesterlo@nomail.com');
insert into RegisteredUser values ('monicama','Monica','Ma','F','68741973','monicama@nomail.com');
insert into RegisteredUser values ('peterpoon','Peter','Poon','M','92234876','peterpoon@nomail.com');
insert into RegisteredUser values ('sharonsu','Sharon','Su','F','95567185','sharonsu@nomail.com');
insert into RegisteredUser values ('steviesu','Stevie','Su','F','94701985','steviesu@nomail.com');
insert into RegisteredUser values ('susansze','Susan','Sze','F','90126523','susansze@nomail.com');
insert into RegisteredUser values ('tiffanytan','Tiffany','Tan','F','64458901','tiffanytan@nomail.com');
insert into RegisteredUser values ('tracytse','Tracy','Tse','F','62340751','tracytse@nomail.com');
insert into RegisteredUser values ('victoriayu','Victoria','Yu','F','93467812','victoriayu@nomail.com');
insert into RegisteredUser values ('wendywong','Wendy','Wong','F','98456781','wendywong@nomail.com');
insert into RegisteredUser values ('xavierxie','Xavier','Xie','M','92671073','xavierxie@nomail.com');
insert into RegisteredUser values ('brunoho','Bruno','Ho','M','96752283','brunoho@nomail.com');
insert into RegisteredUser values ('cindychan','Cindy','Chan','F','98126629','cindychan@nomail.com');
insert into RegisteredUser values ('daisyyeung','Daisy','Yeung','F','98230110','daisyyeung@nomail.com');
insert into RegisteredUser values ('frankfung','Frank','Fung','M','96571245','frankfung@nomail.com');
insert into RegisteredUser values ('rezanlim','Rezan','Lim','M','68201835','rezanlim@nomail.com');
insert into RegisteredUser values ('shirleysit','Shirley','Sit','F','63578892','shirleysit@nomail.com');
insert into RegisteredUser values ('terrytam','Terry','Tam','M','69872395','terrytam@nomail.com');
insert into RegisteredUser values ('timothytu','Timothy','Tu','M','66450912','timothytu@nomail.com');
insert into RegisteredUser values ('walterwu','Walter','Wu','M','61904576','walterwu@nomail.com');
insert into RegisteredUser values ('yvonneyu','Yvonne','Yu','F','61276529','yvonneyu@nomail.com');
insert into RegisteredUser values ('zoeymo','Zoey','Mo','F','36921193','zoeymo@nomail.com');

/********** Event table **********/
insert into Event values (5,'Beyonce Photo Session','21-MAY-22','1930','Grand Hyatt Ballroom',25,50,15,'ended','nonmember',2);
insert into Event values (17,'Beyonce Autograph Session','22-JAN-23','1800','Asia World Expo Room 12',0,0,15,'available','member',2);
insert into Event values (13,'Harry Potter Movie Night','20-DEC-22','1930','Premiere Elements VIP House',250,280,10,'available','nonmember',3);
insert into Event values (7,'J.K. Rowling Harry Potter Reading','21-JUN-22','1930','Conrad Hotel Meeting Room 1',20,0,20,'ended','member',3);
insert into Event values (16,'Harry Potter: A History of Magic','20-JAN-23','1400','Hong Kong History Museum',50,60,14,'available','nonmember',3);
insert into Event values (8,'BTS Autograph Session','10-JUL-22','1430','HKCEC Exhibit Room A',10,0,25,'ended','member',3);
insert into Event values (3,'STARFLEET Annual Meeting','27-JAN-22','1900','HKUST - Room 5530',0,0,18,'cancelled','member',2);
insert into Event values (18,'Star Trek Movie Marathon','25-JAN-23','1300','Premiere Elements VIP House',225,250,15,'unavailable','nonmember',2);
insert into Event values (11,'STARFLEET Annual Dress-up Night','01-DEC-22','2000','HKUST - Tsang Shiu Tim Art Hall',50,100,30,'available','nonmember',3);
insert into Event values (1,'Superman Movie Night','10-AUG-22','1800','Premiere Elements VIP House',260,280,15,'ended','nonmember',3);
insert into Event values (9,'Hong Kong Wants Taylor Swift! Fan Project','16-AUG-22','1400','HKCEC Exhibit Room B',0,0,25,'cancelled','nonmember',3);
insert into Event values (14,'Swifters New Year''s Eve Party','31-DEC-22','1900','Grand Hyatt Hotel Ballroom',1000,1500,30,'available','nonmember',3);
insert into Event values (20,'Drake Pre-concert Party','17-MAR-23','1700','SkyCity Marriott Hotel - Meeting Room B',10,0,150,'unavailable','member',2);
insert into Event values (19,'Jay-Z Photo and Autograph Session','30-JAN-23','1300','Grand Hyatt Meeting Room C',0,0,20,'available','member',3);
insert into Event values (2,'Jay-Z Fanclub Party Night','16-SEP-22','2030','Conrad Hotel Ballroom',100,150,60,'ended','nonmember',3);
insert into Event values (4,'MCU Movie Night','24-APR-22','1930','Premiere Elements VIP House',250,300,15,'ended','nonmember',2);
insert into Event values (6,'STARFLEET and MCU Movie Night','01-JUN-22','1900','Premiere Elements VIP House',250,300,13,'ended','nonmember',2);
insert into Event values (15,'OTR IV Pre-concert Party','01-JAN-23','1730','SkyCity Marriott Hotel - Meeting Room A',50,75,25,'available','nonmember',2);
insert into Event values (12,'Superman and MCU Movie Night','10-DEC-22','1900','Premiere Elements VIP House',240,0,10,'available','member',3);
insert into Event values (10,'National Day Gala Concert','01-OCT-23','1900','Queen Elizabeth Stadium',400,500,10000,'available','nonmember',3);

/*********** ClubMember table ***********/
insert into ClubMember values ('adamau','14-FEB-07','student','secondary');
insert into ClubMember values ('brianmak','18-AUG-93','sales rep','secondary');
insert into ClubMember values ('carolchen','18-DEC-06','student','secondary');
insert into ClubMember values ('fredfan','15-AUG-81','construction manager','secondary');
insert into ClubMember values ('henryho','17-MAR-57','retired','post tertiary');
insert into ClubMember values ('ireneip','25-OCT-83','housewife','secondary');
insert into ClubMember values ('jennyjones','24-AUG-90','receptionist','secondary');
insert into ClubMember values ('kathyko','28-JUN-02','student','tertiary');
insert into ClubMember values ('larrylai','11-OCT-71','chief financial officer','tertiary');
insert into ClubMember values ('lesterlo','20-MAR-89','teacher','tertiary');
insert into ClubMember values ('monicama','09-OCT-09','student','primary');
insert into ClubMember values ('peterpoon','05-APR-52','retired','none');
insert into ClubMember values ('rezanlim','25-APR-02','student','none');
insert into ClubMember values ('sharonsu','23-APR-90','executive assistant','tertiary');
insert into ClubMember values ('steviesu','05-NOV-98','student','tertiary');
insert into ClubMember values ('susansze','25-JUN-02','student','secondary');
insert into ClubMember values ('tiffanytan','30-JAN-88','financial analyst','secondary');
insert into ClubMember values ('tracytse','07-MAY-92','accountant','tertiary');
insert into ClubMember values ('victoriayu','19-JUN-06','student','secondary');
insert into ClubMember values ('wendywong','09-FEB-93','house wife','primary');
insert into ClubMember values ('xavierxie','31-JAN-68','sales manager','secondary');
insert into ClubMember values ('zoeymo','31-MAR-81','professor','post tertiary');

/********** MemberOf table **********/
insert into MemberOf values (1,'lesterlo','31-Jul-02','friend');
insert into MemberOf values (1,'larrylai','15-MAR-13','friend');
insert into MemberOf values (1,'susansze','31-MAR-17','web ad');
insert into MemberOf values (1,'brianmak','26-OCT-07','other');
insert into MemberOf values (1,'xavierxie','28-MAR-00','friend');
insert into MemberOf values (1,'ireneip','23-MAY-19','social media');
insert into MemberOf values (1,'adamau','06-OCT-20','social media');
insert into MemberOf values (1,'kathyko','17-SEP-20','social media');
insert into MemberOf values (1,'steviesu','22-JAN-15','social media');
insert into MemberOf values (2,'lesterlo','12-SEP-05','friend');
insert into MemberOf values (2,'peterpoon','08-JAN-14','friend');
insert into MemberOf values (2,'larrylai','14-JUN-08','print ad');
insert into MemberOf values (2,'fredfan','11-JAN-12','web ad');
insert into MemberOf values (2,'brianmak','18-SEP-18','social media');
insert into MemberOf values (2,'xavierxie','08-MAY-90','print ad');
insert into MemberOf values (2,'henryho','25-JUL-02','friend');
insert into MemberOf values (2,'adamau','11-MAY-99','print ad');
insert into MemberOf values (3,'lesterlo','07-NOV-14','friend');
insert into MemberOf values (3,'peterpoon','21-OCT-08','web ad');
insert into MemberOf values (3,'susansze','02-Feb-13','web ad');
insert into MemberOf values (3,'xavierxie','21-AUG-09','web ad');
insert into MemberOf values (4,'lesterlo','18-NOV-17','friend');
insert into MemberOf values (4,'fredfan','18-JUL-14','social media');
insert into MemberOf values (4,'peterpoon','28-FEB-14','friend');
insert into MemberOf values (4,'susansze','17-MAY-18','web ad');
insert into MemberOf values (4,'carolchen','28-FEB-06','other');
insert into MemberOf values (4,'xavierxie','18-AUG-10','social media');
insert into MemberOf values (4,'ireneip','03-JUL-13','social media');
insert into MemberOf values (4,'kathyko','20-MAR-21','social media');
insert into MemberOf values (4,'monicama','10-JUL-09','social media');
insert into MemberOf values (4,'steviesu','19-OCT-16','web ad');
insert into MemberOf values (5,'monicama','10-DEC-19','friend');
insert into MemberOf values (5,'tracytse','02-JUL-18','social media');
insert into MemberOf values (5,'wendywong','17-AUG-17','social media');
insert into MemberOf values (5,'susansze','19-JUL-17','web ad');
insert into MemberOf values (5,'victoriayu','08-MAR-20','friend');
insert into MemberOf values (5,'jennyjones','07-Jan-17','social media');
insert into MemberOf values (5,'sharonsu','23-FEB-17','friend');
insert into MemberOf values (5,'carolchen','29-NOV-17','other');
insert into MemberOf values (5,'ireneip','16-MAY-19','print ad');
insert into MemberOf values (5,'steviesu','17-JUL-20','print ad');
insert into MemberOf values (6,'lesterlo','10-OCT-09','friend');
insert into MemberOf values (6,'fredfan','17-MAY-14','social media');
insert into MemberOf values (6,'henryho','07-OCT-13','other');
insert into MemberOf values (6,'peterpoon','10-AUG-14','friend');
insert into MemberOf values (6,'tracytse','06-JUN-19','social media');
insert into MemberOf values (6,'susansze','19-JUL-17','web ad');
insert into MemberOf values (6,'victoriayu','21-SEP-19','web ad');
insert into MemberOf values (6,'brianmak','14-FEB-19','web ad');
insert into MemberOf values (6,'carolchen','22-MAR-09','web ad');
insert into MemberOf values (6,'xavierxie','31-MAR-10','print ad');
insert into MemberOf values (6,'ireneip','15-JUL-19','social media');
insert into MemberOf values (6,'adamau','15-OCT-19','social media');
insert into MemberOf values (6,'kathyko','23-NOV-17','print ad');
insert into MemberOf values (6,'monicama','30-SEP-20','social media');
insert into MemberOf values (6,'steviesu','13-MAY-21','social media');
insert into MemberOf values (7,'lesterlo','22-MAY-16','other');
insert into MemberOf values (7,'fredfan','16-JUN-10','friend');
insert into MemberOf values (7,'peterpoon','19-NOV-14','friend');
insert into MemberOf values (7,'tracytse','27-AUG-12','social media');
insert into MemberOf values (7,'susansze','12-FEB-16','print ad');
insert into MemberOf values (7,'xavierxie','18-JUL-10','web ad');
insert into MemberOf values (7,'kathyko','09-MAY-21','print ad');
insert into MemberOf values (7,'steviesu','01-DEC-18','print ad');
insert into MemberOf values (8,'lesterlo','14-FEB-14','social media');
insert into MemberOf values (8,'fredfan','17-MAY-14','social media');
insert into MemberOf values (8,'henryho','20-MAR-12','other');
insert into MemberOf values (8,'peterpoon','21-MAY-14','print ad');
insert into MemberOf values (8,'tracytse','28-SEP-18','friend');
insert into MemberOf values (8,'wendywong','03-DEC-17','web ad');
insert into MemberOf values (8,'susansze','22-JUL-13','friend');
insert into MemberOf values (8,'tiffanytan','03-JAN-17','friend');
insert into MemberOf values (8,'xavierxie','17-MAY-14','web ad');
insert into MemberOf values (8,'ireneip','12-OCT-17','friend');
insert into MemberOf values (8,'kathyko','24-APR-19','social media');
insert into MemberOf values (8,'steviesu','12-AUG-17','web ad');
insert into MemberOf values (9,'lesterlo','11-JUL-16','social media');
insert into MemberOf values (9,'fredfan','11-FEB-18','web ad');
insert into MemberOf values (9,'henryho','04-SEP-16','other');
insert into MemberOf values (9,'peterpoon','13-APR-19','friend');
insert into MemberOf values (9,'wendywong','10-DEC-16','web ad');
insert into MemberOf values (9,'susansze','21-SEP-17','social media');
insert into MemberOf values (9,'brianmak','24-JAN-17','social media');
insert into MemberOf values (9,'xavierxie','07-JAN-20','friend');
insert into MemberOf values (9,'sharonsu','25-DEC-18','social media');
insert into MemberOf values (9,'ireneip','07-NOV-16','social media');
insert into MemberOf values (9,'adamau','08-NOV-16','friend');
insert into MemberOf values (9,'kathyko','20-OCT-17','other');
insert into MemberOf values (9,'steviesu','27-SEP-19','friend');
insert into MemberOf values (10,'lesterlo','28-MAR-19','web ad');
insert into MemberOf values (10,'fredfan','02-OCT-18','other');
insert into MemberOf values (10,'peterpoon','12-JAN-16','friend');
insert into MemberOf values (10,'tracytse','30-JUN-19','friend');
insert into MemberOf values (10,'susansze','13-APR-16','social media');
insert into MemberOf values (10,'carolchen','19-AUG-17','social media');
insert into MemberOf values (10,'xavierxie','08-JUN-20','print ad');
insert into MemberOf values (10,'ireneip','17-APR-20','friend');
insert into MemberOf values (10,'kathyko','20-MAR-21','social media');
insert into MemberOf values (10,'steviesu','19-OCT-17','other');

/********** Remark table **********/
insert into Remark values (1,'Concert please!','We need a BTS concert in Hong Kong.','09-JUN-21',null,null,'club',9,'susansze',null);
insert into Remark values (2,'More members needed','The club is in serious need of more members.','30-MAY-21','done','Organizing membership drive.','club',3,'susansze',2);
insert into Remark values (3,'Useless club','What good is a club that hosts no events?','10-DEC-20','read',null,'club',1,'brianmak',3);
insert into Remark values (4,'No events?','Why are we not having any events?','08-JUL-21','read',null,'club',1,'susansze',null);
insert into Remark values (5,'Events needed!','This fan club needs to have some events or I will leave it!','10-JUL-21','processing',null,'club',1,'susansze',2);
insert into Remark values (6,'Why no events?','I am still waiting for this fan club to have some events!','15-NOV-20',null,null,'club',1,'susansze',null);
insert into Remark values (7,'No club events!','Can this club please have some events?','10-APR-21','done','Organizing events.','club',1,'lesterlo',2);
insert into Remark values (8,'Club events?','Can we have a reading event?','10-JUN-21',null,null,'club',1,'adamau',null);
insert into Remark values (9,'Taylor Swift in Hong Kong','Can we please have a Taylor Swift concert in Hong Kong soon!','30-JUN-21',null,null,'club',7,'susansze',null);
insert into Remark values (10,'More movie nights','Can there be more movie nights?','20-JUN-21','read',null,'club',10,'carolchen',3);
insert into Remark values (11,'Not enough quota','Can more quota be added for such events in future?','10-DEC-20','processing','Noted for future events.','event',5,'kathyko',3);
insert into Remark values (12,'Venue too small','The venue for the photo session was not large enough to accommodate all those attending.','10-FEB-21','read',null,'event',5,'peterpoon',2);
insert into Remark values (13,'Terrible venue','The venue for the photo session was too small and the session was badly run.','05-FEB-21',null,null,'event',5,'kathyko',null);
insert into Remark values (14,'Chaotic session!','The photo session was not well organized.','10-FEB-21',null,'read','event',5,'kathyko',null);
insert into Remark values (15,'Need new organizer','The photo session organizer is completely incompetent!','12-FEB-21',null,null,'event',5,'peterpoon',null);
insert into Remark values (16,'More like this','Can we have more events like this?','13-FEB-21','done',null,'event',1,'cindychan',2);
insert into Remark values (17,'Theatre too cold!','The theatre was way too cold. Please fix for future events.','02-FEB-21',null,null,'event',1,'cindychan',null);
insert into Remark values (18,'Great movie night','The movie night was well organized.','12-FEB-21','done',null,'event',1,'cindychan',2);
insert into Remark values (19,'Another movie night','When is the next Superman movie night?','05-OCT-20',null,null,'event',1,'tiffanytan',null);
insert into Remark values (20,'Waiting','Expectantly waiting for the next movie night.','12-DEC-20',null,null,'event',1,'larrylai',null);
insert into Remark values (21,'Can''t wait','Looking forward to attending the concert.','12-JUL-21',null,null,'event',14,'kathyko',null);
insert into Remark values (22,'Next concert','When will we see BTS again in Hong Kong?','15-JUL-21',null,null,'event',8,'kathyko',null);

/********** Hosts table **********/
insert into Hosts values (6,5);
insert into Hosts values (6,17);
insert into Hosts values (5,13);
insert into Hosts values (5,7);
insert into Hosts values (5,16);
insert into Hosts values (9,8);
insert into Hosts values (2,3);
insert into Hosts values (2,18);
insert into Hosts values (2,11);
insert into Hosts values (3,1);
insert into Hosts values (7,9);
insert into Hosts values (7,14);
insert into Hosts values (8,20);
insert into Hosts values (4,19);
insert into Hosts values (4,2);
insert into Hosts values (10,4);
insert into Hosts values (2,6);
insert into Hosts values (10,6);
insert into Hosts values (6,15);
insert into Hosts values (4,15);
insert into Hosts values (3,12);
insert into Hosts values (10,12);
insert into Hosts values (6,10);
insert into Hosts values (7,10);
insert into Hosts values (4,10);

/********** RegistersFor table **********/
insert into RegistersFor values (1,'cindychan','Y','Y');
insert into RegistersFor values (1,'fredfan','Y','Y');
insert into RegistersFor values (1,'larrylai','Y','Y');
insert into RegistersFor values (1,'steviesu','Y','Y');
insert into RegistersFor values (1,'tiffanytan','Y','Y');
insert into RegistersFor values (1,'tracytse','Y','Y');
insert into RegistersFor values (1,'yvonneyu','Y','Y');
insert into RegistersFor values (2,'daisyyeung','Y','Y');
insert into RegistersFor values (2,'lesterlo','Y','N');
insert into RegistersFor values (2,'henryho','Y','Y');
insert into RegistersFor values (2,'peterpoon','Y','Y');
insert into RegistersFor values (3,'brianmak','N',null);
insert into RegistersFor values (3,'adamau','N',null);
insert into RegistersFor values (3,'lesterlo','N',null);
insert into RegistersFor values (3,'peterpoon','N',null);
insert into RegistersFor values (3,'fredfan','N',null);
insert into RegistersFor values (3,'xavierxie','N',null);
insert into RegistersFor values (4,'carolchen','Y','Y');
insert into RegistersFor values (4,'fredfan','N','Y');
insert into RegistersFor values (4,'lesterlo','Y','Y');
insert into RegistersFor values (5,'brianmak','N','N');
insert into RegistersFor values (5,'cindychan','Y','Y');
insert into RegistersFor values (5,'daisyyeung','Y','Y');
insert into RegistersFor values (5,'fredfan','Y','Y');
insert into RegistersFor values (5,'ireneip','N','N');
insert into RegistersFor values (5,'jennyjones','Y','Y');
insert into RegistersFor values (5,'lesterlo','Y','Y');
insert into RegistersFor values (5,'peterpoon','Y','Y');
insert into RegistersFor values (5,'sharonsu','Y','Y');
insert into RegistersFor values (5,'susansze','Y','Y');
insert into RegistersFor values (5,'timothytu','Y','Y');
insert into RegistersFor values (5,'tracytse','Y','Y');
insert into RegistersFor values (5,'victoriayu','Y','Y');
insert into RegistersFor values (5,'wendywong','N','N');
insert into RegistersFor values (5,'yvonneyu','Y','Y');
insert into RegistersFor values (6,'carolchen','Y','Y');
insert into RegistersFor values (6,'daisyyeung','Y','Y');
insert into RegistersFor values (6,'fredfan','Y','N');
insert into RegistersFor values (6,'henryho','Y','Y');
insert into RegistersFor values (6,'ireneip','Y','N');
insert into RegistersFor values (6,'lesterlo','Y','Y');
insert into RegistersFor values (6,'sharonsu','Y','N');
insert into RegistersFor values (6,'susansze','Y','Y');
insert into RegistersFor values (6,'tracytse','Y','Y');
insert into RegistersFor values (6,'victoriayu','Y','Y');
insert into RegistersFor values (6,'wendywong','Y','Y');
insert into RegistersFor values (6,'xavierxie','Y','Y');
insert into RegistersFor values (6,'yvonneyu','Y','Y');
insert into RegistersFor values (7,'carolchen','Y','Y');
insert into RegistersFor values (7,'ireneip','Y','Y');
insert into RegistersFor values (7,'jennyjones','Y','N');
insert into RegistersFor values (7,'sharonsu','Y','Y');
insert into RegistersFor values (7,'susansze','Y','Y');
insert into RegistersFor values (7,'tracytse','Y','N');
insert into RegistersFor values (7,'victoriayu','Y','Y');
insert into RegistersFor values (7,'wendywong','Y','N');
insert into RegistersFor values (8,'brianmak','Y','Y');
insert into RegistersFor values (8,'henryho','Y','Y');
insert into RegistersFor values (8,'lesterlo','Y','Y');
insert into RegistersFor values (8,'sharonsu','Y','Y');
insert into RegistersFor values (8,'susansze','Y','Y');
insert into RegistersFor values (8,'wendywong','Y','Y');
insert into RegistersFor values (8,'xavierxie','Y','Y');
insert into RegistersFor values (9,'frankfung','N',null);
insert into RegistersFor values (9,'jennyjones','N',null);
insert into RegistersFor values (9,'lesterlo','N',null);
insert into RegistersFor values (9,'peterpoon','N',null);
insert into RegistersFor values (9,'shirleysit','N',null);
insert into RegistersFor values (11,'daisyyeung','Y',null);
insert into RegistersFor values (11,'frankfung','Y',null);
insert into RegistersFor values (11,'jennyjones','Y',null);
insert into RegistersFor values (11,'terrytam','N',null);
insert into RegistersFor values (11,'timothytu','Y',null);
insert into RegistersFor values (12,'carolchen','N',null);
insert into RegistersFor values (12,'fredfan','N',null);
insert into RegistersFor values (12,'ireneip','Y',null);
insert into RegistersFor values (12,'lesterlo','Y',null);
insert into RegistersFor values (12,'peterpoon','Y',null);
insert into RegistersFor values (12,'steviesu','N',null);
insert into RegistersFor values (12,'susansze','N',null);
insert into RegistersFor values (12,'tracytse','Y',null);
insert into RegistersFor values (12,'xavierxie','Y',null);
insert into RegistersFor values (13,'frankfung','Y',null);
insert into RegistersFor values (13,'henryho','Y',null);
insert into RegistersFor values (13,'lesterlo','Y',null);
insert into RegistersFor values (13,'shirleysit','N',null);
insert into RegistersFor values (13,'terrytam','N',null);
insert into RegistersFor values (13,'tiffanytan','Y',null);
insert into RegistersFor values (13,'timothytu','N',null);
insert into RegistersFor values (13,'victoriayu','Y',null);
insert into RegistersFor values (14,'adamau','Y',null);
insert into RegistersFor values (14,'brianmak','N',null);
insert into RegistersFor values (14,'carolchen','Y',null);
insert into RegistersFor values (14,'fredfan','Y',null);
insert into RegistersFor values (14,'henryho','Y',null);
insert into RegistersFor values (14,'ireneip','N',null);
insert into RegistersFor values (14,'jennyjones','Y',null);
insert into RegistersFor values (14,'kathyko','Y',null);
insert into RegistersFor values (14,'larrylai','N',null);
insert into RegistersFor values (14,'lesterlo','Y',null);
insert into RegistersFor values (14,'monicama','N',null);
insert into RegistersFor values (14,'peterpoon','N',null);
insert into RegistersFor values (14,'sharonsu','Y',null);
insert into RegistersFor values (14,'steviesu','Y',null);
insert into RegistersFor values (14,'susansze','Y',null);
insert into RegistersFor values (14,'tiffanytan','Y',null);
insert into RegistersFor values (14,'tracytse','N',null);
insert into RegistersFor values (14,'victoriayu','Y',null);
insert into RegistersFor values (14,'wendywong','Y',null);
insert into RegistersFor values (14,'xavierxie','Y',null);
insert into RegistersFor values (14,'cindychan','Y',null);
insert into RegistersFor values (14,'daisyyeung','Y',null);
insert into RegistersFor values (14,'frankfung','N',null);
insert into RegistersFor values (14,'rezanlim','N',null);
insert into RegistersFor values (14,'shirleysit','Y',null);
insert into RegistersFor values (14,'terrytam','N',null);
insert into RegistersFor values (14,'timothytu','N',null);
insert into RegistersFor values (14,'walterwu','Y',null);
insert into RegistersFor values (14,'yvonneyu','N',null);
insert into RegistersFor values (15,'brianmak','Y',null);
insert into RegistersFor values (15,'cindychan','N',null);
insert into RegistersFor values (15,'frankfung','Y',null);
insert into RegistersFor values (15,'fredfan','Y',null);
insert into RegistersFor values (15,'henryho','Y',null);
insert into RegistersFor values (15,'lesterlo','Y',null);
insert into RegistersFor values (15,'peterpoon','Y',null);
insert into RegistersFor values (15,'sharonsu','N',null);
insert into RegistersFor values (15,'susansze','Y',null);
insert into RegistersFor values (15,'terrytam','N',null);
insert into RegistersFor values (16,'carolchen','Y',null);
insert into RegistersFor values (16,'henryho','Y',null);
insert into RegistersFor values (16,'ireneip','Y',null);
insert into RegistersFor values (16,'jennyjones','Y',null);
insert into RegistersFor values (16,'lesterlo','N',null);
insert into RegistersFor values (16,'monicama','Y',null);
insert into RegistersFor values (16,'peterpoon','N',null);
insert into RegistersFor values (16,'sharonsu','Y',null);
insert into RegistersFor values (16,'steviesu','Y',null);
insert into RegistersFor values (16,'susansze','Y',null);
insert into RegistersFor values (16,'tracytse','Y',null);
insert into RegistersFor values (16,'victoriayu','Y',null);
insert into RegistersFor values (16,'wendywong','Y',null);
insert into RegistersFor values (17,'carolchen','N',null);
insert into RegistersFor values (17,'fredfan','N',null);
insert into RegistersFor values (17,'henryho','Y',null);
insert into RegistersFor values (17,'ireneip','Y',null);
insert into RegistersFor values (17,'lesterlo','Y',null);
insert into RegistersFor values (17,'peterpoon','Y',null);
insert into RegistersFor values (17,'susansze','Y',null);
insert into RegistersFor values (17,'tracytse','N',null);
insert into RegistersFor values (17,'xavierxie','Y',null);

commit;