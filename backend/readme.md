## Assignment Task backend

# # Steps for setup
- Create a virtual Environment using command `python3 -m venv env`
- Activate virtual Environment using command `source env/bin/activate`
- Clone Repository using command `git clone https://github.com/Business-Dev43/assignment_task.git`
- Select project folder using command `cd assignment_task/backend/asssignment_task`
- Install pip `sudo apt install python3-pip`
- Install all the dependencies from requirements.txt using command  `pip install -r requirements.txt`
- Check any packages that are not installed due to version issue
- Make migrations using command  `python manage.py makemigrations`
- Migrate all the changes using command `python manage.py migrate`
- Run the project using command `python manage.py runserver`

# # Test case
- For run test cases using command `python manage.py test`
