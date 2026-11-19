# Frontend Review and Application Views

## 1. Purpose

This document provides a technical review of the existing frontend starter project and defines the planned application views for the **Accommodation Booking Service** (a personal frontend project modeled after a Booking.com-style web interface).

The goal of the frontend application is to provide a clear, fast, and accessible browser interface where users can search for accommodations, compare options, view property details, simulate a booking, and manage their own reservations using local mock data and in-memory/browser state.

---

## 2. Starter Frontend Review

### Existing Project Structure

- **Framework / Library:** Vanilla JavaScript (ES Modules `.mjs` — no UI framework like React or Vue is installed yet; migration to React + TypeScript + Vite is planned in the project roadmap).
- **Programming Language:** JavaScript (ES Modules) & HTML5.
- **Build & Dev Tooling:** Custom Node.js scripts (`build.mjs`, `server.mjs`, `lint.mjs`) configured in `package.json` (no Vite or bundler configured yet).
- **Routing Solution:** None (single-page static entry via `index.html` and `app.mjs`).
- **Existing Pages and Components:**
  - `index.html` — basic HTML entry template.
  - `app.mjs` — starter client-side JavaScript logic.
  - `server.mjs` — lightweight local development server.
  - `build.mjs` & `lint.mjs` — basic build and linting scripts.
  - `app.test.mjs` — starter unit test file.
  - Project documentation & quality templates (`accessibility-checklist.md`, `adr-template.md`, `ai-use-log.md`, `personal-evidence-index.md`, `sprint-review-template.md`, `team-agreement.md`, `user-test-template.md`).
- **Styling Approach:** Plain CSS (`styles.css`).

### Current Implementation

The repository currently contains a minimal, framework-free starter template (`index.html`, `app.mjs`, `styles.css`, `server.mjs`) along with basic build, lint, and test scripts (`package.json`) and structured course documentation templates. It serves as an initial CI-ready skeleton to verify linting, testing, and building workflows.

### Missing Functionality

- **UI Framework & Tooling Setup:** React, TypeScript, and Vite environment setup (as defined in the project technology stack).
- **Client-Side Routing:** Navigation and URL routing between distinct application views.
- **Application Views:** None of the 6 core booking views have been implemented yet.
- **Mock Data & State Management:** Local dataset of accommodations and in-memory/client-side CRUD state management for user bookings.
- **Reusable UI Components:** Search bars, filter panels, accommodation cards, forms, and feedback/modal components.
- **Form Validation & Error Handling:** Input validation for search dates, guest counts, and booking forms.

---

## 3. Planned Application Views

Based on **Concept A (Traditional Search & Card-List Flow)** selected in the project concept plan, the application will consist of **6 main functional views** that cover the complete accommodation booking journey without requiring a real backend or user authentication system:

| # | View | Route | Purpose |
|---|---|---|---|
| 1 | **Home & Search** | `/` | Entry point to start searching by destination, dates, and guests, plus browse featured stays |
| 2 | **Search Results** | `/accommodations` | Browse, filter, and sort matching accommodations in a comparable card list |
| 3 | **Accommodation Details** | `/accommodations/:id` | Inspect full property information, photos, amenities, reviews, and total price |
| 4 | **Booking Form** | `/accommodations/:id/book` | Enter guest contact details, review price breakdown, and submit a simulated booking |
| 5 | **Booking Confirmation** | `/booking-confirmation/:bookingId` | Display reservation summary, unique booking reference number, and next actions |
| 6 | **My Bookings** | `/my-bookings` | View, inspect, and cancel existing reservations stored in browser state |

---

## 4. View Functionality

### 4.1 Home & Search (`/`)
- Provide a prominent search bar for **destination/location**, **check-in and check-out dates**, and **number of guests**.
- Validate search inputs (e.g., prevent check-out dates earlier than check-in).
- Display popular destinations or featured accommodation previews for quick exploration.
- Navigate to the Search Results view with applied query parameters.

### 4.2 Search Results (`/accommodations`)
- Display matching accommodations as a structured, keyboard-accessible **card list** (per architectural decision ADR-1).
- Filter accommodations by **price range**, **location/distance**, **property type**, and **key amenities**.
- Sort results by **price (lowest/highest first)**, **rating (highest first)**, and **number of reviews**.
- Allow modifying search criteria without losing previously selected filters unnecessarily.
- Navigate to the Accommodation Details view when a user selects a property card.

### 4.3 Accommodation Details (`/accommodations/:id`)
- Display property title, location, star/guest rating, and detailed description.
- Display photo gallery and list of available amenities/house rules.
- Show clear **total price calculation** based on selected dates and number of nights before proceeding.
- Provide a clear primary call-to-action button (**"Book Now"**) leading to the Booking Form.

### 4.4 Booking Form (`/accommodations/:id/book`)
- Display a summary of the selected accommodation, check-in/check-out dates, guest count, and total cost.
- Provide input fields for synthetic guest details (full name, email address, phone number, optional special requests).
- Perform client-side validation with clear, actionable inline error messages.
- Simulate booking submission (no real payment processing or bank authentication) and save the reservation to client state.

### 4.5 Booking Confirmation (`/booking-confirmation/:bookingId`)
- Confirm that the simulated reservation succeeded with clear visual feedback.
- Display a generated **booking reference number**, property summary, dates, and total price.
- Provide direct navigation buttons to **My Bookings** or back to **Home & Search**.

### 4.6 My Bookings (`/my-bookings`)
- List all reservations created during the session / stored in browser memory (`localStorage` / React state).
- Display key details for each booking: accommodation name, dates, total price, and current status (e.g., *Confirmed*, *Cancelled*).
- Allow users to view booking details or **cancel a reservation** with a confirmation step before changing its status.
- Display a clear empty state with a call-to-action to search for accommodations when no bookings exist.

---

## 5. Shared UI Components & Design System Foundation

To ensure visual consistency and maintainability across all views, the following reusable components and states are planned:

| Component | Purpose | Defined States |
|---|---|---|
| **Header & Navigation** | Brand logo, primary links (`Home`, `Search`, `My Bookings`), active route indicator | Default, hover, focus-visible, active |
| **Footer** | Project scope notice (simulated prototype), secondary navigation links | Default |
| **Button** | Primary actions (`Search`, `Book Now`, `Confirm`, `Cancel Booking`) | Default, hover, focus-visible, active, disabled, loading |
| **Link** | Inline navigation and secondary details | Default, hover, focus-visible, active |
| **Form Input / Select** | Location, date pickers, guest counters, and booking form fields | Default, focus-visible, disabled, loading, success, error |
| **Accommodation Card** | Property thumbnail, title, location, rating, nightly/total price, CTA | Default, hover, focus-visible, selected |
| **Filter & Sort Panel** | Price range, rating, amenities filters, and sort selector | Default, active filters applied, reset |
| **Feedback Banner / Toast** | Search, validation, and booking process notifications | Success, warning, error, loading |
| **Confirmation Modal** | Confirming destructive actions such as cancelling a booking | Default, loading, success, error |

---

## 6. Main User Journey & Exception Flows

### Primary User Journey
1. **Home & Search (`/`):** User enters destination, check-in/check-out dates, and guest count.
2. **Search Results (`/accommodations`):** User compares property cards, applies price/rating filters, and selects an accommodation.
3. **Accommodation Details (`/accommodations/:id`):** User reviews photos, amenities, and total price, then clicks **Book Now**.
4. **Booking Form (`/accommodations/:id/book`):** User enters synthetic contact details and submits the booking form.
5. **Booking Confirmation (`/booking-confirmation/:bookingId`):** User reviews the confirmed reservation summary and booking ID.
6. **My Bookings (`/my-bookings`):** User views their active reservations and can cancel a booking if needed.

### Planned Exception Flows
- **No Search Results:** Display a helpful empty state suggesting broader dates or resetting filters.
- **Invalid Date Selection:** Prevent search/booking submission and display a clear inline explanation.
- **Invalid Form Input:** Highlight missing or malformed fields and focus user attention on how to fix them.
- **Simulated Booking Failure:** Show a non-destructive error banner while preserving entered form values.
- **Booking Cancellation:** Require explicit user confirmation via modal/dialog before updating booking status.

---

## 7. UI States

Every view will explicitly handle the following interface states:
- **Loading:** Visual feedback while fetching/filtering mock data or processing a simulated booking.
- **Success:** Clear presentation of search results, property details, or booking confirmation.
- **Empty:** Informative guidance when no accommodations match filters or when `My Bookings` is empty.
- **Error:** Actionable error alerts when simulated network/storage operations fail.
- **Validation:** Field-level error indicators and instructions for invalid form inputs.

---

## 8. Non-Functional Requirements

### Visual & Layout System
- **Color Palette & Contrast:** Light surfaces (white/light gray) with dark text and blue/orange accents; targets **WCAG 2.2 AA** contrast ratios ($\ge 4.5:1$ for normal text, $\ge 3:1$ for large text).
- **Spacing & Grid:** 4 px base spacing scale (`4, 8, 16, 24, 32, 48 px`), centered container (`max-width: 1200 px`), Flexbox for component alignment, and CSS Grid for card layouts.

### Responsive Design
- Desktop-first layout with responsive breakpoints at `640px`, `768px`, and `1024px` so core search, detail, booking, and management flows remain usable across desktop, tablet, and mobile viewports.

### Accessibility & Motion
- Semantic HTML5 landmarks (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`), explicit `<label>` associations for all form inputs, full keyboard navigation with visible focus indicators, and respect for `prefers-reduced-motion`.

---

## 9. Scope Boundaries

- **In Scope:** Client-side accommodation search, filtering, sorting, detailed property inspection, simulated booking creation, booking confirmation, and in-memory/browser-persisted booking management (CRUD).
- **Out of Scope:** Production backend server, real database persistence, real payment gateways or bank authentication, real user registration/login authentication systems, administrative dashboards, and real personal data (only synthetic test data is used).

---

## 10. Conclusion

The existing starter frontend has been reviewed, and six functional application views aligned with the project concept (**Concept A**) have been defined. This specification establishes the architectural foundation, component list, user flows, and quality criteria for the upcoming frontend implementation sprints.
