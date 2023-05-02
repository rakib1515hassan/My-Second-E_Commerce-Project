import os
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from Accounts.models import User, Customer, Seller, UserOTP, Customer_Address
from django.contrib import messages


# For Authentication-------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# For OTP Creation---------------------------------------------------
import random


# For Mail Sending -------------------------------------------------
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.

def customer_reg(request):
    if request.method == "POST":
        First_Name = request.POST["first_name"]
        Last_Name = request.POST["last_name"]
        Email_Address = request.POST["email"]
        Phone_Number = request.POST["phone"]
        password = request.POST["password"]
        Confirm_Password = request.POST["c_password"]

        # print("--------------------------------------------")
        # print("Customer Account")
        # print(f"First Name:{First_Name}, Last Name: {Last_Name}, Email: {Email_Address}, Phone: {Phone_Number}, Password: {password}, Confirm Password: {Confirm_Password}")
        # print("--------------------------------------------")

        if password == Confirm_Password:
            if User.objects.filter(email=Email_Address).exists():
                messages.error(request, 'This email is already taken.')
                return redirect(customer_reg)
            else:
                user_obj = User.objects.create(first_name=First_Name, last_name=Last_Name, email=Email_Address, mobile = Phone_Number, password=password, is_customer=True)
                user_obj.set_password(password)
                user_obj.is_active = False
                user_obj.save()
                # It Replace Signals---------------------------
                customer= Customer.objects.create(user=user_obj)
                customer.save()

                # Now Send Mail-------------------------------------------
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = user_obj, otp = usr_otp)

                mess = f"Hello {user_obj.first_name}{user_obj.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user_obj.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': user_obj})

    return render(request, 'Accounts/c_registration.html')







def seller_reg(request):
    if request.method == "POST":
        First_Name = request.POST["first_name"]
        Last_Name = request.POST["last_name"]
        Email_Address = request.POST["email"]
        Phone_Number = request.POST["phone"]
        password = request.POST["password"]
        Confirm_Password = request.POST["c_password"]

        # print("--------------------------------------------")
        # print("Seller Account")
        # print(f"First Name:{First_Name}, Last Name: {Last_Name}, Email: {Email_Address}, Password: {password}, Confirm Password: {Confirm_Password}")
        # print("--------------------------------------------")

        if password == Confirm_Password:
            if User.objects.filter(email=Email_Address).exists():
                messages.error(request, 'This email is already taken.')
                return redirect(seller_reg)
            else:
                user_obj = User.objects.create(first_name=First_Name, last_name=Last_Name, email=Email_Address, mobile = Phone_Number, password=password, is_seller=True)
                user_obj.set_password(password)
                user_obj.is_active = False
                user_obj.save()
                # It Replace Signals---------------------------
                seller= Seller.objects.create(user=user_obj)
                seller.save()
                # Now Send Mail-------------------------------------------
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = user_obj, otp = usr_otp)

                mess = f"Hello {user_obj.first_name}{user_obj.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user_obj.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': user_obj})
            
    return render(request, 'Accounts/s_registration.html')





def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # print("--------------------------------------------")
        # print(f"Email: {email}, Password: {password}")
        # print("--------------------------------------------")

        user_obj = User.objects.filter(email=email).first()
        # user_a = User.objects.filter(email = email).exists()
        if (user_obj is not None) and (user_obj.check_password(password)== True):
            # Customer Login-----------------------------------------------------------------------------------------
            if user_obj.is_customer == True and user_obj.is_active == True:
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('user_profile')
            elif user_obj.is_customer == True and user_obj.is_active == False:
                usr = User.objects.filter(email=email).first()
                UserOTP.objects.get(user = usr).delete()
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = usr, otp = usr_otp)
                mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': usr})
            # Seller Login------------------------------------------------------------------------------------------
            elif user_obj.is_seller == True and user_obj.is_active == True:
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return HttpResponse('<h1 class="text-center">Seller Profile</h1>')
            elif user_obj.is_seller == True and user_obj.is_active == False:
                usr = User.objects.filter(email=email).first()
                UserOTP.objects.get(user = usr).delete()
                usr_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user = usr, otp = usr_otp)
                mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [usr.email],
                    fail_silently = False
                    )
                return render(request, 'Accounts/OTP_verify.html', {'user': usr})
        elif not User.objects.filter(email = email).exists():
            messages.warning(request, f'Please enter a correct email.')
            return redirect('user_login')
        
        elif User.objects.filter(email = email).exists():
            if user_obj.check_password(password)== False:
                messages.warning(request, f"Please enter a correct password You Password does't match.")
                return redirect('user_login')
    
        
    return render(request, 'Accounts/login.html')








def otp_verify(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp') #213243 #None

        if get_otp:
            get_usr = request.POST.get('user_otp')
            user_obj = User.objects.get(email=get_usr)
            if user_obj:
                if user_obj.is_customer == True and user_obj.is_active == False:
                    user = user_obj  # Or users[0]
                    otp_obj = UserOTP.objects.get(user = user)
                    given_otp = int(get_otp)
                    correct_otp = otp_obj.otp
                    # print("-----------------------")
                    # print('Given OTP =', given_otp)
                    # print("User =",user)
                    # print("Correct OTP =",correct_otp)
                    # print("-----------------------")
                    if given_otp == correct_otp:
                        user.is_active = True
                        user.save()
                        messages.success(request, f'Account is Successfully Created. Now {user.first_name}{user.last_name} you can login.')
                        return redirect('user_login')
                    else:
                        messages.warning(request, f'You Entered a Wrong OTP')
                        return render(request, 'Accounts/OTP_verify.html', {'user': user})
                
                elif user_obj.is_seller == True and user_obj.is_active == False:
                    user = user_obj  # Or users[0]
                    otp_obj = UserOTP.objects.get(user = user)
                    given_otp = int(get_otp)
                    correct_otp = otp_obj.otp
                    # print("-----------------------")
                    # print('Given OTP =', given_otp)
                    # print("User =",user)
                    # print("Correct OTP =",correct_otp)
                    # print("-----------------------")
                    if given_otp == correct_otp:
                        user.save()
                        messages.success(request, f'{user.first_name}{user.last_name} Your Account is Successfully Created.')
                        return render(request, 'Accounts/s_registration_2.html', {'user':user})
                    else:
                        messages.warning(request, f'You Entered a Wrong OTP')
                        return render(request, 'Accounts/OTP_verify.html', {'user': user})
            else:
                messages.error(request, f'Your Email is Not Exist.')
                return redirect('home')
        
        
    return render(request, 'Accounts/OTP_verify.html')


## With Javascripts-----------------------------------------------------------------------------------------
# def resend_OTP(request):
#     if request.method == "GET":
#         get_usr = request.GET['user']
#         print("--------------------------")
#         print(get_usr)
#         print("--------------------------")
#     if User.objects.filter(email = get_usr).exists() and not User.objects.get(email = get_usr).is_active:
#         usr = User.objects.get(email=get_usr)
#         UserOTP.objects.get(user = usr).delete()
#         usr_otp = random.randint(100000, 999999)
#         UserOTP.objects.create(user = usr, otp = usr_otp)
#         mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

#         send_mail(
#             "Welcome to IT-MrH Solution - Verify Your Email",
#             mess,
#             settings.EMAIL_HOST_USER,
#             [usr.email],
#             fail_silently = False
#             )
#         return JsonResponse('Sending OTP Sccessfully.')
#     return JsonResponse('We face some tecnical problem.')

## Withot Javascripts----------------------------------------------------------------------------------------
def resend_OTP(request):
    if request.method == "GET":
        get_usr = request.GET.get('otp')
        # print("--------------------------")
        # print("User Email: ",get_usr)
        # print("--------------------------")
        usr = User.objects.filter(email=get_usr).first()
        if User.objects.filter(email = get_usr).exists() and not User.objects.get(email = get_usr).is_active:
            usr = User.objects.get(email=get_usr)
            UserOTP.objects.get(user = usr).delete()
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user = usr, otp = usr_otp)
            mess = f"Hello {usr.first_name}{usr.last_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to IT-MrH Solution - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently = False
                )
            return render(request, 'Accounts/OTP_verify.html', {'user': usr})
        
        return render(request, 'Accounts/OTP_verify.html', {'user': usr})



def seller_info(request):
    if request.method == "POST":
        usr_email = request.POST.get('user')
        shop_nam = request.POST.get('shop_name')
        tread_licence = request.FILES.get('tread_licence')
        nid = request.FILES.get('nid')
        address = request.POST.get('address')
        print('-----------------------------')
        print(usr_email,shop_nam,tread_licence,nid, address)
        print('-----------------------------')
        usr = User.objects.get(email = usr_email)
        seller = Seller.objects.get(user = usr)
        if seller:
            # seller.objects.create(shope_name = shop_name,Trade_license = tread_licence, Owner_NID = nid)
            seller.shop_name = shop_nam
            seller.Trade_license = tread_licence
            seller.Owner_NID = nid
            seller.shop_address = address
            seller.save()
            mess = f"Hello {usr.first_name}{usr.last_name},\nPlease wait patiently, we will verify your information and activate your account. Thank you!"
            send_mail(
                "Welcome to IT-MrH Solution - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently = False
                )
            return render(request, 'Accounts/s_seller_waiting_page.html')

    return render(request, "Accounts/s_registration_2.html")







###---------------------------------------------------  Profile   --------------------------------------------





@login_required
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    print("Requested User: ",user)

    customer = Customer.objects.get(user = request.user)

    if request.method == 'POST':
        pro_pic = request.FILES.get('pro_pic')
        Cov_pic = request.FILES.get('Cov_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')

        Old_Pass = request.POST.get('Old_Password')
        New_Pass = request.POST.get('New_Password')
        Confirm_Pass = request.POST.get('New_Password_Confirmation')

        profile_delete_id = request.POST.get('profile_delete_id')
        Password = request.POST.get('Password')

        # print("Profile Pic :",pro_pic)
        # print("Profile Cover Pic :",Cov_pic)

        # print(f"User First Name :{first_name}, User Last Name : {last_name}")

        # print("User Address :",address)
        # print("User Phone :",phone)
        # print("User Gender :",gender)
        # print("User DateOfBirth :",date_of_birth)

        # print(f"Old Pass: {Old_Pass}, New Pass: {New_Pass}, New Con Pass: {Confirm_Pass}")

        # print(f"Delete Profile Request id: {profile_delete_id}, Password: {Password}")

    ## Set Profile Pic-------------------------------------------
        if pro_pic:
            if len(request.FILES) != 0:
                if customer.profile_pictur:
                    if len(customer.profile_pictur) > 0:
                        os.remove(customer.profile_pictur.path)
            customer.profile_pictur = pro_pic
            customer.save()
            return redirect('user_profile')
    ## Set Cover Pic---------------------------------------------
        if Cov_pic:
            if len(request.FILES) != 0:
                if customer.cover_pictur:
                    if len(customer.cover_pictur) > 0:
                        os.remove(customer.cover_pictur.path)
            customer.cover_pictur = Cov_pic
            customer.save()
            return redirect('user_profile')
    ## Name Change Set--------------------------------------------
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
    ## Address Set------------------------------------------------
        if address:
            customer.address = address
    ## Phone Number Set-------------------------------------------
        if phone:
            user.mobile = phone
    ## Gender Set-------------------------------------------------
        if gender:
            customer.gender = gender
    ## Date Of Birth Set------------------------------------------
        if date_of_birth:
            customer.date_of_birth = date_of_birth
    ## Password Change--------------------------------------------
        if Old_Pass and New_Pass and Confirm_Pass:
            if user.check_password(Old_Pass) == True:
                # print("Our Password Is Match.")
                if New_Pass == Confirm_Pass:
                    user.set_password(New_Pass)
                    user.save()
                    logout(request)
                    return redirect('user_login')
                else:
                    messages.error(request, "New Password and Confirm Password dos't match.")
            else:
                # print("Our Password Is'n Match.")
                messages.error(request, "Your Old Password is't Match.")
    ## Profile Delete---------------------------------------------
        if profile_delete_id:
            user_d  = User.objects.get(id=profile_delete_id)
            customer_d = Customer.objects.get(user = user_d)
            if user_d and user_d.check_password(Password) == True:
                if customer_d.profile_pictur:
                    os.remove(customer_d.profile_pictur.path)
                if customer_d.cover_pictur:
                    os.remove(customer_d.cover_pictur.path)
                user_d.delete()
                return redirect('home')
            else:
                messages.error(request, "Your Password is Wrong.")
                return redirect('user_profile')
    ##------------------------------------------------------------
        user.save()
        customer.save()
        return redirect('user_profile')
    ##------------------------------------------------------------
    data = {
        'user': user,
        'customer': customer,
    }
    return render(request, 'Accounts/customer_profile.html', data)







@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')






@login_required
def email_change(request):
    if request.method == "POST":
    ## OTP Sending New Email---------------------------------------------------------------------------------------
        old_email = request.POST.get('Old_Email')
        new_email = request.POST.get('new_email')
        password = request.POST.get('Password')
        # print("-----------------------")
        # print(f"Old Email: {old_email}, New Email: {new_email}, Password: {password}")
        # print("-----------------------")
        if old_email and new_email and password:
            user_obj = User.objects.get(email = old_email)
            if user_obj and new_email and password:
                if user_obj.check_password(password) == True:
                    usr_otp = random.randint(100000, 999999)

                    request.session['new_email'] = new_email
                    request.session['usr_otp'] = usr_otp

                    # print("-----------------------------------")
                    # print(f"New Email= {new_email}, Correct OTP = {usr_otp}")
                    # print("-----------------------------------")

                    mess = f"Hello {user_obj.first_name}{user_obj.last_name},\nYour OTP is {usr_otp}\nThanks!"

                    send_mail(
                        "Welcome to IT-MrH Solution - Verify Your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [new_email],
                        fail_silently = False
                        )
                    return redirect('email_change')
                else:
                    messages.error(request, "Your Password Is Wrong.")
                    return redirect('user_profile')
            else:
                return redirect('user_profile')

    ## OTP Verify New Email---------------------------------------------------------------------------------------
        otp = request.POST.get('otp')
        usr = request.POST.get('usr')
        if otp and usr:
            n_email = request.session['new_email']
            correct_otp = request.session['usr_otp']

            # print("-----------------------------------")
            # print(f"Given OTP = {otp}, Old Email = {usr}")
            # print(f"New Email= {n_email}, Correct OTP = {correct_otp}")
            # print("-----------------------------------")

            user_obj = User.objects.get(email = usr)
            if int(otp) == int(correct_otp):
                print("OTP is Successfully Match.")
                if user_obj:
                    user_obj.email = n_email
                    user_obj.save()
                    logout(request)
                    messages.success(request, "Your Mail Is Sccessfully Changed.")
                    return redirect('user_login')
                else:
                    messages.error(request, "Your Profile is not found.")
                    return redirect('email_change')
            else:
                messages.error(request, "Your OTP is't match.")
                return redirect('email_change')

    return render(request, "Accounts\email_change_OTP.html", {'user': request.user})




def customer_address(request):
    if request.method == 'POST':
        division = request.POST.get('division')
        sub_division = request.POST.get('sub_division')
        zipcode = request.POST.get('zipcode')
        home = request.POST.get('home')
        r_number = request.POST.get('r_number')

        a_id = request.POST.get('add_id')
        d_id = request.POST.get('delete_id')
        e_id = request.POST.get('edit_id')

        print('---------------------------------')
        print(f"Division={division}, Sub Division={sub_division}, Zipcode={zipcode}, Home={home}, Phone={r_number}")
        print('---------------------------------')

        customer = Customer.objects.get(user = request.user)

        ## Customer Address Add--------------------------------------------------------
        if a_id:
            Customer_Address.objects.create(
                user = customer,
                Division = division,
                Sub_division = sub_division,
                Zipcode = zipcode,
                Home_Address = home,
                Phone = r_number
                )
            messages.success(request, "Your New Address is Successfully save.")
            return redirect('user_profile')
        
        ## Customer Address Delete-----------------------------------------------------
        if d_id:
            address = Customer_Address.objects.get(id=d_id)
            address.delete()
            messages.success(request, "Your Address is Successfully Delete.")
            return redirect('user_profile')
        
        ## Customer Address Edit-------------------------------------------------------
        if e_id:
            address = Customer_Address.objects.get(id=e_id)
            address.Division = division
            address.Sub_division = sub_division
            address.Zipcode = zipcode 
            address.Home_Address = home
            address.Phone = r_number
            address.save()
            messages.success(request, "Your Address is Successfully Change.")
            return redirect('user_profile')
 
    return redirect('user_profile')




@login_required
def seller_profile(request):
    user = request.user
    data = {
        'user': user
    }
    return render(request, 'SellerProfile/seller_profile.html', data)




##------------------------------------------------ Forget Password ------------------------------------------------
def Take_Email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:    
            if User.objects.filter(email = email).exists():
                user = User.objects.get(email = email)
                otp_model = UserOTP.objects.get(user = user)
                new_otp = random.randint(100000, 999999)
                otp_model.otp = new_otp
                otp_model.save()
                request.session['email'] = user.email
                # print('----------------------------')
                # print('New OTP = ',new_otp)
                # print('----------------------------')

                mess = f"Hello {user.first_name}{user.last_name},\n Your OTP Code is {new_otp}, After submit your OTP you can set new password. Thank you!"
                send_mail(
                    "Welcome to IT-MrH Solution - Verify Your Email",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently = False
                    )
                messages.success(request, "Your OTP Code is Successfully sen on your Email.")
                return redirect('Take_OTP')
            else:
                messages.error(request, "Please Giver Correct Mail.")
                return redirect('Take_Email')
    return render(request, "Accounts/ForgetPassword/GetEmail.html")



def Take_OTP(request):
    if request.method == 'POST':
        given_otp = request.POST.get('otp')

        if given_otp:
            email = request.session['email']
            user = User.objects.get(email=email)
            otp_model = UserOTP.objects.get(user = user)
            
            if otp_model.otp == int(given_otp):
                messages.success(request, 'Your OTP is Match, Now You Can Set New Password.')
                request.session['email'] = user.email
                return redirect('Take_New_Password')
            else:
                messages.error(request, "Your OTP Don't Match. Please Give Correct OTP.")
                return redirect('Take_OTP')
    return render(request, "Accounts/ForgetPassword/GetOTP.html")



def Take_New_Password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        if password and c_password:
            if password == c_password:
                email = request.session['email']
                user = User.objects.get(email=email)
                if user:
                    if user.check_password(password) == False:
                        user.set_password(password)
                        user.save()
                        messages.success(request, "Your New Password Is Set, Now You Can Login.")
                        return redirect('user_login')
                    else:
                        messages.error(request, "This is your old password, Please Given a New Password.")
                        return redirect('Take_New_Password')
                else:
                    messages.error(request, "User Not Found.")
                    return redirect('home')
            else:
                messages.error(request, "Your Password and Confirm Password Is Not Match.")
                return redirect('Take_New_Password')


    return render(request, "Accounts/ForgetPassword/GetNewPassword.html")