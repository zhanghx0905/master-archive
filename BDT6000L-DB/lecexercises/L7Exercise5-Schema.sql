/* MSBD 6000L: Exercise8-Schema.sql */

create table Department (
	departmentId    char(4) primary key
		check (departmentId in ('BUS', 'COMP', 'ELEC', 'HUMA', 'MATH')),
	departmentName  varchar2(40) not null,
	roomNo          char(4)
);

create table Student (
	studentId       char(8) primary key,
	firstName       varchar2(20) not null,
	lastName        varchar2(25) not null,
	email           varchar2(15) not null unique,
	phoneNo         char(8),
	cga             number(3,2) check (cga between 0 and 4),
	departmentId    char(4) not null,
	admissionYear   char(4) not null,
	foreign key (departmentId) references Department(departmentId)
		on delete cascade
);

create table Course (
	courseId        char(8) primary key,
	departmentId    char(4) not null,
	courseName     varchar2(40) not null,
	instructor      varchar2(30) not null,
	foreign key (departmentId) references Department(departmentId)
		on delete cascade
);

create table EnrollsIn (
 	studentId   char(8),
	courseId    char(8),
	grade       number(4,1) check (grade between 0 and 100),
	primary key (studentId, courseId),
	foreign key (studentId) references Student(studentId)
		on delete cascade,
	foreign key (courseId) references Course(courseId)
		on delete cascade
);

create table Facility ( 
	departmentId        char(4) primary key,
	numberProjectors    int default 0,
	numberComputers     int default 0,
	foreign key (departmentId) references Department(departmentId)
		on delete cascade
);