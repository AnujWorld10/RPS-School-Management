
# RPS School Management System — API Documentation

Welcome to the RPS School Management System API! This documentation is designed for both beginners and experienced developers. It covers authentication, user roles, endpoints, request/response formats, error handling, and practical usage examples.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Authentication & Authorization](#authentication--authorization)
3. [User Roles](#user-roles)
4. [API Endpoints Overview](#api-endpoints-overview)
5. [Detailed Endpoint Reference](#detailed-endpoint-reference)
6. [Request & Response Examples](#request--response-examples)
7. [Error Handling](#error-handling)
8. [Best Practices & Notes](#best-practices--notes)

---

## Introduction
The RPS School Management System API is a RESTful backend built with FastAPI. It manages users, students, teachers, classes, fees, and administrative operations for a school. All endpoints use JSON for requests and responses. Authentication is handled via JWT tokens.

---

## Authentication & Authorization
- **Authentication:** Uses JWT (JSON Web Token) for secure access.
- **How it works:**
  1. User logs in with username and password.
  2. Server returns a JWT access token.
  3. Client includes this token in the `Authorization` header for all protected requests.
- **Header format:**
  ```
  Authorization: Bearer <access_token>
  ```
- **Token Expiry:** Tokens expire after a set time (default: 30 minutes).

---

## User Roles
| Role         | Description                | Permissions                                  |
|--------------|----------------------------|-----------------------------------------------|
| ADMIN        | School administrator       | Full access to all endpoints                  |
| TEACHER      | School teacher             | Manage/view students, limited admin actions   |
| STUDENT      | School student             | (Future) View own data, limited endpoints     |
| OFFICE_STAFF | Office staff (future use)  | (Planned)                                    |

---

## API Endpoints Overview

| Method | Path                        | Description                | Auth Required | Roles Allowed         |
|--------|-----------------------------|----------------------------|---------------|----------------------|
| POST   | /api/v1/auth/login          | User login (get token)     | No            | All                  |
| POST   | /api/v1/auth/register       | Register new user          | Sometimes*    | ADMIN/First user     |
| GET    | /api/v1/students/           | List all students          | Yes           | ADMIN, TEACHER       |
| POST   | /api/v1/students/           | Add a new student          | Yes           | ADMIN, TEACHER       |
| GET    | /api/v1/teachers/           | List all teachers          | Yes           | ADMIN                |
| POST   | /api/v1/teachers/           | Add a new teacher          | Yes           | ADMIN                |
| GET    | /api/v1/classes/            | List all classes           | Yes           | ADMIN, TEACHER       |
| POST   | /api/v1/classes/            | Add a new class            | Yes           | ADMIN                |
| POST   | /api/v1/admin/fees          | Add a fee record           | Yes           | ADMIN                |

*Registration is open only for the first user. After that, only ADMINs can register new users.*

---

## Detailed Endpoint Reference

### 1. Authentication

#### POST `/api/v1/auth/login`
- **Purpose:** Log in and receive an access token.
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "<JWT>",
    "token_type": "bearer"
  }
  ```
- **Errors:** 401 (Invalid credentials), 400, 500

#### POST `/api/v1/auth/register`
- **Purpose:** Register a new user (see note above).
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "role": "ADMIN|TEACHER|STUDENT"
  }
  ```
- **Response:**
  ```json
  {
    "id": "Rps_XXXXX",
    "username": "string",
    "email": "string",
    "role": "string",
    "is_active": true,
    "generated_password": "RPS-xxxxxx"
  }
  ```
- **Errors:** 401 (if not ADMIN after first user), 400, 500

---

### 2. Students

#### GET `/api/v1/students/`
- **Purpose:** List all students.
- **Auth:** ADMIN, TEACHER
- **Response:** Array of students:
  ```json
  [
    {
      "id": "Rps_XXXXX",
      "user_id": "Rps_XXXXX",
      "class_id": "Rps_XXXXX",
      "name": "Jane Doe",
      "roll_number": "R-001",
      "class_name": "10A"
    },
    ...
  ]
  ```

#### POST `/api/v1/students/`
- **Purpose:** Add a new student.
- **Auth:** ADMIN, TEACHER
- **Request Body:**
  ```json
  {
    "user_id": "Rps_XXXXX",
    "class_id": "Rps_XXXXX",
    "name": "Jane Doe",
    "roll_number": "R-001",
    "admission_date": "2024-06-01",
    "address": "123 Main St",
    "phone": "1234567890",
    "email": "jane@example.com"
  }
  ```
- **Response:**
  ```json
  {
    "id": "Rps_XXXXX",
    "user_id": "Rps_XXXXX",
    "class_id": "Rps_XXXXX",
    "name": "Jane Doe",
    "roll_number": "R-001",
    "class_name": "10A"
  }
  ```
- **Errors:** 400 (duplicate roll number), 401, 403

#### GET `/api/v1/students/{student_id}`
- **Purpose:** Get a student by ID.
- **Auth:** ADMIN, TEACHER
- **Response:**
  ```json
  {
    "id": "Rps_XXXXX",
    "user_id": "Rps_XXXXX",
    "class_id": "Rps_XXXXX",
    "name": "Jane Doe",
    "roll_number": "R-001",
    "class_name": "10A"
  }
  ```
- **Errors:** 404 (not found), 401, 403

---

### 3. Teachers

#### GET `/api/v1/teachers/`
- **Purpose:** List all teachers.
- **Auth:** ADMIN
- **Response:** Array of teachers:
  ```json
  [
    {
      "id": "Rps_XXXXX",
      "name": "Mr. Smith",
      "subject": "Mathematics"
    },
    ...
  ]
  ```

#### POST `/api/v1/teachers/`
- **Purpose:** Add a new teacher.
- **Auth:** ADMIN
- **Request Body:**
  ```json
  {
    "user_id": "Rps_XXXXX",
    "subject_id": "001",
    "name": "Mr. Smith",
    "joining_date": "2024-06-01",
    "salary": 50000,
    "qualifications": "MSc Mathematics"
  }
  ```
- **Response:**
  ```json
  {
    "id": "Rps_XXXXX",
    "name": "Mr. Smith",
    "subject": "Mathematics"
  }
  ```
- **Errors:** 400, 403, 500

#### GET `/api/v1/teachers/{teacher_id}`
- **Purpose:** Get a teacher by ID.
- **Auth:** ADMIN
- **Response:**
  ```json
  {
    "id": "Rps_XXXXX",
    "name": "Mr. Smith",
    "subject": "Mathematics"
  }
  ```
- **Errors:** 404 (not found), 401, 403

---

### 4. Classes

#### GET `/api/v1/classes/`
- **Purpose:** List all classes.
- **Auth:** ADMIN, TEACHER
- **Response:** Array of classes:
  ```json
  [
    {
      "id": "Rps_XXXXX",
      "name": "10A",
      "section": "A",
      "description": "Science stream",
      "class_teacher_id": "Rps_XXXXX"
    },
    ...
  ]
  ```

#### POST `/api/v1/classes/`
- **Purpose:** Add a new class.
- **Auth:** ADMIN
- **Request Body:**
  ```json
  {
    "name": "10A",
    "section": "A",
    "description": "Science stream",
    "class_teacher_id": "Rps_XXXXX"
  }
  ```
- **Response:**
  ```json
  {
    "id": "Rps_XXXXX",
    "name": "10A",
    "section": "A",
    "description": "Science stream",
    "class_teacher_id": "Rps_XXXXX"
  }
  ```
- **Errors:** 400, 401, 403

---

### 5. Admin: Fees

#### POST `/api/v1/admin/fees`
- **Purpose:** Add a fee record for a student.
- **Auth:** ADMIN
- **Request Body:**
  ```json
  {
    "student_id": "Rps_XXXXX",
    "amount": 1000.0,
    "month": "June",
    "status": "Paid",
    "due_date": "2024-06-30"
  }
  ```
- **Response:**
  ```json
  { "message": "Fee added" }
  ```
- **Errors:** 400, 401, 403

---

## Request & Response Examples

### Login and Use Token
```sh
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"secret"}'
# Response: { "access_token": "<JWT>" }

curl -X POST http://localhost:8000/api/v1/students/ \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"Rps_XXXXX","class_id":"Rps_XXXXX","name":"Jane Doe","roll_number":"R-001","admission_date":"2024-06-01","address":"123 Main St","phone":"1234567890","email":"jane@example.com"}'
```

### TypeScript Example
```ts
const token = response.access_token;
axios.post('/api/v1/students/', data, { headers: { Authorization: `Bearer ${token}` } });
```

---

## Error Handling
- **400 Bad Request:** Validation or business logic errors (e.g., duplicate username).
- **401 Unauthorized:** Missing or invalid token, or invalid credentials.
- **403 Forbidden:** Authenticated but insufficient permissions for the action.
- **500 Internal Server Error:** Unexpected server or database errors.

---

## Best Practices & Notes
- Always keep your JWT token secure; never share it publicly.
- Use the correct role for each action (e.g., only ADMIN can add teachers).
- For first-time setup, register the first user without a token; after that, only ADMINs can register new users.
- All dates should be in `YYYY-MM-DD` format.
- For more details, see the backend source code or contact the project maintainer.

---

*Happy coding!*
