# Accommodation booking service

This project is developed as one shared project for three courses:

* **Full Stack -sovelluskehitys: Frontend**  
  *(Full Stack Application Development: Frontend)*
* **Full Stack -sovelluskehitys: Backend**  
  *(Full Stack Application Development: Backend)*
* **Web-ohjelmointi ja sovelluskehykset**  
  *(Web Programming and Application Frameworks)*

Each course focuses on a different part of the same application and adds its own requirements.

---

## Full Stack -sovelluskehitys: Frontend
*(Full Stack Application Development: Frontend)*

The frontend part of the project will include:

* **Responsive views:** The application will have 5-7 functional and responsive views.
* **Accommodation filtering:** Users can filter accommodations by criteria such as location, price, or dates.
* **Booking:** Users can make a booking through the application.
* **Booking data:** Booking information is stored in application memory.
* **My bookings:** Users can view and cancel their own bookings, where applicable.
* **Main user flow:** Users can complete the main user flow without unnecessary guidance.
* **Responsive user interface:** The user interface works across different screen sizes.
* **Accessibility:** The user interface follows key WCAG accessibility principles.
* **CI build:** The project can be built in a CI environment, such as GitHub Actions.

---

## Full Stack -sovelluskehitys: Backend
*(Full Stack Application Development: Backend)*

The backend part of the project will include:

* **REST API:** Provides endpoints for searching and managing accommodations, bookings, and user accounts.
* **User management and authentication:** Users can register and log in, their identity can be verified, and access rights can be checked.
* **Booking system:** Users can create, view, and cancel their bookings, while booking business rules and data validation are handled by the backend.
* **Database:** A relational database is used and its structure is managed through database migrations.
* **Security:** Passwords are handled securely and sensitive information is protected.
* **Testing:** The project includes unit tests for business logic, controller/API tests, and integration tests using the database.
* **CI and version control:** GitHub, feature branches, Pull Requests, and automated tests are used in the CI environment.
* **Documentation:** The project includes installation and usage instructions.

---

## Web-ohjelmointi ja sovelluskehykset
*(Web Programming and Application Frameworks)*

The project will include the following main requirements:

* **Authentication and JWT:** Users can register and log in, passwords are securely hashed, and JWT tokens are used for protected API requests.
* **Database migrations:** The relational database schema is created and updated through version-controlled migrations instead of being created manually.
* **One-to-many relationship and eager loading:** An accommodation can have multiple related rooms or bookings, and related data is loaded efficiently without N+1 query problems.
* **Many-to-many relationship:** Accommodations can have multiple services or features, such as Wi-Fi, sauna, and parking, and the same service can belong to multiple accommodations.
* **Service layer:** At least three business rules that prevent an operation are implemented in the service layer rather than in controllers. For example, bookings cannot be made for past dates, overlapping bookings cannot be made for the same room, and a booking cannot be modified without the required permission.
* **Ownership-based authorization:** Users can modify or delete only their own accommodations and bookings, while an administrator can have broader permissions.
* **Interface with two implementations:** An interface-based dependency has two alternative implementations, and the implementation is selected through dependency injection registration.
* **Centralized error handling:** API errors are handled centrally without repetitive `try/catch` blocks in controllers, and the original server exception message is not returned directly to the client.
* **Documentation:** The project includes installation and usage instructions.

---

## Out of Scope

The following features and capabilities are outside the scope of the entire project:

* Real payment services and bank authentication.
* Real personal data.
* Real email notifications.
* Separate mobile application.
* Complex cloud storage.
* Production infrastructure and external commercial services.
* Large-scale administration dashboard.
* Custom policies or route guards.
* Additional unit testing requirements.

---

# Full Stack Frontend -aloitusprojekti 2026.09.01

Tämä Moodlesta ladattava lähtöprojekti on teknologianeutraali, riippuvuuksista vapaa selainkäyttöliittymä. Sen tarkoitus on varmistaa, että jokainen opiskelija voi aloittaa turvallisesti myös silloin, kun projektin varsinainen framework- tai yritysympäristö ei ole vielä käytettävissä.

## Tuettu ympäristö

- moderni selain
- Node.js 24 tai uudempi paikallista palvelinta, testejä ja build-esimerkkiä varten

## Käynnistys

```sh
npm start
```

Avaa selaimessa `http://localhost:8080`.

## Tarkistus

```sh
npm run lint
npm test
npm run build
```

Luo tiedostoista oma Git-repositorio ja tallenna ensimmäisen commitin SHA lähtötunnisteeksi. Sovita rakenne valittuun frontend-teknologiaan projektisuunnitelman hyväksymisen jälkeen.

Älä tallenna repositorioon salasanoja, tokeneita, henkilötietoja, asiakastietoja, yrityksen luottamuksellista aineistoa tai tuotantolokeja. Käytä vain synteettistä testidataa.

Lisenssi: Apache-2.0.
