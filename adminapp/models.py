from django.db import models
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

import pandas as pd



class Room(models.Model):
    room_number = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.room_number

    class Meta:
        db_table = 'Rooms'

class AddTimeTable(models.Model):
    subject = models.CharField(max_length=100)
    iv_cse_a_faculty = models.CharField(max_length=100, verbose_name='CSE A Faculty' ,default="Prabhakara Rao")
    iv_cse_b_faculty = models.CharField(max_length=100, verbose_name='CSE B Faculty',default="Akhila")
    iv_cse_c_faculty = models.CharField(max_length=100, verbose_name='CSE C Faculty',default="SriLatha")

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'AddTimeTable'


class AddStudent(models.Model):
    rollnumber = models.CharField(null=True, max_length=50, unique=True)
    name = models.CharField(null=True, max_length=50)
    department = models.CharField(null=True, max_length=100)
    email = models.EmailField(null=True, max_length=100)
    contact = models.CharField(null=True, max_length=10)
    year = models.IntegerField(null=True)
    semester = models.IntegerField(null=True)
    profile_url = models.URLField(null=True, max_length=200)
    password = models.CharField(max_length=20, null=True)
    class Meta:
        db_table = "AddStudent"

    @classmethod
    def create_from_excel(cls, excel_file):
        if excel_file.name.endswith('.xlsx'):
            # Read the Excel file into a DataFrame
            df = pd.read_excel(excel_file)
            
            # Preprocess the 'Contact' column: convert to string and remove leading/trailing spaces
            df['Contact'] = df['Contact'].apply(lambda x: str(x).strip())
            
            # Iterate over rows in the DataFrame
            for index, row in df.iterrows():
                rollnumber = str(row['Roll.No'])  # Assuming Roll Number is in the 'Roll Number' column
                name = row['Student Name']  # Assuming Student Name is in the 'Student Name' column
                department = row['Department']  # Assuming Department is in the 'Department' column
                email = row['Email']  # Assuming Email is in the 'Email' column
                contact = str(int(row['Contact']))  # Convert contact to string without decimal
                year = row['Year']  # Assuming Year is in the 'Year' column
                semester = row['Semester']  # Assuming Semester is in the 'Semester' column

                # Create a new student instance
                student = cls(
                    roll_number=rollnumber,
                    name=name,
                    department=department,
                    email=email,
                    contact=contact,
                    year=year,
                    semester=semester
                )
                
                # Save the student instance to the database
                student.save()

        else:
            raise ValueError("Please upload a valid Excel file.")

class AdminAnnounce(models.Model):
    announcement = models.TextField(null=True)
    senderemail = models.EmailField(null=True)
    annuncementdate = models.DateField(default=timezone.now)


    class Meta:
        db_table = "Announcement"

# adminapp/models.py
class AddexamHall(models.Model):
    date = models.DateField(null=True)
    noofrooms = models.PositiveIntegerField(null=True)
    noofbenches = models.PositiveIntegerField(null=True)
    total_benches = models.PositiveIntegerField(null=True)
    total_seats = models.PositiveIntegerField(null=True)
    rooms_list = models.CharField(max_length=255, null=True)

    STUDENTS_PER_BENCH_CHOICES = [(2, 'Two students per bench'), (3, 'Three students per bench')]
    students_per_bench = models.IntegerField(choices=STUDENTS_PER_BENCH_CHOICES, null=True)

    # ✅ These two lines should be present:
    subject1 = models.CharField(max_length=100, null=True, blank=True)
    subject2 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "AddexamHall"



class Examallotment(models.Model):
    department = models.CharField(max_length=50, null=True)
    RoomNo = models.CharField(max_length=20, null=True)
    BenchNo = models.CharField(max_length=20, null=True)
    SeatNumber = models.CharField(max_length=20, null=True)
    Student_Id = models.CharField(null=True, max_length=20)
    date = models.DateField(null=True)
    starttime = models.TimeField(null=True)
    endtime = models.TimeField(null=True)


    class Meta:
        db_table = "Examallotment"
    

class AddFaculty(models.Model):
    name = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=10, null=True)
    contact = models.CharField(max_length=10, null=True)
    branch = models.CharField(max_length=10, null=True)
    subject = models.CharField(max_length=10, null=True)
    semester = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    image = models.FileField(
        upload_to=os.path.join("static", "faculty"))
    profilename = models.CharField(null=True, max_length=50)
    password = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "Addfaculty"

