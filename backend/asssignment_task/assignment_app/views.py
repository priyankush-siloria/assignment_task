from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from assignment_app.models import PostModel
from assignment_app.serializers import PostSerializer

# Create your views here.


class ApiLoginView(APIView):
    """
    User LOGIN View
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response(
                {"error": "Please provide both username and password"},
                status=404
            )
        use_obj = User.objects.filter(username=username).first()
        if use_obj:
            if use_obj.is_active:
                user = authenticate(username=username, password=password)
                if not user:
                    return Response(
                        {"error": "Invalid Credentials"},
                        status=404)
                else:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({"token": token.key, "user": user.id}, status=200)
            else:
                return Response(
                    {
                        "error": "User Is not active",
                        "username": use_obj.username,
                        "message": "Please Verify username",
                    },
                    status=404,
                )
        else:
            return Response({"error": "Invalid Credentials"}, status=401)
    

class ApiLogoutView(APIView):
    """
    Logout View
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logout Succesfull"}, status=200)
    

class RegistrationView(APIView):

    def post(self, request):
        try:
            required_field = ['username', 'first_name', 'last_name', 'password']
            request_data_key = list(request.data.keys())
            missing_field = list(set(required_field).difference(request_data_key))
            if missing_field:
                value = ','.join(missing_field)
                return Response({"error": f"Please enter {value}"}, status=400)
            username = request.data.get("username")
            first_name = request.data.get("first_name")
            last_name = request.data.get('last_name')
            password = request.data.get('password')
            user_check = User.objects.filter(username=username).first()
            if not user_check:
                user_obj = User.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                user_obj.set_password(password)
                user_obj.save()
                return Response({"message": "Register Succesfull"}, status=201)  
            else:
                return Response({"error": "Username already exits!"}, status=400)
            
        except Exception as err:
            return Response({"error": str(err)}, status=400)
        

class PostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    model_class = PostModel

    def get(self, request, postid=None):
        if postid:
            obj = self.model_class.objects.filter(id=postid).first()
            if obj:
                serializer = self.serializer_class(obj)
                return Response({
                    "data": serializer.data
                    }, status=200)
            else:
                return Response({
                    "error": "Post not found!"
                    }, status=404)
        all_objects = self.model_class.objects.filter(is_active=True)
        serializer = self.serializer_class(all_objects, many=True)
        return Response({
                    "data": serializer.data
                    }, status=200)

    def post(self, request, postid=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Post created Succesfull",
                    "data": serializer.data
                    }, status=201)
            else:
                return Response({
                    "error": serializer.errors
                }, status=400)

        except Exception as err:
            return Response({
                    "error": str(err)
                }, status=400)
        
    def put(self, request, postid=None):
        try:
            obj = self.model_class.objects.filter(id=postid).first()
            if obj:
                serializer = self.serializer_class(obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                    "message": "Post update Succesfull",
                    "data": serializer.data
                    }, status=200)
                else:
                    return Response({
                    "error": serializer.errors
                    }, status=200)
            else:
                return Response({
                    "error": "Post not found!"
                    }, status=404)
        except Exception as err:
            return Response({
                    "error": str(err)
                }, status=400)







    def delete(self, request, postid=None):
        try:
            obj = self.model_class.objects.filter(id=postid, is_active=True).first()
            if obj:
                obj.is_active = False
                obj.save()
                return Response({
                    "message": "Post Deleted Succesfull",
                    }, status=200)
            else:
                return Response({
                    "error": "Post not found!"
                    }, status=404)
        except Exception as err:
            return Response({
                    "error": str(err)
                }, status=400)
