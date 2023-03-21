from django import forms
from django.forms import ModelForm, Textarea, TextInput
from main.models import Bus, newsAndUpdate, Routes
from datetime import datetime, timedelta
import datetime
import time
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# getting the data from the database for the validation

class LoginForm(forms.Form):
    userName = forms.CharField(
        required=False,
        label='Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'name': 'username', 'placeholder': 'Username'})
    )

    passwd = forms.CharField(
        required=False,
        label='Username',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'name': 'password', 'placeholder': 'Password'})
    )

    def clean_userName(self):
        user_name = self.cleaned_data.get('userName')
        user_str = str(user_name)
        return user_str

    def clean_passwd(self):
        user_passwd = self.cleaned_data.get('passwd')
        user_passwd_str = str(user_passwd)
        return user_passwd_str


# bus registration form
class busRegForm(forms.Form):
    bus_plate_no = forms.CharField(
        required=False,
        label='bus plate no',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'bus_plate_no', 'placeholder': 'Bus Number Plate'})
    )
    driver_name = forms.CharField(
        required=False,
        label='driver name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'driver_name', 'placeholder': 'Driver name'})
    )
    no_of_seat = forms.CharField(
        required=False,
        label='bus plate no',
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'no_of_seat', 'placeholder': 'No of Seat'})
    )
    choice = [
        ('', 'Select the availability'),
        (1, 'Available'),
        (0, 'Not Available'),
    ]
    vehicle_status = forms.CharField(
        required=False,
        label='no of seat',
        widget=forms.Select(
            attrs={'class': 'form-control', 'name': 'vehicle_status', 'placeholder': 'Vehicle status'},
            choices=choice
        )
    )
    contact_no = forms.CharField(
        required=False,
        label='contact no',
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'contact no', 'placeholder': 'Contact no'})
    )
    other_details = forms.CharField(
        required=False,
        label='other details',
        widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'other_details', 'placeholder': 'Other details'})
    )

    def clean_bus_plate_no(self):
        plate_no = self.cleaned_data.get('bus_plate_no')
        plate_no_str = str(plate_no)
        if len(plate_no_str) == 0:
            raise forms.ValidationError('Empty field')
        elif len(plate_no_str) >= 19:
            raise forms.ValidationError('Data is too log for this field.')

    def clean_driver_name(self):
        driver_name = self.cleaned_data.get('driver_name')
        driver_name_str = str(driver_name)
        if len(driver_name_str) == 0:
            raise forms.ValidationError('Empty field')
        elif len(driver_name_str) >= 49:
            raise forms.ValidationError('Data is too log for this field.')

    def clean_no_of_seat(self):
        no_of_seat = self.cleaned_data.get('no_of_seat')
        no_of_seat_str = str(no_of_seat)
        if len(no_of_seat_str) == 0:
            raise forms.ValidationError('Empty field')
        elif len(no_of_seat_str) >= 3:
            raise forms.ValidationError('Data is too log for this field.')
        elif not int(no_of_seat_str) <= 66:
            raise forms.ValidationError('Number Must be less than 67.')

    def clean_vehicle_status(self):
        vehicle_status = self.cleaned_data.get('vehicle_status')
        if vehicle_status == '':
            raise forms.ValidationError('Empty field')

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        contact_no_str = str(contact_no)
        vl = contact_no_str.replace("-", "")
        if len(contact_no_str) == 0:
            raise forms.ValidationError('Empty field')
        elif len(contact_no_str) >= 12:
            raise forms.ValidationError('Data is too log for this field.')
        elif not vl.isnumeric():
            raise forms.ValidationError('Enter valid phone number.')

    # def clean_other_details(self):
    #     other_details = self.cleaned_data.get('other_details')
    #     other_details_str = str(other_details)
    #     if len(other_details_str) == 0:
    #         raise forms.ValidationError('Empty field')


class routeRegForm(forms.Form):
    # buses = Bus.objects.all()
    # choice = [('', 'Select the bus')]
    # for bus in buses:
    #     choice.append((bus.bus_plate_no, bus.bus_plate_no))

    plate_no = forms.ModelChoiceField(
        required=False,
        queryset=Bus.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control', 'name': 'plate_no'},
        )
    )

    route_no = forms.CharField(
        required=False,
        label='route no',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'route_no', 'placeholder': 'Route no'},
        )

    )
    start_location = forms.CharField(
        required=False,
        label='start_location',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'start_location', 'placeholder': 'Departure'})
    )
    end_location = forms.CharField(
        required=False,
        label='end_location',
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'end_location', 'placeholder': 'Arrival'})
    )
    yesterday = datetime.date.today()
    route_date = forms.DateField(
        required=False,
        label='date',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'route_date', 'min': str(yesterday), 'type': 'date'},
            # format='%m/%d/%Y'
        )
    )

    route_time = forms.TimeField(
        required=False,
        label='time',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'route_time', 'type': 'time'},
            # format='%I:%M %p'

        )
    )

    total_distance = forms.CharField(
        required=False,
        label='total_distance',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'total_distance',
                   'placeholder': 'Total Distance (Enter without KM)'})
    )
    # avg_run_time = forms.CharField(
    #     required=False,
    #     label='avg_run_time',
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'name': 'avg_run_time', 'placeholder': 'Average Run Time'},
    #
    #     )
    # )

    choice = [
        ('', 'select the availability'),
        (1, 'Available'),
        (0, 'Not Available')
    ]
    route_status = forms.CharField(
        required=False,
        label='vehicle_status',
        widget=forms.Select(
            attrs={'class': 'form-control', 'name': 'route_status', 'placeholder': 'Route Status'},
            choices=choice
        )
    )

    # route_available = forms.BooleanField(
    #     label='available',
    #     required=False,
    #     widget=forms.CheckboxInput(
    #         attrs={'class': 'form-check-input me-2', 'id': 'available'}
    #     )
    # )

    #  # adding values to the forms to change
    # def __init__(self, *args, **kwargs):
    #     initial = kwargs.get('initial', {})
    #     route_no = initial.get('route_no', '5966')
    #     start_location = initial.get('start_location', '')
    #     super(routeRegForm, self).__init__(*args, **kwargs)
    #
    #     route_id_id = kwargs.pop('route_no', None)
    #     if route_no:
    #         route_no = Routes.objects.get(pk=route_id_id)
    #         print(route_no)
    #         self.fields['route_no'].initial = '22'

    def clean_plate_no(self):
        plate_no = self.cleaned_data.get('plate_no')
        plate_no_str = str(plate_no)
        if plate_no is None:
            raise forms.ValidationError('Please Fill This Field')

    def clean_route_no(self):
        route_no = self.cleaned_data.get('route_no')
        route_no_str = str(route_no)
        if len(route_no_str) == 0:
            raise forms.ValidationError('Please fill this field')
        elif len(route_no_str) >= 11:
            raise forms.ValidationError('Data is too long to this field.')

    def clean_start_location(self):
        start_location = self.cleaned_data.get('start_location')
        start_location_str = str(start_location)
        if len(start_location_str) == 0:
            raise forms.ValidationError('please fill this field')

    def clean_end_location(self):
        end_location = self.cleaned_data.get('end_location')
        end_location_str = str(end_location)
        if len(end_location_str) == 0:
            raise forms.ValidationError('please fill this field')

    def clean_route_date(self):
        route_date = self.cleaned_data.get('route_date')
        # route_date_str = str( route_date)
        if route_date is None:
            raise forms.ValidationError('please fill this field')

    def clean_route_time(self):
        route_time = self.cleaned_data.get('route_time')
        # route_time_str = str(route_time)
        # print(route_time_str)
        if route_time is None:
            raise forms.ValidationError('please fill this field')

    def clean_total_distance(self):
        total_distance = self.cleaned_data.get('total_distance')

        total_distance_str = str(total_distance)
        if len(total_distance_str) == 0:
            raise forms.ValidationError('please fill this field')
        elif len(total_distance_str) >= 999:
            raise forms.ValidationError('Please enter value below 1000')
        elif total_distance_str:
            try:
                total_d = float(total_distance)
            except ValueError:
                raise forms.ValidationError("Enter without KM")

    # def clean_avg_run_time(self):
    #     avg_run_time = self.cleaned_data.get('avg_run_time')
    #     avg_run_time_str = str(avg_run_time)
    #     if len(avg_run_time_str) == 0:
    #         raise forms.ValidationError('please fill this field')

    def clean_route_status(self):
        route_status = self.cleaned_data.get('route_status')
        if route_status == 1 or route_status == 0:
            raise forms.ValidationError('Please select Available or Not Available')
        elif route_status == '':
            raise forms.ValidationError('Please fill this field.')

    # def clean_route_available(self):
    #     data = self.cleaned_data.get('route_available')
    #     if not data:
    #         raise forms.ValidationError("You can't continue father without agree the term and conditions.")


class newsandupdateForm(forms.Form):
    subject = forms.CharField(
        required=False,
        label='Enter subject',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'subject', 'placeholder': 'Enter Subject'}
        )
    )
    edit = forms.CharField(
        required=False,
        label='Message body',
        widget=CKEditorWidget(attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'Enter your message....', 'width':'500px;'})
    )

    # email = forms.CharField(
    #     required=False,
    #     label='email',
    #     widget=forms.Textarea(
    #         attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'Enter your message....'}
    #
    #     )
    # )

    def clean_subject(self):
        mail_sub = self.cleaned_data.get('subject')
        mail_sub_str = str(mail_sub)
        if len(mail_sub_str) == 0:
            raise forms.ValidationError('This field is empty.')

    def clean_email(self):
        pass


# class newsandupdateForm(ModelForm):
#     class Meta:
#         model = newsAndUpdate
#         fields = ['subject', 'email']
#
#         labels = {
#             'subject': 'Enter subject',
#             'email': 'Message body '
#         }
#
#         widgets = {
#             'subject': TextInput(
#                 attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'Enter your subject....'}),
#             'name': Textarea(attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'Enter your message....'}),
#         }
#
#     def clean_subject(self):
#         mail_sub = self.cleaned_data.get('subject')
#         mail_sub_str = str(mail_sub)
#         if len(mail_sub_str) == 0:
#             raise forms.ValidationError('This field is empty.')


class ticket_searchForm(forms.Form):
    search_from = forms.CharField(
        required=False,
        label='search',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search Invoice No', 'name': 'search_invoice'})
    )

    # def clean_search_from(self):
    #     search = self.cleaned_data.get('search_from')
    #     search_str = str(search)
    #     print(search_str)
    #     print("333")
    #     return search


class bus_searchForm(forms.Form):
    search_from = forms.CharField(
        required=False,
        label='search',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search Bus Number Plate', 'name': 'sebus'})
    )

    def clean_search_from(self):
        search = self.cleaned_data.get('search_from')
        search_str = str(search)
        print(search_str)
        print("333")
        return search


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        # required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'email address'}
        )
    )
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        labels = {
            'username': 'Username',
            'email': 'Email address',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        # self.fields['username'].widget.attrs['required'] = False
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def clean_email(self):
        emailaddr = self.cleaned_data.get('email')
        email_str = str(emailaddr)
        if not email_str is None:
            if not emailaddr:
                raise forms.ValidationError("Please fill the Email filed ")
            elif not '@' in email_str:
                raise forms.ValidationError('Please enter with "@" symbol')
            elif emailaddr:
                check_patter = str(emailaddr).split('@')
                if check_patter[1].__contains__('.'):
                    check_dot = str(check_patter[1]).split('.')
                    print(check_dot)
                    if len(check_dot[0]) == 0:
                        raise forms.ValidationError('invalid email address')
                else:
                    raise forms.ValidationError("please enter valid email address")
        else:
            raise forms.ValidationError("Email field is empty")
        return emailaddr

    # def clean_username(self):
    #     get_username = self.cleaned_data.get('username')
    #     if not get_username:
    #         raise forms.ValidationError("Please fill this field.")

class del_form(forms.Form):
    del_field = forms.CharField(
        required=False,
        label='del_field',
        widget=forms.HiddenInput(
            attrs={'name': 'del_route', 'id': 'del_route', 'value': ''}
        )

    )


class del_form2(forms.Form):
    del_bus = forms.CharField(
        required=False,
        label='del_bus',
        widget=forms.HiddenInput(
            attrs={'name': 'del_bus', 'id': 'del_bus', 'value': ''}
        )

    )


class del_form3(forms.Form):
    del_feedback = forms.CharField(
        required=False,
        label='del_feedback',
        widget=forms.HiddenInput(
            attrs={'name': 'del_feedback', 'id': 'del_feedback', 'value': ''}
        )

    )


class feed_back_reviewed(forms.Form):
    feedback_reviewed = forms.CharField(
        required=False,
        label='feedback_reviewed',
        widget=forms.HiddenInput(
            attrs={'name': 'feedback_reviewed', 'id': 'feedback_reviewed', 'value': ''}
        )

    )


class make_refund(forms.Form):
    refund_ticket = forms.CharField(
        required=False,
        label='refund_ticket',
        widget=forms.HiddenInput(
            attrs={'name': 'refund_ticket', 'id': 'refund_ticket', 'value': ''}
        )

    )
