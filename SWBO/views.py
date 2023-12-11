from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from app.models import Task, Project, Customer
from django.http import HttpResponse
from SWBO import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail

from app.models import Customer


def homepage(request):
    tasks = []
    projects = []
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        current_datetime = timezone.now()

        tasks = Task.objects.filter(
            user=request.user,
            on_date__gte=current_datetime,
            completed=False
        ).order_by('on_date')[:2]

        projects = Project.objects.filter(
            user=request.user,
            end_date__gte=current_datetime,
            completed=False
        ).order_by('end_date')[:2]

        context = {
            'customer': customer,
            'tasks': tasks,
            'projects': projects,
        }
        return render(request, 'homepage.html', context)
    else:
        return render(request, 'homepage.html')


def zadanie(request):
    return render(request, 'zadanie.html')


def baza(request):
    tasks = Task.objects.all()
    projects = Project.objects.all()
    events = list(tasks) + list(projects)
    return render(request, 'baza.html', {'events': events})


def zadania_dodaj(request):
    if request.method == 'POST':
        typ_elementu = request.POST.get('typ_elementu')
        nazwa_elementu = request.POST.get('nazwa_elementu')

        if typ_elementu == 'task':
            nowe_zadanie = Task.objects.create(
                user=request.user,
                title=nazwa_elementu,
                on_date=request.POST.get('on_date'),
                priority=request.POST.get('priority')
            )
            nowe_zadanie.save()
            messages.success(request, "Twoje zadanie zostało pomyślnie utworzone!")

        elif typ_elementu == 'project':
            nowy_projekt = Project.objects.create(
                user=request.user,
                title=nazwa_elementu,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                priority=request.POST.get('priority'),
            )
            nowy_projekt.save()
            messages.success(request, "Twój projekt został pomyślnie utworzony!")

        return HttpResponseRedirect('/zadaniaD/')

    events = []
    customer = None
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        current_datetime = timezone.now()

        tasks = Task.objects.filter(
            user=request.user,
            on_date__gte=current_datetime,
            completed=False
        ).order_by('on_date')

        projects = Project.objects.filter(
            user=request.user,
            end_date__gte=current_datetime,
            completed=False
        ).order_by('end_date')

        events = list(tasks) + list(projects)

    context = {
        'customer': customer,
        'events': events,
    }

    return render(request, 'zadaniaD.html', context)


# Widok dla usuwania zadań
def zadania_usun(request):
    if request.method == 'POST':
        item_id = request.POST.get('element_do_usuniecia')

        try:
            if Task.objects.filter(id=item_id).exists():
                item = Task.objects.get(id=item_id)
            elif Project.objects.filter(id=item_id).exists():
                item = Project.objects.get(id=item_id)
            else:
                raise ValueError("Wybrany element nie istnieje.")

            item.delete()
            messages.success(request, "Element został pomyślnie usunięty.")
        except (Task.DoesNotExist, Project.DoesNotExist):
            messages.error(request, "Wybrany element nie istnieje.")

        return HttpResponseRedirect('/zadaniaU/')

    events = []
    customer = None
    tasks = []
    projects = []

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        current_datetime = timezone.now()

        # Pobranie zadań i projektów dla aktualnie zalogowanego użytkownika
        tasks = Task.objects.filter(
            user=request.user,
            on_date__gte=current_datetime,
            completed=False
        ).order_by('on_date')

        projects = Project.objects.filter(
            user=request.user,
            end_date__gte=current_datetime,
            completed=False
        ).order_by('end_date')

        events = list(tasks) + list(projects)

    context = {
        'customer': customer,
        'events': events,
        'tasks': tasks,
        'projects': projects,  # Dodanie listy projektów do kontekstu
    }

    return render(request, 'zadaniaU.html', context)


# Widok dla wyszukiwania zadań na dany dzień
def zadania_wyszukaj(request):
    not_completed_tasks = Task.objects.filter(user=request.user, completed=False)
    not_completed_projects = Project.objects.filter(user=request.user, completed=False)

    not_completed_items = list(not_completed_tasks) + list(not_completed_projects)

    completed_tasks = Task.objects.filter(user=request.user, completed=True)
    completed_projects = Project.objects.filter(user=request.user, completed=True)

    completed_items = list(completed_tasks) + list(completed_projects)

    item = None

    if request.method == 'POST':
        element_id = request.POST.get('element_do_zakonczenia')
        password = request.POST.get('haslo_uzytkownika')

        if check_password(password, request.user.password):
            if Task.objects.filter(id=element_id).exists():
                item = get_object_or_404(Task, id=element_id)
            elif Project.objects.filter(id=element_id).exists():
                item = get_object_or_404(Project, id=element_id)
            else:
                item = None

        if item:
            item.completed = True
            item.save()
            messages.success(request, "Wydarzenie zostało oznaczone jako ukończone.")
            return redirect('/zadaniaW/')

        messages.error(request, "Nie udało się oznaczyć wydarzenia jako ukończonego.")

    context = {
        'not_completed_items': not_completed_items,
        'completed_items': completed_items,
    }

    return render(request, 'zadaniaW.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['registerUsername']
        fname = request.POST['registerName']
        lname = request.POST['registerSurname']
        email = request.POST['registerEmail']
        haslo = request.POST['registerPassword']
        phaslo = request.POST['confirmPassword']

        if len(username) > 12:
            messages.error(request, "Nazwa użytkownika może zawierać maksymalnie 12 znaków")
            return redirect('homepage')  # Przekierowanie z powrotem do formularza rejestracji

        if haslo != phaslo:
            messages.error(request, "Hasła nie są takie same")
            return redirect('homepage')  # Przekierowanie z powrotem do formularza rejestracji

        if User.objects.filter(username=username).exists():
            messages.error(request, "Użytkownik już istnieje")
            return redirect('homepage')  # Przekierowanie z powrotem do formularza rejestracji

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email został wcześniej użyty")
            return redirect('homepage')

        myuser = User.objects.create_user(username, email, haslo)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Twoje konto zostało pomyślnie utworzone!")

        customer = Customer.objects.create(
            user=myuser,
            name=fname,
            surname=lname,
            email=email
        )
        customer.save()

        #Welcome email
        #subject = 'Super, że wpadłeś na mój System Zarządzania Projektami!'
        #message = "Cześć " + myuser.first_name + "! \n" + "Nawet nie wiesz jak jestem szczęśliwy, że to działa!"
        #from_email = settings.EMAIL_HOST_USER
        #to_list = [myuser.email]
        #send_mail(subject, message, from_email, to_list, fail_silently=False)

        return redirect('signup')

    return render(request, 'signup.html')


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        avatar_url = request.POST.get('avatarURL')
        if avatar_url:
            customer = Customer.objects.get(user=request.user)
            customer.profile_image_url = avatar_url
            customer.save()
            return redirect('homepage')
        else:
            messages.error(request, "Nie podano adresu URL obrazka.")
            return redirect('homepage')

    return render(request, 'homepage.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_new_password = request.POST.get('confirmNewPassword')

        if new_password != confirm_new_password:
            messages.error(request, "Nowe hasła nie pasują do siebie.")
            return redirect('homepage')  # Zmień na nazwę widoku zmiany hasła

        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Aktualne hasło jest nieprawidłowe.")
            return redirect('homepage')  # Zmień na nazwę widoku zmiany hasła

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Utrzymuje sesję zalogowanego użytkownika
        messages.success(request, "Zmieniono hasło!")
        return redirect('homepage')  # Przekierowanie po pomyślnej zmianie hasła

    return render(request, 'homepage.html')


@login_required
def delete_account(request):
    if request.method == 'POST':
        confirm_password = request.POST.get('confirmPassword')

        # Sprawdzanie, czy potwierdzenie hasła jest poprawne
        user = authenticate(username=request.user.username, password=confirm_password)
        if user is not None:
            # Poprawne potwierdzenie hasła
            user.delete()  # Usunięcie użytkownika z bazy danych
            logout(request)  # Wylogowanie użytkownika, jeśli jest zalogowany
            messages.success(request, "Twoje konto zostało usunięte.")
            return redirect('homepage')  # Przekierowanie do strony głównej po usunięciu konta
        else:
            # Niepoprawne potwierdzenie hasła
            messages.error(request, "Nieprawidłowe potwierdzenie hasła.")
            return redirect('delete_account')  # Powrót do formularza usuwania konta

    return render(request, 'homepage.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['loginUsername']
        haslo = request.POST['loginPassword']

        user = authenticate(username=username, password=haslo)

        if user is not None:
            login(request, user)
            messages.success(request, "Zostałeś zalogowany!")
            return redirect('homepage')
        else:
            messages.error(request, "Niepoprawne dane logowania")
            return redirect('homepage')
    return render(request, 'homepage.html')


@login_required
def signout(request):
    logout(request)
    messages.success(request, "Zostałeś wylogowany!")
    return redirect('homepage')
