"""
    This module handles the models for incidents
"""
import json
import datetime
import psycopg2
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel
from app.api.v2.models.users import UserModel



class IncidentsModel(DbModel):
    """
        This class handles data for the redflags views
    """
    def __init__(self, record_type=None,location=None, status=None,
                images=None, video=None, title=None, comment=None, createdBy=None):
        super().__init__('main')
        self.createdOn = datetime.datetime.now()
        self.modifiedOn = datetime.datetime.now()
        self.record_type = record_type
        self.location = location
        self.status = status
        self.images = images
        self.video = video
        self.title = title
        self.comment = comment
        self.createdBy = self.current_user()


   

    
    def find_incident_by_comment(self, comment):
        """ gets an incident from comment"""
        try:
            self.cur.execute(
                "SELECT * FROM incidents WHERE comment=%s", (comment,)
                )
            comment = self.findOne()
            print(comment)
            return comment
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        
    def find_incident_id(self,comment):
        """ Finds the id of the posted incident"""
        try:
            self.cur.execute(
                "SELECT incident_id FROM incidents WHERE comment=%s", (comment,)
                )
            incident_id = self.findOne().get('incident_id')
            print(incident_id)
            return incident_id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def post_incident(self):
        """
            This method saves an incident to the database
        """
        try:
            data =( self.record_type, self.location, self.images, self.video, self.title, self.comment, self.createdBy, self.createdOn,self.modifiedOn )
            
            self.cur.execute(
                """
                    INSERT INTO incidents (record_type, location, images, video, title, comment, createdBy, createdOn, modifiedOn)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            print('success')
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('could not save to db')

    def get_all_incidents(self):
        """
            This method returns all the posted incidents
        """
        try:
            self.cur.execute(
                "SELECT * FROM incidents"
            )
            data = self.findAll()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
       
    def get_incident_by_id(self, id):
        """
            This method retrieves an incident by id from the database.
            It takes the id of the incident as parameter and
            It returns the incident as a result
        """
        try:
            self.cur.execute(
                "SELECT * FROM incidents WHERE incident_id=%s", (id,)
                )
            incident = self.findOne()
            return incident
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None


    def edit_incident(self, id):
        """
            This method can modify one or all the fields of an incident
            It takes the id of the incident as the parameter and,
            It returns the updated incident as a result.
        """
        pass

    def delete_incident(self, incident_id):
        """ 
            This method removes an incident by id from the database.
            It takes an id of the incident as parameter and,
            It returns the list of incidents.
        """
        try:
            self.cur.execute(
                "DELETE FROM incidents WHERE incident_id=%s", (incident_id,)
                )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def edit_incident_comment(self, comment, incident_id):
        """
            This method modifies the description field of an incident.
            It takes an id as parameter and,
            It returns The updated incident as a result.
            
        """
        try:
            print('print something')
            self.cur.execute(
                """
                UPDATE incidents
                SET comment = %s
                WHERE incident_id = %s;
                """, (comment, incident_id)
                )
            self.commit()
            print("Print comment")
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def edit_location(self, id):
        """
            This method modifies the location field of an incident.
            It takes an id as the parameter.
            It returns the updated incident.
        """
        return None

    def upload_image(self, id):
        """
            This method posts an image or images to the database
        """
        pass

    def upload_video(self, id):
        """
            This method posts a video or videos to the database.
        """
        pass

    def current_user(self):
        """
            This method gets the logged in user from jwt token.
            It returns the username.
        """
        username = get_jwt_identity()
        return username
