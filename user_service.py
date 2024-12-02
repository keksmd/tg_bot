from sqlalchemy import select

from models import User


class UserService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_by_telegram_id(self, telegram_id):
        with self.session_factory() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            user = session.execute(stmt).scalars().first()
            return user

    def get_by_itmo_id(self, itmo_id):
        with self.session_factory() as session:
            stmt = select(User).where(User.itmo_id == itmo_id)
            user = session.execute(stmt).scalars().first()
            return user

    def get_admins(self):
        with self.session_factory() as session:
            stmt = select(User).where(User.is_admin == True)
            admins = session.execute(stmt).scalars().all()
            return admins

    def create_user(self, telegram_id, username=None):
        with self.session_factory() as session:
            existing_user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not existing_user:
                new_user = User(telegram_id=telegram_id, username=username)
                session.add(new_user)
                session.commit()
                return new_user
            return existing_user

    def is_verified(self, telegram_id):
        with self.session_factory() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if user is None:
                raise UserNotFoundException('Пользователь не найден')
            return user.verified

    def verify_user(self, telegram_id, itmo_id):
        with self.session_factory() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            user = session.execute(stmt).scalars().first()

            if user:
                user.itmo_id = itmo_id
                user.verified = True
                session.commit()
                return user
            else:
                return None


class UserNotFoundException(Exception):
    ...