# Generated by Django 4.1 on 2022-10-21 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('bus_plate_no', models.CharField(db_column='busPlateNo', max_length=20, primary_key=True, serialize=False)),
                ('driver_name', models.CharField(blank=True, db_column='driverName', max_length=50, null=True)),
            ],
            options={
                'db_table': 'bus',
            },
        ),
        migrations.CreateModel(
            name='BusBookingDetails',
            fields=[
                ('bus_booking_id', models.AutoField(db_column='bus_booking_id', primary_key=True, serialize=False)),
                ('c_time', models.DateTimeField(auto_now_add=True, db_column='c_time')),
            ],
            options={
                'db_table': 'bus_booking_details',
            },
        ),
        migrations.CreateModel(
            name='busDetails',
            fields=[
                ('bus_data_id', models.AutoField(db_column='busDataId', primary_key=True, serialize=False)),
                ('route_no', models.CharField(blank=True, db_column='routeNo', default='None', max_length=10, null=True)),
                ('start_location', models.CharField(blank=True, db_column='startLocation', default='None', max_length=25, null=True)),
                ('end_location', models.CharField(blank=True, db_column='endLocation', default='None', max_length=25, null=True)),
                ('avg_run_time', models.DecimalField(blank=True, db_column='avgRunTime', decimal_places=2, max_digits=4, null=True)),
                ('route_time', models.TimeField(blank=True, db_column='routeTime', null=True)),
                ('total_distance', models.CharField(blank=True, db_column='totalDistance', max_length=10, null=True)),
                ('vehicle_status', models.BooleanField(blank=True, db_column='vehicleStatus', null=True)),
                ('contact_no', models.CharField(blank=True, db_column='contactNo', max_length=10, null=True)),
                ('other_details', models.TextField(blank=True, db_column='otherDetails', max_length=200, null=True)),
                ('bus_plate_no', models.ForeignKey(db_column='busPlateNo', on_delete=django.db.models.deletion.CASCADE, to='main.bus')),
            ],
            options={
                'db_table': 'bus_details',
            },
        ),
        migrations.CreateModel(
            name='BusSeat',
            fields=[
                ('seat_id', models.AutoField(db_column='seat_id', primary_key=True, serialize=False)),
                ('seat_no', models.IntegerField(blank=True, db_column='seat_no')),
                ('booking_status', models.BooleanField(blank=True, db_column='booking_status', null=True)),
                ('no_of_seat', models.IntegerField(blank=True, db_column='no_of_seat', null=True)),
                ('bus_plate_no', models.ForeignKey(db_column='busPlateNo', on_delete=django.db.models.deletion.CASCADE, to='main.bus')),
            ],
            options={
                'db_table': 'bus_seat',
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('userName', models.CharField(db_column='userName', max_length=20, primary_key=True, serialize=False)),
                ('firstName', models.CharField(db_column='firstName', max_length=20)),
                ('lastName', models.CharField(db_column='lastName', max_length=20, null=True)),
                ('dob', models.DateField(blank=True, db_column='dob', null=True)),
                ('email', models.EmailField(blank=True, db_column='email', max_length=50, null=True)),
                ('country', models.CharField(db_column='country', max_length=30, null=True)),
                ('passwd', models.CharField(db_column='passwd', max_length=50)),
                ('contactNo', models.CharField(blank=True, db_column='contactNo', max_length=10, null=True)),
                ('hotLine', models.CharField(blank=True, db_column='hotline', max_length=10, null=True)),
                ('otherDetails', models.CharField(blank=True, db_column='otherDetails', max_length=100, null=True)),
                ('accountStatus', models.BooleanField(blank=True, db_column='accStatus', null=True)),
            ],
            options={
                'db_table': 'owner',
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('passengerID', models.AutoField(db_column='taxiDetailId', primary_key=True, serialize=False)),
                ('nic', models.CharField(db_column='nic', max_length=12)),
                ('firstname', models.CharField(db_column='firstName', max_length=20)),
                ('lastname', models.CharField(blank=True, db_column='lastName', max_length=20, null=True)),
                ('telePhoneNo', models.CharField(blank=True, db_column='telephoneNo', max_length=10, null=True)),
                ('select_bus', models.ManyToManyField(to='main.bus')),
            ],
            options={
                'db_table': 'passenger',
            },
        ),
        migrations.CreateModel(
            name='PassengerPayment',
            fields=[
                ('payment_id', models.AutoField(db_column='payment_id', primary_key=True, serialize=False)),
                ('card_type', models.BooleanField(db_column='card_type')),
                ('total_amount', models.IntegerField(blank=True, db_column='total_amount', null=True)),
                ('description', models.TextField(blank=True, db_column='description', max_length=200, null=True)),
                ('c_time', models.DateTimeField(auto_now_add=True, db_column='c_time')),
                ('bus_booking_id', models.ForeignKey(db_column='bus_booking_id', on_delete=django.db.models.deletion.DO_NOTHING, to='main.busbookingdetails')),
                ('passengerID', models.ForeignKey(db_column='passengerID', on_delete=django.db.models.deletion.DO_NOTHING, to='main.passenger')),
            ],
            options={
                'db_table': 'passenger_payment',
            },
        ),
        migrations.CreateModel(
            name='Taxi',
            fields=[
                ('taxi_plate_no', models.CharField(db_column='taxiPlateNo', max_length=20, primary_key=True, serialize=False)),
                ('driver_name', models.CharField(blank=True, db_column='driver_name', max_length=50, null=True)),
                ('location', models.CharField(blank=True, db_column='location', max_length=40, null=True)),
                ('username', models.ForeignKey(db_column='userName', on_delete=django.db.models.deletion.CASCADE, to='main.owner')),
            ],
            options={
                'db_table': 'taxi',
            },
        ),
        migrations.CreateModel(
            name='TaxiDetails',
            fields=[
                ('taxi_detail_id', models.AutoField(db_column='taxiDetailId', primary_key=True, serialize=False)),
                ('type_of_vehicle', models.CharField(blank=True, db_column='type_of_vehicle', max_length=20, null=True)),
                ('no_of_seat', models.IntegerField(blank=True, db_column='no_of_seat', null=True)),
                ('vehicle_status', models.BooleanField(blank=True, db_column='vehicle_status', null=True)),
                ('other_details', models.TextField(blank=True, db_column='other_details', max_length=200, null=True)),
                ('taxi_plate_no', models.ForeignKey(db_column='taxi_plate_no', on_delete=django.db.models.deletion.CASCADE, to='main.taxi')),
            ],
            options={
                'db_table': 'taxi_details',
            },
        ),
        migrations.CreateModel(
            name='TaxiReceipt',
            fields=[
                ('taxi_receipt_id', models.AutoField(db_column='taxi_receipt_id', primary_key=True, serialize=False)),
                ('c_time', models.DateTimeField(auto_now_add=True, db_column='c_time')),
                ('receipt_status', models.BooleanField(db_column='receipt_status')),
                ('description', models.TextField(blank=True, db_column='description', max_length=200, null=True)),
                ('passengerID', models.ForeignKey(db_column='passengerID', on_delete=django.db.models.deletion.DO_NOTHING, to='main.passenger')),
                ('payment_id', models.ForeignKey(blank=True, db_column='payment_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.passengerpayment')),
                ('taxi_detail_id', models.ForeignKey(blank=True, db_column='taxi_detail_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.taxidetails')),
                ('taxi_plate_no', models.ForeignKey(blank=True, db_column='taxi_plate_no', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.taxi')),
            ],
            options={
                'db_table': 'taxi_receipt',
            },
        ),
        migrations.CreateModel(
            name='TaxiBookingDetails',
            fields=[
                ('taxi_book_id', models.AutoField(db_column='taxi_book_id', primary_key=True, serialize=False)),
                ('booking_time', models.DateTimeField(auto_now_add=True, db_column='booking_time')),
                ('passengerID', models.ForeignKey(blank=True, db_column='passengerID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.passenger')),
                ('taxi_detail', models.ForeignKey(db_column='taxiDetailId', on_delete=django.db.models.deletion.DO_NOTHING, to='main.taxidetails')),
                ('taxi_plate_no', models.ForeignKey(db_column='taxi_plate_no', on_delete=django.db.models.deletion.DO_NOTHING, to='main.taxi')),
            ],
            options={
                'db_table': 'taxi_booking_details',
            },
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('route_id', models.AutoField(db_column='route_id', primary_key=True, serialize=False)),
                ('c_time', models.DateField(auto_now_add=True, db_column='c_time')),
                ('bus_data_id', models.ForeignKey(db_column='busPlateId', on_delete=django.db.models.deletion.CASCADE, to='main.busdetails')),
                ('bus_plate_no', models.ForeignKey(db_column='busPlateNo', on_delete=django.db.models.deletion.CASCADE, to='main.bus')),
            ],
            options={
                'db_table': 'routes',
            },
        ),
        migrations.CreateModel(
            name='PostDestinations',
            fields=[
                ('Post_id', models.AutoField(db_column='post_id', primary_key=True, serialize=False)),
                ('head_line', models.TextField(db_column='head_line', max_length=100)),
                ('picture', models.ImageField(db_column='picture', upload_to='')),
                ('description', models.TextField(db_column='description', max_length=300)),
                ('c_time', models.DateTimeField(auto_now_add=True, db_column='current_time')),
                ('owner_name', models.ForeignKey(db_column='userName', on_delete=django.db.models.deletion.DO_NOTHING, to='main.owner')),
            ],
        ),
        migrations.AddField(
            model_name='passengerpayment',
            name='taxi_book_id',
            field=models.ForeignKey(db_column='taxi_book_id', on_delete=django.db.models.deletion.DO_NOTHING, to='main.taxibookingdetails'),
        ),
        migrations.AddField(
            model_name='passenger',
            name='userSearch_taxi',
            field=models.ManyToManyField(to='main.taxi'),
        ),
        migrations.AddField(
            model_name='passenger',
            name='userSelectRoutes',
            field=models.ManyToManyField(to='main.routes'),
        ),
        migrations.CreateModel(
            name='BusTicket',
            fields=[
                ('ticket_id', models.AutoField(db_column='ticket_id', primary_key=True, serialize=False)),
                ('total_amount', models.IntegerField(blank=True, db_column='total_amount', null=True)),
                ('company_name', models.CharField(blank=True, db_column='company_name', max_length=30, null=True)),
                ('ticket_status', models.BooleanField(db_column='ticket_status')),
                ('c_time', models.DateTimeField(auto_now_add=True, db_column='c_time')),
                ('bus_data_id', models.ForeignKey(db_column='bus_data_id', on_delete=django.db.models.deletion.DO_NOTHING, to='main.busdetails')),
                ('bus_plate_no', models.ForeignKey(db_column='bus_plate_no', on_delete=django.db.models.deletion.DO_NOTHING, to='main.bus')),
                ('passengerID', models.ForeignKey(db_column='passengerID', on_delete=django.db.models.deletion.DO_NOTHING, to='main.passenger')),
                ('payment_id', models.ForeignKey(db_column='payment_id', on_delete=django.db.models.deletion.DO_NOTHING, to='main.passengerpayment')),
                ('seat_id', models.ForeignKey(db_column='seat_id', on_delete=django.db.models.deletion.DO_NOTHING, to='main.busseat')),
            ],
            options={
                'db_table': 'bus_ticket',
            },
        ),
        migrations.AddField(
            model_name='busseat',
            name='passengerID',
            field=models.ForeignKey(db_column='passengerID', on_delete=django.db.models.deletion.CASCADE, to='main.passenger'),
        ),
        migrations.AddField(
            model_name='busbookingdetails',
            name='bus_data',
            field=models.ForeignKey(db_column='busDataId', on_delete=django.db.models.deletion.DO_NOTHING, to='main.busdetails'),
        ),
        migrations.AddField(
            model_name='busbookingdetails',
            name='bus_plate_no',
            field=models.ForeignKey(db_column='busPlateNo', max_length=20, on_delete=django.db.models.deletion.DO_NOTHING, to='main.bus'),
        ),
        migrations.AddField(
            model_name='busbookingdetails',
            name='passengerID',
            field=models.ForeignKey(db_column='passengerID', on_delete=django.db.models.deletion.DO_NOTHING, to='main.passenger'),
        ),
        migrations.AddField(
            model_name='busbookingdetails',
            name='seat_id',
            field=models.ForeignKey(db_column='seat_id', on_delete=django.db.models.deletion.DO_NOTHING, to='main.busseat'),
        ),
        migrations.AddField(
            model_name='bus',
            name='userName',
            field=models.ForeignKey(blank=True, db_column='userName', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.owner'),
        ),
    ]
