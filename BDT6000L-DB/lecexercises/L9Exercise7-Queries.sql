/* MSBD 6000L: L9Exercise7-Queries-Solution.sql */

/**********************************************************/
/*** Use only SQL constructs discussed in the lectures. ***/
/***  Your submission will be run in Oracle Database.   ***/
/*** If there are any syntax errors in your submission, ***/
/***         your grade will be at most 0.5.            ***/
/**********************************************************/

/* Query 1: Find the minimum, maximum, average and total number of computers  
			over all departments. */
-- ↓↓↓↓↓ Construct Query 1 below this line ↓↓↓↓↓

select
	min(numberComputers) "MINIMUM",
	max(numberComputers) "MAXIMUM",
	avg(numberComputers) "AVERAGE",
	sum(numberComputers) "TOTAL"
from Department natural join Facility;

/* Query 2: Find, for each course, the course id and the average cga of the students 
			enrolled in the course. Order the result by average cga descending. */
-- ↓↓↓↓↓ Construct Query 2 below this line ↓↓↓↓↓

select courseId, trunc(avg(cga), 2) "AVG CGA"
from Student natural join EnrollsIn
group by courseId
order by avg(cga) desc;

/* Query 3: Find, for each course, the course id, student last and first name, 
			department id and cga of the students who have the highest cga  
			and the students who have the lowest in the course. Order the  
			result first by course id ascending and then by cga descending. */
-- ↓↓↓↓↓ Construct Query 3 below this line ↓↓↓↓↓

with StuEnrolls as (
	select * from Student natural join EnrollsIn
)
select courseId, lastName, firstName, departmentId, cga
from StuEnrolls S1
where cga in (
		select min(cga) from StuEnrolls S2
		where S1.courseId = S2.courseId
		union
		select max(cga) from StuEnrolls S2
		where S1.courseId = S2.courseId
	)
order by courseId, cga desc;

/* Query 4: Find, for each student enrolled in the COMP department, the first name, 
			last name and the number of courses in which the student is enrolled. 
			Order the result first by the number of courses descending and second 
			by last name ascending. If a student is not enrolled in any course the 
			number of enrolled courses should be shown a 0 not as null. */
-- ↓↓↓↓↓ Construct Query 4 below this line ↓↓↓↓↓

select firstName, lastName, count(courseId) "NUMBER OF COURSES"
from Student natural left outer join EnrollsIn
where departmentId = 'COMP'
group by studentId, firstName, lastName
order by count(courseId) desc, lastName;

/* Query 5: Find the first and last name of the students who have the highest cga  
			and also find the name, id and grade of the courses in which they 
			had the highest grade. */
-- ↓↓↓↓↓ Construct Query 5 below this line ↓↓↓↓↓

with TopStuCourse as (
	select * from
	Student natural join EnrollsIn natural join (
			select courseName, courseId from Course
		)
	where cga = (
			select max(cga) from Student
		)
)
select firstName, lastName, courseName, courseId, grade
from TopStuCourse S
where grade = (
		select max(grade) from EnrollsIn E
		where E.courseId = S.courseId
	)
