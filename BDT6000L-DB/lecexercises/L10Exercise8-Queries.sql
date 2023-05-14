/* MSBD 6000L: L10Exercise8-Queries.sql */

/**********************************************************/
/*** Use only SQL constructs discussed in the lectures. ***/
/***  Your submission will be run in Oracle Database.   ***/
/*** If there are any syntax errors in your submission, ***/
/***         your grade will be at most 0.5.           ***/
/*********************************************************/

/***********************************************************/
/*** 1. Drop all tables, views and triggers.             ***/
/*** 2. Run the script files L10Exercise8-Schema.sql and ***/
/***    L10Exercise8-Data.sql                            ***/
/***********************************************************/


/* Create View: Create a view named HonorsStudent based on the Student relation that
				includes the student id, first name, last name and total credits 
				and that contains only those students whose cga is greater than 
				or equal to 3 and who have a total credit load of at least 12. */
-- ↓↓↓↓↓ Place the HonorsStudent view statements below this line ↓↓↓↓↓

create view HonorsStudent as 
select studentId, firstName, lastName, totalCredits
-- select * 
from Student
where cga >= 3 and totalCredits >= 12;


/***************************************************************************/
/* To test the view, run a select statement using the view after creating  */
/* the following trigger and running the script file L10Exercise8-Data.sql */
/***************************************************************************/

/* Create Trigger:  Create a trigger named IncreaseTotalCredits that will update 
                    the attribute totalCredits in the Student relation whenever
                    an EnrollsIn tuple is inserted for a student. */
-- ↓↓↓↓↓ Place the IncreaseTotalCredits trigger statements below this line ↓↓↓↓↓

create trigger IncreaseTotalCredits after insert on EnrollsIn 
for each row BEGIN
        update Student
        set totalCredits = totalCredits + (
                select credits
                from course
                where courseId = :new.courseId
            )
        where studentId = :new.studentId;
END;

-- ↑↑↑↑↑ Place the IncreaseTotalCredits trigger statements above this line ↑↑↑↑↑
-- DO NOT delete the next line.
/


/*****************************************************************/
/* To test the trigger run the script file L10Exercise8-Data.sql */
/*****************************************************************/

/* Query 1: Find, for each course, the course name, student last name, student
            first name and cga of the honors students enrolled in the course. 
            Use the HonorsStudent view created above to answer this query. 
            Order the result first by course name and then by student last name. */
-- ↓↓↓↓↓ Place Query 1 below this line ↓↓↓↓↓


select courseName, lastName, firstName
from HonorsStudent natural join EnrollsIn natural join (
    select courseName, courseId from Course
)
order by courseName, lastName;


/* Query 2: Find the name of the department that offers the most courses. */
-- ↓↓↓↓↓ Place Query 2 below this line ↓↓↓↓↓

with DepCourses(depId, depName, cnt) as (
    select departmentId, departmentName, count(*)
    from Course natural join Department
    group by departmentId, departmentName
)
select depName
from DepCourses
where
    cnt = (
        select max(cnt)
        from depCourses
    );

/* Query 3: Find, for each course, the course id and name, student last name, first
            name and grade of the students who have the highest grade in the course. 
			Order the result first by course id and then by student last name. */
-- ↓↓↓↓↓ Place Query 3 below this line ↓↓↓↓↓

with StuCourse as (
    select *
    from Student natural join EnrollsIn natural join (
            select courseName, courseId from Course
        )
)
select courseId, courseName, lastName, firstName, grade
from StuCourse S
where grade = (
        select max(grade)
        from EnrollsIn E
        where E.courseId = S.courseId
    )
order by courseId, lastName;

/* Query 4: Find the last and first name of the students who are enrolled in every 
			course. Order the result by student last name. */
-- ↓↓↓↓↓ Place Query 4 below this line ↓↓↓↓↓

select lastName, firstName
from Student
where totalCredits = (
    select sum(credits) 
    from Course
)
order by lastName;
