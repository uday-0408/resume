from django.shortcuts import render

# user ,1234
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDescriptionSerializer, JobDescription, ResumeSerializer
from .models import Resume
from .analyzer import process_resume


class JobDescriptionAPI(APIView):
    def get(self, request):
        queryset = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(queryset, many=True)
        return Response({"status": True, "data": serializer.data})


class AnalyzeResumeAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            if not data.get("job_description"):
                return Response(
                    {
                        "status": False,
                        "massage": "job_description is required",
                        "data": {},
                    }
                )
            serializer = ResumeSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        "status": False,
                        "massage": "errors",
                        "data": serializer.errors,
                    }
                )
            serializer.save()
            _data = serializer.data
            resume_instance = Resume.objects.get(id=_data["id"])  # type: ignore
            resume_path = resume_instance.resume.path
            data = process_resume(
                resume_path,
                JobDescription.objects.get(id=data.get("job_description")),
            )
            return Response(
                {
                    "status": True,
                    "massage": "Resume Analyzed",
                    "data": data,
                }
            )

        except Exception as e:
            print(f"Error from AnalyzeResumeAPI: {e}")
            return Response({"data": False})
