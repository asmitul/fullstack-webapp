# Fix Test Failures in GitHub Actions

## Issue Description

The tests were failing in the GitHub Actions workflow with the following errors:

1. First error: Pydantic validation error
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for UserInDB
disabled
  Input should be a valid boolean [type=bool_type, input_value=None, input_type=NoneType]
```

2. Second error: URL path issues
```
assert 307 == 201
 +  where 307 = <Response [307 Temporary Redirect]>.status_code
```

## Root Causes

1. **Pydantic Model Conflict**:
   - There was a conflict between the two `UserInDB` models:
     - In `app/models/user.py`, `UserInDB` has `disabled: bool = False` (with a default value)
     - In `app/schemas/user.py`, `UserInDB` inherits from `User`, which inherits from `UserBase` where `disabled` is defined as `Optional[bool] = None`

2. **URL Path Issues**:
   - The tests were using paths like `/api/v1/tasks` but the test client's `base_url` was set to `"http://test"` without accounting for the API version prefix
   - This caused 307 Temporary Redirect responses

## Fixes Applied

1. **Fixed Pydantic Model Conflict**:
   - Updated `UserCreate` in `app/schemas/user.py` to set a default value for the `disabled` field:
     ```python
     class UserCreate(UserBase):
         email: EmailStr
         username: str
         password: str
         disabled: bool = False
     ```

2. **Fixed URL Path Issues**:
   - Updated all test files to use paths without the `/api/v1` prefix:
     ```python
     # Before
     response = await async_client.post("/api/v1/tasks", ...)
     
     # After
     response = await async_client.post("/tasks", ...)
     ```

3. **Updated Deprecated Methods**:
   - Replaced all occurrences of the deprecated `dict()` method with `model_dump()`:
     ```python
     # Before
     user_dict = user_in.dict()
     result = await db.db.users.insert_one(user_db.dict(exclude={"id"}))
     
     # After
     user_dict = user_in.model_dump()
     result = await db.db.users.insert_one(user_db.model_dump(exclude={"id"}))
     ```

## Status

- [x] Fix Pydantic validation errors
- [x] Fix URL path issues in tests
- [x] Replace deprecated `dict()` method with `model_dump()`
- [x] Re-enable tests in GitHub Actions workflow

## Remaining Tasks

- [ ] Consolidate the `UserInDB` models to avoid duplication
- [ ] Add more test cases to catch these issues in the future 