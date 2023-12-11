//logowanie i rejestracja
function showLogin() {
    // Ukrycie wszystkich sekcji i wyświetlenie sekcji logowania
    var sections = document.querySelectorAll('.user');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById('loginSection').style.display = 'flex';
    document.getElementById('registerSection').style.display = 'none';
}

function showRegister() {
    // Ukrycie wszystkich sekcji i wyświetlenie sekcji rejestracji
    var sections = document.querySelectorAll('.user');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById('registerSection').style.display = 'flex';
    document.getElementById('loginSection').style.display = 'none';
}

// Zabawy widocznoscia
function hideSection(sectionClass) {
    var sectionToHide = document.querySelector(sectionClass);
    sectionToHide.classList.add('hidden');
}

function showAvatarChange() {
    hideSection('.change-password-section');
    hideSection('.delete-account-section');

    var avatarSection = document.querySelector('.avatar');
    avatarSection.classList.remove('hidden');
}

function showChangePassword() {
    hideSection('.avatar');
    hideSection('.delete-account-section');

    var changePasswordSection = document.querySelector('.change-password-section');
    changePasswordSection.classList.remove('hidden');
}

function showPasswordConfirmation() {
    hideSection('.avatar');
    hideSection('.change-password-section');

    var deleteAccountSection = document.querySelector('.delete-account-section');
    deleteAccountSection.classList.remove('hidden');
}

function cancelChangePassword() {
    var changePasswordSection = document.querySelector('.change-password-section');
    changePasswordSection.classList.add('hidden'); // Ukrycie sekcji zmiany hasła

    var buttons = document.querySelectorAll('.buttons button:not(:last-child)'); // Znalezienie wszystkich przycisków poza ostatnim (Anuluj)
    buttons.forEach(button => {
        button.style.display = 'inline-block'; // Przywrócenie widoczności innych funkcji
    });
}

function cancelDelete() {
    var deleteAccountSection = document.querySelector('.delete-account-section');
    deleteAccountSection.classList.add('hidden'); // Ukrycie sekcji zmiany hasła

    var buttons = document.querySelectorAll('.buttons button:not(:last-child)'); // Znalezienie wszystkich przycisków poza ostatnim (Anuluj)
    buttons.forEach(button => {
        button.style.display = 'inline-block'; // Przywrócenie widoczności innych funkcji
    });
}

function cancelAvatarChange() {
    var avatarChangeSection = document.querySelector('.avatar');
    avatarChangeSection.classList.add('hidden'); // Ukrycie sekcji zmiany hasła

    var buttons = document.querySelectorAll('.buttons button:not(:last-child)'); // Znalezienie wszystkich przycisków poza ostatnim (Anuluj)
    buttons.forEach(button => {
        button.style.display = 'inline-block'; // Przywrócenie widoczności innych funkcji
    });
}

// Zabawa z wyświetlaniem strony
function toggleDarkMode() {
    var bodyElement = document.body;
    var headerElement = document.querySelector('header');
    var footerElement = document.querySelector('footer');

    var isLightModeEnabled = bodyElement.classList.contains("light-mode");

    if (isLightModeEnabled) {
        bodyElement.classList.remove("light-mode");
        headerElement.classList.remove("light-mode");
        footerElement.classList.remove("light-mode");
        localStorage.removeItem("lightModeEnabled");
    }

    bodyElement.classList.toggle("dark-mode");
    headerElement.classList.toggle("dark-mode");
    footerElement.classList.toggle("dark-mode");

    // Zapisanie preferencji trybu ciemnego w localStorage
    if (bodyElement.classList.contains("dark-mode")) {
        localStorage.setItem("darkModeEnabled", "true");
        if (isBackgroundCleared) {
            bodyElement.style.background = "linear-gradient(to right, #171818, #002325)"; // Ustaw tło na czarne lub inny kolor
        }
    } else {
        localStorage.removeItem("darkModeEnabled");
        if (isBackgroundCleared) {
            bodyElement.style.background = "linear-gradient(to right, #7a777a, #0b2534)";
        }
    }
}

// Odczytanie preferencji trybu ciemnego z localStorage i ustawienie odpowiedniego trybu
document.addEventListener("DOMContentLoaded", function () {
    var darkModeEnabled = localStorage.getItem("darkModeEnabled");

    if (darkModeEnabled) {
        document.body.classList.add("dark-mode");
        document.querySelector('header').classList.add("dark-mode");
        document.querySelector('footer').classList.add("dark-mode");
    }
});

function toggleLightMode() {
    var bodyElement = document.body;
    var headerElement = document.querySelector('header');
    var footerElement = document.querySelector('footer');

    var isDarkModeEnabled = bodyElement.classList.contains("dark-mode");

    if (isDarkModeEnabled) {
        bodyElement.classList.remove("dark-mode");
        headerElement.classList.remove("dark-mode");
        footerElement.classList.remove("dark-mode");
        localStorage.removeItem("darkModeEnabled");
    }

    bodyElement.classList.toggle("light-mode");
    headerElement.classList.toggle("light-mode");
    footerElement.classList.toggle("light-mode");

    // Zapisanie preferencji trybu jasnego w localStorage
    if (bodyElement.classList.contains("light-mode")) {
        localStorage.setItem("lightModeEnabled", "true");
        if (isBackgroundCleared) {
            bodyElement.style.background = "linear-gradient(to right, #9fa4a4, #39afbb)"; // Ustaw tło na białe lub inny kolor
        }
    } else {
        localStorage.removeItem("lightModeEnabled");
        if (isBackgroundCleared) {
            bodyElement.style.background = "linear-gradient(to right, #7a777a, #0b2534)";
        }
    }
}

// Odczytanie preferencji trybu jasnego z localStorage i ustawienie odpowiedniego trybu
document.addEventListener("DOMContentLoaded", function () {
    var lightModeEnabled = localStorage.getItem("lightModeEnabled");

    if (lightModeEnabled) {
        document.body.classList.add("light-mode");
        document.querySelector('header').classList.add("light-mode");
        document.querySelector('footer').classList.add("light-mode");
    }
});

function clearBackground() {
    isBackgroundCleared = true;

    var bodyElement = document.body;
    var clearBackgroundButton = document.querySelector('.background-zero');
    var restoreBackgroundButton = document.querySelector('.restore-background');
    var isDarkModeEnabled = bodyElement.classList.contains("dark-mode");
    var isLightModeEnabled = bodyElement.classList.contains("light-mode");

    if (isDarkModeEnabled) {
        bodyElement.style.background = "linear-gradient(to right, #171818, #002325)"; // Ustaw tło na czarne lub inny kolor
    } else if (isLightModeEnabled) {
        bodyElement.style.background = "linear-gradient(to right, #9fa4a4, #39afbb)"; // Ustaw tło na białe lub inny kolor
    } else {
        bodyElement.style.background = "linear-gradient(to right, #7a777a, #0b2534)";
    }
    clearBackgroundButton.style.display = 'none';
    restoreBackgroundButton.style.display = '';
    saveBackgroundPreference('clear');
}

function restoreBackground() {
    isBackgroundCleared = false;

    var bodyElement = document.body;
    var restoreBackgroundButton = document.querySelector('.restore-background');
    var clearBackgroundButton = document.querySelector('.background-zero');

    bodyElement.style.backgroundImage = "url('https://www.atepaa.com.pl/wp-content/uploads/2019/03/widok-z-gory-1024x724.jpg')";
    bodyElement.style.backgroundSize = "cover";
    bodyElement.style.backgroundRepeat = "no-repeat";
    bodyElement.style.backgroundAttachment = "fixed";
    restoreBackgroundButton.style.display = 'none';
    clearBackgroundButton.style.display = '';
    saveBackgroundPreference('restore');
}

function saveBackgroundPreference(background) {
    localStorage.setItem('backgroundPreference', background);
}

function applySavedBackground() {
    const savedBackground = localStorage.getItem('backgroundPreference');
    if (savedBackground === 'clear') {
        clearBackground();
    } else if (savedBackground === 'restore') {
        restoreBackground();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    applySavedBackground();
});

//Losowe zadanie
document.addEventListener("DOMContentLoaded", function () {
    var taskList = document.getElementById("taskList");
    var wiseTasks = [
        "Przebiegnij dziś 2 km na siłowni.",
        "Przeczytaj książkę w tydzień.",
        "Zlicz kalorie z dnia.",
        "Zaplanuj lekcje obcego języka.",
        "Zaplanuj wyjścia z kolegami do końca miesiąca.",
        "Zapisz swój dzisiejszy sen",
        "Napisz krótką listę rzeczy, za które jesteś wdzięczny.",
        "Znajdź i zapisz cytat, który Cię zmotywuje.",
        "Zaplanuj sobie krótką sekwencję ćwiczeń fizycznych.",
        "Spróbuj nauczyć się nowej piosenki na instrumencie muzycznym.",
        "Zapisz kilka zdrowych przepisów na posiłki.",
        "Stwórz listę filmów do obejrzenia w nadchodzącym miesiącu.",
        "Napisz krótką opowieść na podstawie jakiejś ciekawej sytuacji z Twojego życia.",
        "Znajdź i zapamiętaj kilka ciekawych faktów o zwierzętach.",
        "Poszukaj zdjęć z podróży i zapisz krótki opis ulubionego miejsca.",
        "Przeczytaj krótki artykuł z dziedziny nauki, której nie znasz dobrze.",
    ];

    // Losowanie liczby od 0 do długości tablicy - 1
    var randomIndex = Math.floor(Math.random() * wiseTasks.length);

    // Wybór losowego zadania z tablicy
    var randomTask = wiseTasks[randomIndex];

    // Wyczyszczenie listy zadań i dodanie wylosowanego zadania
    taskList.innerHTML = "<li>" + randomTask + "</li>";
    displayRandomTask();

});

// Dodawanie zadań
function showFields() {
    var selectElement = document.getElementById("typ_elementu");
    var onDateDiv = document.getElementById("on_date_div");
    var projectFieldsDiv = document.getElementById("project_fields");

    var selectedValue = selectElement.value;

    // Pokaż pola odpowiednie dla wybranej opcji
    if (selectedValue === "task") {
        onDateDiv.style.display = "block";
        projectFieldsDiv.style.display = "none";
    } else if (selectedValue === "project") {
        onDateDiv.style.display = "none";
        projectFieldsDiv.style.display = "block";
    } else {
        onDateDiv.style.display = "none";
        projectFieldsDiv.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const priorityFilter = document.getElementById('priority-filter');
    const statusFilter = document.getElementById('status-filter');
    const tasks = document.querySelectorAll('.task');

    // Filtruj zadania według priorytetu
    priorityFilter.addEventListener('change', function () {
        filterTasks();
    });

    // Filtruj zadania według statusu
    statusFilter.addEventListener('change', function () {
        filterTasks();
    });

    // Funkcja do filtrowania zadań
    function filterTasks() {
        const selectedPriority = priorityFilter.value;
        const selectedStatus = statusFilter.value;
        tasks.forEach(task => {
            const taskPriority = task.getAttribute('data-priority');
            const isCompleted = task.getAttribute('data-completed') === 'true';
            if ((selectedPriority === "" || taskPriority === selectedPriority) &&
                (selectedStatus === 'all' ||
                    (selectedStatus === 'completed' && isCompleted) ||
                    (selectedStatus === 'in-progress' && !isCompleted))) {
                task.style.display = '';
            } else {
                task.style.display = 'none';
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', (event) => {
    // Znajdź wszystkie przyciski zamknięcia w powiadomieniach
    const closeButtons = document.querySelectorAll('.alert .close');

    // Dodaj obsługę zdarzenia kliknięcia dla każdego przycisku
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Znajdź najbliższy element alert dla przycisku i ukryj go
            const messagesContainer = this.closest('.messages');
            if (messagesContainer) {
                messagesContainer.style.display = 'none';
            }
        });
    });
});