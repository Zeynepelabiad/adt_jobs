# adt_jobs
Summary:
The web application provides a list of available data science jobs for people looking for jobs in the data science field from 13 states, which have the most available data science jobs in the US. The states are California, Virginia, New York, Texas, Florida, Ohio, Pennsylvania, Illinois, North Carolina, Georgia, Massachusetts, Michigan, and Washington. 

Data: The latest available data science jobs from 13 selected states were scraped from the Glassdoor website using Beautiful Soup. The data has six columns and 654 rows. The columns are publishing date, Estimated salary range, Location, Job Title, Company, and Company score for each job. I used MySQL database to store the data.

User Functionalities:
Only authorized users in the database can do CRUD operations on the web application. 
The admin user can add a new job and edit or remove a record. 
Normal users can select a specific state and view the available jobs in their preferred state. They can also view the available visualization from the visualization page.

Reference

1) https://www.glassdoor.com
2) https://www.tutorialspoint.com/flask/index.htm
3) https://youtu.be/Pu9XhFJduEw
4) https://stackoverflow.com/questions/5440657/how-to-hide-columns-in-html-table
5) https://www.askpython.com/python-modules/flask/flask-mysql-database
6) https://getbootstrap.com
7) https://flask-mysql.readthedocs.io/en/stable/
