from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from calendar import month_name
from datetime import datetime, timedelta


# ========================================
# CREATE (ADD) ENDPOINTS
# ========================================

@csrf_exempt
def add_student(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        gender = data.get('gender')
        date_of_birth = data.get('date_of_birth')
        contact = data.get('contact')
        email = data.get('email')
        university = data.get('university')
        course = data.get('course')
        year_of_study = data.get('year_of_study')

        if not all([name, gender, date_of_birth, contact, email]):
            return JsonResponse({'error': 'name, gender, date_of_birth, contact, email are required.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO students 
                (name, gender, date_of_birth, contact, email, university, course, year_of_study)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [name, gender, date_of_birth, contact, email, university, course, year_of_study])
            student_id = cursor.lastrowid

        return JsonResponse({
            'message': 'Student added successfully!',
            'student_id': student_id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def add_sponsor(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        organization_name = data.get('organization_name')
        contact_person = data.get('contact_person')
        contact = data.get('contact')
        email = data.get('email')
        address = data.get('address')

        if not all([organization_name, contact_person, contact, email, address]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO sponsors (organization_name, contact_person, contact, email, address)
                VALUES (%s, %s, %s, %s, %s)
            """, [organization_name, contact_person, contact, email, address])
            sponsor_id = cursor.lastrowid

        return JsonResponse({
            'message': 'Sponsor added successfully!',
            'sponsor_id': sponsor_id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def add_scholarship_program(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        sponsor_id = data.get('sponsor_id')
        program_name = data.get('program_name')
        amount_per_student = data.get('amount_per_student')
        duration = data.get('duration')

        if not all([sponsor_id, program_name, amount_per_student, duration]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO scholarship_programs (sponsor_id, program_name, amount_per_student, duration)
                VALUES (%s, %s, %s, %s)
            """, [sponsor_id, program_name, amount_per_student, duration])
            program_id = cursor.lastrowid

        return JsonResponse({
            'message': 'Scholarship program added successfully!',
            'program_id': program_id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def add_sponsorship_allocation(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id')
        program_id = data.get('program_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        status = data.get('status', 'Active')

        if not all([student_id, program_id, start_date, end_date]):
            return JsonResponse({'error': 'student_id, program_id, start_date, end_date are required.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO sponsorship_allocations (student_id, program_id, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s)
            """, [student_id, program_id, start_date, end_date, status])
            allocation_id = cursor.lastrowid

        return JsonResponse({
            'message': 'Sponsorship allocation added successfully!',
            'allocation_id': allocation_id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def add_payment(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        allocation_id = data.get('allocation_id')
        amount = data.get('amount')
        payment_date = data.get('payment_date')
        semester = data.get('semester')

        if not all([allocation_id, amount, payment_date, semester]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO payments (allocation_id, amount, payment_date, semester)
                VALUES (%s, %s, %s, %s)
            """, [allocation_id, amount, payment_date, semester])
            payment_id = cursor.lastrowid

        return JsonResponse({
            'message': 'Payment added successfully!',
            'payment_id': payment_id
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ========================================
# READ (LIST) ENDPOINTS
# ========================================

@csrf_exempt
def show_students(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT student_id, name, gender, date_of_birth, contact, email, university, course, year_of_study
                FROM students
            """)
            rows = cursor.fetchall()

        students = [
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
            for row in rows
        ]

        return JsonResponse({'students': students}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def show_sponsors(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT sponsor_id, organization_name, contact_person, contact, email, address
                FROM sponsors
            """)
            rows = cursor.fetchall()

        sponsors = [
            {
                'sponsor_id': row[0],
                'organization_name': row[1],
                'contact_person': row[2],
                'contact': row[3],
                'email': row[4],
                'address': row[5]
            }
            for row in rows
        ]

        return JsonResponse({'sponsors': sponsors}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def show_scholarship_programs(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT program_id, sponsor_id, program_name, amount_per_student, duration
                FROM scholarship_programs
            """)
            rows = cursor.fetchall()

        programs = [
            {
                'program_id': row[0],
                'sponsor_id': row[1],
                'program_name': row[2],
                'amount_per_student': float(row[3]) if row[3] else None,
                'duration': row[4]
            }
            for row in rows
        ]

        return JsonResponse({'scholarship_programs': programs}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def show_sponsorship_allocations(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT allocation_id, student_id, program_id, start_date, end_date, status
                FROM sponsorship_allocations
            """)
            rows = cursor.fetchall()

        allocations = [
            {
                'allocation_id': row[0],
                'student_id': row[1],
                'program_id': row[2],
                'start_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'end_date': row[4].strftime('%Y-%m-%d') if row[4] else None,
                'status': row[5]
            }
            for row in rows
        ]

        return JsonResponse({'sponsorship_allocations': allocations}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def show_payments(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT payment_id, allocation_id, amount, payment_date, semester
                FROM payments
            """)
            rows = cursor.fetchall()

        payments = [
            {
                'payment_id': row[0],
                'allocation_id': row[1],
                'amount': float(row[2]) if row[2] else None,
                'payment_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'semester': row[4]
            }
            for row in rows
        ]

        return JsonResponse({'payments': payments}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# DASHBOARD ENDPOINTS
# ========================================

@csrf_exempt
def dashboard_totals(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM students"); total_students = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM sponsors"); total_sponsors = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM scholarship_programs"); total_programs = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM sponsorship_allocations WHERE status = 'Active'"); total_active = cursor.fetchone()[0]
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM payments"); total_payments = cursor.fetchone()[0]

        return JsonResponse({
            'total_students': total_students,
            'total_sponsors': total_sponsors,
            'total_programs': total_programs,
            'total_active_allocations': total_active,
            'total_payments': float(total_payments)
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
                SELECT s.name, sp.program_name, sa.start_date
                FROM sponsorship_allocations sa
                JOIN students s ON sa.student_id = s.student_id
                JOIN scholarship_programs sp ON sa.program_id = sp.program_id
                ORDER BY sa.start_date DESC
                LIMIT 3
            """)
            rows = cursor.fetchall()

        recent = [
            {
                'student_name': row[0],
                'program_name': row[1],
                'start_date': row[2].strftime('%Y-%m-%d') if row[2] else None
            }
            for row in rows
        ]

        return JsonResponse({'recent_allocations': recent}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# UPDATE ENDPOINTS (PUT / PATCH)
# ========================================

@csrf_exempt
def update_student(request, student_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Only PUT or PATCH method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        fields = [
            'name', 'gender', 'date_of_birth', 'contact', 'email',
            'university', 'course', 'year_of_study'
        ]
        updates = []
        params = []

        for field in fields:
            value = data.get(field)
            if value is not None:
                updates.append(f"{field} = %s")
                params.append(value)

        if not updates:
            return JsonResponse({'error': 'No fields to update.'}, status=400)

        params.append(student_id)
        set_clause = ", ".join(updates)

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE students SET {set_clause} WHERE student_id = %s", params)
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Student {student_id} not found.'}, status=404)

        return JsonResponse({'message': f'Student {student_id} updated successfully!'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def update_sponsor(request, sponsor_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Only PUT or PATCH method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        fields = ['organization_name', 'contact_person', 'contact', 'email', 'address']
        updates, params = [], []

        for field in fields:
            value = data.get(field)
            if value is not None:
                updates.append(f"{field} = %s")
                params.append(value)

        if not updates:
            return JsonResponse({'error': 'No fields to update.'}, status=400)

        params.append(sponsor_id)
        set_clause = ", ".join(updates)

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE sponsors SET {set_clause} WHERE sponsor_id = %s", params)
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Sponsor {sponsor_id} not found.'}, status=404)

        return JsonResponse({'message': f'Sponsor {sponsor_id} updated!'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def update_scholarship_program(request, program_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Only PUT or PATCH method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        fields = ['sponsor_id', 'program_name', 'amount_per_student', 'duration']
        updates, params = [], []

        for field in fields:
            value = data.get(field)
            if value is not None:
                updates.append(f"{field} = %s")
                params.append(value)

        if not updates:
            return JsonResponse({'error': 'No fields to update.'}, status=400)

        params.append(program_id)
        set_clause = ", ".join(updates)

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE scholarship_programs SET {set_clause} WHERE program_id = %s", params)
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Program {program_id} not found.'}, status=404)

        return JsonResponse({'message': f'Program {program_id} updated!'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def update_sponsorship_allocation(request, allocation_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Only PUT or PATCH method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        fields = ['student_id', 'program_id', 'start_date', 'end_date', 'status']
        updates, params = [], []

        for field in fields:
            value = data.get(field)
            if value is not None:
                updates.append(f"{field} = %s")
                params.append(value)

        if not updates:
            return JsonResponse({'error': 'No fields to update.'}, status=400)

        params.append(allocation_id)
        set_clause = ", ".join(updates)

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE sponsorship_allocations SET {set_clause} WHERE allocation_id = %s", params)
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Allocation {allocation_id} not found.'}, status=404)

        return JsonResponse({'message': f'Allocation {allocation_id} updated!'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def update_payment(request, payment_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Only PUT or PATCH method allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        fields = ['allocation_id', 'amount', 'payment_date', 'semester']
        updates, params = [], []

        for field in fields:
            value = data.get(field)
            if value is not None:
                updates.append(f"{field} = %s")
                params.append(value)

        if not updates:
            return JsonResponse({'error': 'No fields to update.'}, status=400)

        params.append(payment_id)
        set_clause = ", ".join(updates)

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE payments SET {set_clause} WHERE payment_id = %s", params)
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Payment {payment_id} not found.'}, status=404)

        return JsonResponse({'message': f'Payment {payment_id} updated!'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ========================================
# DELETE ENDPOINTS
# ========================================

@csrf_exempt
def delete_student(request, student_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s", [student_id])
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Student {student_id} not found.'}, status=404)
        return JsonResponse({'message': f'Student {student_id} deleted successfully!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def delete_sponsor(request, sponsor_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sponsors WHERE sponsor_id = %s", [sponsor_id])
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Sponsor {sponsor_id} not found.'}, status=404)
        return JsonResponse({'message': f'Sponsor {sponsor_id} deleted!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def delete_scholarship_program(request, program_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM scholarship_programs WHERE program_id = %s", [program_id])
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Program {program_id} not found.'}, status=404)
        return JsonResponse({'message': f'Program {program_id} deleted!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def delete_sponsorship_allocation(request, allocation_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sponsorship_allocations WHERE allocation_id = %s", [allocation_id])
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Allocation {allocation_id} not found.'}, status=404)
        return JsonResponse({'message': f'Allocation {allocation_id} deleted!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def delete_payment(request, payment_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM payments WHERE payment_id = %s", [payment_id])
            if cursor.rowcount == 0:
                return JsonResponse({'error': f'Payment {payment_id} not found.'}, status=404)
        return JsonResponse({'message': f'Payment {payment_id} deleted!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ========================================
# ANALYTICS: SPONSORSHIP TRENDS
# ========================================

@csrf_exempt
def sponsorship_trends(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)
        
    year_param = request.GET.get('year')
    if not year_param:
        year = datetime.now().year
    else:
        try:
            year = int(year_param)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Year must be a valid integer.'}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT MONTH(start_date), COUNT(*)
                FROM sponsorship_allocations
                WHERE YEAR(start_date) = %s
                GROUP BY MONTH(start_date)
                ORDER BY MONTH(start_date)
            """, [year])
            rows = cursor.fetchall()

        trends = {i: 0 for i in range(1, 13)}
        for month, count in rows:
            trends[month] = count

        monthly = [
            {'month': month_name[i], 'new_allocations': trends[i]}
            for i in range(1, 13)
        ]

        return JsonResponse({'data': monthly, 'year': year}, status=200)

    except ValueError:
        return JsonResponse({'error': 'Year must be a valid integer.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# DASHBOARD ANALYTICS ENDPOINTS
# ========================================

@csrf_exempt
def students_by_university(request):
    """📊 Students per University (Bar Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.university, COUNT(DISTINCT s.student_id) as student_count
                FROM students s
                INNER JOIN sponsorship_allocations sa ON s.student_id = sa.student_id
                WHERE s.university IS NOT NULL
                GROUP BY s.university
                ORDER BY student_count DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'university': row[0] if row[0] else 'Unknown', 'count': row[1]}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def sponsorship_status_distribution(request):
    """🥧 Sponsorship Status Distribution (Pie Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM sponsorship_allocations
                GROUP BY status
                ORDER BY count DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'status': row[0], 'count': row[1]}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def payments_per_semester(request):
    """💰 Payments per Semester (Column Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT semester, COALESCE(SUM(amount), 0) as total_amount
                FROM payments
                WHERE semester IS NOT NULL
                GROUP BY semester
                ORDER BY semester
            """)
            rows = cursor.fetchall()

         # normalize rows into categories + series (make semester index numeric when possible)
        categories = []
        series_data = []
        raw = []
        for sem, total in rows:
            # keep the original label
            label = str(sem)
            # try to extract numeric semester index (e.g. "Semester 1" -> 1)
            sem_idx = None
            try:
                # try if sem is already numeric
                sem_idx = int(sem)
            except Exception:
                # try to parse "Semester N"
                parts = label.split()
                try:
                    sem_idx = int(parts[-1])
                except Exception:
                    sem_idx = None

            categories.append(label)
            series_data.append(float(total) if total is not None else 0.0)
            raw.append({'semester': label, 'semester_index': sem_idx, 'amount': float(total) if total is not None else 0.0})

            # return both chart-friendly and raw formats
            payload = {
                'categories': categories,
                'series': [
                    {'name': 'Payments', 'data': series_data}
                ],
                'data': raw
            }
            return JsonResponse(payload, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def sponsor_contributions(request):
    """🏛️ Sponsor Contributions (Horizontal Bar Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT sp.organization_name, COALESCE(SUM(sp2.amount_per_student), 0) as total_contribution
                FROM sponsors sp
                LEFT JOIN scholarship_programs sp2 ON sp.sponsor_id = sp2.sponsor_id
                LEFT JOIN sponsorship_allocations sa ON sp2.program_id = sa.program_id
                WHERE sa.status = 'Active' OR sa.status IS NULL
                GROUP BY sp.sponsor_id, sp.organization_name
                ORDER BY total_contribution DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'sponsor_name': row[0], 'total_amount': float(row[1])}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# DASHBOARD ANALYTICS ENDPOINTS
# ========================================

@csrf_exempt
def students_by_university(request):
    """📊 Students per University (Bar Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.university, COUNT(DISTINCT s.student_id) as student_count
                FROM students s
                INNER JOIN sponsorship_allocations sa ON s.student_id = sa.student_id
                WHERE s.university IS NOT NULL
                GROUP BY s.university
                ORDER BY student_count DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'university': row[0] if row[0] else 'Unknown', 'count': row[1]}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def sponsorship_status_distribution(request):
    """🥧 Sponsorship Status Distribution (Pie Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM sponsorship_allocations
                GROUP BY status
                ORDER BY count DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'status': row[0], 'count': row[1]}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def payments_per_semester(request):
    """💰 Payments per Semester (Column Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT semester, COALESCE(SUM(amount), 0) as total_amount
                FROM payments
                WHERE semester IS NOT NULL
                GROUP BY semester
                ORDER BY semester
            """)
            rows = cursor.fetchall()

        data = [
            {'semester': row[0], 'amount': float(row[1])}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def sponsor_contributions(request):
    """🏛️ Sponsor Contributions (Horizontal Bar Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT sp.organization_name, COALESCE(SUM(sp2.amount_per_student), 0) as total_contribution
                FROM sponsors sp
                LEFT JOIN scholarship_programs sp2 ON sp.sponsor_id = sp2.sponsor_id
                LEFT JOIN sponsorship_allocations sa ON sp2.program_id = sa.program_id
                WHERE sa.status = 'Active' OR sa.status IS NULL
                GROUP BY sp.sponsor_id, sp.organization_name
                ORDER BY total_contribution DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'sponsor_name': row[0], 'total_amount': float(row[1])}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def students_by_year(request):
    """🎓 Students by Year of Study (Bar Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.year_of_study, COUNT(DISTINCT s.student_id) as student_count
                FROM students s
                INNER JOIN sponsorship_allocations sa ON s.student_id = sa.student_id
                WHERE s.year_of_study IS NOT NULL
                GROUP BY s.year_of_study
                ORDER BY s.year_of_study
            """)
            rows = cursor.fetchall()

        data = [
            {'year_of_study': row[0], 'count': row[1]}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def gender_distribution(request):
    """👩🎓 Gender Distribution (Pie Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.gender, COUNT(DISTINCT s.student_id) as student_count
                FROM students s
                INNER JOIN sponsorship_allocations sa ON s.student_id = sa.student_id
                WHERE s.gender IS NOT NULL
                GROUP BY s.gender
                ORDER BY student_count DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'gender': row[0], 'count': row[1]}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def upcoming_end_dates(request):
    """📅 Upcoming Sponsorship End Dates (Timeline or Table)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        # Default to 6 months ahead
        months_ahead = int(request.GET.get('months', 18))
        future_date = (datetime.now() + timedelta(days=months_ahead * 30)).date()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.name, sp.program_name, sa.end_date
                FROM sponsorship_allocations sa
                JOIN students s ON sa.student_id = s.student_id
                JOIN scholarship_programs sp ON sa.program_id = sp.program_id
                WHERE sa.end_date >= CURDATE()
                AND sa.end_date <= %s
                AND sa.status = 'Active'
                ORDER BY sa.end_date ASC
            """, [future_date])
            rows = cursor.fetchall()

        data = [
            {
                'student_name': row[0],
                'program_name': row[1],
                'end_date': row[2].strftime('%Y-%m-%d') if row[2] else None
            }
            for row in rows
        ]

        return JsonResponse({'data': data, 'months_ahead': months_ahead}, status=200)

    except ValueError:
        return JsonResponse({'error': 'Months parameter must be a valid integer.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def average_scholarship_amount(request):
    """💵 Average Scholarship Amount per Sponsor (Line or Donut Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT sp.organization_name, COALESCE(AVG(sp2.amount_per_student), 0) as avg_amount
                FROM sponsors sp
                LEFT JOIN scholarship_programs sp2 ON sp.sponsor_id = sp2.sponsor_id
                GROUP BY sp.sponsor_id, sp.organization_name
                ORDER BY avg_amount DESC
            """)
            rows = cursor.fetchall()

        data = [
            {'sponsor_name': row[0], 'average_amount': float(row[1])}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def top_programs_by_funding(request):
    """🧮 Top 5 Programs by Funding (Bar Chart)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        limit = int(request.GET.get('limit', 5))
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT program_name, amount_per_student
                FROM scholarship_programs
                ORDER BY amount_per_student DESC
                LIMIT %s
            """, [limit])
            rows = cursor.fetchall()

        data = [
            {'program_name': row[0], 'amount_per_student': float(row[1])}
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except ValueError:
        return JsonResponse({'error': 'Limit parameter must be a valid integer.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# REPORT FORM ENDPOINTS
# ========================================

@csrf_exempt
def student_sponsorship_report(request):
    """a) Student Sponsorship Report - View which students are under which sponsors/programs"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        university = request.GET.get('university')
        year_of_study = request.GET.get('year_of_study')
        sponsor_id = request.GET.get('sponsor_id')

        query = """
            SELECT s.name, s.university, s.year_of_study, sp.program_name, 
                   sp2.organization_name, sa.status
            FROM sponsorship_allocations sa
            JOIN students s ON sa.student_id = s.student_id
            JOIN scholarship_programs sp ON sa.program_id = sp.program_id
            JOIN sponsors sp2 ON sp.sponsor_id = sp2.sponsor_id
            WHERE 1=1
        """
        params = []

        if university:
            query += " AND s.university = %s"
            params.append(university)

        if year_of_study:
            query += " AND s.year_of_study = %s"
            params.append(year_of_study)

        if sponsor_id:
            query += " AND sp2.sponsor_id = %s"
            params.append(sponsor_id)

        query += " ORDER BY s.name"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        data = [
            {
                'student_name': row[0],
                'university': row[1],
                'year_of_study': row[2],
                'program_name': row[3],
                'sponsor_name': row[4],
                'status': row[5]
            }
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def payment_summary_report(request):
    """b) Payment Summary Report - View payments made within a date or semester range"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        semester = request.GET.get('semester')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        query = """
            SELECT p.payment_id, s.name as student_name, p.amount, 
                   p.payment_date, p.semester
            FROM payments p
            JOIN sponsorship_allocations sa ON p.allocation_id = sa.allocation_id
            JOIN students s ON sa.student_id = s.student_id
            WHERE 1=1
        """
        params = []

        if semester:
            query += " AND p.semester = %s"
            params.append(semester)

        if start_date:
            query += " AND p.payment_date >= %s"
            params.append(start_date)

        if end_date:
            query += " AND p.payment_date <= %s"
            params.append(end_date)

        query += " ORDER BY p.payment_date DESC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        data = [
            {
                'payment_id': row[0],
                'student_name': row[1],
                'amount': float(row[2]),
                'payment_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'semester': row[4]
            }
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def sponsor_contribution_report(request):
    """c) Sponsor Contribution Report - See total contribution per sponsor"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        sponsor_id = request.GET.get('sponsor_id')

        query = """
            SELECT sp.organization_name,
                   COALESCE(SUM(sp2.amount_per_student), 0) as total_amount,
                   COUNT(DISTINCT sa.student_id) as number_of_students
            FROM sponsors sp
            LEFT JOIN scholarship_programs sp2 ON sp.sponsor_id = sp2.sponsor_id
            LEFT JOIN sponsorship_allocations sa ON sp2.program_id = sa.program_id
            WHERE 1=1
        """
        params = []

        if sponsor_id:
            query += " AND sp.sponsor_id = %s"
            params.append(sponsor_id)

        query += " GROUP BY sp.sponsor_id, sp.organization_name ORDER BY total_amount DESC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        data = [
            {
                'sponsor_name': row[0],
                'total_amount': float(row[1]),
                'number_of_students': row[2]
            }
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def scholarship_program_summary(request):
    """d) Scholarship Program Summary - Get details of all programs under each sponsor"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        sponsor_id = request.GET.get('sponsor_id')

        query = """
            SELECT sp.program_name, sp.amount_per_student, sp.duration,
                   sp2.organization_name
            FROM scholarship_programs sp
            JOIN sponsors sp2 ON sp.sponsor_id = sp2.sponsor_id
            WHERE 1=1
        """
        params = []

        if sponsor_id:
            query += " AND sp.sponsor_id = %s"
            params.append(sponsor_id)

        query += " ORDER BY sp2.organization_name, sp.program_name"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        data = [
            {
                'program_name': row[0],
                'amount_per_student': float(row[1]),
                'duration': row[2],
                'sponsor_name': row[3]
            }
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def active_completed_sponsorships(request):
    """e) Active vs Completed Sponsorships - Summarize sponsorships by status"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        status = request.GET.get('status')  # 'Active' or 'Completed'

        query = """
            SELECT s.name as student_name, sp.program_name, 
                   sa.start_date, sa.end_date, sa.status
            FROM sponsorship_allocations sa
            JOIN students s ON sa.student_id = s.student_id
            JOIN scholarship_programs sp ON sa.program_id = sp.program_id
            WHERE 1=1
        """
        params = []

        if status:
            query += " AND sa.status = %s"
            params.append(status)

        query += " ORDER BY sa.status, sa.end_date DESC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        data = [
            {
                'student_name': row[0],
                'program_name': row[1],
                'start_date': row[2].strftime('%Y-%m-%d') if row[2] else None,
                'end_date': row[3].strftime('%Y-%m-%d') if row[3] else None,
                'status': row[4]
            }
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def students_per_university_report(request):
    """f) Students per University Report - Show count of students per university"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed.'}, status=405)

    try:
        university = request.GET.get('university')

        query = """
            SELECT s.university, COUNT(DISTINCT s.student_id) as student_count
            FROM students s
            INNER JOIN sponsorship_allocations sa ON s.student_id = sa.student_id
            WHERE s.university IS NOT NULL
        """
        params = []

        if university:
            query += " AND s.university = %s"
            params.append(university)

        query += " GROUP BY s.university ORDER BY student_count DESC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        data = [
            {
                'university': row[0],
                'number_of_students': row[1]
            }
            for row in rows
        ]

        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)