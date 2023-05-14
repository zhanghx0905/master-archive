/* MSBD 6000L Lecture 8 Exercise7 */

/* Query 1:	Query 1: Find the student id, first name, last name, email and cga of the students who 
			are not in the COMP or BUS departments. Order the result from highest to lowest cga. */
-- ***** Construct Query 1 below this line *****

select studentId "Id", firstName "First name", lastName "Last name", email "Email", cga 
from Student
where departmentId not in ('COMP', 'BUS')
order by cga desc;

/* Query 2: Find the first name of the students whose first name
			contains the letter "b" as the 3rd character. */
-- ***** Construct Query 2 below this line *****

select firstName from Student
where firstName like '__b%';

/* Query 3:	Find the last name of the students whose last name
			contains either the letter "c" or the letter "z". */
-- ***** Construct Query 3 below this line *****

select lastName from Student
where regexp_like(lastName, '(c|z)');


/* Query 4: Find the last name, first name and cga of the students 
			who have the three lowest cgas. */
-- ***** Construct Query 4 below this line *****

select lastName, firstName, cga 
from Student
order by cga
fetch first 3 rows only;

/* Query 5: Find the student id, first name, last name, cga and department name of
			the students who are in the COMP or the ELEC department and whose CGA
			is not in the range 2.5 to 3.5. Order the result by last name ascending. */
-- ***** Construct Query 5 below this line *****

select studentId, firstName, lastName, cga, departmentName
from (
	select * from Student
	where cga not between 2.5 and 3.5
)  NATURAL JOIN (
	select departmentId, departmentName
	from Department 
	where departmentId in ('COMP', 'ELEC')
)
order by lastName;