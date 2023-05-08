from auth import check_auth, check_password, hash_password
from crud import create_item, delete_item, get_item, patch_item
from errors import ApiError
from flask import jsonify, request
from flask.views import MethodView
from models import Token, User, get_session_maker, Advertisments
from schema import Login, PatchUser, Register, validate, CreateAdvertisment, PatchAdv

Session = get_session_maker()


def register():
    user_data = validate(Register, request.json)
    with Session() as session:
        user_data["password"] = hash_password(user_data["password"])
        user = create_item(session, User, **user_data)
        return jsonify({"id": user.id})


def login():
    login_data = validate(Login, request.json)
    with Session() as session:
        user = session.query(User).filter(User.email == login_data["email"]).first()
        if user is None or not check_password(user.password, login_data["password"]):
            raise ApiError(401, "Invalid user or password")

        token = Token(user=user)
        session.add(token)
        session.commit()
        return jsonify({"token": token.id})


class UserView(MethodView):
    def get(self, user_id):
        with Session() as session:
            user = get_item(session, User, user_id)
            return jsonify(
                {"id": user.id, "email": user.email, "registration_time": user.registration_time.isoformat()}
            )

    def patch(self, user_id: int):
        with Session() as session:
            patch_data = validate(PatchUser, request.json)
            if "password" in patch_data:
                patch_data["password"] = hash_password(patch_data["password"])

            token = check_auth(session)
            user = get_item(session, User, user_id)
            if token.user_id != user.id:
                raise ApiError(403, "user has no access")
            user = patch_item(session, user, **patch_data)

            return jsonify(
                {
                    "id": user.id,
                    "email": user.email,
                    "registration_time": user.registration_time.isoformat(),
                }
            )

    def delete(self, user_id: int):
        with Session() as session:
            user = get_item(session, User, user_id)
            token = check_auth(session)
            if token.user_id != user.id:
                raise ApiError(403, "user has no access")

            delete_item(session, user)

            return {"deleted": True}


def create_adv():
    adv_data = validate(CreateAdvertisment, request.json)
    with Session() as session:
        token = check_auth(session)
        if not token:
            raise ApiError(403, "user is not logged in")
        adv_data["owner"] = token.user.id

        adv = create_item(session, Advertisments, **adv_data)
        return jsonify({"id": adv.id})


class AdvertismentsView(MethodView):
    def get(self, advertisments_id):
        with Session() as session:
            advertisment = get_item(session, Advertisments, advertisments_id)
            return jsonify(
                {"id": advertisment.id,
                 "header": advertisment.header,
                 "date_creation": advertisment.date_of_creation.isoformat()}
            )

    def patch(self, advertisments_id: int):
        with Session() as session:
            patch_data = validate(PatchAdv, request.json)

            token = check_auth(session)
            advertisment = get_item(session, Advertisments, advertisments_id)
            if token.user_id != advertisment.owner:
                raise ApiError(403, "user has no access")
            advertisment = patch_item(session, advertisment, **patch_data)

            return jsonify(
                {
                    "id": advertisment.id,
                    "email": advertisment.header,
                    "registration_time": advertisment.date_of_creation.isoformat(),
                }
            )

    def delete(self, advertisments_id: int):
        with Session() as session:
            token = check_auth(session)
            advertisment = get_item(session, Advertisments, advertisments_id)
            if token.user_id != advertisment.owner:
                raise ApiError(403, "user has no access")

            delete_item(session, advertisment)

            return {"deleted": True}