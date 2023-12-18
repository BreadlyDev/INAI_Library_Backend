from .models import User, ROLES


def is_admin(user: User):
    if user.role != ROLES[0][1]:
        return False
    return True


def is_authenticated(user: User):
    if not user.is_authenticated:
        return False
    return True


def is_librarian(user: User):
    if user.role != ROLES[2][1]:
        return False
    return True


def is_student(user: User):
    if user.role != ROLES[2][1]:
        return False
    return True


def not_student(user: User):
    if user.role == ROLES[1][1]:
        return False
    return True
