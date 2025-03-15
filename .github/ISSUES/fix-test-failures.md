# Fix Test Failures in GitHub Actions

## Issue Description

The tests are failing in the GitHub Actions workflow with the following error:

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for UserInDB
disabled
  Input should be a valid boolean [type=bool_type, input_value=None, input_type=NoneType]
```

## Root Cause

There's a conflict between the two `UserInDB` models:

1. In `app/models/user.py`, `UserInDB` has `disabled: bool = False` (with a default value)
2. In `app/schemas/user.py`, `UserInDB` inherits from `User`, which inherits from `UserBase` where `disabled` is defined as `Optional[bool] = None`

## Partial Fix

We've made the following changes:

1. Updated `UserCreate` in `app/schemas/user.py` to set a default value for the `disabled` field:
   ```python
   class UserCreate(UserBase):
       email: EmailStr
       username: str
       password: str
       disabled: bool = False
   ```

2. Updated the auth endpoint to use `model_dump()` instead of the deprecated `dict()` method:
   ```python
   user_dict = user_in.model_dump()
   # ...
   result = await db.db.users.insert_one(user_db.model_dump(exclude={"id"}))
   ```

## Remaining Issues

The tests are still failing because:

1. We need to update all test files to use the correct model structure
2. We need to ensure all Pydantic models are consistent in their field definitions
3. We need to update any other occurrences of the deprecated `dict()` method

## Action Items

- [ ] Consolidate the `UserInDB` models to avoid duplication
- [ ] Update all test files to use the correct model structure
- [ ] Replace all occurrences of `dict()` with `model_dump()`
- [ ] Add more test cases to catch these issues in the future 