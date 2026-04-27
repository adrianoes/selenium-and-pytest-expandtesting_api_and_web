API_BASE_URL = 'https://practice.expandtesting.com'
API_USERS_BASE = f'{API_BASE_URL}/notes/api/users'
API_NOTES_BASE = f'{API_BASE_URL}/notes/api/notes'
API_HEALTH_CHECK = f'{API_BASE_URL}/notes/api/health-check'

API_USERS_ENDPOINTS = {
    'CHANGE_PASSWORD': '/change-password',
    'DELETE_ACCOUNT': '/delete-account',
    'LOGIN': '/login',
    'LOGOUT': '/logout',
    'PROFILE': '/profile',
    'REGISTER': '/register',
}

API_MESSAGES = {
    'ACCESS_TOKEN_INVALID': 'Access token is not valid or has expired, you will need to login',
    'ACCOUNT_DELETED_SUCCESSFULLY': 'Account successfully deleted',
    'CATEGORY_INVALID': 'Category must be one of the categories: Home, Work, Personal',
    'LOGIN_SUCCESSFUL': 'Login successful',
    'INCORRECT_EMAIL_OR_PASSWORD': 'Incorrect email address or password',
    'INVALID_CONTENT_FORMAT': 'Invalid X-Content-Format header, Only application/json is supported.',
    'NEW_PASSWORD_BETWEEN_6_30': 'New password must be between 6 and 30 characters',
    'NOTE_COMPLETED_MUST_BE_BOOLEAN': 'Note completed status must be boolean',
    'NOTE_ID_MUST_BE_VALID': 'Note ID must be a valid ID',
    'NOTE_SUCCESSFULLY_CREATED': 'Note successfully created',
    'NOTE_SUCCESSFULLY_DELETED': 'Note successfully deleted',
    'NOTE_SUCCESSFULLY_RETRIEVED': 'Note successfully retrieved',
    'NOTE_SUCCESSFULLY_UPDATED': 'Note successfully Updated',
    'NOTES_API_RUNNING': 'Notes API is Running',
    'NOTES_SUCCESSFULLY_RETRIEVED': 'Notes successfully retrieved',
    'PROFILE_SUCCESSFUL': 'Profile successful',
    'PROFILE_UPDATED_SUCCESSFUL': 'Profile updated successful',
    'THE_PASSWORD_WAS_SUCCESSFULLY_UPDATED': 'The password was successfully updated',
    'USER_ACCOUNT_CREATED_SUCCESSFULLY': 'User account created successfully',
    'USER_HAS_BEEN_SUCCESSFULLY_LOGGED_OUT': 'User has been successfully logged out',
    'USER_NAME_BETWEEN_4_30': 'User name must be between 4 and 30 characters',
    'VALID_EMAIL_REQUIRED': 'A valid email address is required',
}
