from django import forms

# getting the data from the database for the validation
from .models import SubEmail


# class routeSearch(forms.Form):
#     arrival = forms.CharField(
#         required=False,
#         label="Arrival",
#         widget=forms.TextInput(
#             attrs={'class': 'search_dropdown d-flex flex-row align-items-center justify-content-start',
#                    'placeholder': 'Arrival', 'name': 'arrival', 'id': 'nic'}
#         )
#     )


class PassengerForm(forms.Form):
    seat = forms.CharField(
        required=False,
        label='seat',
        widget=forms.HiddenInput(attrs={'name': 'seat', 'id': 'seat', "value": ''})
    )

    nic = forms.CharField(
        required=False,
        label="nic",
        widget=forms.TextInput(
            attrs={'class': 'form-control nic2 form-control-lg', 'placeholder': 'Enter NIC', 'name': 'nic', 'id': 'nic'}
        )
    )

    emailaddr = forms.CharField(
        required=False,
        label="emailaddr",
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email address', 'name': 'emailaddr',
                   'id': 'emailaddr'}
        )
    )
    agreement = forms.BooleanField(
        label='agree',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input me-2', 'id': 'agreement'}
        )
    )

    def clean_seat(self):
        seat_data = self.cleaned_data.get('seat')
        if not seat_data:
            raise forms.ValidationError('Please select a seat.')

    #  validation for the nic field
    def clean_nic(self):
        nic_data = self.cleaned_data.get('nic')
        data_nic = str(nic_data)

        lower_data_nic = data_nic.lower()

        if len(lower_data_nic) == 10:
            try:
                nic_index = lower_data_nic.index('v')
                if not nic_index == 9:
                    raise forms.ValidationError("Invalid NIC")
            except ValueError:
                raise forms.ValidationError('please put V end of the NIC no')
        elif len(lower_data_nic) == 12:
            if not lower_data_nic.isnumeric():
                raise forms.ValidationError('Invalid Nic, only numbers')
        else:
            raise forms.ValidationError("NIC length is incorrect")
        return nic_data

    # validation for the phone number filed
    def clean_emailaddr(self):
        emailaddr = self.cleaned_data.get('emailaddr')
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

    def clean_agreement(self):
        data = self.cleaned_data.get('agreement')
        if not data:
            raise forms.ValidationError("You can't continue father without agree the term and conditions.")


#  ************************************************* credit card *******************************************************

class CreditCardForm(forms.Form):
    card_no = forms.CharField(
        required=False,
        label="card no",
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'card no', 'placeholder': 'XXXX-XXXX-XXXX-XXXX'})
    )
    expire_date = forms.CharField(
        required=False,
        label="expire date",
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'expire-date', 'placeholder': '00/00'})
    )
    code_cvv = forms.CharField(
        required=False,
        label="code cvv",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'cv-no', 'placeholder': '000'})
    )
    name = forms.CharField(
        required=False,
        label="name",
        widget=forms.TextInput(
            attrs={'class': 'form-control text-uppercase', 'name': 'name', 'placeholder': 'your name'})
    )

    def clean_card_no(self):
        data = self.cleaned_data.get('card_no')
        card_no = str(data)
        # print(card_no)
        card_no1 = card_no.replace("-", "")
        # card_no1 = card_no.replace(".", "")
        if not card_no1.isnumeric():
            # print('val')
            raise forms.ValidationError('Invalid card number')
        else:
            number = card_no1  # credit card validator
            sum_odd_digits = sum_even_digits = total = 0
            card_number = number
            card_number = card_number[::-1]

            for x in card_number[::2]:
                sum_odd_digits += int(x)

            for x in card_number[1::2]:
                x = int(x) * 2
                if x >= 10:
                    sum_even_digits += (1 + (x % 10))
                else:
                    sum_even_digits += x
        total = sum_odd_digits + sum_even_digits

        if total % 10 == 0:
            print("valid")
        else:
            # print("invalid")
            raise forms.ValidationError('Invalid card number')

    def clean_expire_date(self):
        data = self.cleaned_data.get('expire_date')
        expire_date = str(data).replace('/', '')

        # print(card_no)
        if not expire_date.isnumeric():
            # print('val')
            raise forms.ValidationError('Invalid expire date')

    def clean_code_cvv(self):
        data = self.cleaned_data.get('code_cvv')
        code_cvv = str(data)
        # print(card_no)
        if not code_cvv.isnumeric():
            # print('val')
            raise forms.ValidationError('Invalid Cvv')

    def clean_name(self):
        data = self.cleaned_data.get('name')
        name = str(data)
        # print(card_no)
        # if not name.isalpha():
        #     # print('val')
        #     raise forms.ValidationError('Invalid Name')
        if name is None:
            raise forms.ValidationError('Enter correct Name')

        elif len(name) == 0:
            raise forms.ValidationError('Empty Field')


#  ************************************************* Feed back *******************************************************

class FeedBackForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        label='First name',
        widget=forms.TextInput(
            attrs={'class': 'form-control contact_input', 'name': 'first_name', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=False,
        label='Last name',
        widget=forms.TextInput(
            attrs={'class': 'form-control contact_input', 'name': 'last_name', 'placeholder': 'Last name'})
    )
    message = forms.CharField(
        required=False,
        label='message',
        widget=forms.Textarea(
            attrs={'class': 'form-control contact_textarea contact_input', 'name': 'message',
                   'placeholder': 'Message.. or request refund'})
    )

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        fname_str = str(name)
        print(fname_str)
        if not fname_str.isalpha():
            raise forms.ValidationError('Enter valid name')
        elif len(fname_str) == 0:
            raise forms.ValidationError('Empty Field')

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')
        lname_str = str(name)
        if not lname_str.isalpha():
            raise forms.ValidationError('Enter valid name')
        elif len(lname_str) == 0:
            raise forms.ValidationError('Empty Field')
    # def clean_message(self):
    #     mgs = self.cleaned_data.get('message_name')
    #     message_str = str(mgs)
    #     if message_str.isalpha():
    #         raise forms.ValidationError('Enter valid name')


#  ************************************************* Email subscription ************************************************

class EmailSubscriptionForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='email',
        widget=forms.TextInput(
            attrs={'class': 'form-control newsletter_input', 'name': 'email', 'placeholder': 'your email..'})
    )

    def clean_email(self):
        newslatter = SubEmail.objects.all()
        # print(newslatter)
        email = self.cleaned_data.get('email')
        email_str = str(email)
        if not '@' in email_str:
            raise forms.ValidationError('Please enter with "@" symbol')

        elif email:
            for mail in newslatter:
                # print(mail)
                if email_str == mail:
                    raise forms.ValidationError('Email is already exits.')
