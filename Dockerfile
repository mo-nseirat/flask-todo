#بختار من اي ايمج انزل
FROM python:latest
#المكان اللي رح انسخ عليه الapp
WORKDIR /app
#اول اشي بنسخ المتطلبات بكون حاطهم بملف واحد
COPY requirements.txt . 
#هون بيب زي مثلا apt  بس لبايثون
RUN pip install -r requirements.txt 
#برجع بنسخ باقي الملفات
COPY . . 

EXPOSE  5000
#جنيكورن هو موقع استضافة مخصص لبايثون وفلاسك
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

#طبعا لما نبني الايمج رح نستخدم سطر  docker build -t todo-app .  
#يعني بعطيه اسم والنقطة بتقله انه رح ابني هاد الايمج بالمكان اللي انا موجود عليه 

