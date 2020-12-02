from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .serializers import *
from .models import *
from bs4 import BeautifulSoup as bs4
import sqlite3
import os
import subprocess
from multiprocessing import Pool
import requests
import json

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreatUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) <= 4:
            body = {"message": "아이디는 4글자 이상이여야 합니다."}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        
        if len(request.data["password"]) <= 8:
            body = {"message": "비밀번호는 8글자 이상이여야 합니다."}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    
    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) <= 4:
            body = {"message": "아이디는 4글자 이상이여야 합니다."}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        
        if len(request.data["password"]) <= 8:
            body = {"message": "비밀번호는 8글자 이상이여야 합니다."}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )

class UserAPI(generics.RetrieveAPIView):
    lookup_field = "user_pk"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileUpdateAPI(generics.UpdateAPIView):
    lookup_field = "user_pk"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class fileAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM file")
        db = cur.fetchall()

        cur.execute("SELECT count(class_name) from file")
        file_count = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        file_json = []
        for i in range(0, file_count):
            temp = {}
            temp["id"] = i + 1
            temp['class_name'] = db[i][0]
            temp['title'] = db[i][1]
            temp['description'] = db[i][2]
            temp['link'] = db[i][3]
            file_json.append(temp)

        return Response(
            {
                "file": file_json
            }
        )

class homeworkAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM homework")
        db = cur.fetchall()

        cur.execute("SELECT count(class_name) from homework")
        homework_count = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        homework_json = []
        for i in range(0, homework_count):
            temp = {}
            temp['class_name'] = db[i][0]
            temp['title'] = db[i][1]
            temp['due_date'] = db[i][2]
            temp['status'] = db[i][3]
            temp['grade'] = db[i][4]
            temp['link'] = db[i][5]
            homework_json.append(temp)

        return Response(
            {
                "homework": homework_json
            }
        )

class quizAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM quiz")
        db = cur.fetchall()

        cur.execute("SELECT count(class_name) from quiz")
        quiz_count = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        quiz_json = []
        for i in range(0, quiz_count):
            temp = {}
            temp['class_name'] = db[i][0]
            temp['title'] = db[i][1]
            temp['due_date'] = db[i][2]
            temp['grade'] = db[i][3]
            temp['link'] = db[i][4]
            quiz_json.append(temp)

        return Response(
            {
                "quiz": quiz_json
            }
        )

class noticeAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM notice")
        db = cur.fetchall()

        cur.execute("SELECT count(class_name) from notice")
        notice_count = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        notice_json = []
        for i in range(0, notice_count):
            temp = {}
            temp['class_name'] = db[i][0]
            temp['title'] = db[i][1]
            temp['creation_date'] = db[i][2]
            temp['link'] = db[i][3]
            notice_json.append(temp)

        return Response(
            {
                "notice": notice_json
            }
        )

class classAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM user_data")
        db = cur.fetchall()

        cur.execute("SELECT count(class_name) from user_data")
        class_count = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        class_json = []
        for i in range(0, class_count):
            temp = {}
            temp['class_name'] = db[i][0]
            temp['division'] = db[i][1]
            temp['professor'] = db[i][2]
            temp['class_link'] = db[i][3]
            class_json.append(temp)

        return Response(
            {
                "class": class_json
            }
        )


class calendarAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM quiz ORDER BY due_date")
        quiz_db = cur.fetchall()

        cur.execute("SELECT count(class_name) from quiz")
        quiz_count = cur.fetchall()[0][0]

        cur.execute("SELECT * FROM homework ORDER BY due_date")
        homework_db = cur.fetchall()

        cur.execute("SELECT count(class_name) from homework")
        homework_count = cur.fetchall()[0][0]

        cur.close()
        conn.close()

        day = []
        calendar_json = {}
        for i in range(0, homework_count):
            temp = {}
            temp2 = []

            temp['class_name'] = homework_db[i][0]
            temp['title'] = homework_db[i][1]
            temp['due_date'] = homework_db[i][2]

            if calendar_json.get(homework_db[i][2][:10]) != None:
                for j in range(0, len(calendar_json[homework_db[i][2][:10]])):
                    temp2.append(calendar_json[homework_db[i][2][:10]][j])
            temp2.append(temp)
            calendar_json[homework_db[i][2][:10]] = temp2
            day.append(homework_db[i][2][:10])

        for i in range(0, quiz_count):
            temp = {}
            temp2 = []

            temp['class_name'] = quiz_db[i][0]
            temp['title'] = quiz_db[i][1]
            temp['due_date'] = quiz_db[i][2]

            if calendar_json.get(quiz_db[i][2][:10]) != None:
                for j in range(0, len(calendar_json[quiz_db[i][2][:10]])):
                    temp2.append(calendar_json[quiz_db[i][2][:10]][j])
            temp2.append(temp)
            calendar_json[quiz_db[i][2][:10]] = temp2
            day.append(quiz_db[i][2][:10])


        day = set(day)
        day = list(day)
        day.sort()
        
        return Response(
            {
                "calendar": calendar_json,
                "day": day
            }
        )