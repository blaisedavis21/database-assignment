from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json


@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        try:
            # 1️⃣ Read and decode the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))

            # 2️⃣ Extract fields from the request
            name = data.get('name')
            gender = data.get('gender')
            date_of_birth = data.get('date_of_birth')
            contact = data.get('contact')
            email = data.get('email')
            university = data.get('university')
            course = data.get('course')
            year_of_study = data.get('year_of_study')

            # 3️⃣ Basic validation (optional but useful)
            if not all([name, gender, date_of_birth, contact, email]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # 4️⃣ Insert into MySQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO students (name, gender, date_of_birth, contact, email, university, course, year_of_study)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [name, gender, date_of_birth, contact, email, university, course, year_of_study])
                student_id = cursor.lastrowid  # get the new student’s ID

            # 5️⃣ Respond with success message
            return JsonResponse({
                'message': 'Student added successfully!',
                'student_id': student_id
            }, status=201)

        except Exception as e:
            # 6️⃣ Handle any error (like missing column or bad data)
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # 7️⃣ If not POST, reject
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)


@csrf_exempt
def add_sponsor(request):
    if request.method == 'POST':
        try:
            # Read and decode JSON data
            data = json.loads(request.body.decode('utf-8'))

            # Extract fields
            organization_name = data.get('organization_name')
            contact_person = data.get('contact_person')
            contact = data.get('contact')
            email = data.get('email')
            address = data.get('address')

            # Basic validation
            if not all([organization_name, contact_person, contact, email, address]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Insert into MySQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sponsors (organization_name, contact_person, contact, email, address)
                    VALUES (%s, %s, %s, %s, %s)
                """, [organization_name, contact_person, contact, email, address])
                sponsor_id = cursor.lastrowid

            # Respond with success
            return JsonResponse({
                'message': 'Sponsor added successfully!',
                'sponsor_id': sponsor_id
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)
    

@csrf_exempt
def add_scholarship_program(request):
    if request.method == 'POST':
        try:
            # Read and decode JSON data
            data = json.loads(request.body.decode('utf-8'))

            # Extract fields
            sponsor_id = data.get('sponsor_id')
            program_name = data.get('program_name')
            amount_per_student = data.get('amount_per_student')
            duration = data.get('duration')

            # Basic validation
            if not all([sponsor_id, program_name, amount_per_student, duration]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Insert into MySQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO scholarship_programs (sponsor_id, program_name, amount_per_student, duration)
                    VALUES (%s, %s, %s, %s)
                """, [sponsor_id, program_name, amount_per_student, duration])
                program_id = cursor.lastrowid

            # Respond with success
            return JsonResponse({
                'message': 'Scholarship program added successfully!',
                'program_id': program_id
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)
    

@csrf_exempt
def add_sponsorship_allocation(request):
    if request.method == 'POST':
        try:
            # 1️⃣ Read and decode the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))

            # 2️⃣ Extract fields from the request
            student_id = data.get('student_id')
            program_id = data.get('program_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            status = data.get('status', 'Active')  # Default to 'Active' as per schema

            # 3️⃣ Basic validation (optional but useful)
            if not all([student_id, program_id, start_date, end_date]):
                return JsonResponse({'error': 'student_id, program_id, start_date, and end_date are required.'}, status=400)

            # 4️⃣ Insert into MySQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sponsorship_allocations (student_id, program_id, start_date, end_date, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, [student_id, program_id, start_date, end_date, status])
                allocation_id = cursor.lastrowid  # get the new allocation’s ID

            # 5️⃣ Respond with success message
            return JsonResponse({
                'message': 'Sponsorship allocation added successfully!',
                'allocation_id': allocation_id
            }, status=201)

        except Exception as e:
            # 6️⃣ Handle any error (like missing column or bad data)
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # 7️⃣ If not POST, reject
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)


@csrf_exempt
def add_payment(request):
    if request.method == 'POST':
        try:
            # 1️⃣ Read and decode the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))

            # 2️⃣ Extract fields from the request
            allocation_id = data.get('allocation_id')
            amount = data.get('amount')
            payment_date = data.get('payment_date')
            semester = data.get('semester')

            # 3️⃣ Basic validation (optional but useful)
            if not all([allocation_id, amount, payment_date, semester]):
                return JsonResponse({'error': 'allocation_id, amount, payment_date, and semester are required.'}, status=400)

            # 4️⃣ Insert into MySQL
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO payments (allocation_id, amount, payment_date, semester)
                    VALUES (%s, %s, %s, %s)
                """, [allocation_id, amount, payment_date, semester])
                payment_id = cursor.lastrowid  # get the new payment’s ID

            # 5️⃣ Respond with success message
            return JsonResponse({
                'message': 'Payment added successfully!',
                'payment_id': payment_id
            }, status=201)

        except Exception as e:
            # 6️⃣ Handle any error (like missing column or bad data)
            return JsonResponse({'error': str(e)}, status=400)

    else:
        # 7️⃣ If not POST, reject
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)        
    
@csrf_exempt
def show_students(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                # Query to select all students
                cursor.execute("""
                    SELECT student_id, name, gender, date_of_birth, contact, email, university, course, year_of_study
                    FROM students
                """)
                students = cursor.fetchall()

                # Format the results into a list of dictionaries
                student_list = [
                    {
                        'student_id': row[0],
                        'name': row[1],
                        'gender': row[2],
                        'date_of_birth': row[3].strftime('%Y-%m-%d') if row[3] else None,
                        'contact': row[4],
                        'email': row[5],
                        'university': row[6],
                        'course': row[7],
                        'year_of_study': row[8]
                    }
                    for row in students
                ]

                # Return the list of students
                return JsonResponse({'students': student_list}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)
    
@csrf_exempt
def show_sponsors(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT sponsor_id, organization_name, contact_person, contact, email, address
                    FROM sponsors
                """)
                sponsors = cursor.fetchall()

                sponsor_list = [
                    {
                        'sponsor_id': row[0],
                        'organization_name': row[1],
                        'contact_person': row[2],
                        'contact': row[3],
                        'email': row[4],
                        'address': row[5]
                    }
                    for row in sponsors
                ]

                return JsonResponse({'sponsors': sponsor_list}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method allowed.'}, status=405)


@csrf_exempt
def show_scholarship_programs(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT program_id, sponsor_id, program_name, amount_per_student, duration
                    FROM scholarship_programs
                """)
                programs = cursor.fetchall()

                program_list = [
                    {
                        'program_id': row[0],
                        'sponsor_id': row[1],
                        'program_name': row[2],
                        'amount_per_student': float(row[3]) if row[3] else None,
                        'duration': row[4]
                    }
                    for row in programs
                ]

                return JsonResponse({'scholarship_programs': program_list}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method allowed.'}, status=405)


@csrf_exempt
def show_sponsorship_allocations(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT allocation_id, student_id, program_id, start_date, end_date, status
                    FROM sponsorship_allocations
                """)
                allocations = cursor.fetchall()

                allocation_list = [
                    {
                        'allocation_id': row[0],
                        'student_id': row[1],
                        'program_id': row[2],
                        'start_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                        'end_date': row[4].strftime('%Y-%m-%d') if row[4] else None,
                        'status': row[5]
                    }
                    for row in allocations
                ]

                return JsonResponse({'sponsorship_allocations': allocation_list}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method allowed.'}, status=405)


@csrf_exempt
def show_payments(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT payment_id, allocation_id, amount, payment_date, semester
                    FROM payments
                """)
                payments = cursor.fetchall()

                payment_list = [
                    {
                        'payment_id': row[0],
                        'allocation_id': row[1],
                        'amount': float(row[2]) if row[2] else None,
                        'payment_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                        'semester': row[4]
                    }
                    for row in payments
                ]

                return JsonResponse({'payments': payment_list}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET method allowed.'}, status=405)


@csrf_exempt
def dashboard_totals(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            # Total students
            cursor.execute("SELECT COUNT(*) FROM students")
            total_students = cursor.fetchone()[0]

            # Total sponsors
            cursor.execute("SELECT COUNT(*) FROM sponsors")
            total_sponsors = cursor.fetchone()[0]

            # Total scholarship programs
            cursor.execute("SELECT COUNT(*) FROM scholarship_programs")
            total_programs = cursor.fetchone()[0]

            # Total active allocations
            cursor.execute("SELECT COUNT(*) FROM sponsorship_allocations WHERE status = 'Active'")
            total_active_allocations = cursor.fetchone()[0]

            # Total payments
            cursor.execute("SELECT SUM(amount) FROM payments")
            total_payments = cursor.fetchone()[0] or 0  # Handle NULL sum

        return JsonResponse({
            'total_students': total_students,
            'total_sponsors': total_sponsors,
            'total_programs': total_programs,
            'total_active_allocations': total_active_allocations,
            'total_payments': float(total_payments) if total_payments else 0.0
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def show_recent_allocations(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s.name AS student_name,
                    sp.program_name,
                    sa.start_date
                FROM sponsorship_allocations sa
                JOIN students s ON sa.student_id = s.student_id
                JOIN scholarship_programs sp ON sa.program_id = sp.program_id
                ORDER BY sa.start_date DESC
                LIMIT 3
            """)
            rows = cursor.fetchall()

        recent_allocations = []
        for row in rows:
            recent_allocations.append({
                'student_name': row[0],
                'program_name': row[1],
                'start_date': row[2].strftime('%Y-%m-%d') if row[2] else None
            })

        return JsonResponse({'recent_allocations': recent_allocations}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)    
    

#editing students
@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE student_id = %s", [student_id])

            return JsonResponse({'message': f'Student {student_id} deleted successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

#deleting students

@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE student_id = %s", [student_id])

            return JsonResponse({'message': f'Student {student_id} deleted successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)


# --------------------------------------------
# UPDATE APIS
# --------------------------------------------

@csrf_exempt
def update_sponsor(request, sponsor_id):
    """Update sponsor information by sponsor_id"""
    if request.method in ['PUT', 'POST']:
        try:
            data = json.loads(request.body.decode('utf-8'))
            organization_name = data.get('organization_name')
            contact_person = data.get('contact_person')
            contact = data.get('contact')
            email = data.get('email')
            address = data.get('address')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE sponsors SET
                        organization_name = COALESCE(%s, organization_name),
                        contact_person = COALESCE(%s, contact_person),
                        contact = COALESCE(%s, contact),
                        email = COALESCE(%s, email),
                        address = COALESCE(%s, address)
                    WHERE sponsor_id = %s
                """, [organization_name, contact_person, contact, email, address, sponsor_id])

            return JsonResponse({'message': f'Sponsor {sponsor_id} updated successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only PUT or POST method allowed.'}, status=405)

@csrf_exempt
def update_scholarship_program(request, program_id):
    """Update scholarship program by program_id"""
    if request.method in ['PUT', 'POST']:
        try:
            data = json.loads(request.body.decode('utf-8'))
            sponsor_id = data.get('sponsor_id')
            program_name = data.get('program_name')
            amount_per_student = data.get('amount_per_student')
            duration = data.get('duration')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE scholarship_programs SET
                        sponsor_id = COALESCE(%s, sponsor_id),
                        program_name = COALESCE(%s, program_name),
                        amount_per_student = COALESCE(%s, amount_per_student),
                        duration = COALESCE(%s, duration)
                    WHERE program_id = %s
                """, [sponsor_id, program_name, amount_per_student, duration, program_id])

            return JsonResponse({'message': f'Program {program_id} updated successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only PUT or POST method allowed.'}, status=405)

@csrf_exempt
def update_sponsorship_allocation(request, allocation_id):
    """Update sponsorship allocation by allocation_id"""
    if request.method in ['PUT', 'POST']:
        try:
            data = json.loads(request.body.decode('utf-8'))
            student_id = data.get('student_id')
            program_id = data.get('program_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            status = data.get('status')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE sponsorship_allocations SET
                        student_id = COALESCE(%s, student_id),
                        program_id = COALESCE(%s, program_id),
                        start_date = COALESCE(%s, start_date),
                        end_date = COALESCE(%s, end_date),
                        status = COALESCE(%s, status)
                    WHERE allocation_id = %s
                """, [student_id, program_id, start_date, end_date, status, allocation_id])

            return JsonResponse({'message': f'Allocation {allocation_id} updated successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only PUT or POST method allowed.'}, status=405)

@csrf_exempt
def update_payment(request, payment_id):
    """Update payment information by payment_id"""
    if request.method in ['PUT', 'POST']:
        try:
            data = json.loads(request.body.decode('utf-8'))
            allocation_id = data.get('allocation_id')
            amount = data.get('amount')
            payment_date = data.get('payment_date')
            semester = data.get('semester')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE payments SET
                        allocation_id = COALESCE(%s, allocation_id),
                        amount = COALESCE(%s, amount),
                        payment_date = COALESCE(%s, payment_date),
                        semester = COALESCE(%s, semester)
                    WHERE payment_id = %s
                """, [allocation_id, amount, payment_date, semester, payment_id])

            return JsonResponse({'message': f'Payment {payment_id} updated successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only PUT or POST method allowed.'}, status=405)

# --------------------------------------------
# DELETE APIS
# --------------------------------------------

@csrf_exempt
def delete_sponsor(request, sponsor_id):
    """Delete a sponsor by sponsor_id"""
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sponsors WHERE sponsor_id = %s", [sponsor_id])
            return JsonResponse({'message': f'Sponsor {sponsor_id} deleted successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

@csrf_exempt
def delete_scholarship_program(request, program_id):
    """Delete a scholarship program by program_id"""
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM scholarship_programs WHERE program_id = %s", [program_id])
            return JsonResponse({'message': f'Program {program_id} deleted successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

@csrf_exempt
def delete_sponsorship_allocation(request, allocation_id):
    """Delete a sponsorship allocation by allocation_id"""
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sponsorship_allocations WHERE allocation_id = %s", [allocation_id])
            return JsonResponse({'message': f'Allocation {allocation_id} deleted successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

@csrf_exempt
def delete_payment(request, payment_id):
    """Delete a payment by payment_id"""
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM payments WHERE payment_id = %s", [payment_id])
            return JsonResponse({'message': f'Payment {payment_id} deleted successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)