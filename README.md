# Accommodation booking service

This project is developed as one shared project for three courses:
* Full Stack -sovelluskehitys: Frontend
* Full Stack -sovelluskehitys: Backend
* Web-ohjelmointi ja sovelluskehykset
Each course focuses on a different part of the same application and adds its own requirements.

---

## Full Stack -sovelluskehitys: Frontend (Full Stack Application Development: Frontend)

The frontend part of the project will include:

- A responsive Booking.com-style web user interface.
- 5–7 main views for the accommodation booking process.
- Accommodation search with filters such as location, price, dates and rating.
- Accommodation search results with sorting and filtering.
- Accommodation detail pages with information, images and reviews.
- A booking form with input validation.
- Simulated booking confirmation and booking number.
- A "My Bookings" view for viewing and managing the user's bookings.
- Client-side state management and CRUD operations for bookings.
- Responsive design for mobile and desktop screen sizes.
- Accessible user interface following key WCAG principles.
- Error states and user-friendly error messages.
- Frontend testing.
- CI build and code quality checks.
- Documentation and version control using Git and GitHub.

---

## Full Stack -sovelluskehitys: Backend (Full Stack Application Development: Backend)

The backend part of the project will include:

- A REST API for searching and managing accommodation data.
- Accommodation and booking management through API endpoints.
- User registration, login and authentication.
- Secure password hashing and user authentication.
- Authorization and access control.
- A relational database for storing application data.
- Database schema management using version-controlled migrations.
- Booking creation, viewing and cancellation.
- Validation of booking data and business rules.
- Protection of sensitive user information.
- Unit tests for business logic.
- Controller/API tests.
- Integration tests using the database.
- Git version control, feature branches and Pull Requests.
- Automated tests in the CI environment.
- Installation, configuration and usage documentation.

---

## Web-ohjelmointi ja sovelluskehykset (Web Programming and Application Frameworks)

The web programming and application framework part of the project will demonstrate:

- User registration and authentication using JWT.
- Secure password hashing.
- Database migrations managed through version control.
- One-to-many relationships with appropriate data loading.
- Many-to-many relationships between accommodations and services/features.
- A service layer containing business rules outside the controllers.
- At least three booking-related business rules.
- Ownership-based authorization for modifying and deleting resources.
- Interface-based dependency injection with two alternative implementations.
- Centralized API error handling.
- Clean separation between controllers, services and data access.
- Installation and usage documentation.

---

## Out of Scope

The following features and capabilities are outside the scope of the project:

- Real payment gateways and real payment transactions.
- Real email notification services.
- A large-scale administration dashboard.
- Complex cloud-based image storage.
- Production-grade infrastructure and deployment to commercial cloud services.
- A separate native mobile application.
- Real personal or sensitive user data; the project uses synthetic/test data.
- A custom authorization policy or route guard beyond the planned role- and ownership-based authorization.
- A separate, comprehensive unit-test coverage-reporting system beyond the testing requirements defined for the other project components.

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
